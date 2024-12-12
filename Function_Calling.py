class Function:
    """
    Класс для создания и управления JSON-описанием функции.
    
    Параметры:
    - Name (str): Имя функции.
    - Description (str): Описание функции.
    """
    def __init__(self, Name: str, Description: str):
        self.FunctionJSON = {
            "type": "function",
            "function": {
                "name": Name,
                "description": Description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "strict": True
        }
        self.Function = self.FunctionJSON["function"]["parameters"]
        
    def add_param(self, FName, FType, FDescription, Enum=[], FRequire=True):
        """
        Добавляет параметр к функции.
        
        Параметры:
        - FName (str): Имя параметра.
        - FType (str): Тип параметра (например, "number", "string" и т.д.).
        - FDescription (str): Описание параметра.
        - Enum (list): Возможные значения для параметра (по умолчанию пустой список).
        - FRequire (bool): Определяет, является ли параметр обязательным (по умолчанию False).
        
        Возвращает:
        dict: Обновленный словарь параметров.
        """
        self.Function["properties"].update(
            {FName: {"type": FType, "description": FDescription}}
        )
        if FRequire:
            self.Function["required"].append(FName)
        if len(Enum) > 0:
            self.Function["properties"][FName].update({"enum": Enum})
        return self.Function["properties"][FName]
    
    def add_param_number(self, FName, FDescription, FRequire=True, Enum=[]):
        """
        Добавляет числовой параметр.
        
        Параметры:
        - FName (str): Имя параметра.
        - FDescription (str): Описание параметра.
        - FRequire (bool): Определяет, является ли параметр обязательным (по умолчанию False).
        - Enum (list): Возможные значения для параметра (по умолчанию пустой список).
        
        Возвращает:
        Function: Экземпляр класса Function.
        """
        self.add_param(FName, "number", FDescription, Enum=Enum, FRequire=FRequire)
        return self
        
    def add_param_integer(self, FName, FDescription, FRequire=True, Enum=[]):
        """
        Добавляет целочисленный параметр.
        
        Параметры:
        - FName (str): Имя параметра.
        - FDescription (str): Описание параметра.
        - FRequire (bool): Определяет, является ли параметр обязательным (по умолчанию False).
        - Enum (list): Возможные значения для параметра (по умолчанию пустой список).
        
        Возвращает:
        Function: Экземпляр класса Function.
        """
        self.add_param(FName, "integer", FDescription, Enum=Enum, FRequire=FRequire)
        return self
        
    def add_param_string(self, FName, FDescription, FRequire=True, Enum=[]):
        """
        Добавляет строковый параметр.
        
        Параметры:
        - FName (str): Имя параметра.
        - FDescription (str): Описание параметра.
        - FRequire (bool): Определяет, является ли параметр обязательным (по умолчанию False).
        - Enum (list): Возможные значения для параметра (по умолчанию пустой список).
        
        Возвращает:
        Function: Экземпляр класса Function.
        """
        self.add_param(FName, "string", FDescription, Enum=Enum, FRequire=FRequire)
        return self
        
    def add_param_array(self, FName, FDescription, FRequire=True, Enum=[]):
        """
        Добавляет массивовой параметр.
        
        Параметры:
        - FName (str): Имя параметра.
        - FDescription (str): Описание параметра.
        - FRequire (bool): Определяет, является ли параметр обязательным (по умолчанию False).
        - Enum (list): Возможные значения для параметра (по умолчанию пустой список).
        
        Возвращает:
        Function: Экземпляр класса Function.
        """
        self.add_param(FName, "array", FDescription, Enum=Enum, FRequire=FRequire)
        return self
        
    def add_param_enum(self, FName, FDescription, FRequire=True, Enum=[]):
        """
        Добавляет параметр типа enum.
        
        Параметры:
        - FName (str): Имя параметра.
        - FDescription (str): Описание параметра.
        - FRequire (bool): Определяет, является ли параметр обязательным (по умолчанию False).
        - Enum (list): Возможные значения для параметра (по умолчанию пустой список).
        
        Возвращает:
        Function: Экземпляр класса Function.
        """
        self.add_param(FName, "enum", FDescription, Enum=Enum, FRequire=FRequire)
        return self
        
    def add_param_boolean(self, FName, FDescription, FRequire=True, Enum=[]):
        """
        Добавляет булевый параметр.
        
        Параметры:
        - FName (str): Имя параметра.
        - FDescription (str): Описание параметра.
        - FRequire (bool): Определяет, является ли параметр обязательным (по умолчанию False).
        - Enum (list): Возможные значения для параметра (по умолчанию пустой список).
        
        Возвращает:
        Function: Экземпляр класса Function.
        """
        self.add_param(FName, "boolean", FDescription, Enum=Enum, FRequire=FRequire)
        return self
    
    def add_param_object(self, FName, FObject: dict, FDescription, FRequire=True):
        """
        Добавляет объектный параметр.
        
        Параметры:
        - FName (str): Имя параметра.
        - FObject (dict): Описание объекта.
        - FDescription (str): Описание параметра.
        - FRequire (bool): Определяет, является ли параметр обязательным (по умолчанию False).
        
        Возвращает:
        Function: Экземпляр класса Function.
        """
        obj = self.add_param(FName, "object", FDescription, FRequire=FRequire)
        obj.update({"properties": FObject()["function"]["parameters"]["properties"]})
        return self
        
    def __call__(self):
        """
        Возвращает JSON-описание функции.
        
        Возвращает:
        dict: JSON-описание функции.
        """
        return self.FunctionJSON
class Object(Function):
    """
    Класс для создания объекта.
    """
    def __init__(self):
        super().__init__(Name="", Description="")
