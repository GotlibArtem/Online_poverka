from webapp.verification.scripts.format_value import get_value_without_postfix, add_postfix_to_value


class ElectricalMeasurements:
    """
    Class describes standard verification operations
    for all instruments that perform electrical measurements
    """

    def __init__(self):
        pass

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


class PortableMultimeters(ElectricalMeasurements):
    """
    Class is designed to process data for verification
    of a portable multimeter and the formation of a final
    dictionary from the information for the html file
    """

    def __init__(self):
        pass

    def get_measurement_error(self,
                              point: str,
                              inaccuracy: list,
                              emp: str
                              ) -> str:
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

    def electrical_meas(self,
                        table_name: str,
                        unit: str,
                        num_of_headers: int,
                        parameters: list
                        ) -> dict:
        """
        Function is used to form a dictionary with data
        for displaying a standard table of electrical measurements
        with 6 or 7 columns

        :param table_name: name of measurement table
        :param unit: unit of measure
        :param num_of_headers: number of table columns
        :param parameters: parametes for measurement table
        :return: dictionary containing the name of the table,
        the name of the columns and rows of the table
        """
        headers = [f'Предел измерения, {unit}',
                   f'Поверяемая точка, {unit}',
                   f'Измеренное значение, {unit}',
                   f'Абсолютная погрешность измерения, {unit}',
                   f'Предел допускаемой погрешности, {unit}',
                   'Вывод о соответствии'
                   ]
        if num_of_headers == 7:
            headers.insert(2, 'Частота, Гц')

        rows = []
        for parameter in parameters:
            for value in parameter['points']:
                if num_of_headers == 6:
                    meas_error = self.get_measurement_error(
                        value,
                        parameter['inaccuracy'],
                        parameter['emp']
                    )
                    rows.append([
                        [parameter['limit'], 'limit'],
                        [value, 'point'],
                        [value, 'input_value'],
                        [add_postfix_to_value(0, parameter['emp']), 'abs_error'],
                        [meas_error, 'meas_error'],
                        ['Соотв.', 'result']
                    ])
                elif num_of_headers == 7:
                    for frequency in value[1]:
                        frequency = str(frequency)
                        meas_error = self.get_measurement_error(
                            value[0],
                            parameter['inaccuracy'][frequency],
                            parameter['emp']
                        )
                        rows.append([
                            [parameter['limit'], 'limit'],
                            [value[0], 'point'],
                            [frequency, 'freq'],
                            [value[0], 'input_value'],
                            [add_postfix_to_value(0, parameter['emp']), 'abs_error'],
                            [meas_error, 'meas_error'],
                            ['Соотв.', 'result']
                        ])

        return {
            'table_name': table_name,
            'headers': headers,
            'rows': rows
        }
