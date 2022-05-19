from backend.dal import client


def get_all_items():
    result = client.find("wardrobe", {})
    return []
    return result


def add_item(item):
    return client.insert("wardrobe", item.to_dict())


def remove_item(id):
    return client.remove("wardrobe", id)
