class Function:
    def __init__(self, Name: str, Description: str):
        self.FunctionJSON = {
            "type": "function",
            "function": {
                "name": Name,
                "description": Description,
                "parameters": {
                    "type": "object",
                    "properties": {
                    },
                    "required": []
                }
            },
            "strict": True
        }
        self.Function = self.FunctionJSON["function"]["parameters"]
        
    def add_param(self, FName, FType, FDescription, Enum=[], FRequire = False):
        self.Function["properties"].update(
            {FName: {"type": FType, "description": FDescription}}
        )
        if FRequire: self.Function["required"].append(FName)
        if len(Enum) > 0: self.Function["properties"][FName].update({"enum": Enum})
        return self.Function["properties"][FName]
    
    def add_param_number(self, FName, FDescription, FRequire = False, Enum=[]):
        self.add_param(FName, "number", FDescription, Enum=Enum, FRequire=FRequire)
        return self
        
    def add_param_integer(self, FName, FDescription, FRequire = False, Enum=[]):
        self.add_param(FName, "integer", FDescription, Enum=Enum, FRequire=FRequire)
        return self
        
    def add_param_string(self, FName, FDescription, FRequire = False, Enum=[]):
        self.add_param(FName, "string", FDescription, Enum=Enum, FRequire=FRequire)
        return self
        
    def add_param_array(self, FName, FDescription, FRequire = False, Enum=[]):
        self.add_param(FName, "array", FDescription, Enum=Enum, FRequire=FRequire)
        return self
        
    def add_param_enum(self, FName, FDescription, FRequire = False, Enum=[]):
        self.add_param(FName, "enum", FDescription, Enum=Enum, FRequire=FRequire)
        return self
        
    def add_param_boolean(self, FName, FDescription, FRequire = False, Enum=[]):
        self.add_param(FName, "boolean", FDescription, Enum=Enum, FRequire=FRequire)
        return self
    
    def add_param_object(self, FName, FObject: dict, FDescription, FRequire = False):
        obj = self.add_param(FName, "object", FDescription, FRequire=FRequire)
        obj.update({"properties": FObject["function"]["parameters"]["properties"]})
        return self
        
    def __call__(self):
        return self.FunctionJSON
class Object(Function):
    def __init__(self):
        super().__init__(Name="", Description="")