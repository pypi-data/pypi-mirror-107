from .config import UrlConfig, ConfigKeyHost
import requests
from .dnc_sdk import MobioDNCSDK
import re

# from flask import request
from .contact_spam_model import ContactSpamModel


@MobioDNCSDK.lru_cache.add()
def get_info_merchant_config(
    merchant_id,
    key=None,
    admin_version=None,
    request_timeout=MobioDNCSDK.DEFAULT_REQUEST_TIMEOUT_SECONDS,
):
    api_version = MobioDNCSDK().admin_version
    if admin_version and admin_version in MobioDNCSDK.LIST_VERSION_VALID:
        api_version = admin_version
    adm_url = str(UrlConfig.ADMIN_CONFIG).format(
        host=MobioDNCSDK().admin_host,
        version=api_version,
        merchant_id=merchant_id,
    )
    request_header = {}
    if MobioDNCSDK().request_header:
        request_header.update(MobioDNCSDK().request_header)
    response = requests.get(
        adm_url,
        headers=request_header,
        timeout=request_timeout,
    )
    response.raise_for_status()
    result = response.json()
    data = result.get("data", {})
    if key:
        return data.get(key)
    return data


def __is_get_from_onpremise__(merchant_id, is_onpremise_key, onpremise_host_key):
    is_onpremise = get_info_merchant_config(merchant_id, onpremise_host_key) or "0"
    dest_is_onpremise = get_info_merchant_config(merchant_id, is_onpremise_key) or "0"
    return is_onpremise == dest_is_onpremise


def get_dnc_host(merchant_id):
    if __is_get_from_onpremise__(
        merchant_id,
        ConfigKeyHost.DNC_IS_ONPREMISE,
        ConfigKeyHost.DNC_ONPREMISE_HOST,
    ):
        social_host = get_info_merchant_config(
            merchant_id, ConfigKeyHost.DNC_ONPREMISE_HOST
        )
        if not social_host:
            social_host = get_info_merchant_config(merchant_id, ConfigKeyHost.DNC_HOST)
        return social_host
    return get_info_merchant_config(merchant_id, ConfigKeyHost.DNC_HOST)


def check_one_contact_in_spam(
    merchant_id=None,
    params=None,
    token_value=None,
):
    if not merchant_id:
        return {"code": 400, "message": "merchant_id not found"}
    if not params or not params.get("contact"):
        return {"code": 400, "message": "contact not found in params"}
    contact = params.get("contact").strip()
    if validate_phone_number(contact):
        contact = phone_number_standardize(contact)
    contact_spam = ContactSpamModel().find_one_contact_spam(merchant_id, contact)
    if contact_spam:
        return {
            "code": 200,
            "data": contact_spam,
        }
    else:
        return {"code": 404, "message": "Not Found"}


def check_many_contact_in_spam(
    merchant_id=None,
    params=None,
    token_value=None,
):
    if not merchant_id:
        return {"code": 400, "message": "merchant_id not found"}
    if not params or not params.get("contact"):
        return {"code": 400, "message": "contact not found in params"}
    contact = params.get("contact").strip()
    list_contact = contact.split(",")
    for idx, item in enumerate(list_contact):
        contact_format = item.strip()
        if validate_phone_number(contact_format):
            contact_format = phone_number_standardize(contact_format)
        list_contact[idx] = contact_format
    result_data = []
    list_chunk = split_list(list_contact, 20)
    for chunk in list_chunk:
        list_contact_spam = ContactSpamModel().find_many_contact_spam(
            merchant_id, chunk
        )
        result_data.extend(list_contact_spam)
    return {
        "code": 200,
        "data": result_data,
    }


def split_list(input_list, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(input_list), n):
        yield input_list[i : i + n]


def validate_phone_number(phone):
    if bool(re.match("(^[+0-9]{1,3})*([0-9]{9,11}$)", phone)):
        return True
    else:
        return False


def phone_number_standardize(phone_number):
    if phone_number.startswith("0"):
        phone_number = "84" + phone_number[1:]
    if phone_number.startswith("+"):
        phone_number = phone_number[1:]
    return phone_number
