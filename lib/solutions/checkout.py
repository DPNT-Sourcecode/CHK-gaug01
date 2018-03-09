from collections import Counter

PRICES = [
    {
        "item": "A",
        "price": 50,
        "offers": [  # used for special offer
            {
                "quantity": 3,
                "special_price": 130
            },
            {
                "quantity": 5,
                "special_price": 200
            }
        ]
    },
    {
        "item": "B",
        "price": 30,
        "offers": [  # used for special offer
            {
                "quantity": 2,
                "special_price": 45
            }
        ]
    },
    {
        "item": "C",
        "price": 20,
        "offers": []
    },
    {
        "item": "D",
        "price": 15,
        "offers": []
    },
]
ITEMS = [item['item'] for item in PRICES]


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    if not skus:
        return 0

    sku_list = list(skus)
    if len(sku_list) > 0:
        denomination = Counter(sku_list)
        keys = set(denomination.keys())
        item_keys = set(ITEMS)

        # process only if given `skus` match
        # the existing ITEMS list
        if keys.issubset(item_keys):
            total_price = 0
            for key, value in denomination.items():
                price_obj = [price for price in PRICES if price['item'] == key]
                if len(price_obj) > 0:
                    item_price = 0
                    obj = price_obj[0]
                    individual_price = obj.get('price')
                    offers = obj.get('offers')

                    if offers:
                        offers = sorted(
                            offers,
                            key=lambda k: k['quantity'],
                            reverse=True
                        )

                        remainder = value
                        for offer in offers:
                            quantity = offer.get('quantity')
                            if remainder >= quantity:
                                special_price = offer.get('special_price')
                                remainder = value % quantity
                                offered_quantity = value / quantity
                                if remainder == 0:
                                    item_price += (
                                        offered_quantity * special_price
                                    )
                                else:
                                    if offered_quantity > 0:
                                        item_price += (
                                            offered_quantity * special_price
                                        )
                        # value here is equivalent to remainder.
                        # if there's still a remainder, compute using
                        # the individual price
                        if remainder > 0:
                            item_price += (remainder * individual_price)

                    else:  # No special offer
                        item_price = value * individual_price
                    total_price += item_price
            return total_price
    return -1
