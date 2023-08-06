from mobio.libs.Singleton import Singleton
from mobio.libs.caching import LruCache
from .config import StoreCacheType, Cache


# from mobio.libs.ciphers import MobioCrypt2


def sdk_pre_check(func):
    def decorated_function(*args, **kwargs):
        if not MobioDNCSDK().admin_host:
            raise ValueError("admin_host None")
        if not MobioDNCSDK().lru_cache:
            raise ValueError("redis_uri None")
        if not MobioDNCSDK().module_encrypt:
            raise ValueError("module_encrypt None")
        if not MobioDNCSDK().module_use:
            raise ValueError("module_use None")
        if MobioDNCSDK().admin_version not in MobioDNCSDK.LIST_VERSION_VALID:
            raise ValueError("admin_version invalid")
        if not MobioDNCSDK().module_valid:
            raise ValueError("module invalid")
        return func(*args, **kwargs)

    return decorated_function


@Singleton
class MobioDNCSDK(object):
    lru_cache = None
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 20
    LIST_VERSION_VALID = ["v1.0", "api/v2.0", "api/v2.1"]

    def __init__(self):
        self.admin_host = ""
        self.admin_version = MobioDNCSDK.LIST_VERSION_VALID[-1]
        self.module_encrypt = ""
        self.module_use = ""
        self.request_header = None
        self.module_valid = False
        self.redis_uri = None

    @property
    def p_module_valid(self):
        return self.module_valid

    def config(
        self,
        admin_host=None,
        redis_uri=None,
        module_use=None,
        module_encrypt=None,
    ):
        self.admin_host = admin_host
        self.module_encrypt = module_encrypt
        self.module_use = module_use

        if module_use:
            self.request_header = {"X-Module-Request": module_use}
        if module_use and module_encrypt:
            # if module_use == MobioCrypt2.d1(module_encrypt, enc="utf-8"):
            #     self.module_valid = True
            # else:
            #     self.module_valid = False
            self.module_valid = True
        if redis_uri:
            self.redis_uri = redis_uri
            MobioDNCSDK.lru_cache = LruCache(
                store_type=StoreCacheType.REDIS,
                cache_prefix=Cache.PREFIX_KEY,
                redis_uri=redis_uri,
            )

    @staticmethod
    @sdk_pre_check
    def request_check_one_contact_spam(
        merchant_id,
        params=None,
        token_value=None,
    ):
        from .utils import check_one_contact_in_spam

        return check_one_contact_in_spam(
            merchant_id,
            params=params,
            token_value=token_value,
        )

    @staticmethod
    @sdk_pre_check
    def request_check_many_contact_spam(
        merchant_id,
        params=None,
        token_value=None,
    ):
        from .utils import check_many_contact_in_spam

        return check_many_contact_in_spam(
            merchant_id,
            params=params,
            token_value=token_value,
        )
