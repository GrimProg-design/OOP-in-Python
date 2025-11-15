class Product:
    def __init__(self, name, price, category, discount=0):
        self.name = name
        self.price = price
        self.category = category
        self.discount = discount

    def get_final_price(self):
        return self.price * (1 - self.discount / 100)

    def __eq__(self, other):
        return isinstance(other, Product) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"{self.name} ({self.category}) — {self.price}coм (-{self.discount}%)"


class ShoppingCart:
    def __init__(self, owner, budget):
        self.owner = owner
        self.budget = budget
        self.items = {}
        self.used_promocodes = set()
        self.promocodes = {
            "FOOD10": {"category": "food", "discount": 10},
            "TECH20": {"category": "tech", "discount": 20},
            "ALL5": {"category": None, "discount": 5},
        }

    def __len__(self):
        return sum(self.items.values())

    def __getitem__(self, product):
        return self.items.get(product, 0)

    def __setitem__(self, product, quantity):
        if quantity < 0:
            raise ValueError("Количество товара не может быть отрицательным")

        if quantity == 0:
            self.items.pop(product, None)
            return

        if product not in self.items:
            if self.get_total() + product.get_final_price() * quantity > self.budget:
                raise ValueError("Бюджет превышен")

        self.items[product] = quantity

    def __delitem__(self, product):
        self.items.pop(product, None)

    def __contains__(self, product):
        return product in self.items

    def __iter__(self):
        return iter(self.items.keys())

    def __add__(self, other):
        new_cart = ShoppingCart(self.owner, self.budget)
        new_cart.items = self.items.copy()

        for product, quantity in other.items.items():
            if product in new_cart.items:
                new_cart.items[product] += quantity
            else:
                new_cart.items[product] = quantity

        return new_cart

    def __iadd__(self, product):
        if product in self.items:
            new_qty = self.items[product] + 1
        else:
            new_qty = 1

        if self.get_total() + product.get_final_price() > self.budget:
            raise ValueError("Недостаточно бюджета для добавления товара")

        self.items[product] = new_qty
        return self

    def __str__(self):
        if not self.items:
            return f"Корзина пуста. Бюджет: {self.budget}₽"

        text = f"Корзина {self.owner} (бюджет: {self.budget}сом):\n"
        for product, qty in self.items.items():
            text += f"  - {product.name} х {qty} = {product.get_final_price() * qty:.2f}сом\n"
        text += f"\nИтого: {self.get_total():.2f}₽"
        return text


    def get_total(self):
        total = 0
        for product, qty in self.items.items():
            total += product.get_final_price() * qty

        for code in self.used_promocodes:
            promo = self.promocodes.get(code)
            if not promo:
                continue

            category = promo["category"]
            discount = promo["discount"]

            if category is None:
                total *= (1 - discount / 100)
            else:
                for product, qty in self.items.items():
                    if product.category == category:
                        total -= product.get_final_price() * qty * (discount / 100)

        return total

    def apply_promo_code(self, code):
        if code in self.used_promocodes:
            raise ValueError("Промокод уже использован")

        if code not in self.promocodes:
            raise ValueError("Неверный промокод")

        self.used_promocodes.add(code)

    def can_afford(self):
        return self.get_total() <= self.budget

    def most_expensive(self):
        if not self.items:
            return None
        return max(self.items.keys(), key=lambda p: p.get_final_price())

p1 = Product("Яблоко", 10, "food")
p2 = Product("Наушники", 3000, "tech", discount=10)
p3 = Product("Печенье", 150, "food")

cart = ShoppingCart("Илья", 5000)

cart += p1
cart += p3
cart[p2] = 1

print(cart)

cart.apply_promo_code("FOOD10")

print("\nПосле промокода:")
print(cart)
