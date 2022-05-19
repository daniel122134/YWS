from backend.dal import client


def get_known_drinks():
    result = client.find("wardrobe", {})
    return result


def add_item(item_date):
    return client.insert("wardrobe", item_date)


def remove_item(id):
    return client.remove("wardrobe", id)
