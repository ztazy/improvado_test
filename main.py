import xml.etree.ElementTree as etree
import json
import csv
from itertools import chain


FILEPATH = [
    'data/csv_data_1.csv',
    'data/csv_data_2.csv',
    'data/json_Data.json',
    'data/xml_data.xml'
]


def min_finder(keys):
    D_max = int(max(filter(lambda x: x[0] == 'D', keys), key=lambda x: int(x[1:]))[1:])
    M_max = int(max(filter(lambda x: x[0] == 'M', keys), key=lambda x: int(x[1:]))[1:])
    min_value = min(D_max, M_max)

    return min_value


def sorter(list_input):
    for dict_input in list_input:
        d_items = [item for item in dict_input.items() if item[0][0] == 'D']
        m_items = [item for item in dict_input.items() if item[0][0] == 'M']
        d_items_sorted = sorted(d_items, key=lambda x: int(x[0][1:]))
        m_items_sorted = sorted(m_items, key=lambda x: int(x[0][1:]))
        yield dict(d_items_sorted+m_items_sorted)


def json_reader(file_path):
    # list_out = []
    with open(file_path) as json_data:
        data = json.load(json_data)
        # for field in data['fields']:
        #     list_out.append(field)

    return sorter(data['fields']), min_finder(data['fields'][0].keys())


def csv_reader(file_path):
    data = list()
    with open(file_path, "r") as csv_data:
        reader = csv.reader(csv_data)
        reader = list(reader)
        keys = reader[0]
        for row in reader[1:]:
            data.append({
                keys[i]: row[i]
                for i in range(len(row))
            })
    return sorter(data), min_finder(keys)


def xml_reader(file_path):
    data = {}
    tree = etree.parse(file_path)
    root = tree.getroot()
    for objects in root:
        for xml_object in objects:
            key = xml_object.attrib
            for value in xml_object:
                data[key['name']] = value.text
    return sorter([data]), min_finder(data.keys())


def cutter(list_input, min_index_input):
    return [
        dict(
            (key, value)
            for key, value in dict_item.items()
            if int(key[1:]) <= min_index
        )
        for dict_item in list_input
    ]


csv_data1, min_value_csv1 = csv_reader(FILEPATH[0])
csv_data2, min_value_csv2 = csv_reader(FILEPATH[1])
json_data, min_value_json = json_reader(FILEPATH[2])
xml_data, min_value_xml = xml_reader(FILEPATH[3])
min_index = min(min_value_csv1, min_value_csv2, min_value_json, min_value_xml)
csv_data1, csv_data2, json_data, xml_data = map(lambda item: cutter(item, min_index), [csv_data1, csv_data2, json_data, xml_data])

all_data = list(chain(csv_data1, csv_data2, json_data, xml_data))

all_data = sorted(all_data, key=lambda item: item['D1'])

header = all_data[0].keys()
result = "\t".join(header) + '\n'

for data in all_data:
    result += "\t".join(map(str, data.values())) + '\n'

# print(json_data[0].values())
print(result)

