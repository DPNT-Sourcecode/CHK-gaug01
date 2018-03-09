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
    },
    {
        "item": "F",
        "price": 10,
        "offers": [
            {
                "free": "F",
                "quantity": 2
            }
        ]
    }
]
ITEMS = [item['item'] for item in PRICES]


def get_item(obj_list, lookup):
    """
    Returns a dictionary object based on the given
    `lookup` parameter
    """
    return next(
        (
            item for item in obj_list
            if item['item'] == lookup
        ),
        None
    )


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
            skipped_keys = []
            key_items = sorted(
                denomination.most_common(),
                key=lambda k: k[0],
                reverse=True
            )
            for key, value in key_items:
                occurence = value
                skipped_obj = get_item(skipped_keys, key)
                if skipped_obj:
                    occurence -= skipped_obj['quantity']
                    if occurence == 0:  # skip key if already free
                        continue

                has_free = False
                obj = get_item(PRICES, key)
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

                        remainder = occurence
                        for offer in offers:

                            quantity = offer.get('quantity')
                            if remainder >= quantity:
                                extra = remainder % quantity
                                offered_quantity = remainder / quantity
                                free = offer.get('free', False)
                                if free:
                                    item_price += (
                                        remainder * individual_price
                                    )
                                    print(item_price)
                                    if free == obj['item']:
                                        item_price -= (offered_quantity * individual_price)
                                        # extra = remainder % (quantity + 1)
                                        # print(extra)
                                        # print(offered_quantity)
                                        # if extra == 0:
                                        #     print("zero")
                                        #     item_price -= (
                                        #         individual_price * offered_quantity
                                        #     )
                                        # else:
                                        #     print("extra")
                                        #     item_price -= (
                                        #         individual_price * offered_quantity
                                        #     )
                                        has_free = True

                                    elif free in keys:
                                        free_obj = get_item(PRICES, free)
                                        if free_obj:
                                            skipped_keys.append({
                                                'item': free_obj['item'],
                                                'quantity': offered_quantity
                                            })
                                        has_free = True

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

                        # occurence here is equivalent to remainder.
                        # if there's still a remainder, compute using
                        # the individual price
                        if not has_free and remainder > 0:
                            item_price += (remainder * individual_price)

                    else:  # No special offer
                        item_price = occurence * individual_price
                    total_price += item_price
            return total_price
    return -1
