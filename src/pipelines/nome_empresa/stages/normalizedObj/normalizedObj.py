class NormalizeObj:
    def __init__(self):
        self.new_object = []
    
    def get_children(self, obj, key):
        return obj[key]
    
    def linearilize_object(self, object, parent_key=''):
        new_object = {}
        for key, value in object.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                new_object.update(self.linearilize_object(value, new_key))
            else:
                new_object[new_key] = value
        return new_object

    def get_types(self, obj_list):
        fields = {}
        for obj in obj_list:
            for field in obj:
                if field not in fields:
                    fields[field] = {}
                    fields[field][type(obj[field]).__name__] = 1
                elif type(obj[field]).__name__ not in fields[field]:
                    fields[field][type(obj[field]).__name__] = 1
                else:
                    fields[field][type(obj[field]).__name__] = fields[field][type(obj[field]).__name__] + 1
        return fields
    def set_types(self, obj_list, types = {}):
        new_objects = []
        for obj in obj_list:
            for field in obj:
                if (type(obj[field]).__name__ in types):
                    converted_value = self.convert_to_type(value=obj[field], type= type(obj[field]).__name__)
                    obj[field] = converted_value
                else:
                    obj[field]= str(obj[field])

            new_objects.append(obj)
        return new_objects
    def get_all_childs(self, list_obj, level = 0):
        if level == 0:
            self.new_object = []
            
        list_obj= self.delete_keys(obj=list_obj, delete_keys=[
            "dtref",
            "livres",
            "start",
            "end",
            "livres",
            "__v",
            "deliverable"
        ])

        for i in range(len(list_obj)):        
            if type(list_obj[i]).__name__ == 'dict':
                level = level + 1
                temp_list_obj = list_obj[i]
                if 'data' in temp_list_obj:
                    del temp_list_obj['data']

                self.new_object.append(temp_list_obj)
                
                self.get_all_childs(self.find_list(list_obj[i]), level)

        return self.new_object
                
    def find_list(self, obj):
        for i in obj:
            if(type(obj[i]).__name__ == 'list'):
                return obj[i]
        return []
    
    def delete_keys(self, obj, delete_keys=[]):
        for i in obj:
            for del_key in delete_keys:
                if del_key in i:
                    del i[del_key]

        return obj

    def convert_to_type(self, value, type):
        try:
            return eval(type)(value)
        except ValueError:
            raise ValueError(f"Valor inválido para conversão para o type '{type}'")
        except TypeError:
            raise ValueError(f"Tipo '{type}' não é válido")