from backend.dal import client


def get_all_items():
    result = client.find("explore", {})
    return result


def add_item(item):
    return client.insert("explore", item.to_dict())


def remove_item(id):
    return client.remove("explore", id)
