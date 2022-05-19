import json
import random

from backend.dal.wardrobe import get_all_items


def pickme():
    data = get_all_items()
    shirts = []
    pants = []
    what_goes = {"red": ["black"],
                 "blue": ["white", "black"],
                 "green": ["white", "black"],
                 "purple": ["white", "black"],
                 "yellow": ["white", "black"],
                 "white": ["purple", "yellow", "blue", "black", ],
                 "black": ["purple", "yellow", "blue", "white", ]}
    for item in data:
        if item["category"] == "shirt":
            shirts.append(item)
        if item["category"] == "pants":
            pants.append(item)
    picked_shirt = random.choice(shirts)
    filter1_pants = []
    for item in pants:
        if item["color"] == "black":
            filter1_pants.append(item)
        else:
            for col in what_goes[picked_shirt["color"]]:
                if col == item["color"]:
                    filter1_pants.insert(item)
    possibro_pants = []
    for item in filter1_pants:
        if item["is_business"] == picked_shirt["is_business"] and item["weather"] == picked_shirt["weather"] and \
                item["is_business"] == picked_shirt["is_business"]:
            possibro_pants.insert(item)
    return picked_shirt, random.choice(possibro_pants)
