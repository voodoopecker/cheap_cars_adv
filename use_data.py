import json


with open('cleared_data.json', 'r', encoding='utf-8') as input_file:
    cleared_data = json.load(input_file)
    for k, v in cleared_data.items():
        print(k, v)
print()

async def post_message():
    with open('filtered_data.json', 'r', encoding='utf-8') as input_file:
        filtered_data = json.load(input_file)
        messages = {}
        for k, v in filtered_data.items():
            if k in cleared_data.keys():
                continue
            else:
                messages[k] = v
    return messages
