import json
import logging
import requests
import functools
import inspect
from datetime import datetime

from pyrasgo.version import __version__ as pyrasgo_version
from pyrasgo.api.session import Environment

PRODUCTION_HEAP_KEY = '540300130'
STAGING_HEAP_KEY = '3353132567'

HEAP_URL = "https://heapanalytics.com/api"
# HEAP_PROPS_URL = f"{HEAP_URL}/add_user_properties"


def track_usage(func):
    @functools.wraps(func)
    def decorated(self, *args, **kwargs):
        try:
            self._api_key
        except AttributeError:
            logging.debug(f"Cannot track functions called from {self.__class__.__name__} class.")
            return func(self, *args, **kwargs)

        if self._environment == Environment.LOCAL:
            logging.info(f"Called {func.__name__} with parameters: {kwargs}")
        else:
            try:
                track_call(
                    app_id=PRODUCTION_HEAP_KEY if self._environment == Environment.PRODUCTION else STAGING_HEAP_KEY,
                    identity=self._profile.get('id', 0),
                    event=func.__name__,
                    properties={"hostname": self._environment.value,
                                "source": "pyrasgo",
                                "class": self.__class__.__name__,
                                "version": pyrasgo_version,
                                "userId": self._profile.get('id', 0),
                                "username": self._profile.get('username', 'Unknown'),
                                "orgId": self._profile.get('organizationId', 0)
                                })
                                #"input": args,
                                #**kwargs})
            except Exception as e:
                logging.debug(f"Called {func.__name__} with parameters: {kwargs}")
                logging.debug(e)
        return func(self, *args, **kwargs)

    return decorated


def identify(app_id: str,
             identity: int):
    """
    Send an "identify" event to the Heap Analytics API server
    
    :param identity: unique id used to identify the user
    """
    data = {"app_id": app_id,
            "identity": identity}

    response = requests.post(url=f"{HEAP_URL}/identify",
                             data=json.dumps(data),
                             headers={"Content-Type": "application/json"})
    response.raise_for_status()
    return response


def add_user_properties(app_id: str,
                        identity: int,
                        properties: dict = None):
    """
    Send a "add_user_properties" event to the Heap Analytics API server
    
    :pram: identity: unique id used to identify the user
    :param properties: optional, additional properties to associate with the user
    """
    data = {"app_id": app_id,
            "identity": identity}
    
    if properties is not None:
        data["properties"] = properties

    response = requests.post(url=f"{HEAP_URL}/add_user_properties",
                             data=json.dumps(data),
                             headers={"Content-Type": "application/json"})
    response.raise_for_status()
    return response


def track_call(app_id: str,
               identity: int,
               event: str,
               properties: dict = None):
    """
    Send a "track" event to the Heap Analytics API server.

    :param identity: unique id used to identify the user
    :param event: event name
    :param properties: optional, additional event properties
    """
    data = {"app_id": app_id,
            "identity": identity,
            "event": event}

    if properties is not None:
        data["properties"] = properties

    response = requests.post(url=f"{HEAP_URL}/track",
                             data=json.dumps(data),
                             headers={"Content-Type": "application/json"})
    response.raise_for_status()
    return response


def log_event(func):
    @functools.wraps(func)
    def decorated(self, *args, **kwargs):
        try:
            self._api_key
            experiment = self._experiment
            df_id = kwargs["rasgo_df_id"]
        except AttributeError:
            logging.debug(f"Cannot create events for functions called from {self.__class__.__name__} class.")
            return func(self, *args, **kwargs)
        except KeyError:
            logging.debug(f"To create events for functions called from " \
                            f"{self.__class__.__name__} class, a dataframe must be tagged by ID.")
            return func(self, *args, **kwargs)

        if experiment:
            event_timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%f")
            experiment_name = experiment
            event_name = func.__name__
            event_type = self.__class__.__name__
            event_dict = {
                "event_timestamp": event_timestamp,
                "experiment_name": experiment_name,
                "dataframe_id": df_id,
                "event_type": event_type,
                "event_name": event_name,
                "event_details": {},
            }

        try:
            self._post(f"/event-logging", event_dict, api_version=1).json()
        except Exception as e:
            logging.info(f"Unable to log event with exception: {e}")
        return func(self, *args, **kwargs)
    return decorated
