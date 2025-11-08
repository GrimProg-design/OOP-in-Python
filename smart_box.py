class Product:
    def __init__(self, name, price, category, discount):
        self.name = name
        self.price = price
        self.category = category
        self.discount = discount

    def get_final_price(self):
        return self.price

    def __eq__(self, value):
        pass

    def __bash__():
        pass

class ShoppingCart:
    def __init__(self, owner, budget):
        self.owner = owner
        self.budget = budget
        self.items = {1: 'apple'}

    def __len__(self):
        return f'Всего товаров в корзине: {len(self.items)}'

    def __getitem__(self, key):
            if key in self.items:
                return self.items.get(key)
            else:
                raise KeyError(f'товара c id: {key} нет')

    def __setitem__(self, key, value):
        if key in self.items:
            raise KeyError(f'Товар с id: {key} уже существует в корзине выберите другой')
        else:
            self.items.update({key: value})
            return f'Товар {value} успешно добавлен'

    def __delitem__(self, key):
        if key in self.items:
            self.items.pop(key)
            return 'Товар успешно удален'
        else:
            raise KeyError(f'Товара с id: {key} нет')

    def __contains__(self, item):
        for i in self.items.values():
            if i == item:
                return 'товар есть в корзине'
            else:
                return 'товара нет в корзине'

    def __iter__():
        pass

    def __add__():
        pass

    def __iadd__():
        pass

    def __str__(self):
        pass

    def get_total():
        pass

    def apply_promo_code(code):
        pass

    def can_afford():
        pass

    def most_expensive():
        pass

class User:
    def __init__(self, name):
        self.name = name
        self.sum = 0

    def __len__(self):
        self.sum += self.name
        return self.sum


try:
    new_product = Product('apple', 23, 'fruit', False)
    new_product_2 = Product('banana', 27, 'fruit', False)
    box = ShoppingCart('Ilia', 200)
    print(new_product.get_final_price())
    print(box.__len__())
    print(box.__getitem__(1))
    print(box.__setitem__(2, 'banana'))
    print(box.__getitem__(2))

    print(box.__setitem__(5, 'Abrokos'))
    print(box.__len__())
    print(box.__delitem__(5))
    print(box.__len__())

    print(box.__contains__('apple'))
except KeyError as err:
    print('Ошибка:', err)