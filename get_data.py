import re

from loguru import logger as LOGGER

with open('source.html', encoding='utf-8') as input_file:
    page = input_file.read()
LOGGER.success('source.html has been successfully uploaded')

regex_main = re.findall(
    ',\"year\":(\d+).*?'
    ',\"tag_range\":{\"from\":(\d+)'
    ',\"to\":(\d+).*?'
    # ',\"hash\":\"(\w+)\".*?'
    # ',\"id\":\"(\d+)\",.*?'
    '{\"price\":(\d+),.*?'
    '\"saleId\":\"(\d+-\w+)\",.*?'
    '\"mileage\":(\d+).*?'
    # '\"mark_info\".*?\"name\":\"(\w+)\",.*?'
    # '\"model_info\".*?\"name\":\"(\w+).*?'
    # '\"super_gen\".*?\"name\":\"(.*?)\"'  # fix bug with city name as super_gen with ru cars
    , page, flags=re.DOTALL | re.MULTILINE)

# regex = re.findall(',\"year\":(\d+).*?\"tag_range\":{\"from\":(\d+),\"to\":(\d+).*?,\"hash\":\"(\w+)\",.*?\"id\":\"(\d+)\",.*?{\"price\":(\d+),.*?\"saleId\":\"(\d+-\w+).*?\"mileage\":(\d+).*?\"mark_info\".*?\"name\":\"(\w+)\".*?\"model_info\".*?\"name\":\"(\w+).*?\"super_gen\".*?\"name\":\"(.*?)\"', page)
regex_saleid_photo = re.findall('\"saleId\":\"(\d+-\w+)\",.*?\"mileage\":(\d+).*?,\"1200x900n\":\"(.*?)\".*?', page)
regex_name_link_saleid_price = re.findall(r'240\",\"name\":\"(.*?|\s*?)\",(.*?|\s*?)\"url\":\"(.*?|\s*?/)(\d+-\w+)/\",\"price\":(\d+)', page)

# for num, item in enumerate(regex_main, 1):
#     print(num, item)
# print()
# for num, item in enumerate(regex_saleid_photo, 1):
#     print(num, item)
# print()
# for num, item in enumerate(regex_name_link_saleid_price, 1):
#     print(num, item)

sale_ids = list(map(lambda x: x[3], regex_name_link_saleid_price))
data_dict = dict.fromkeys(sale_ids, {})

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
        data_dict[item] = None

cleared_data = {key: value for key, value in data_dict.items() if data_dict[key]}  # without None values

filtered_data = {key: value for key, value in cleared_data.items()  # items with discount only
                 if float(data_dict[key]['lower_market_rate'][:-1]) > 0}
print(filtered_data)