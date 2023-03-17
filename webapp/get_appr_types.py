"""Imports"""
import math
from datetime import datetime
import requests


# Headers for requests
headers = {
        'Host': 'fgis.gost.ru',
        'User-Agent': 'Chrome/102.0.5005.134 YaBrowser/22.7.1.806',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }


def get_json_on_request(page_num=1, page_size=100):
    """
    Function to get info about approved types by API.

    :param page_num: page number for getting info
    :param page_size: number of records to upload for one request
    :return: json with info about approved types
    """
    url = f'https://fgis.gost.ru/fundmetrology/api/registry/4/data?' \
          f'pageNumber={page_num}&pageSize={page_size}'
    response = requests.get(url=url, headers=headers, timeout=30)
    json_object = response.json().get('result')

    return json_object


def format_values_in_appr_type(appr_type: dict) -> dict:
    """
    Function for formatting info about approved type
    and casting types to types from the database.

    :param appr_type: a dict with info about approved type
    :return: formatted dict
    """
    for key, value in appr_type.items():
        if value != '':
            if isinstance(value, list):
                value = ', '.join(value)
            value = value.replace('\n', '').strip()
            if key in ['description_si', 'method_verif_si']:
                value = f"https://fgis.gost.ru/fundmetrology{value}"
            elif key in ['publication_date', 'certificate_date']:
                value = datetime.strptime(value, '%d.%m.%Y').date()
        else:
            value = None
        appr_type[key] = value

    return appr_type


def get_dict_from_item(item: list, corresponding_keys: dict) -> dict:
    """
    Function to create a dictionary with the same keys, assigning a column in
    the database according to the data about the approved type from arshin.

    :param item: a dict that contains all information about the approved type
    :return: formed dictionary according to the required keys
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


def unload_all_app_types(total_count: int, page_size: int) -> list:
    """
    Function for uploading all approved types to the dictionary.

    :param total_count: number of all approved types
    :return: dictionary with all approved types
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
        'part_verif_siv': 'foei:PartVerifSI',
        'status_si': 'foei:StatusSI',
    }
    appr_types = []
    page_num = 1
    max_page_num = math.ceil(total_count / page_size)
    while page_num <= max_page_num:
        items = get_json_on_request(page_num, page_size).get('items')
        for item in items:
            appr_type = get_dict_from_item(item['properties'],
                                           corresponding_keys)
            appr_types.append(appr_type)
        print(appr_types)
        # print(f'Unloaded {page_num} page out of {max_page_num}.')
        page_num += 1

    return appr_types


def main() -> None:
    """
    The script uploads information for each approved type page by page
    from the site https://fgis.gost.ru/fundmetrology/registry/4
    """
    total_count = get_json_on_request().get('totalCount')
    unload_all_app_types(total_count=total_count, page_size=100)


if __name__ == "__main__":
    main()
