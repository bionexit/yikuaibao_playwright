[原始页面地址](https://docs.ekuaibao.com/docs/open-api/datalink-extend/ldap)
数据获取时间 2025-06-23 13:00:17

# 同步LDAP用户数据

# 同步LDAP用户数据

POST**/api/openapi/v1/ldap/sync**

## Query Parameters​

名称| 类型| 描述| 是否必填| 默认值| 备注  
---|---|---|---|---|---  
**accessToken**|  String| 认证token| 必填| -| 通过 [获取授权](/docs/open-api/getting-started/auth) 获取 `accessToken`  
  
## Body Parameters​

名称| 类型| 描述| 是否必填| 默认值| 备注  
---|---|---|---|---|---  
**ldapUsers**|  Array| 员工集合| 必填| -| 员工集合  
**∟ mail**|  String| 邮箱| 必填| -| 邮箱  
**∟ name**|  String| 用户名| 必填| -| 用户名  
**∟ employeeNumber**|  String| 工号| 必填| -| 工号  
**∟ mobile**|  String| 手机号| 必填| -| 手机号  
**∟ login**|  String| 登录名| 必填| -| 登录名  
  
## CURL​
    
    
    curl --location --request POST 'https://app.ekuaibao.com/api/openapi/v1/ldap/sync?accessToken=_qkc1MVHQofY00' \  
    --header 'Content-Type: application/json' \  
    --data-raw '{  
        "ldapUsers": [  
            {  
                "mail": "test@mail",  
                "name": "user",  
                "employeeNumber": "123434",  
                "mobile": "13260304463",  
                "login": "name"  
            }  
        ]  
    }'  
    

## 成功响应​
    
    
    {  
        "value": {  
            "code": "200",  
            "errorCode": null,  
            "errorMessage": null  
        }  
    }  
    

## 失败响应​

HTTP状态码| 错误码| 描述| 排查建议  
---|---|---|---  
**200**|  401| 请求参数无效| 请确认 `ldapUsers`（员工集合）中的参数是否正确
