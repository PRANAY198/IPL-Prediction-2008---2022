import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprcessor.pkl")

class DataTransformation:
    def __init__(self):
 
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformation_object(self):
        '''
        this fuction responsiable for data transformaton
        
        '''
        try:
            numerical_columns =["Overs", "current_score","wickets_left","current_run_rate","required_run_rate"]
            categorical_columns =[
                "BattingTeam",
                "BowlingTeam",
                "Venue",
            ]
            
            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
                ]
            )

            cat_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")

            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            logging.info(f'Train Dataframe shape : \n{train_df.shape}')
            logging.info(f'Test Dataframe shape  : \n{test_df.shape}')

            logging.info("obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformation_object()

            target_column_name="target"
            drop_columns = [target_column_name]

            input_feature_train_df=train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]


            logging.info(
                f"Applying preprocessing object on training dateframe and testing dataframe."
            )
            
            logging.info(f'Input feature Train Dataframe shape : \n{input_feature_train_df.shape}')
            logging.info(f'target feature Train Dataframe shape  : \n{target_feature_train_df.shape}')

            logging.info(f'Input feature Test Dataframe shape : \n{input_feature_test_df.shape}')
            logging.info(f'Target feature Test Dataframe shape  : \n{target_feature_test_df.shape}')
            
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )


        except Exception as e:
            raise CustomException(e,sys)