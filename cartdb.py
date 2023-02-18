import json
class Cart:
    def __init__(self,cart_path:str):
        self.cart_path = cart_path
      
        self.data = {
            'cart':[]
        }
        with open(self.cart_path,'r') as file:
            self.data = json.load(file)


    def add(self,brand,model_id):
        self.data['cart'].append({
            'brand':brand,
            'model_id':model_id
        })
        self.save()

    def save(self):
        with open(self.cart_path,'w') as file:
            json.dump(self.data,file,indent=4)

    def get_cart(self):
        return self.data['cart']


# cart = Cart('cartdb.json')
# cart.add('Redmi','Redmi 9')
# print(cart.data)


        