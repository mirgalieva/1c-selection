import PySimpleGUI as sg
import copy

# from entity.Indicator import Indicator
# from entity.Attribute import Attribute
import sys

sys.path.append("src")
from windows.createWindows import new_attr_layout, new_unsupported_values
from business.dictFunctions import *

def create_lsit_attr_layout(indicator, attributes_list, unsupp_list): #ОТВРАТИТЕЛЬНАЯ ПРАКТИКА indicator содержит attributes_list
    data_rows = []
    button_rows = []
    beauty_unsupp_list = []

    def get_values_by_hashes(attributes_list, input_hashes):
        # Создаем пустой список для результатов
        result_values = []
        
        # Проходим по каждой сущности в списке
        for attr in attributes_list:
            # Проходим по каждому хешу в списке хешей сущности
            for i, hash_ in enumerate(attr.unique_hash):
                # Если этот хеш есть во входных хэшах
                if hash_ in input_hashes:
                    # Добавляем соответствующее значение в результат
                    result_values.append("{}-{} \n".format(attr.name, attr.list_values[i]))
        
        return result_values
    
    if (len(unsupp_list) > 0):
        for condition in unsupp_list:
            hashes = condition.split(' и ')
            beauty_unsupp_list.append(get_values_by_hashes(attributes_list, hashes))

    print(beauty_unsupp_list)

    for i, attribute in enumerate(attributes_list):
        # Добавляем значения в таблицу по одному
        # for val in attribute.list_values:

        data_rows.append([attribute.name, attribute.type_name, attribute.dict_name, attribute.list_values[0]])
        # Добавляем оставшиеся значения в таблицу с пустыми ячейками
        for val in attribute.list_values[1:]:
            data_rows.append(["", "", "", val])
        # Добавляем кнопку для каждого атрибута
        button_rows.append([sg.Button('Удалить', key=f'-DELETE_{i}-')])

    data_column = [
        [sg.Table(values=data_rows, headings=['Имя атрибута', 'Тип', 'Названия справочника', 'Значения'], display_row_numbers=False,
                  auto_size_columns=True,  size=(80, 10), num_rows=min(25, len(data_rows)))],
    ]

    layout = [
        [sg.Text("Название показателя:"), sg.Text(indicator.name)],
        [sg.Text("ID показателя:"), sg.Text(indicator.id_)],
        [sg.Text("Описание показателя:"), sg.Text(indicator.description)],
        [sg.Column(data_column), sg.Column(button_rows)],
        [sg.Button('Создать', size=(10, 1), key='-CREATE-', font=("Arial", 12), pad=((500, 0), 3))],
        [sg.Button('Добавить в таблицу', size=(20, 1), key='-TABLE-', font=("Arial", 12), pad=((500, 0), 3))],
        [sg.Button('Добавить недопустимые сочетания', size=(20, 1), key='-UNSUPP-', font=("Arial", 12), pad=((500, 0), 3))],
        [sg.Text("Список добавленных недопустимых значений", font=("Arial", 14))],  # Это ваш заголовок
        [sg.Listbox(values=beauty_unsupp_list, size=(80, 10), font=("Arial", 12))], # 80 - это ширина виджета, 10 - количество видимых строк

    ]
    return layout



def list_attr_layout(indicator):
    # indicator_copy = copy.deepcopy(indicator)

    attributes_list = indicator.list_attributes
    # attributes_list.append(Attribute("mem", 0))
    unsupp_list = []
    # Создаем таблицу
    window = sg.Window("Окно создания атрибутов", create_lsit_attr_layout(indicator, attributes_list, unsupp_list), finalize=True, resizable=True, font=("Arial", 12))

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            window.close()
            return False, []
            
        # Создается атрибут и переходим на страничку редактирования атрибута
        if event.startswith('-DELETE_'):
            # if( == '0-'):
            #     index_to_delete = 0
            # else:
            index_to_delete = int(event.split('_')[-1].split('-')[0])  # Извлекаем индекс из ключа

                # Проверяем, что индекс не выходит за пределы списка
            del attributes_list[index_to_delete]  # Удаляем атрибут из списка

            # Обновляем layout
            new_layout = create_lsit_attr_layout(indicator, attributes_list, unsupp_list)
            # window.Layout(new_layout)
            window.close()
            window = sg.Window("Окно создания атрибутов", new_layout, finalize=True, resizable=True, font=("Arial", 12))

        if event == '-CREATE-':
            new_attr_layout(indicator)
            new_layout = create_lsit_attr_layout(indicator, attributes_list, unsupp_list)
            # window.Layout(new_layout)
            window.close()
            window = sg.Window("Окно создания атрибутов", new_layout, finalize=True, resizable=True, font=("Arial", 12))
        
        if event == '-UNSUPP-':
            unsupp_list.append(new_unsupported_values(attributes_list))
            new_layout = create_lsit_attr_layout(indicator, attributes_list, unsupp_list)
            # window.Layout(new_layout)
            window.close()
            window = sg.Window("Окно создания атрибутов", new_layout, finalize=True, resizable=True, font=("Arial", 12))

        if event == '-TABLE-':
            if confirm_action():
                break
                
    window.close()
    return True, unsupp_list

def confirm_action():
    layout = [
        [sg.Text("Вы уверены в добавлении атрибутов в таблицу?")],
        [sg.Button("Да"), sg.Button("Нет")]
    ]

    window = sg.Window("Подтверждение", layout)

    event, values = window.read()

    window.close()

    if event == "Да":
        return True
    else:
        return False
    


class CustomObject:
    def __init__(self, name, dict_, unique_hash):
        self.name = name
        self.dict = dict_
        self.unique_hash = unique_hash

# Пример объектов:
obj1 = CustomObject("name1", "dict1", "3872f60e485f6e688cf55edb959efd6a02f389139ded2e86e5f839b8907f1b10")
obj2 = CustomObject("name2", "dict2", "c6d1e464452a7af1a5c23837ade79ffc72ffebd176fedecf7b5d8d93a778c103")

# Создаем словарь для сопоставления:
hash_to_object = {obj1.unique_hash: obj1, obj2.unique_hash: obj2}
hashes = ['3872f60e485f6e688cf55edb959efd6a02f389139ded2e86e5f839b8907f1b10 и c6d1e464452a7af1a5c23837ade79ffc72ffebd176fedecf7b5d8d93a778c103']

def convert_hash_to_string(hash_str):
    hashes_in_str = hash_str.split(' и ')
    return ' и '.join([f"{hash_to_object[h].name}.{hash_to_object[h].dict}" for h in hashes_in_str])

converted = [convert_hash_to_string(hash_str) for hash_str in hashes]
print(converted)  # ['name1.dict1 и name2.dict2']
