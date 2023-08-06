import os
import re
from copy import deepcopy


class StoreCacheType:
    LOCAL = 1
    REDIS = 2


class Cache:
    PREFIX_KEY = "dnc_sdk_"


class ConfigKeyHost:
    PROFILING_HOST = "profiling_host"
    PROFILING_IS_ONPREMISE = "profiling_is_onpremise"
    PROFILING_ONPREMISE_HOST = "profiling_onpremise_host"

    ON_PREMISE_TOKEN = "p_t"

    SOCIAL_HOST = "social_host"
    SOCIAL_IS_ONPREMISE = "social_is_onpremise"
    SOCIAL_ONPREMISE_HOST = "social_onpremise_host"

    CALLCENTER_IS_ONPREMISE = "callcenter_is_onpremise"
    CALLCENTER_HOST = "callcenter_host"

    NM_HOST = "nm_host"
    VOUCHER_HOST = "voucher_host"

    DNC_HOST = "dnc_host"
    DNC_IS_ONPREMISE = "dnc_is_onpremise"
    DNC_ONPREMISE_HOST = "dnc_onpremise_host"


class UrlConfig:
    ADMIN_CONFIG = "{host}/adm/{version}/merchants/{merchant_id}/configs"
    PARTNER_INFO = "{host}/adm/{version}/partners/{partner_id}/info"
    PARTNER_INFO_CIPHER_ENCRYPT = (
        "{host}/adm/{version}/partners/{partner_id}/info/encrypt"
    )
    DNC_CHECK_ONE_CONTACT_IN_SPAM = "{host}/dnc/api/v1.0/contact/find"
    DNC_CHECK_MANY_CONTACT_IN_SPAM = "{host}/dnc/api/v1.0/contact/find_many"


class Mongo:
    DNC_MONGO_DB = os.environ.get(
        "DNC_MONGO_URI", "mongodb://dncuser:O!Z7PobLEUAq@api-test1.mobio.vn:27018/dnc"
    )
    dnc_mongo_db_name = re.search(
        r"^mongodb://[^@]+@[^/]+/([^?$]+).*$", DNC_MONGO_DB
    ).group(1)
    DNC_MONGO_DB_DB_NAME = deepcopy(str(dnc_mongo_db_name))
