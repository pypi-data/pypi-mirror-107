from .mongo_connection import BaseCollectionMongoDB
from pymongo import ReadPreference


class ContactSpamModel(BaseCollectionMongoDB):
    """
    Bảng lưu thông tin contact_spam
    """

    _ID = "_id"
    merchant_id = "merchant_id"
    contact = "contact"
    contact_type = "contact_type"
    page_name = "page_name"
    social_page_id = "social_page_id"
    social_type = "social_type"
    profile_id = "profile_id"
    staff_id = "staff_id"
    source = "source"
    create_on = "create_on"
    stringee_id = "stringee_id"

    contact_type_phone = "phone"
    contact_type_email = "email"
    contact_type_social = "social"
    list_contact_type = [contact_type_phone, contact_type_email, contact_type_social]

    social_type_facebook = 1
    social_type_zalo = 2
    social_type_instagram = 3
    social_type_youtube = 4
    social_type_line = 5
    social_type_chattool = 6
    list_social_type = [
        social_type_facebook,
        social_type_zalo,
        social_type_instagram,
        social_type_youtube,
        social_type_line,
        social_type_chattool,
    ]
    # merchant_id, contact,contact_type,page_name,social_page_id,social_type,profile_id,staff_id,create_on
    list_field = [
        merchant_id,
        contact,
        contact_type,
        page_name,
        social_page_id,
        social_type,
        profile_id,
        staff_id,
        create_on,
    ]

    def __init__(self):
        super().__init__()
        self.table_name = "contact_spam"
        self.coll_primary = self.db.get_collection(self.table_name)
        self.coll_secondary = self.db.get_collection(
            self.table_name, read_preference=ReadPreference.SECONDARY_PREFERRED
        )

    def find_one_contact_spam(self, merchant_id, contact):
        try:
            result = self.coll_secondary.find_one(
                {self.merchant_id: merchant_id, self.contact: contact},
                {self._ID: 0, self.create_on: 0},
            )
            return result
        except Exception as er:
            err_msg = "dnc_sdk find_one_contact_spam ERR: {}".format(er)
            print(err_msg)
            return None

    def find_many_contact_spam(self, merchant_id, list_contact):
        try:
            obj_query = {
                self.merchant_id: merchant_id,
                self.contact: {"$in": list_contact},
            }
            result = self.coll_secondary.find(
                obj_query,
                {self._ID: 0, self.create_on: 0},
            )
            return list(result)
        except Exception as er:
            err_msg = "dnc_sdk find_many_contact_spam ERR: {}".format(er)
            print(err_msg)
            return []
