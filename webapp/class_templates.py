"""Imports"""
from format_value import get_value_without_postfix, add_postfix_to_value


class PortableMultimeters:
    """
    Class is designed to process data for verification
    of a portable multimeter and the formation of a final
    dictionary from the information for the html file
    """

    def __init__(self):
        return

    def visual_inspection(self, item_name='Внешний осмотр') -> dict:
        """
        Function for forming a dictionary from the data
        for the verification visual inspection

        :param item_name: name of the verification point
        :return: dictionary with data for the verification visual inspection
        """
        return {'item_name': item_name,
                'positive_result': 'соответствует',
                'negative_result': 'не соответствует'
                }

    def testing(self, item_name='Опробование') -> dict:
        """
        Function for forming a dictionary from the data
        for the verification testing

        :param item_name: name of the verification point
        :return: dictionary with data for the verification testing
        """
        return {'item_name': item_name,
                'positive_result': 'соответствует',
                'negative_result': 'не соответствует'
                }

    def get_measurement_error(self, point: str, inaccuracy: list, emp: str) -> str:
        """
        Function for calculating the measurement error
        and formatting it by discreteness

        :param point: verified point
        :param inaccuracy: list of parameters for calculating measurement error
        :param emp: low order unit
        :return: formatted measurement error
        """
        value = get_value_without_postfix(point)
        discreteness = get_value_without_postfix(emp)
        meas_error = abs(value) * inaccuracy[0] + discreteness * inaccuracy[1]

        return f'± {add_postfix_to_value(meas_error, emp)}'

    def dc_voltage(self, table_name: str, parameters: list) -> dict:
        """
        Function
        """
        headers = ['Предел измерения, В',
                   'Поверяемая точка, В',
                   'Измеренное значение, В',
                   'Абсолютная погрешность измерения, В',
                   'Предел допускаемой погрешности, В',
                   'Вывод о соответствии'
                   ]
        rows = []
        for parameter in parameters:
            limit = parameter['limit']
            inaccuracy = parameter['inaccuracy']
            emp = parameter['emp']
            current_error = add_postfix_to_value(0, emp)
            for point in parameter['points']:
                meas_error = self.get_measurement_error(point, inaccuracy, emp)
                rows.append([
                    [limit, 'value'],
                    [point, 'value'],
                    [point, 'input_value'],
                    [current_error, 'change_value'],
                    [meas_error, 'value'],
                    ['Соотв.', 'result']
                    ])

        return {
            'table_name': table_name,
            'headers': headers,
            'rows': rows
        }

    def ac_voltage(self, table_name: str, parameters: list) -> dict:
        """
        Function
        """
        headers = ['Предел измерения, В',
                   'Поверяемая точка, В',
                   'Частота, Гц',
                   'Измеренное значение, В',
                   'Абсолютная погрешность измерения, В',
                   'Предел допускаемой погрешности, В',
                   'Вывод о соответствии'
                   ]
        rows = []
        for parameter in parameters:
            limit = parameter['limit']
            inaccuracy = parameter['inaccuracy']
            emp = parameter['emp']
            current_error = add_postfix_to_value(0, emp)
            for values in parameter['points']:
                point = values[0]
                frequencies = values[1]
                for frequency in frequencies:
                    frequency = str(frequency)
                    meas_error = self.get_measurement_error(
                        point,
                        inaccuracy[frequency],
                        emp
                        )
                    rows.append([
                        [limit, 'value'],
                        [point, 'value'],
                        [frequency, 'value'],
                        [point, 'input_value'],
                        [current_error, 'change_value'],
                        [meas_error, 'value'],
                        ['Соотв.', 'result']
                        ])

        return {
            'table_name': table_name,
            'headers': headers,
            'rows': rows
        }

    def dc_current(self, table_name: str, parameters: list) -> dict:
        """
        Function
        """
        headers = ['Предел измерения, А',
                   'Поверяемая точка, А',
                   'Измеренное значение, А',
                   'Абсолютная погрешность измерения, А',
                   'Предел допускаемой погрешности, А',
                   'Вывод о соответствии'
                   ]
        rows = []
        for parameter in parameters:
            limit = parameter['limit']
            inaccuracy = parameter['inaccuracy']
            emp = parameter['emp']
            current_error = add_postfix_to_value(0, emp)
            for point in parameter['points']:
                meas_error = self.get_measurement_error(point, inaccuracy, emp)
                rows.append([
                    [limit, 'value'],
                    [point, 'value'],
                    [point, 'input_value'],
                    [current_error, 'change_value'],
                    [meas_error, 'value'],
                    ['Соотв.', 'result']
                    ])

        return {
            'table_name': table_name,
            'headers': headers,
            'rows': rows
        }

    def ac_current(self, table_name: str, parameters: list) -> dict:
        """
        Function
        """
        headers = ['Предел измерения, А',
                   'Поверяемая точка, А',
                   'Частота, Гц',
                   'Измеренное значение, А',
                   'Абсолютная погрешность измерения, А',
                   'Предел допускаемой погрешности, А',
                   'Вывод о соответствии'
                   ]
        rows = []
        for parameter in parameters:
            limit = parameter['limit']
            inaccuracy = parameter['inaccuracy']
            emp = parameter['emp']
            current_error = add_postfix_to_value(0, emp)
            for values in parameter['points']:
                point = values[0]
                frequencies = values[1]
                for frequency in frequencies:
                    frequency = str(frequency)
                    meas_error = self.get_measurement_error(
                        point,
                        inaccuracy[frequency],
                        emp
                        )
                    rows.append([
                        [limit, 'value'],
                        [point, 'value'],
                        [frequency, 'value'],
                        [point, 'input_value'],
                        [current_error, 'change_value'],
                        [meas_error, 'value'],
                        ['Соотв.', 'result']
                        ])

        return {
            'table_name': table_name,
            'headers': headers,
            'rows': rows
        }

    def resistance(self, table_name: str, parameters: list) -> dict:
        """
        Function
        """
        headers = ['Предел измерения, Ом',
                   'Поверяемая точка, Ом',
                   'Измеренное значение, Ом',
                   'Абсолютная погрешность измерения, Ом',
                   'Предел допускаемой погрешности, Ом',
                   'Вывод о соответствии'
                   ]
        rows = []
        for parameter in parameters:
            limit = parameter['limit']
            inaccuracy = parameter['inaccuracy']
            emp = parameter['emp']
            current_error = add_postfix_to_value(0, emp)
            for point in parameter['points']:
                meas_error = self.get_measurement_error(point, inaccuracy, emp)
                rows.append([
                    [limit, 'value'],
                    [point, 'value'],
                    [point, 'input_value'],
                    [current_error, 'change_value'],
                    [meas_error, 'value'],
                    ['Соотв.', 'result']
                    ])

        return {
            'table_name': table_name,
            'headers': headers,
            'rows': rows
        }

    def frequency_ac_voltage(self, table_name: str, parameters: list) -> dict:
        """
        Function
        """
        headers = ['Предел измерения, Гц',
                   'Поверяемая точка, Гц',
                   'Измеренное значение, Гц',
                   'Абсолютная погрешность измерения, Гц',
                   'Предел допускаемой погрешности, Гц',
                   'Вывод о соответствии'
                   ]
        rows = []
        for parameter in parameters:
            limit = parameter['limit']
            inaccuracy = parameter['inaccuracy']
            emp = parameter['emp']
            current_error = add_postfix_to_value(0, emp)
            for point in parameter['points']:
                meas_error = self.get_measurement_error(point, inaccuracy, emp)
                rows.append([
                    [limit, 'value'],
                    [point, 'value'],
                    [point, 'input_value'],
                    [current_error, 'change_value'],
                    [meas_error, 'value'],
                    ['Соотв.', 'result']
                    ])

        return {
            'table_name': table_name,
            'headers': headers,
            'rows': rows
        }

    def capacitance(self, table_name: str, parameters: list) -> dict:
        """
        Function
        """
        headers = ['Предел измерения, Ф',
                   'Поверяемая точка, Ф',
                   'Измеренное значение, Ф',
                   'Абсолютная погрешность измерения, Ф',
                   'Предел допускаемой погрешности, Ф',
                   'Вывод о соответствии'
                   ]
        rows = []
        for parameter in parameters:
            limit = parameter['limit']
            inaccuracy = parameter['inaccuracy']
            emp = parameter['emp']
            current_error = add_postfix_to_value(0, emp)
            for point in parameter['points']:
                meas_error = self.get_measurement_error(point, inaccuracy, emp)
                rows.append([
                    [limit, 'value'],
                    [point, 'value'],
                    [point, 'input_value'],
                    [current_error, 'change_value'],
                    [meas_error, 'value'],
                    ['Соотв.', 'result']
                    ])

        return {
            'table_name': table_name,
            'headers': headers,
            'rows': rows
        }
