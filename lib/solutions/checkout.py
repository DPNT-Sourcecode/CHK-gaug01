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
    {
        "item": "E",
        "price": 40,
        "offers": [
            {
                "free": "B",
                "quantity": 2
            }
        ]
    }
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
                obj = next(
                    (
                        price for price in PRICES
                        if price['item'] == key
                    ),
                    None
                )
                if obj:
                    item_price = 0
                    individual_price = obj.get('price')
                    offers = obj.get('offers')

                    if offers:
                        offers = sorted(
                            offers,
                            key=lambda k: k.get('quantity'),
                            reverse=True
                        )

                        remainder = value
                        for offer in offers:

                            quantity = offer.get('quantity')
                            if remainder >= quantity:
                                extra = remainder % quantity
                                offered_quantity = remainder / quantity
                                has_free = offer.get('free', False)
                                if has_free in keys:
                                    free_obj = next(
                                        (
                                            item for item in PRICES
                                            if item['item'] == has_free
                                        ),
                                        None
                                    )
                                    if free_obj:
                                        item_price -= free_obj['price']

                                else:
                                    special_price = offer.get('special_price')
                                    if extra == 0:
                                        item_price += (
                                            offered_quantity * special_price
                                        )
                                    else:
                                        if offered_quantity > 0:
                                            item_price += (
                                                offered_quantity * special_price
                                            )
                                remainder = extra

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
