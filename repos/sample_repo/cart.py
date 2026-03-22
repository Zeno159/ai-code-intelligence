from models import Product, calculate_discount


class Cart:
    def __init__(self, user):
        self.user = user
        self.items = []  # list of {"product": Product, "quantity": int}

    def add_item(self, product, quantity):
        if not product.is_available():
            return False
        for item in self.items:
            if item["product"].name == product.name:
                item["quantity"] += quantity
                return True
        self.items.append({"product": product, "quantity": quantity})
        return True

    def remove_item(self, product_name):
        self.items = [i for i in self.items if i["product"].name != product_name]

    def get_total(self):
        total = 0
        for item in self.items:
            total += item["product"].price * item["quantity"]
        return round(total, 2)

    def apply_cart_discount(self, percent):
        total = get_total(self)
        return calculate_discount(total, percent)

    def checkout(self):
        if not self.items:
            return {"success": False, "reason": "Cart is empty"}
        summary = build_order_summary(self.user, self.items, self.get_total())
        self.items = []
        return summary


def build_order_summary(user, items, total):
    return {
        "user": user.get_profile(),
        "items": [
            {"name": i["product"].name, "qty": i["quantity"], "price": i["product"].price}
            for i in items
        ],
        "total": total,
    }


def get_total(cart):
    return cart.get_total()
