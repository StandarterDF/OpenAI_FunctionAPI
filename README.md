# Примеры использования (AI):

```python
from openai import OpenAI
import math, json, Function_Calling

# Connect to LM Studio
client = OpenAI(base_url="http://192.168.0.124:1234/v1", api_key="qwen2.5-coder-3b-instruct")


# --- Пример 1: Функция для сложения чисел ---
add_func = Function_Calling.Function("add_function", "Складывает два числа")
add_func.add_param_number("num1", "Первое число", FRequire=True)
add_func.add_param_number("num2", "Второе число", FRequire=True)


# --- Пример 2: Функция для вычисления степени ---
power_func = Function_Calling.Function("power_function", "Возводит число в степень")
power_func.add_param_number("base", "Основание", FRequire=True)
power_func.add_param_number("exponent", "Показатель степени", FRequire=True)


# --- Пример 3: Функция для создания информации о книге ---
book_func = Function_Calling.Function("book_info", "Создает информацию о книге")
book_func.add_param_string("title", "Название книги", FRequire=True)
book_func.add_param_string("author", "Автор книги", FRequire=True)
book_func.add_param_integer("year", "Год издания", FRequire=True)



# --- Пример 4: Функция с массивом и перечислением ---

array_enum_func = Function_Calling.Function("array_enum_function", "Функция с массивом и перечислением")
array_enum_func.add_param_array("colors", "Список цветов", FRequire=True, Enum=["red", "green", "blue"])
array_enum_func.add_param_enum("size", "Размер", FRequire=True, Enum=["small", "medium", "large"])


# --- Пример 5: Вложенные объекты ---

address_object = Function_Calling.Object().add_param_string("street", "Улица").add_param_string("city", "Город")

user_func = Function_Calling.Function("user_info", "Создает информацию о пользователе")
user_func.add_param_string("name", "Имя пользователя", FRequire=True)
user_func.add_param_object("address", address_object, "Адрес пользователя", FRequire=True)



while True:
    prompt = input("Enter prompt: ")
    response = client.chat.completions.create(
        model="qwen2.5-coder-3b-instruct",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": f"{prompt}"}
        ],
        tools=[add_func(), power_func(), book_func(), array_enum_func(), user_func()], # Добавляем все функции
        temperature=0.3
    )

    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if function_name == "add_function":
                result = arguments["num1"] + arguments["num2"]
                print(f"Результат сложения: {result}")
            elif function_name == "power_function":
                result = arguments["base"] ** arguments["exponent"]
                print(f"Результат возведения в степень: {result}")
            elif function_name == "book_info":
                print(f"Информация о книге: {arguments}")
            elif function_name == "array_enum_function":
                 print(f"Массив и перечисление: {arguments}")
            elif function_name == "user_info":
                print(f"Информация о пользователе: {arguments}")
            else:
                print(f"Неизвестная функция: {function_name}")
```
# Описание функций библиотеки (AI)
```python
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
        
    def add_param(self, FName, FType, FDescription, Enum=[], FRequire=False):
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
    
    def add_param_number(self, FName, FDescription, FRequire=False, Enum=[]):
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
        
    def add_param_integer(self, FName, FDescription, FRequire=False, Enum=[]):
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
        
    def add_param_string(self, FName, FDescription, FRequire=False, Enum=[]):
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
        
    def add_param_array(self, FName, FDescription, FRequire=False, Enum=[]):
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
        
    def add_param_enum(self, FName, FDescription, FRequire=False, Enum=[]):
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
        
    def add_param_boolean(self, FName, FDescription, FRequire=False, Enum=[]):
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
    
    def add_param_object(self, FName, FObject: dict, FDescription, FRequire=False):
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
```
