[原始页面地址](https://docs.ekuaibao.com/docs/open-api/invoice/get-flow-invoice)
数据获取时间 2025-06-23 13:00:17

# 根据单据编号或ID查询发票ID和明细ID

# 根据单据编号或ID查询发票ID和明细ID  
  
POST**/api/openapi/v2/extension/flow/INVOICE/search**

**更新日志**

  * [**2.0.0**](/updateLog/update-log#200)
    * 🐞 修复了 `invoiceType`（发票类型）无法返回 **医疗发票** 和 **财政票据** 类型的BUG。




## Query Parameters​

名称| 类型| 描述| 是否必填| 默认值| 备注  
---|---|---|---|---|---  
**accessToken**|  String| 认证token| 必填| -| 通过 [获取授权](/docs/open-api/getting-started/auth) 获取 `accessToken`  
  
## Body Parameters​

名称| 类型| 描述| 是否必填| 默认值| 备注  
---|---|---|---|---|---  
**type**|  String| 查询参数类型| 必填| -| `code` : 单据编号 `id` : 单据ID  
**codeOrIds**|  Array| 查询参数| 必填| -| 传对应参数类型值，单据编号或者单据ID  
  
## CURL​
    
    
    curl --location --request POST 'https://app.ekuaibao.com/api/openapi/v2/extension/flow/INVOICE/search?accessToken=ZyEbyCA-_Auk00' \  
    --header 'Content-Type: application/json' \  
    --data-raw '{  
        "type":"id",  
        "codeOrIds":["j7sbyDMhYUpU00"]  //单据ID  
    }'  
    

## 成功响应​
    
    
    {  
        "value": {  
            "j7sbyDMhYUpU00": [                   //单据ID或者单据编号，与传参对应  
                {  
                    "invoiceId": "gwobfjObAAno00:3700171320:38415400",    //发票ID  
                    "invoiceItemId": [            //发票明细ID  
                        "zz4byDMhYUh400",   
                        "k1IbyDMhYUiQ00",  
                        "ehQbyDMhYUjI00",  
                        "5AobyDMhYUio00",  
                        "8EQbyDMhYUjg00",  
                        "YIwbyDMhYUhw00",  
                        "buUbyDMhYUhY00"  
                    ],  
                    "invoiceType": "invoice"        //发票类型  
                },  
                {  
                    "invoiceId": "5-sbyDJSOI0800",  //发票ID   
                    "invoiceItemId": [],            //发票明细ID  
                    "invoiceType": "taxi"           //发票类型  
                }  
            ]  
        }  
    }  
    

## 失败响应​

HTTP状态码| 错误码| 描述| 排查建议  
---|---|---|---  
**200**|  -| `{"value": {}}`| 返回空表示没有查询到数据  
请确认 `codeOrIds`（查询参数） 是否正确  
**400**|  -| 不支持此类型type=name| 请确认 `type`（查询参数类型） 是否为 **备注** 中的固定值
