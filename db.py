import json

class DB:
    def __init__(self,path):
        self.path = path
        # Read the data from the file
        self.data = {}
        with open(self.path,'r') as f:
            self.data = json.load(f)


    def getPhone(self,brand,idx):
        """
        Return phone data by brand
        args:
            brand: str
        return:
            dict
        """
        phone = self.data[brand][idx]
        data = {
            'model':phone['name'],
            'color':phone['color'],
            'ram':phone['RAM'],
            'price':phone['price'],
            'memory':phone['memory'],
            'image':phone['img_url'],
        }
        return data

    def get_phone_list(self,brend):
        """
        Return phone list
        """
        phone = self.data[brend]
        return list(phone.keys())

        

# db = DB('db.json')
# print(db.getPhone('Apple'))
# print(db.get_phone_list('Apple'))


