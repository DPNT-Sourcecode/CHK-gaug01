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
    sku_list = list(skus.upper())
    if len(sku_list) > 0:
        denomination = Counter(sku_list)
        total_price = 0
        for key, value in denomination.items():
            price_obj = [price for price in PRICES if price['item'] == key]
            if len(price_obj) > 0:
                obj = price_obj[0]
                individual_price = obj.get('price')
                offer = obj.get('offer')
                if offer:  # check if there is a special offer
                    quantity = offer.get('quantity')
                    special_price = offer.get('special_price')
                    remainder = value % quantity
                    offered_quantity = value / quantity
                    if remainder == 0:
                        item_price = offered_quantity * special_price
                    else:
                        # check if special offer applies
                        if offered_quantity > 0:  # Apply special offer
                            numbered_quantity = value - remainder
                            item_price = numbered_quantity * special_price
                            remainder_price = remainder * individual_price
                            item_price += remainder_price
                        else:
                            item_price = remainder * individual_price
                    total_price += item_price
    return -1
