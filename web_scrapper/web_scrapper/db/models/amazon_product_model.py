from mongoengine import Document, StringField


class AmazonProductModel(Document):
    description = StringField(required=True, default="")
    image_src = StringField(required=True, default="")
    price = StringField(required=True, default="")
    rating = StringField(required=True, default="")
    date = StringField(required=True, default="")


class AmazonHashModel(Document):
    description = StringField(required=True, default="")
    image_src = StringField(required=True, default="")
    price = StringField(required=True, default="")
    rating = StringField(required=True, default="")
    date = StringField(required=True, default="")
