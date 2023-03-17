"""Imports"""
import math
from datetime import datetime
import requests

from webapp.model import db, Approved_types
from webapp import create_app

# Headers for requests
headers = {
        'Host': 'fgis.gost.ru',
        'User-Agent': 'Chrome/102.0.5005.134 YaBrowser/22.7.1.806',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
app = create_app()


def get_json_on_request(page_num=1, page_size=100):
    """
    Function to get info about approved types by API.

    :param page_num: page number for getting info
    :param page_size: number of records to upload for one request
    :return: json with info about approved types
    """
    url = f'https://fgis.gost.ru/fundmetrology/api/registry/4/data?' \
          f'pageNumber={page_num}&pageSize={page_size}'
    while True:
        try:
            response = requests.get(url=url, headers=headers, timeout=30)
            json_object = response.json().get('result')
            break
        except ConnectionError:
            print('Ошибка соединения.')
        except TimeoutError:
            print('Timeout.')
        except requests.exceptions.JSONDecodeError:
            print('Ошибка выгрузки.')

    return json_object


def format_values_in_appr_type(appr_type: dict) -> dict:
    """
    Function for formatting info about approved type
    and casting types to types from the database.

    :param appr_type: a dict with info about approved type
    :return: formatted dict
    """
    for key, value in appr_type.items():
        if value != '' and value is not None:
            if isinstance(value, list):
                value = ', '.join(value)
            value = value.replace('\n', '').strip()
            if key in ['description_si', 'method_verif_si']:
                value = f"https://fgis.gost.ru/fundmetrology{value}"
            elif key in ['publication_date', 'certificate_date']:
                try:
                    value = datetime.strptime(value, '%d.%m.%Y').date()
                except ValueError:
                    value = None
            elif key in ['next_verif_si', 'part_verif_si']:
                if value == 'Да':
                    value = True
                else:
                    value = False
        else:
            value = None
        appr_type[key] = value

    return appr_type


def get_dict_from_item(item: list, corresponding_keys: dict) -> dict:
    """
    Function to create a dictionary with the same keys, assigning a column in
    the database according to the data about the approved type from arshin.

    :param item: a dict that contains all information about the approved type
    :return: formatted dictionary according to the required keys
    """
    appr_type = dict.fromkeys(corresponding_keys, '')
    for key_db, key_arshin in corresponding_keys.items():
        for field in item:
            if field.get('name') == key_arshin:
                if key_arshin in ['foei:DescriptionSI', 'foei:MethodVerifSI']:
                    appr_type[key_db] = field.get('link')
                else:
                    appr_type[key_db] = field.get('value')

    return format_values_in_appr_type(appr_type)


def save_appr_type(appr_type: dict) -> None:
    """
    Function of saving info about approved type.
    """
    with app.app_context():
        appr_type_for_db = Approved_types(number_si=appr_type['number_si'],
                                        name_si=appr_type['name_si'],
                                        designation_si=appr_type['designation_si'],
                                        number_record=appr_type['number_record'],
                                        id_arshin=appr_type['id_arshin'],
                                        publication_date=appr_type['publication_date'],
                                        manufacturer_si=appr_type['manufacturer_si'],
                                        description_si=appr_type['description_si'],
                                        method_verif_si=appr_type['method_verif_si'],
                                        proced_si=appr_type['proced_si'],
                                        certificate_date=appr_type['certificate_date'],
                                        mpi_si=appr_type['mpi_si'],
                                        next_verif_si=appr_type['next_verif_si'],
                                        part_verif_si=appr_type['part_verif_si'],
                                        status_si=appr_type['status_si'])
        db.session.add(appr_type_for_db)
        db.session.commit()


def unload_all_app_types(total_count: int, page_size: int) -> None:
    """
    Function for uploading all approved types to the dictionary.

    :param total_count: number of all approved types
    """
    corresponding_keys = {
        'number_si': 'foei:NumberSI',
        'name_si': 'foei:NameSI',
        'designation_si': 'foei:DesignationSI',
        'number_record': 'foei:number',
        'id_arshin': 'id',
        'publication_date': 'foei:date',
        'manufacturer_si': 'foei:ManufacturerTotalSI',
        'description_si': 'foei:DescriptionSI',
        'method_verif_si': 'foei:MethodVerifSI',
        'proced_si': 'foei:ProcedSI',
        'certificate_date': 'foei:CertificateLifeSI',
        'mpi_si': 'foei:MPISI',
        'next_verif_si': 'foei:NextVerifSI',
        'part_verif_si': 'foei:PartVerifSI',
        'status_si': 'foei:StatusSI',
    }
    page_num = math.ceil(total_count / page_size)
    max_page_num = page_num
    while page_num >= 1:
        items = get_json_on_request(page_num, page_size).get('items')
        for item in items:
            appr_type = get_dict_from_item(item['properties'],
                                           corresponding_keys)
            save_appr_type(appr_type)
        count_pages = max_page_num - page_num + 1
        print(f'Unloaded {count_pages} page out of {max_page_num}.')
        page_num -= 1


def main() -> None:
    """
    The script uploads information for each approved type page by page
    from the site https://fgis.gost.ru/fundmetrology/registry/4
    """
    total_count = get_json_on_request().get('totalCount')
    unload_all_app_types(total_count=total_count, page_size=100)


if __name__ == "__main__":
    main()
