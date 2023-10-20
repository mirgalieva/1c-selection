import hashlib

class Attribute:
    
    '''
    Класс атрибутов. Реализует обьект аттрибута, содержит тип, название справочника и допустимые значения справочника
    '''

    def __init__(self, name: str, type_: str):
        self.__name = name
        self.__type = type_
        self.__dict_name = {}
        self.__list_values = []
        self.__type_name = None
        self.__unique_hash = []

    # Геттеры
    @property
    def name(self) -> str:
        return self.__name

    @property
    def type_(self) -> str:
        return self.__type

    @property
    def dict_name(self) -> dict:
        return self.__dict_name

    @property
    def list_values(self) -> list:
        return self.__list_values
    
    @property
    def type_name(self) -> str:
        return self.__type_name
    
    @property
    def unique_hash(self) -> list:
        return self.__unique_hash

    # Сеттеры
    @name.setter
    def name(self, value: str):
        self.__name = value

    @type_.setter
    def type_(self, value: str):
        
        self.__type = value

    @dict_name.setter
    def dict_name(self, value: dict):
        self.__dict_name = value

    @list_values.setter
    def list_values(self, value: list):
        self.__list_values = value

    @type_name.setter
    def type_name(self, value: str):
        if (self.type_):
            self.__type_name = "Классифицируемый атрибут"
        else:
            self.__type_name = "Неклассифицируемый атрибут"     

    @unique_hash.setter
    def unique_hash(self, value: list):
        self.__unique_hash = value

    def calculate_hash(self):
        self.__unique_hash = []
        for value in self.__list_values:
            hash_input = f"{self.__name}{self.__type}{self.__dict_name}{value}".encode('utf-8')
            hash_value = hashlib.sha256(hash_input).hexdigest()
            self.__unique_hash.append(hash_value)       