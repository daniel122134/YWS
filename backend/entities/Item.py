class Item:
    def __init__(self, id, size, brand, picture, body_area, weather, is_sport, is_business, category,color):
        self.id = id
        self.size = size
        self.brand = brand
        self.picture = picture
        self.body_area = body_area
        self.weather = weather
        self.is_sport = is_sport
        self.is_business = is_business
        self.category = category
        self.color = color

    def to_dict(self):
        data = {}
        data["_id"] = self.id
        data["size"] = self.size
        data["brand"] = self.brand
        data["picture"] = self.picture
        data["body_area"] = self.body_area
        data["weather"] = self.weather
        data["is_sport"] = self.is_sport
        data["is_business"] = self.is_business
        data["category"] = self.category
        data["color"] = self.color

        return data

    @staticmethod
    def from_dict(data):
        return Item(data["_id"],
                    data["size"]
                    , data["brand"]
                    , data["picture"]
                    , data["body_area"]
                    , data["weather"]
                    , data["is_sport"]
                    , data["is_business"]
                    , data["category"]
                    , data["color"])


