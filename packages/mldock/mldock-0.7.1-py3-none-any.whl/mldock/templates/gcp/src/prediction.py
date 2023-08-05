import os
import io
import csv
import logging
import numpy as np

import pickle
import pandas as pd

from mldock.platform_helpers.mldock.model_service import base
from mldock.platform_helpers.mldock.errors import extract_stack_trace
from src.container.assets import environment, logger

class ModelService(base.ModelService):
    model = None
    transformer = None

    def __init__(self, model_path, transformer_path):

        self.load_model(file_path=model_path)
        self.load_transformer(file_path=transformer_path)

    def load_model(self, file_path):
        """Get the model object for this instance, loading it if it's not already loaded."""

        if self.model == None:

            with open(file_path, 'rb') as file_:
                self.model = pickle.load(file_)

        return self

    def load_transformer(self, file_path):
        """Get the model object for this instance, loading it if it's not already loaded."""

        if self.transformer == None:

            with open(file_path, 'rb') as file_:
                self.transformer = pickle.load(file_)

        return self

    def input_transform_json(self, data):
        """transform numpy array of predictions into json payload"""
        # transform json dict to model input
        X = pd.DataFrame([data['input']])
        return self.transformer.transform(X)

    def input_transform_csv(self, data):
        """Transform numpy array of predictions in to csv"""

        # transform sting/bytes to model input
        s=data.decode('utf-8')

        data = io.StringIO(s)

        X = pd.read_csv(data)
        return self.transformer.transform(X)

    def input_transform(self, data, **kwargs):
        """
            Custom input transformer

            args:
                input: raw input from request
        """
        content_type = kwargs.get('content_type', 'json')
        if  content_type == 'csv':
            return self.input_transform_csv(data)
        elif content_type == 'json':
            return self.input_transform_json(data)
        else:
            raise Exception((
                "{} content type not supported. "
                "Only supports json or csv.".format(content_type)
            ))

    @staticmethod
    def output_transform_json(pred):
        """transform numpy array of predictions into json payload"""
        results = pred.tolist()
        return {'results': results}

    @staticmethod
    def output_transform_csv(pred, headers=False):
        """Transform numpy array of predictions in to csv"""
        predictions = pred.tolist()

        # create results
        results = []
        if headers == True:
            results.append(('idx','prediction'))
        # append values
        [
            results.append(
                (i,
                pred)
            ) for (i, pred) in enumerate(predictions)
        ]

        return results

    def output_transform(self, predictions, **kwargs):
        """
            Custom output transformation code
        """
        content_type = kwargs.get('content_type')
        if  content_type == 'csv':
            return self.output_transform_csv(
                predictions,
                headers=kwargs.get('headers', False)
            )
        elif content_type == 'json':
            return self.output_transform_json(predictions)
        else:
            raise Exception((
                "{} content type not supported. "
                "Only supports json or csv.".format(content_type)
            ))

    def predict(self, data):
        """For the input, do the predictions and return them.

        Args:
            data (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        try:
            pred = self.model.predict(data)
            return pred
        except Exception as exception:
            # get stack trace as exception
            stack_trace = extract_stack_trace()
            reformatted_log_msg = (
                    'Server Error: {ex}'.format(ex=stack_trace)
            )
            return reformatted_log_msg


def handler(data, content_type='json'):
    """
    Prediction given the request input
    :param data: [dict], request input
    :return: [dict], prediction
    """
    
    # (TODO)
    # Investigate the server costs to self vs cls implementation
    # Since the server executes code and simplifying user use of "modelservice" is key, then keep "self"
    # if there is an advantage to cls, perhaps loading model once on the server vs each time handler called.
    # due to threads on server, it would be interesting to see if thread use is more optimal with cls.
    model_service = ModelService(
        model_path=os.path.join(environment.model_dir, "iris/model.pkl"),
        transformer_path = os.path.join(environment.model_dir, 'iris/transformer.pkl')
    )
    logger.info(data)
    # transform input
    model_input = model_service.input_transform(
        data,
        content_type=content_type
    )
    logger.info(model_input)
    # model.predict
    pred = model_service.predict(model_input)
    logger.info(pred)

    # transform output
    results = model_service.output_transform(
        predictions=pred,
        content_type=content_type,
        headers=environment.environment_variables.bool('MLDOCK_HEADERS')
    )

    return results
