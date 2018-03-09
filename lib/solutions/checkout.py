from collections import Counter

PRICES = [
    {
        "item": "A",
        "price": 50,
        "offer": {  # used for special offer
            "quantity": 3,
            "special_price": 130
        }
    },
    {
        "item": "B",
        "price": 30,
        "offer": {  # used for special offer
            "quantity": 2,
            "special_price": 45
        }
    },
    {
        "item": "C",
        "price": 20,
        "offer": {}
    },
    {
        "item": "D",
        "price": 15,
        "offer": {}
    },
]

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    price = -1
    sku_list = list(skus)
    if len(sku_list) > 0:
        denomination = Counter(sku_list)
        for key, value in denomination.items():
            price_obj = [price for price in PRICES if price['item'] == key]
            if len(price_obj) > 0:
                obj = price_obj[0]
                item_price = obj.get('price')
                offer = obj.get('offer')
                if offer:  # check if there is a special offer
                    quantity = offer.get('quantity')
                    special_price = offer.get('special_price')
                    remainder = value % quantity
                    offered_quantity = value / quantity
                    if remainder == 0:
                        price = offered_quantity * special_price
                    else:
                        # check if special offer applies
                        if offered_quantity > 0:  # Apply special offer
                            numbered_quantity = value - remainder
                            price = numbered_quantity * special_price
                            remainder_price = remainder * item_price
                            price += remainder_price
                        else:
                            price = remainder * item_price
    return price
