import os
import json
from webapp.verification.scripts import class_templates


class DictConstructor:
    """
    The class is intended for the formation of a data dictionary
    containing information about the procedure for checking
    the measuring instrument, for its further rendering on the html page
    """

    def __init__(self, number_mi: str, model: str):
        path_file = self.get_path_file(number_mi)

        if self.check_file(path_file):
            self.dict_for_html = self.formation_dict_for_html(
                path_file,
                number_mi,
                model
            )
        else:
            self.dict_for_html = None

    def get_path_file(self, number_mi: str) -> str:
        """
        Function describes the path to the json file

        :param number_mi: number in the state register
        :return: path to json file
        """
        path = "webapp/appr_type/scripts/"

        return path + f'{number_mi}.json'

    def check_file(self, path_file: str) -> bool:
        """
        Function checks if json exists for a specific number of approved type

        :param path_file: path to json file
        :return: result of file existence in boolean form
        """
        return os.path.exists(path_file)

    def formation_list_operations(self,
                                  class_mi: str,
                                  operations_mi: dict
                                  ) -> dict:
        """
        The function sends a dictionary with verification operations
        to the class template of the measuring instrument to form dictionary
        with tables of procedures for further rendering on the html page

        :param class_mi: class name of the measuring
        instrument from the class_templates.py
        :param operations_mi: verification operations (main and metrolog)
        from json file
        :return: dictionary with tables of verification procedures
        """
        meas_instrument = getattr(class_templates, class_mi)()
        operations = {'main_operations': [],
                      'metrolog_operations': []}

        for main_operation in operations_mi[0]:
            if 'name' in main_operation:
                operation = getattr(
                    meas_instrument,
                    main_operation['function']
                )(main_operation['name'])
            else:
                operation = getattr(
                    meas_instrument,
                    main_operation['function']
                )()
            operations['main_operations'].append(operation)

        for metrolog_operation in operations_mi[1]:
            operation = getattr(
                meas_instrument,
                metrolog_operation['function']
            )(metrolog_operation['name'],
              metrolog_operation['unit'],
              metrolog_operation['num_of_headers'],
              metrolog_operation['parameters'])
            operations['metrolog_operations'].append(operation)

        return operations

    def formation_dict_for_html(self,
                                path_file: str,
                                number_mi: str,
                                model: str
                                ) -> dict:
        """
        The function generates a dictionary containing data of the verification
        the measuring instrument for further rendering on the html page

        :param path_file: path to json file
        :param number_mi: number in the state register
        :param model: name of the measuring instrument model
        :return: dictionary with data of the verification
        the measuring instrument
        """
        appr_type_data = JsonHandler(path_file)
        model_data = appr_type_data.get_data_model(model)
        header_for_model = appr_type_data.get_header_for_model(model)
        operations_mi = appr_type_data.get_operations(model_data)
        dict_for_html = self.formation_list_operations(
            appr_type_data.class_mi,
            operations_mi
            )
        dict_for_html['number_mi'] = number_mi
        dict_for_html['model'] = model
        dict_for_html['header'] = header_for_model

        return dict_for_html


class JsonHandler:
    """
    The class is designed to process json containing data on the procedure
    for checking measuring instruments according to one approved type,
    and extract the necessary parameters
    """

    def __init__(self, file: str):
        self.file = file
        self.data_mi = self.get_dict()
        self.class_mi = self.get_class_mi()

    def get_dict(self) -> dict:
        """
        Function to read json file and convert to dictionary

        :return: dictionary generated from json file
        """
        with open(self.file, 'r', encoding='utf-8') as json_file:
            data_mi = json.load(json_file)

        return data_mi

    def get_class_mi(self) -> str:
        """
        Function returns the class of the measuring instrument

        :return: class of the measuring instrument
        """
        return self.data_mi['class_mi']

    def get_methods(self) -> list:
        """
        Function returns the names of verification methods
        used for verification of the approved type

        :return: list of names of verification methods
        """
        methods = []
        for method in self.data_mi['method_verif_mi']:
            methods.append(method['name_verif_proc'])

        return methods

    def get_models(self) -> list:
        """
        Function returns the names of all models for the approved type

        :return: list of names of all models
        """
        models = []
        for method in self.data_mi['method_verif_mi']:
            for model in method['models_mi']:
                models.append(model['name_model'])

        return models

    def get_header_for_model(self, model: str) -> str:
        """
        Function returns a header for verification
        the current measuring instrument model

        :param model: name of the measuring instrument model
        :return: header for verification
        """
        for method in self.data_mi['method_verif_mi']:
            for model_mi in method['models_mi']:
                if model_mi['name_model'].lower() == model.strip():
                    header_for_model = model_mi['header']

        return header_for_model

    def get_data_model(self, model: str) -> dict:
        """
        Function returns a dictionary with all the data for verification
        the current measuring instrument model

        :param model: name of the measuring instrument model
        :return: dictionary with all the data for verification
        """
        for method in self.data_mi['method_verif_mi']:
            for model_mi in method['models_mi']:
                if model_mi['name_model'].lower() == model.strip():
                    data_model = model_mi

        return data_model

    def get_operations(self, data_model: dict) -> tuple[list, list]:
        """
        Function returns two lists containing main and metrology operations
        for verification the current measuring instrument model

        :param data_model: dictionary with all the data for verification
        :return: list with main operations
        :return: list with metrology operations
        """
        operations = data_model['operations']
        main_operations = operations['main_operations']
        metrolog_operations = operations['metrolog_operations']

        return main_operations, metrolog_operations
