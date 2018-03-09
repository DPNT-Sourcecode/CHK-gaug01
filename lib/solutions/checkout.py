from collections import Counter

prices = [
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
    sku_list = list(skus)
    if len(sku_list) > 0:
        denomination = Counter(sku_list)
        for key, value in denomination.items():
            
    return -1
