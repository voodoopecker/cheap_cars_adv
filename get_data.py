import re

with open('source.html', encoding='utf-8') as input_file:
    page = input_file.read()

regex = re.findall(
    ',\"year\":(\d+).*?'
    ',\"tag_range\":{\"from\":(\d+)'
    ',\"to\":(\d+).*?'
    ',\"hash\":\"(\w+)\".*?'
    ',\"id\":\"(\d+)\",.*?'
    '{\"price\":(\d+),.*?'
    '\"saleId\":\"(\d+-\w+)\",.*?'
    '\"mileage\":(\d+).*?'
    '\"mark_info\".*?\"name\":\"(\w+)\",.*?'
    '\"model_info\".*?\"name\":\"(\w+).*?'
    '\"super_gen\".*?\"name\":\"(.*?)\"'  # fix bug with city name as super_gen with ru cars
    , page)

# regex_photo = re.findall('\"saleId\":\"(\d+-\w+)\",.*?\"mileage\":(\d+).*?,\"1200x900n\":\"(.*?)\".*?', page)

for num, item in enumerate(regex, 1):
    print(num, item)
