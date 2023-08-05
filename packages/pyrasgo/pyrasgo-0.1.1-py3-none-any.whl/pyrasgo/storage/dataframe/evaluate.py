import datetime
import numpy as np
import pandas as pd
from typing import List
import webbrowser

from pyrasgo.api.connection import Connection
from pyrasgo.api.error import APIError
from pyrasgo.api.create import Create
from pyrasgo.schemas.feature import featureImportanceStats, ColumnProfiles
from pyrasgo.storage.dataframe.utils import generate_unique_id, map_pandas_df_type, tag_dataframe
from pyrasgo.utils.monitoring import log_event, track_usage

class Evaluate(Connection):

    def __init__(self, experiment="", **kwargs):
        super().__init__(**kwargs)
        self.create = Create(api_key=self._api_key)
        self._experiment = experiment

    @track_usage
    def duplicate_rows(self, df: pd.DataFrame, 
                       columns: List[str] = None) -> pd.DataFrame:
        """ 
        Returns a DataFrame of rows that are duplicated in your original DataFrame 
        
        Parameters
        ----------
            df: pandas DataFrame:
                Dataframe to operate on
            columns: (Optional) List[str]:
                List of column names to check for duplicates in
        
        Returns
        -------
            pandas DataFrame
        """
        df_out = df.copy(deep=True)
        if columns:
            df_out = df.iloc[:0].copy()
            for column in columns:
                df_out = df_out.append(df[df.duplicated([column])])
        else:
            df_out = df[df.duplicated()]
        return df_out

    @track_usage
    @log_event
    def feature_importance(self, df: pd.DataFrame, 
                           target_column: str, 
                           exclude_columns: List[str] = None,
                           return_cli_only: bool = False,
                           rasgo_df_id: str = None
                           ) -> dict:
        """
        Calculates importance of a target feature using Shapley values. Opens a page in the 
        Rasgo WebApp with feature importance graph OR return raw json of feature importance.

        Parameters
        ----------
            df: pandas DataFrame:
                Dataframe to operate on
            target_columns: str: 
                Column name of target feature
            exclude_columns: List[str]: 
                Column names of features to be filered out from profile
            return_cli_only: (Optional) bool:
                Instructs function to not open Rasgo WebApp and return json in the CLI only
            rasgo_df_id: (Optional) str:
                Allows user to manually associate this dataframe with a previous run of feature importance
        
        Returns
        -------
            dict
        """
        # Check if we can run this
        try:
            import shap
            import catboost
            from sklearn.metrics import mean_squared_error
            from sklearn.metrics import r2_score
        except ModuleNotFoundError:
            raise APIError('These packages will need to be installed to run this function: catboost, shap, sklearn')

        if target_column not in df.columns:
            raise APIError(f'Column {target_column} does not exist in DataFrame')

        # assign a unique id to the DF before we alter it
        if rasgo_df_id:
            tag_dataframe(df, {"RasgoID": rasgo_df_id})
        else:
            rasgo_df_id = generate_unique_id(df)

        # Copy df so we can alter it without impacting source data
        fi_df = df.copy(deep=True)
        
        # Prep DataFrame
        # NOTE: Nulls cause a problem with the importance calc:
        fi_df = fi_df.dropna()
        # NOTE: Dates cause a problem with the importance cals:
        fi_df = fi_df.select_dtypes(exclude=['datetime'])
        if exclude_columns:
            for col in exclude_columns:
                if col not in fi_df.columns:
                    raise APIError(f'Column {col} does not exist in DataFrame')
                fi_df = fi_df.drop(col, 1)

        # Create x and y df's based off target column
        df_x = fi_df.loc[:, fi_df.columns != target_column]
        df_y = fi_df.loc[:, fi_df.columns == target_column]
        
        # Get categorical feature indices to pass to catboost
        cat_features = np.where(df_x.dtypes != np.number)[0]

        # Create the catboost dataset
        try:
            dataset = catboost.Pool(data=df_x, label=df_y, cat_features=cat_features)
        except TypeError as e:
            raise APIError(f"Catboost error: {e}: "
                           f"One or more of the fields in your dataframe is a date that cannot be automatically filtered out. "
                           f"You can use the exclude_columns=[''] parameter to exclude these manually and re-run this fuction.")
        model = catboost.CatBoostRegressor(iterations=300, random_seed=123)
        model.fit(dataset, verbose=False, plot=False)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(dataset)
        df_shap = pd.DataFrame(shap_values, columns=df_x.columns)

        # Start building output json
        c_data = {}
        c_data["targetFeature"] = target_column

        # Histogram binning of shapley values
        c_data['featureShapleyDistributions'] = {}
        for column in df_shap:
            try:
                H, xedges, yedges = np.histogram2d(x=fi_df[column], y=df_shap[column], bins=10)
                df_hist = pd.DataFrame(zip(H.tolist(), xedges, yedges), columns=['Histogram','feature_edges','shap_edges'])
                fhist = df_hist.to_dict(orient="list")
                c_data['featureShapleyDistributions'][column] = fhist
            except:
                list_of_counts = []
                list_of_values = []
                col_min = df_shap[column].min()
                col_max = df_shap[column].max()
                unique_values = df[column].value_counts().index.tolist()
                if len(unique_values) > 10:
                    top_10_values = unique_values[:10]
                else:
                    top_10_values = unique_values
                df_combined = pd.concat([df[column], df_shap[column]], axis=1)
                shapcol = column+"_shap"
                df_combined.columns = [column, shapcol]
                for val in top_10_values:
                    count, division = np.histogram(df_combined.query('{0}==@val'.format(column))[shapcol], bins=10, range=(col_min, col_max), density=False)
                    list_of_counts.append(count.tolist())
                    list_of_values.append(val)
                df_hist = pd.DataFrame(zip(list_of_counts, list_of_values, division), columns=['Histogram','feature_edges','shap_edges'])
                fhist = df_hist.to_dict(orient="list")
                c_data['featureShapleyDistributions'][column] = fhist
                
        # Mean absolute value by feature
        c_data['featureImportance'] = df_shap.abs().mean().to_dict()
        
        # TODO: Split train and test when supported
        
        # Model performance
        c_data['modelPerformance'] = {}
        pred = model.predict(df_x)
        rmse = (np.sqrt(mean_squared_error(df_y, pred)))
        r2 = r2_score(df_y, pred)
        c_data['modelPerformance']['RMSE'] = rmse
        c_data['modelPerformance']['R2'] = r2

        # Prepare the response
        url = f'{self._environment.app_path}/dataframes/{rasgo_df_id}/importance'
        response = {
                    "url": url,
                    "targetfeature": target_column,
                    "featureImportance": c_data['featureImportance']
                }

        if not return_cli_only:
            json_payload = featureImportanceStats(
                targetFeature= target_column,
                featureShapleyDistributions= c_data['featureShapleyDistributions'],
                featureImportance= c_data['featureImportance'],
                modelPerformance= c_data['modelPerformance']
            )
            # save json to Api
            self.create.column_importance_stats(id = rasgo_df_id, payload = json_payload)
            # open the profile in a web page
            webbrowser.open(url)
        return response

    @track_usage
    def missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """ 
        Print all columns in a Dataframe with null values
        and return rows with null values
        
        Parameters
        ----------
            df: pandas DataFrame:
                Dataframe to operate on
        
        Returns
        -------   
            'Columns with null values:'
            '-------------------------'
            'column, count of rows'
            '-------------------------'
            'List[index of rows with null values]'
        """
        column_with_nan = df.columns[df.isnull().any()]
        template="%-20s %-6s"
        print(template % ("Column", "Count of Nulls"))
        print("-"*35)
        for column in column_with_nan:
            print(template % (column, df[column].isnull().sum()))
        print("-"*35)
        return df[df.isnull().any(axis=1)]

    @track_usage
    def profile(self, df: pd.DataFrame, 
                exclude_columns: List[str] = None,
                return_cli_only: bool = False,
                rasgo_df_id: str = None) -> dict:
        """
        Profile a DataFrame locally, and push metadata to rasgo to display.

        Parameters
        ----------
            df: pandas DataFrame:
                Dataframe to operate on
            exclude_columns: List[str]: 
                Column names of features to be filered out from profile
            return_cli_only: (Optional) bool:
                Instructs function to not open Rasgo WebApp and return json in the CLI only
            rasgo_df_id: (Optional) str:
                Allows user to manually associate this dataframe with a previous run of feature importance
        
        Returns
        -------
            dict
        """
        # NOTE: List of optimizations post-mvp:
        # - add frequency and outlier data to commonValues

        # assign a unique id to the DF before we alter it
        if rasgo_df_id:
            tag_dataframe(df, {"RasgoID": rasgo_df_id})
        else:
            rasgo_df_id = generate_unique_id(df)

        # Copy df so we can alter it without impacting source data
        p_df = df.copy(deep=True)
        # Remove columns before profiling
        if exclude_columns:
            for col in exclude_columns:
                if col not in p_df.columns:
                    raise APIError(f'Column {col} does not exist in DataFrame')
                p_df = p_df.drop(col, 1)

        # Create an object to hold intermediate data calculated via pandas
        profile_data = {}
        for col_label in p_df:
            profile_data[col_label] = {}

        # label is the name of the attribute in the api request/response
        # mean is the name of the pandas function that calculates it
        # last item is any kwargs required for the function
        labels_and_functions = [
            ('recCt', 'count', {'axis': 0}),
            ('distinctCt', 'nunique', None),
            ('meanVal', 'mean', {'axis': 0, 'numeric_only': True}),
            ('medianVal', 'median', {'axis': 0, 'numeric_only': True}),
            ('maxVal', 'max', {'axis': 0, 'numeric_only': True}),
            ('minVal', 'min', {'axis': 0, 'numeric_only': True}),
            ('sumVal', 'sum', {'axis': 0, 'numeric_only': True}),
            ('stdDevVal', 'std', {'axis': 0, 'numeric_only': True})
        ]
        for label, func_name, extra_args in labels_and_functions:
            results = self._evaluate_df(p_df, func_name, extra_args)
            for col_label in p_df:
                try:
                    # store under key name for column, if the value exists
                    profile_data[col_label][label] = results[col_label]
                except KeyError:
                    pass
        
        # Generate values histogram
        histo_data = {}
        common_values = {}
        for col_label in p_df:
            try:
                # Histogram for numeric
                counts, edges = np.histogram(p_df[col_label], bins='auto', density=False)
                df_hist = pd.DataFrame(zip(counts, edges), columns=['height','bucketFloor'])
                df_hist['bucketCeiling']  = df_hist['bucketFloor']
                fhist = df_hist.to_dict(orient="records")
                # Common values for numeric
                ch = p_df[col_label].value_counts().rename_axis('val').reset_index(name='recCt')
                top5 = ch.head(10).to_dict(orient="records")
            except: 
                # Histogram for non-numeric
                dh = p_df[col_label].apply(str).value_counts().rename_axis('bucketFloor').reset_index(name='height')
                dh['bucketCeiling'] = dh['bucketFloor']
                fhist = dh.head(10).to_dict(orient="records")
                # Common values for non-numeric
                ch = dh.rename({"bucketFloor":"val", "height":"recCt"})
                top5 = ch.head(10).to_dict(orient="records")
            histo_data[col_label] = fhist
            common_values[col_label] = top5

        # Prepare response
        response = {
            'columnProfiles': []
        }
        for col_label in profile_data:
            column_stats = {
                'columnName': col_label,
                'dataType': map_pandas_df_type(p_df[col_label].dtype.name),
                'featureStats': profile_data[col_label],
                'commonValues': common_values[col_label],
                'histogram': [] if return_cli_only else histo_data[col_label]
            }
            response['columnProfiles'].append(column_stats)

        url = f'{self._environment.app_path}/dataframes/{rasgo_df_id}/features'
        response['url'] = url

        if not return_cli_only:
            json_payload = ColumnProfiles(**response)
            # save json to Api
            self.create.dataframe_profile(id=rasgo_df_id, payload=json_payload)
            # open the feature profiles in a web page
            webbrowser.open(url)
        return response

    @track_usage
    def timeseries_gaps(self, df: pd.DataFrame, 
                        datetime_column: str,
                        partition_columns: List[str] = []) -> pd.DataFrame:
        """
        Returns a dataframe of rows before and after timeseries gaps
        
        Parameters
        ----------
            df: pandas DataFrame:
                Dataframe to operate on
            datetime_column: str: 
                Name of column to check for timeseries gaps
            partition_columns: List[str]:
                Column names to group by

        Returns
        -------
            pandas DataFrame
        """
        # NOTE: List of optimizations post-mvp:
        # - Check that datetime_column can convert to_datetime without error
        # - Support non-date grains

        # Check for columns
        sort_columns = partition_columns.copy()
        sort_columns.append(datetime_column)
        for col in sort_columns:
            if col not in df.columns:
                raise APIError(f'Column {col} does not exist in DataFrame')

        # Calculate lags and sort
        ts_df = df.copy(deep=True)
        ts_df.sort_values(by=sort_columns, inplace=True)
        ts_df['TSGAPDateCol'] = pd.to_datetime(ts_df[datetime_column], infer_datetime_format=True)
        ts_df['TSGAPLastDate'] = ts_df.groupby(partition_columns)['TSGAPDateCol'].shift(1)
        ts_df['TSGAPNextDate'] = ts_df.groupby(partition_columns)['TSGAPDateCol'].shift(-1)

        # NOTE: This assumes a day grain in the timeseries column, we'll need to expand this to support more grains 
        # Select the rows for output
        df_out = ts_df[(ts_df['TSGAPNextDate'] - ts_df['TSGAPDateCol'] != '1 days') 
                     | (ts_df['TSGAPDateCol'] - ts_df['TSGAPLastDate'] != '1 days')]
        df_out.drop(['TSGAPDateCol'], axis=1, inplace=True)
        #df_out.drop(['TSGAPNextDate', 'TSGAPLastDate'], axis=1, inplace=True)

        return df_out

    @track_usage
    def train_test_split(self, df: pd.DataFrame, 
                         training_percentage: float = .8,
                         timeseries_index: str = None) -> pd.DataFrame:
        """
        Returns training and test dataframes based on a percentage

        Parameters
        ----------
            df: pandas DataFrame:
                    Dataframe to operate on
            training_percentage: float: 
                Percentage of rows to use as training set (default = 80%)
            timeseries_index: str: 
                Name of column to use as timeseries index
        
        Returns
        -------
            pandas DataFrame, pandas DataFrame
        """
        if timeseries_index:
            if timeseries_index not in df.columns:
                raise APIError(f'Column {timeseries_index} does not exist in DataFrame')
            else:
                df = self._set_timeseries_index(df, timeseries_index)
        
        # Confirm df is indexed by a datetime field
        if df.index.get_level_values(0).dtype not in ['datetime64[ns]']:
            raise APIError("Index is not a datetime column. Try passing in a timeseries df with a datetime index "
                           "or passing the name of a datetime column in the 'timeseries_index' parameter.")
        df.sort_index(inplace=True)

        # split into 2 frames based on training percentage
        row_ct = df.shape[0]
        train_ct = round(row_ct * training_percentage)
        test_ct = round(row_ct * (1-training_percentage))
        train_df = df.head(train_ct)
        test_df = df.tail(test_ct)
        return train_df, test_df

    @track_usage
    def type_mismatches(self, df: pd.DataFrame, 
                        column: str, 
                        data_type: str) -> pd.DataFrame:
        """ 
        Return a copy of your DataFrame with a column cast to another datatype
        
        Parameters
        ----------
            df: pandas DataFrame:
                Dataframe to operate on
            column: str:
                The column name in the DataFrame to cast
            data_type: str:
                The data type to cast to Accepted Values: ['datetime', 'numeric']
        
        Returns
        -------
            pandas DataFrame
        """
        new_df = pd.DataFrame()
        if data_type == 'datetime':
            new_df[column] = pd.to_datetime(df[column], errors='coerce', infer_datetime_format=True)
        elif data_type == 'numeric':
            new_df[column] = pd.to_numeric(df[column], errors='coerce')
        else:
            return "Supported data_type values are: 'datetime' or 'numeric'"
        total = df[column].count()
        cant_convert = new_df[column].isnull().sum()
        print(f"{(total - cant_convert) / total}%: {cant_convert} rows of {total} rows cannot convert.")
        new_df.rename(columns = {column:f'{column}CastTo{data_type.title()}'}, inplace = True)
        return new_df

    def _set_timeseries_index(self, df: pd.DataFrame,
                             datetime_column: str) -> pd.DataFrame:
        """Returns a timeseries dataframe indexed by a date or datetime column"""
        df['datetimeIdx'] = pd.to_datetime(df[datetime_column])
        df.drop([datetime_column], axis=1, inplace=True)
        return df.set_index('datetimeIdx')

    @classmethod
    def _evaluate_df(cls, df: pd.DataFrame, func_name: str, extra_args: dict):
        extra_args = extra_args or {}
        # Get the correct DataFrame function by name
        results = getattr(df, func_name)(**extra_args)
        return results
