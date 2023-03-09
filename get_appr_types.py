"""Imports"""
import math
import requests

# Headers for requests
headers = {
        'Host': 'fgis.gost.ru',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.1.806 Yowser/2.5 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }


def get_json_on_request(page_num=1, page_size=100):
    """
    Function to get information about approved types by API.

    :param page_num: page number for getting info
    :param page_size: number of records to upload for one request
    :return: json with information about approved types
    """
    url = f'https://fgis.gost.ru/fundmetrology/api/registry/4/data?pageNumber={page_num}&pageSize={page_size}'
    response = requests.get(url=url, headers=headers, timeout=30)
    json_object = response.json().get('result')

    return json_object


def unload_all_app_types(total_count: int, page_size: int) -> list:
    """
    Function for uploading all approved types to the dictionary.

    :param total_count: number of all approved types
    :return: dictionary with all approved types
    """
    appr_types = []
    unused_keys = ['msaccessSI', 'FactoryNumSI', 'NoteSI', 'status', 'sortKey', 'SvedenSI']
    page_num = 1
    max_page_num = math.ceil(total_count / page_size)
    while page_num <= max_page_num:
        items = get_json_on_request(page_num=page_num, page_size=page_size).get('items')
        for item in items:
            appr_type = {}
            fields = item['properties']
            for field in fields:
                key = field['name'].replace('foei:', '')
                if key not in unused_keys:
                    if isinstance(field['value'], list):
                        appr_type[key] = field['value'][0]
                    else:
                        appr_type[key] = field['value'].replace('\n', '').strip()
            appr_types.append(appr_type)
        # print(appr_types)
        print(f'Unloaded {page_num} page out of {max_page_num}.')
        page_num += 1

    return appr_types


def main() -> None:
    """Main function."""
    total_count = get_json_on_request().get('totalCount')
    unload_all_app_types(total_count=total_count, page_size=100)


if __name__ == "__main__":
    main()
