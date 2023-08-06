##  Thư viện gọi api bên DNC.


### Cài đặt:
```bash
 $ pip3 install mobio-dnc-sdk.test
 ```


### Sử dụng:

##### 1. Khởi tạo sdk:
   ```python
    from mobio.sdks.dnc import MobioDNCSDK

    MobioDNCSDK().config(
        admin_host="",	# admin host
        redis_uri="",	# redis uri
        module_use="",	# liên hệ admin để khai báo tên của module
        module_encrypt="",	# liên hệ admin để lấy mã
    )
    
   ```

##### 2. Kiểm tra 1 contact có trong spam :
   ```python
    from mobio.sdks.dnc import MobioDNCSDK
    query_search = {"contact": "5361451387259452"}
    result = MobioDNCSDK().request_check_one_contact_spam(
        merchant_id,
        params=query_search,
    )
    """
    {
      "code": 200,
      "data": {
          "contact": "5361451387259452",
          "contact_type": "social",
          "staff_id": "c0713108-7449-4bd6-86d5-1198b73495c7",
          "social_page_id": "d59d4779-b707-4558-a594-4eb65f106ccc",
          "social_type": 1,
          "page_name": "Mobio shop",
        },
      
    }
    """
   ```

##### 3. Kiểm tra nhiều contact có trong spam :
   ```python
    from mobio.sdks.dnc import MobioDNCSDK
    query_search = {"contact": "5361451387259452,0371234567"}
    result = MobioDNCSDK().request_check_many_contact_spam(
        merchant_id,
        params=query_search,
    )
    """
    {
      "code": 200,
      "data": [
        {
          "contact": "5361451387259452",
          "contact_type": "social",
          "staff_id": "c0713108-7449-4bd6-86d5-1198b73495c7",
          "social_page_id": "d59d4779-b707-4558-a594-4eb65f106ccc",
          "social_type": 1,
          "page_name": "Mobio shop",
        },
        {
          "contact": "84371234567",
          "contact_type": "phone",
          "staff_id": "c0713108-7449-4bd6-86d5-1198b73495c7",
        },
      ]
      
    }
    """
   ```


#### Log - 1.0.0 
    - tạo sdk 

#### Log - 1.0.1 
    - sửa cơ chế call api sang call trực tiếp db mongo 