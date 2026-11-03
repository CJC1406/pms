from decimal import Decimal, ROUND_HALF_UP

from src.models.product import Product
from src.services.inventory_service import get_total_stock


CENT = Decimal("0.01")


def money(value):
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def get_available_stock(session, product_id):
    return get_total_stock(session, product_id)


def add_cart_item(session, cart, product_id, quantity):
    if isinstance(product_id, bool) or not isinstance(product_id, int) or product_id <= 0:
        raise ValueError("Invalid product ID.")

    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Quantity must be a positive whole number.")

    product = session.get(Product, product_id)

    if product is None or not product.is_active:
        raise ValueError("Product not found or inactive.")

    existing_quantity = cart.get(product_id, {}).get("quantity", 0)
    new_quantity = existing_quantity + quantity
    available_stock = get_available_stock(session, product_id)

    if new_quantity > available_stock:
        raise ValueError("Requested quantity exceeds available stock.")

    unit_price = money(product.selling_price)

    cart[product_id] = {
        "product_id": product.id,
        "product_name": product.name,
        "sku": product.sku,
        "quantity": new_quantity,
        "unit_price": unit_price,
        "line_total": money(unit_price * new_quantity),
    }

    return cart[product_id]


def update_cart_quantity(session, cart, product_id, quantity):
    if product_id not in cart:
        raise ValueError("Product is not in the cart.")

    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Quantity must be a positive whole number.")

    available_stock = get_available_stock(session, product_id)

    if quantity > available_stock:
        raise ValueError("Requested quantity exceeds available stock.")

    item = cart[product_id]
    item["quantity"] = quantity
    item["line_total"] = money(item["unit_price"] * quantity)

    return item


def remove_cart_item(cart, product_id):
    if product_id not in cart:
        raise ValueError("Product is not in the cart.")

    del cart[product_id]


def calculate_cart_totals(items, tax_rate=Decimal("0"), discount_rate=Decimal("0")):
    tax_rate = Decimal(str(tax_rate))
    discount_rate = Decimal(str(discount_rate))

    if not tax_rate.is_finite() or not Decimal("0") <= tax_rate <= Decimal("100"):
        raise ValueError("Tax rate must be between 0 and 100.")

    if not discount_rate.is_finite() or not Decimal("0") <= discount_rate <= Decimal("100"):
        raise ValueError("Discount rate must be between 0 and 100.")

    subtotal = Decimal("0.00")

    for item in items:
        quantity = item.get("quantity")
        unit_price = Decimal(str(item.get("unit_price")))

        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Cart quantities must be positive whole numbers.")

        if not unit_price.is_finite() or unit_price < 0:
            raise ValueError("Unit price cannot be negative.")

        subtotal += money(unit_price * quantity)

    subtotal = money(subtotal)
    discount_amount = money(subtotal * discount_rate / Decimal("100"))
    taxable_amount = money(subtotal - discount_amount)
    tax_amount = money(taxable_amount * tax_rate / Decimal("100"))
    total = money(taxable_amount + tax_amount)

    return {
        "subtotal": subtotal,
        "discount_rate": discount_rate,
        "discount_amount": discount_amount,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "total": total,
    }
