from backend.dal.wardrobe import get_all_items


def pickme():
    data = get_all_items()
    shirts = []
    pants = []
    what_goes = {"null": [],
                 "red": ["black"],
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

    results = []
    for shirt in shirts:
        for pant in pants:
            if shirt["color"] == "black":
                results.append((shirt, pant))
            else:
                for col in what_goes[shirt.get("color", "null")]:
                    if col == pant["color"]:
                        results.append((shirt, pant))

    return results
