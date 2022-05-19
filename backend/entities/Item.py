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
        data = {"_id": self.id, "size": self.size, "brand": self.brand, "picture": self.picture,
                "body_area": self.body_area, "weather": self.weather, "is_sport": self.is_sport,
                "is_business": self.is_business, "category": self.category, "color": self.color}

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


