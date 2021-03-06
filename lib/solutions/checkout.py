from collections import Counter
from itertools import (
    combinations,
    combinations_with_replacement,
    izip_longest,
)


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
    },
    {
        "item": "G",
        "price": 20,
        "offers": []
    },
    {
        "item": "H",
        "price": 10,
        "offers": [  # used for special offer
            {
                "quantity": 5,
                "special_price": 45
            },
            {
                "quantity": 10,
                "special_price": 80
            }
        ]
    },
    {
        "item": "I",
        "price": 35,
        "offers": []
    },
    {
        "item": "J",
        "price": 60,
        "offers": []
    },
    {
        "item": "K",
        "price": 70,
        "offers": [  # used for special offer
            {
                "quantity": 2,
                "special_price": 120
            }
        ]
    },
    {
        "item": "L",
        "price": 90,
        "offers": []
    },
    {
        "item": "M",
        "price": 15,
        "offers": []
    },
    {
        "item": "N",
        "price": 40,
        "offers": [
            {
                "free": "M",
                "quantity": 3
            }
        ]
    },
    {
        "item": "O",
        "price": 10,
        "offers": []
    },
    {
        "item": "P",
        "price": 50,
        "offers": [  # used for special offer
            {
                "quantity": 5,
                "special_price": 200
            }
        ]
    },
    {
        "item": "Q",
        "price": 30,
        "offers": [  # used for special offer
            {
                "quantity": 3,
                "special_price": 80
            }
        ]
    },
    {
        "item": "R",
        "price": 50,
        "offers": [  # used for special offer
            {
                "quantity": 3,
                "free": "Q"
            }
        ]
    },
    {
        "item": "S",
        "price": 20,
        "offers": []
    },
    {
        "item": "T",
        "price": 20,
        "offers": []
    },
    {
        "item": "U",
        "price": 40,
        "offers": [
            {
                "free": "U",
                "quantity": 3
            }
        ]
    },
    {
        "item": "V",
        "price": 50,
        "offers": [  # used for special offer
            {
                "quantity": 2,
                "special_price": 90
            },
            {
                "quantity": 3,
                "special_price": 130
            }
        ]
    },
    {
        "item": "W",
        "price": 20,
        "offers": []
    },
    {
        "item": "X",
        "price": 17,
        "offers": []
    },
    {
        "item": "Y",
        "price": 20,
        "offers": []
    },
    {
        "item": "Z",
        "price": 21,
        "offers": []
    },
]
ITEMS = [item['item'] for item in PRICES]

GROUP_PROMO = {
    "group": ["S", "T", "X", "Y", "Z"],
    "special_price": 45,
    "quantity": 3
}
PROMO_COMBINATIONS = [
    comb for comb in combinations_with_replacement(
        GROUP_PROMO['group'], GROUP_PROMO['quantity']
    )
]


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


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)


def get_combinations(item_list):
    """
    Returns tuple of promo keys and list of combinations based
    on the promo keys
    """
    promo = [char for char in item_list if char in GROUP_PROMO['group']]
    objs = [get_item(PRICES, sku) for sku in promo]
    sorted_objs = sorted(
        objs,
        key=lambda k: k['price'],
        reverse=True
    )
    sorted_promo = [char['item'] for char in sorted_objs]
    combination = list(grouper(3, sorted_promo))
    combination = [comb for comb in combination if None not in comb]

    return sorted_promo, combination


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    if not skus:
        return 0

    sku_list = list(skus)
    if len(sku_list) > 0:
        total_price = 0
        promo, combination = get_combinations(sku_list)
        promo_len = len(promo)
        if promo_len > 0:

            num_group = promo_len / GROUP_PROMO['quantity']
            total_price += (GROUP_PROMO['special_price'] * num_group)

            # format sku_list to remove the promo items
            index = num_group * GROUP_PROMO['quantity']
            promo = promo[:index]
            for sku in promo:
                sku_list.remove(sku)

        denomination = Counter(sku_list)
        keys = set(denomination.keys())
        item_keys = set(ITEMS)

        # process only if given `skus` match
        # the existing ITEMS list
        if keys.issubset(item_keys):
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

                                    # F case
                                    if free == obj['item']:
                                        factor = remainder / (quantity + 1)
                                        item_price -= (
                                            factor * individual_price
                                        )
                                        has_free = True

                                    # E case
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
