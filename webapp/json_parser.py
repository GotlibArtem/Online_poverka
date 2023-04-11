"""Imports"""
import os
import json
import class_templates


class DictConstructor:

    def __init__(self, number_mi: str, model: str):
        path_file = self.get_path_file(number_mi)
        if self.check_file(path_file):
            self.dict_for_html = self.formation_dict_for_html(path_file,
                                                              number_mi,
                                                              model)
        else:
            self.dict_for_html = None

    def get_path_file(self, number_mi: str) -> str:
        """
        Function describes the path to the json file
        """
        path = "scripts/"
        return path + f'{number_mi}.json'

    def check_file(self, path_file: str) -> bool:
        """
        Function checks if json exists for a specific number of approved type
        """
        return os.path.exists(path_file)

    def formation_list_operations(self, class_mi: str, operations_mi: dict) -> dict:
        """
        Function
        """
        meas_instrument = getattr(class_templates, class_mi)()
        operations = {'main_operations': [],
                      'metrolog_operations': []}
        for main_operation in operations_mi[0]:
            if 'name' in main_operation:
                operation = getattr(meas_instrument, main_operation['function'])(
                    main_operation['name']
                    )
            else:
                operation = getattr(meas_instrument, main_operation['function'])()
            operations['main_operations'].append(operation)
        for metrolog_operation in operations_mi[1]:
            operation = getattr(meas_instrument, metrolog_operation['function'])(
                metrolog_operation['name'],
                metrolog_operation['parameters']
                )
            operations['metrolog_operations'].append(operation)

        return operations

    def formation_dict_for_html(self,
                                path_file: str,
                                number_mi: str,
                                model: str):
        """
        Function
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

    def __init__(self, file: str):
        self.file = file
        self.data_mi = self.get_dict()
        self.class_mi = self.get_class_mi()

    def get_dict(self) -> dict:
        """
        Function
        """
        with open(self.file, 'r', encoding='utf-8') as json_file:
            data_mi = json.load(json_file)
            json_file.close()

        return data_mi

    def get_class_mi(self):
        """
        Function
        """
        return self.data_mi['class_mi']

    def get_methods(self):
        """
        Function
        """
        methods = []
        for method in self.data_mi['method_verif_mi']:
            methods.append(method['name_verif_proc'])

        return methods

    def get_models(self):
        """
        Function
        """
        models = []
        for method in self.data_mi['method_verif_mi']:
            for model in method['models_mi']:
                models.append(model['name_model'])

        return models

    def get_header_for_model(self, model: str) -> str:
        """
        Function
        """
        for method in self.data_mi['method_verif_mi']:
            for model_mi in method['models_mi']:
                if model_mi['name_model'] == model:
                    header_for_model = model_mi['header']

        return header_for_model

    def get_data_model(self, model: str) -> dict:
        """
        Function
        """
        for method in self.data_mi['method_verif_mi']:
            for model_mi in method['models_mi']:
                if model_mi['name_model'] == model:
                    data_model = model_mi

        return data_model

    def get_operations(self, data_model: dict):
        """
        Function
        """
        operations = data_model['operations']
        main_operations = operations['main_operations']
        metrolog_operations = operations['metrolog_operations']

        return main_operations, metrolog_operations
