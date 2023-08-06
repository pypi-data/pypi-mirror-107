from typing import List, Optional

from .connection import Connection
from .error import APIError
from pyrasgo.utils.monitoring import track_usage

class Delete(Connection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def collection(self, id: int):
        """
        Permanently delete a Rasgo Collection. There is no way to undo this operation.
        """
        try:
            response = self._delete(f"/models/{id}", api_version=1)
            if response.status_code == 200:
                return f"Collection {id} successfully deleted"
            if response.status_code == 403:
                raise APIError(f"User does not have access to delete Collection {id}")
            raise APIError(f"Problem deleting Collection {id}.")
        except:
            raise APIError(f"Problem deleting Collection {id}.")

    def data_source(self, id: int):
        """
        Permanently delete a Rasgo DataSource. There is no way to undo this operation.
        """
        try:
            response = self._delete(f"/data-source/{id}", api_version=1)
            if response.status_code == 200:
                return f"DataSource {id} successfully deleted"
            if response.status_code == 403:
                raise APIError(f"User does not have access to delete DataSource {id}")
            return f"Problem deleting DataSource {id}."
        except:
            return f"Problem deleting DataSource {id}."

    def feature(self, id: int):
        """
        Permanently delete a Rasgo Feature. There is no way to undo this operation.
        """
        try:
            response = self._delete(f"/features/{id}", api_version=1)
            if response.status_code == 200:
                return f"Feature {id} successfully deleted"
            if response.status_code == 403:
                raise APIError(f"User does not have access to delete Feature {id}")
            return f"Problem deleting Feature {id}."
        except:
            return f"Problem deleting Feature {id}."