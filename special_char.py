import json

with open('C:/Users/mhammed/Downloads/comments_export2.json', 'r') as f:
    data = json.load(f)
    #     print(data)

for key in data:
    text = data[key]['text']
    special_char_map = {ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe', ord('Ö'): 'Oe', ord('ß'): 'ss'}
    #     print(text.translate(special_char_map))

    text = text.translate(special_char_map)
    data[key]['text'] = text

with open('C:/Users/mhammed/Downloads/comments_export3.json', 'w') as f:
json.dump(data, f, indent=4)
