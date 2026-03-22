class User:
    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def get_profile(self):
        return {
            "username": self.username,
            "email": self.email,
            "age": self.age,
            "active": self.is_active,
        }

    def update_email(self, new_email):
        if validate_email(new_email):
            self.email = new_email
            return True
        return False


class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def is_available(self):
        return self.stock > 0

    def apply_discount(self, percent):
        discounted = calculate_discount(self.price, percent)
        self.price = discounted
        return self.price

    def restock(self, quantity):
        self.stock += quantity


def validate_email(email):
    return "@" in email and "." in email


def calculate_discount(price, percent):
    if percent < 0 or percent > 100:
        raise ValueError("Discount percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)
