"""Collection of functions used for gathering and filtering data from source page"""

__all__ = ['gathering_data', 'saving_cleared_data_to_file', 'reduce_cleared_data', 'saving_filtered_data_to_file']

import re
import json
import os

from loguru import logger as LOGGER


async def gathering_data():
    """Function to filter and struct data"""

    with open('source.html', 'r', encoding='utf-8') as input_file:
        page = input_file.read()

    regex_main = re.findall(
        ',\"year\":(\d+).*?'
        ',\"tag_range\":{\"from\":(\d+)'
        ',\"to\":(\d+).*?'
        '{\"price\":(\d+),.*?'
        '\"saleId\":\"(\d+-\w+)\",.*?'
        '\"mileage\":(\d+).*?'
        , page, flags=re.DOTALL | re.MULTILINE)

    regex_name_link_saleid_price = re.findall(r'ImageObject.*?\",\"name\":\"(.*?|\s*?)\",\"creator\"(.*?|\s*?)\"url\":\"(.*?|\s*?\/)(\d+-\w+)\/\",\"price\":(\d+)', page)

    sale_ids = list(map(lambda x: x[3], regex_name_link_saleid_price))
    data_dict = dict.fromkeys(sale_ids, {})

    regex_saleid_photo = []
    for item in sale_ids:
        regex_photo = re.findall(fr'({item})\",.*?\"mileage\":(\d+).*?,\"1200x900n\":\"(.*?)\".*?', page, flags=re.DOTALL | re.MULTILINE)
        try:
            regex_saleid_photo.append(*regex_photo)
        except:
            LOGGER.error(f'Error while getting photo of saleid: {item}')

    counter = 0
    for item in sale_ids:
        counter += 1
        filtered_name_link_saleid_price = list(*filter(lambda x: x[3] == item, regex_name_link_saleid_price))
        filtered_main = list(*filter(lambda x: x[4] == item, regex_main))
        filtered_saleid_photo = list(*filter(lambda x: x[0] == item, regex_saleid_photo))
        try:
            data_dict[item] = {'name': filtered_name_link_saleid_price[0],
                               'price': f'{filtered_name_link_saleid_price[4]}р',
                               'year': f'{filtered_main[0]}г',
                               'mileage': f'{filtered_main[5]}км',
                               'price_range': f'{filtered_main[1]}р - {filtered_main[2]}р',
                               'lower_market_rate': f'{round(100 - (int(filtered_name_link_saleid_price[4]) * 100 / int(filtered_main[1])), 2)}%',
                               'photo_link': f'https:{filtered_saleid_photo[2]}',
                               'adv_link': f'{filtered_name_link_saleid_price[2]}{filtered_name_link_saleid_price[3]}'
                               }
        except Exception as err:
            LOGGER.error(f'{counter} - {item} - {filtered_name_link_saleid_price[0]} - {err}')
            data_dict[item] = {}

    cleared_data = {key: value for key, value in data_dict.items() if data_dict[key]}  # without None values
    filtered_data = {key: value for key, value in cleared_data.items()  # items with discount only
                     if float(data_dict[key]['lower_market_rate'][:-1]) > 0}
    LOGGER.debug(f'Number of items in new cleared_data: {len(cleared_data)}')
    LOGGER.debug(f'Number of items in filtered_data: {len(filtered_data)}')

    await saving_cleared_data_to_file(cleared_data)
    await reduce_cleared_data()
    await saving_filtered_data_to_file(filtered_data)


async def saving_cleared_data_to_file(cleared_data):
    """Function to save data dictionary without None items"""

    if not os.path.exists('cleared_data.json'):
        with open('cleared_data.json', 'w', encoding='utf-8') as output_file:
            output_file.write('{}')

    with open('cleared_data.json', 'r', encoding='utf-8') as input_file:
        data = json.load(input_file)

    updated_data = data | cleared_data  # join previous data with new one

    with open('cleared_data.json', 'w', encoding='utf-8') as output_file:
        json.dump(updated_data, output_file)
    LOGGER.success(f'cleared_data.json has been updated with new data. Total items: {len(updated_data)}')


async def reduce_cleared_data():
    """Function to reduce maximum elements in cleared data"""

    with open('cleared_data.json', 'r', encoding='utf-8') as input_file:
        data = json.load(input_file)
        if len(data) > 500:
            for i in range(len(data)-300):
                del data[list(data)[0]]

            with open('cleared_data.json', 'w', encoding='utf-8') as output_file:
                json.dump(data, output_file)
            LOGGER.success('cleared_data.json has been reduced')


async def saving_filtered_data_to_file(filtered_data):
    """Function to save data dictionary with filtered advertisements only"""

    if not os.path.exists('filtered_data.json'):
        with open('filtered_data.json', 'w', encoding='utf-8') as output_file:
            output_file.write('{}')

    if filtered_data:
        with open('filtered_data.json', 'w', encoding='utf-8') as output_file:
            json.dump(filtered_data, output_file)
        LOGGER.success(f'filtered_data has been saved to file:')
        for saleid, data in filtered_data.items():
            LOGGER.debug(f'{saleid} - {data}')
    else:
        LOGGER.debug('filtered_data was empty')
