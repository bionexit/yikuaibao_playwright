[原始页面地址](https://docs.ekuaibao.com/docs/open-api/tools/staffs-getOpenUserId)
数据获取时间 2025-06-23 13:00:17

# 获取企业微信OpenUserId

# 获取企业微信OpenUserId  
  
通过企业微信的员工明文userId获取加密后的OpenUserId。

POST**/api/openapi/v1/staffs/getOpenUserId**

**更新日志**

  * [**1.5.1**](/updateLog/update-log#151)
    * 🆕 新增了本接口。



caution

  * 仅 **2021年11月** 之后的，且经过开通【**通讯录接口** 】定制化改造的新企微版客户适用此接口。



## Query Parameters​

名称| 类型| 描述| 是否必填| 默认值| 备注  
---|---|---|---|---|---  
**accessToken**|  String| 认证token| 必填| -| 通过 [获取授权](/docs/open-api/getting-started/auth) 获取 `accessToken`  
  
## Body Parameters​

名称| 类型| 描述| 是否必填| 默认值| 备注  
---|---|---|---|---|---  
**ids**|  Array| 企微明文userId| 必填| -| 企微明文userId数组，**最大数量不能超过`100`**  
  
## CURL​
    
    
    curl --location --request POST 'https://wx2.ekuaibao.com/api/openapi/v1/staffs/getOpenUserId?accessToken=ID_3GjSy1OEUwM:dAY3noVGjy4s7w' \  
    --header 'Content-Type: application/json' \  
    --data-raw '{  
        "ids":["id1","id2"]  
    }'  
    

## 成功响应​
    
    
    {  
        "items":[  
            {  
                "userid":"userID",          //企微的明文userId  
                "open_userid":"open_userid" //合思获取到的open_userid  
            }  
        ]  
    }  
    
