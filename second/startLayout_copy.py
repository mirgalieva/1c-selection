import PySimpleGUI as sg
from entity import Indicator
from entity.Attribute import Attribute
import sys
sys.path.append("src")

from business.dictFunctions import *

# Layout для создания нового показателя
# def start_layout(indicator_list):
#     col = [[sg.Listbox(values=[(ind.id_, ind.name) for ind in indicator_list], size=(60, 20), key="-IND_LIST-")]]
#     return [
#         [sg.Column(col, key='-COL1-', expand_x=True, expand_y=True)],
#         [sg.Button("Создать атрибут", size=(20, 1), font=("Arial", 12))]
#     ]

def start_layout(indicator_list):
    listbox_layout = [
        [sg.Listbox(values=[(ind.id_, ind.name, ind.description) for ind in indicator_list], key="-IND_LIST-", size=(100, 30))],
    ]

    layout = [
        [sg.Column(listbox_layout, key='-COL1-', expand_x=True, expand_y=True, pad=((10, 10), (10, 0)))],
        [sg.Button("Создать показатель", size=(20, 1), font=("Arial", 12), pad=((10, 10), (10, 10)))],
        [sg.Button("Завершить работу", size=(30, 1), font=("Arial", 12), pad=((10, 10), (10, 10)))]

    ]
    return layout



