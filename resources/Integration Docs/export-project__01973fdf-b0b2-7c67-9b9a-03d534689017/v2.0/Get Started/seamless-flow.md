---
title: "Steps for Seamless Integration"
slug: "seamless-flow"
excerpt: "Integrate directly with Seamless APIs to process payment, payment page is rendered by Merchant."
hidden: true
createdAt: "Tue Sep 21 2021 12:24:55 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jun 25 2024 10:58:30 GMT+0000 (Coordinated Universal Time)"
---
If a merchant is [PCI DSS](https://www.pcisecuritystandards.org/pci_security/maintaining_payment_security) compliant then they can integrate in the seamless mode. In this mode a merchant can themselves accept card instrument details on their website, which gives a good user experience for the end customer given they are not redirected to another URL to make the payment. There are three main steps to process a payment in a seamless flow.

- Create Order
- Process Payment
- Check Status

## Create Order

\[[API Reference](https://developer.pluralonline.com/reference/create-order)]  
Order represents the shopping cart in a payment journey. Order plays a central part in the payment flow as the subsequent transactions such as payment, refund, get status are linked to it. For this, an order must be identified uniquely and to do so you can create and assign a random and unique order_id to an order. This order_id can be used for any subsequently linked transactions to the order.

An order comprises of the following details:

- Order Identifier - Order Id
- Payment details - Amount, Currency and Preferred PG
- Customer details - Customer Id, Customer Email, Customer Mobile.
- Product details - Product Id
- Address - Billing Address and Shipping Address
- Other details

Refer sample request body for Create Order

```json
{
   "merchant_data":{
      "merchant_id":"11607",
      "merchant_access_code":"25ca9633-3ac2-484a-a632-a067ac6c0eed",
      "merchant_return_url":"http://10.200.146.139:9020/chargingrespnew.aspx",
      "merchant_order_id":"API-DEMO-DOC-2"
   },
   "payment_info_data":{
      "amount":200,
      "currency_code":"INR",
      "order_desc":"Test Order"
   },
   "customer_data":{
      "country_code":"91",
      "mobile_number":"9121004028",
      "email_id":"john.doe@gmail.com"
   },
   "billing_address_data":{
      "first_name":"John",
      "last_name":"Doe",
      "address1":"House No. 123",
      "address2":"Road XYZ",
      "address3":"Bengaluru",
      "pin_code":"111111",
      "city":"Bengaluru",
      "state":"Karnataka",
      "country":"India"
   },
   "shipping_address_data":{
      "first_name":"John",
      "last_name":"Doe",
      "address1":"House No. 123",
      "address2":"Road XYZ",
      "address3":"Bengaluru",
      "pin_code":"111111",
      "city":"Bengaluru",
      "state":"Karnataka",
      "country":"India"
   },
   "product_info_data":{
      "product_details":[
         {
            "product_code":"40",
            "product_amount":200
         }
      ]
   },
   "additional_info_data":{
      "rfu1":"123"
   }
}
```

Once you have created the request body, it has to be encoded in base64 format. Also a `x-verify` header is needed which would be a SHA256 hash of the encoded request using your [Secret Key](https://developer.pluralonline.com/docs/setup). [Refer here to see hash generation logic.](https://developer.pluralonline.com/docs/hash-generation-logic) 

#### Curl for Create order with encoded request body and x-verify header.

```curl
curl --request POST \
     --url https://api-staging.pluralonline.com/api/v1/order/create \
     --header 'Accept: application/json' \
     --header 'Content-Type: application/json' \
     --header 'cache-control: no-cache' \
     --header 'x-verify: 09F7992D0B503D95551CD5D0571F50BAC77F161B72679967765623DC645972CC' \
     --data '
{
     "request": "ewogICAibWVyY2hhbnRfZGF0YSI6ewogICAgICAibWVyY2hhbnRfaWQiOiIxMTYwNyIsCiAgICAgICJtZXJjaGFudF9hY2Nlc3NfY29kZSI6IjI1Y2E5NjMzLTNhYzItNDg0YS1hNjMyLWEwNjdhYzZjMGVlZCIsCiAgICAgICJtZXJjaGFudF9yZXR1cm5fdXJsIjoiaHR0cDovLzEwLjIwMC4xNDYuMTM5OjkwMjAvY2hhcmdpbmdyZXNwbmV3LmFzcHgiLAogICAgICAibWVyY2hhbnRfb3JkZXJfaWQiOiJBUEktREVNTy1ET0MtMSIKICAgfSwKICAgInBheW1lbnRfaW5mb19kYXRhIjp7CiAgICAgICJhbW91bnQiOjIwMCwKICAgICAgImN1cnJlbmN5X2NvZGUiOiJJTlIiLAogICAgICAib3JkZXJfZGVzYyI6IlRlc3QgT3JkZXIiCiAgIH0sCiAgICJjdXN0b21lcl9kYXRhIjp7CiAgICAgICJjb3VudHJ5X2NvZGUiOiI5MSIsCiAgICAgICJtb2JpbGVfbnVtYmVyIjoiOTEyMTAwNDAyOCIsCiAgICAgICJlbWFpbF9pZCI6ImpvaG4uZG9lQGdtYWlsLmNvbSIKICAgfSwKICAgImJpbGxpbmdfYWRkcmVzc19kYXRhIjp7CiAgICAgICJmaXJzdF9uYW1lIjoiSm9obiIsCiAgICAgICJsYXN0X25hbWUiOiJEb2UiLAogICAgICAiYWRkcmVzczEiOiJIb3VzZSBOby4gMTIzIiwKICAgICAgImFkZHJlc3MyIjoiUm9hZCBYWVoiLAogICAgICAiYWRkcmVzczMiOiJCZW5nYWx1cnUiLAogICAgICAicGluX2NvZGUiOiIxMTExMTEiLAogICAgICAiY2l0eSI6IkJlbmdhbHVydSIsCiAgICAgICJzdGF0ZSI6Ikthcm5hdGFrYSIsCiAgICAgICJjb3VudHJ5IjoiSW5kaWEiCiAgIH0sCiAgICJzaGlwcGluZ19hZGRyZXNzX2RhdGEiOnsKICAgICAgImZpcnN0X25hbWUiOiJKb2huIiwKICAgICAgImxhc3RfbmFtZSI6IkRvZSIsCiAgICAgICJhZGRyZXNzMSI6IkhvdXNlIE5vLiAxMjMiLAogICAgICAiYWRkcmVzczIiOiJSb2FkIFhZWiIsCiAgICAgICJhZGRyZXNzMyI6IkJlbmdhbHVydSIsCiAgICAgICJwaW5fY29kZSI6IjExMTExMSIsCiAgICAgICJjaXR5IjoiQmVuZ2FsdXJ1IiwKICAgICAgInN0YXRlIjoiS2FybmF0YWthIiwKICAgICAgImNvdW50cnkiOiJJbmRpYSIKICAgfSwKICAgInByb2R1Y3RfaW5mb19kYXRhIjp7CiAgICAgICJwcm9kdWN0X2RldGFpbHMiOlsKICAgICAgICAgewogICAgICAgICAgICAicHJvZHVjdF9jb2RlIjoiNDAiLAogICAgICAgICAgICAicHJvZHVjdF9hbW91bnQiOjIwMAogICAgICAgICB9CiAgICAgIF0KICAgfSwKICAgImFkZGl0aW9uYWxfaW5mb19kYXRhIjp7CiAgICAgICJyZnUxIjoiMTIzIgogICB9Cn0="
}
'
```

#### Sample successful response for Create Order API call

```json
{
  "token": "8MLlV%2Fpl1MG1Enbv2W6snVvIXuyCX0Ym6i5Ie1AA1fs%3D",
  "plural_order_id": "106853"
}
```

## Process Payment

\[[API Reference](https://developer.pluralonline.com/reference/process-payment-card)]  
Once the order is created successfully, an order reference id (`plural_order_id`) is returned which the merchant needs to save in his database for future reference of the created order along with an order token. Also an order `token` is returned which needs to be sent in the next Payment Processing API call along with Payment details.

#### Curl for Process Payment API

```curl
curl --request POST \
     --url 'https://api-staging.pluralonline.com/api/v1/card/process/payment?token=hYXk0LUy2%2B6bilShXGpKH31WhMAZ24xazC8PsXKN1jE%3D' \
     --header 'Accept: application/json' \
     --header 'Content-Type: application/json' \
     --header 'checkoutmode: SEAMLESS' \
     --data '
{
     "card_data": {
          "card_number": "4012001037141112",
          "cvv": "123",
          "card_holder_name": "John Doe",
          "card_expiry_year": "2023",
          "card_expiry_month": "03"
     },
     "customer_data": {
          "country_code": "91",
          "mobile_no": "9050157978",
          "email_id": "john.doe@gmail.com"
     }
}
'
```

> 📘 Customer Data
> 
> Customer data needs to be present either in Process Payment API call or Create Order Call

#### Response from Process Payment API

```json
{
  "content": "&lt;html>&lt;head>&lt;Meta HTTP-EQUIV=&quot;Cache-Control&quot; CONTENT=&quot;no-cache&quot; >&lt;Meta HTTP-EQUIV=&quot;Pragma&quot; CONTENT=&quot;no-cache&quot;>&lt;Meta HTTP-EQUIV=&quot;Expires&quot; CONTENT=&quot;0&quot;>&lt;title>Card Info&lt;/title>&lt;SCRIPT LANGUAGE = JavaScript>\n&lt;!--\nisNN = document.layers ? 1 : 0; \nfunction noContext(){return false;}\nfunction noClick(e){\nif(isNN){\nif(e.which > 1) {return false;}\n} else { \nif(event.button > 1){return false;}\n}\n}\nif(isNN){ \ndocument.captureEvents(Event.MOUSEDOWN);\n}\n\t\tdocument.oncontextmenu = noContext;\n\t\tdocument.onmousedown   = noClick;\n\t\tdocument.onmouseup     = noClick;\n //-->\n &lt;/SCRIPT>\n&lt;script language=&quot;javascript&quot;>window.history.forward(); function noBack() { window.history.forward(); } &lt;/script>&lt;style type=&quot;text/css&quot;> body { font-family: Arial, Helvetica, sans-serif; font-weight:normal; color:#474747; font-size: 14px; margin:15% auto 0 auto; } #intermediatepage { background-image:url(&#39;/images/ccavenue_logo.gif&#39;); background-position:center top; background-repeat:no-repeat; padding:10px 20px 0 20px;} #intermediatepage div.process { background-image:url(&#39;/images/loader.gif&#39;); background-position:center 35px; background-repeat:no-repeat;}&lt;/style> &lt;/head>&lt;body oncontextmenu=&quot;return false;&quot; onLoad=&quot;noBack();document.MalltoEpay.submit();&quot;>&lt;label id=&quot;requestId&quot; style=&quot;display:none;&quot;>110296807983&lt;/label>\n&lt;form name=&quot;MalltoEpay&quot; method=&quot;POST&quot; action=&quot;https://sbipg.sbi/PG/VPAS.htm&quot; >\n&lt;input type=&quot;hidden&quot; name=&quot;actionVPAS&quot; value=&quot;VbvVEReqProcessHTTP&quot;>\n&lt;input type=&quot;hidden&quot; name=&quot;trandata&quot; value=&quot;AC7B87F02E55C592B4DEBD10404A8B5AF495DA2B02E8655EB652C16DE13491A3148B23BB9E47C45F197445087A363866F25A7A809C60C354A81273D8E0E4B2D036AA600767D16AC94B7760E770C3BEF51B6420E4F4DA73F828FB6B616FB1F008B771262B2E349324C2C7C2BFFEC0459F0377FEA98985A95FC8DB2C4B97ACE84AD76DA38B5FC8638233581E5FC977CBD2BD0A485A0BDC5392C29C687C036124DB1F0520E8F2A84E35AE26A4197364008BF14B5A69B51E3C227FEB4713178527BB82B836265437CFDABF32F9D2D726018613EFD950F6EED3FBEC6FC388C08018A79161C66490F8E1B2E3ABB7039589810FC04512605EB9A0F8DD67DC8198FCC400F1EC32C908118652BE80DC38628FF5930CB847B3B0D541ECBF24F8C70B7D02E1ABDE11D194DDCD545C2DEE711DB1DD59B6CE5000D4363E89DCE14861A190351DEE91FE6C31D724E22B6FA0B03046EBF6B310628D27CDAA37BEE9BB731E71FF115BCBA14901255BD971800DCB0C4969D0B7B3980A00B9D1227BFD35CBB4A739A986FA4FC8772B6532B067DFA22A9A84BC6E5E4EBB7946158FC70A02EB599F6E0910DD58CE7AF965558AB2EAE8D1AC01CB631E94F4994092E1038A4C299064A25E2DB136D06E39BE5E3D58B5A4C10618A94CFE86DE95CED42FEC9751C1F5A0EA0DF99A117FFDC585FC1E1278883CEC206BC194F563DE8D1663B07C1A9C60B7D02912A3C11DFAD0707810B76C4D201692344739014F34DDE7BA0E4F9F30F576F7CF0410C9CF18BA0EE1EF3B27D222130D29D85198C6798CED12D116C0CBBEA0E0CE7934077A3662D45F8C477CFD32EB3B84DD67ECC29976B21BC1219C4AA6A91624F07DF50541E28457F4DDD531A25B12697A28933BA248EC77EE21C77E1699898E82DC8FF2A7D5CCFD5AEDD426D72FBC67840F50300230F8BB94EA704DC3626CB06D179A8E0746F9B816295F796E35C203ABB1F1E621183FF0AC8F35BF328FC3229065D098C98CC5B2A7B76D67FA9DBF100C52BC40B73B28AF74AA0148C32589B24CA7AFD7ECB559E7263980CE278EA16B2540AE4F5435FBF80D483E14BDD880048D248B568BA845009F93733F4FFEEEB88E7831D822B968AD0CA44C2EDF0754C7920EF555433AB73263F96A9A96FCB8511B763057B816C0AF96EFEA9E260A593818050EE71E41DF9F7D886284AA3B9D0DAF6E1B4D765B994F6EFFF93E83FFD0FE86C09E767B121C136BD54CF432AB3C5D36F0BF5AF8B3EBA4F3166C08E077C2609610C5FA503F52CF387C90493501D1ED4FEB239F74CFAFA7C5AC0DC6FD22949745ACCF7030A9C6EB395736C0EE2F8DB4D50E6C06C26E29086370DC826DEDF30F69D427E8F13BF77E2CE899C8751D5CC383FC3B189CAFF37EBD01DD86BFA95B9D51C23B8610CE49EE5F08F5C2C0D86EEA3CEB59C41BDBD81412DE713FF7F840CFE03BDE14FE57C16947A3E7865B17DED5E8A908A8D562DF3385438784355C96A0D1A62C4040676F5166B68228C6ACC44A2AD094DC6B7301171BB46AB5DC68E3114A09E117D5775966B2A6EF94FDCA082C983F9CCB1665F2C8B0311723893EDCE2DFA1802A2EA5F2CA44C73F1E29F475DDDC0FEC8BA23D35923CDB12A441788890&quot;>\n&lt;input type=&quot;hidden&quot; name=&quot;errorURL&quot; value=&quot;https://secure.ccavenue.com/receive/198/M_81800542/servlet/BankRespReceive&quot;>\n&lt;input type=&quot;hidden&quot; name=&quot;responseURL&quot; value=&quot;https://secure.ccavenue.com/receive/198/M_81800542/servlet/BankRespReceive&quot;>\n&lt;input type=&quot;hidden&quot; name=&quot;tranportalId&quot; value=&quot;81800543&quot;>\n&lt;/form>\n&lt;div id=&quot;intermediatepage&quot; align=&quot;center&quot;>&lt;div class=&quot;process&quot;>&lt;br />&lt;br />&lt;br />&lt;br />&lt;br />&lt;br />&lt;span class=&quot;content-text&quot; style=&quot;font-size:24px; font-weight:bold;&quot;>Please be patient while your transaction is being processed.&lt;/span>&lt;br style=&quot;line-height:35px;&quot; />&lt;span>Do not &quot;close the window&quot; or press &quot;refresh&quot; or &quot;browser back/forward button&quot;.&lt;/span>&lt;br />&lt;br />&lt;/div>&lt;/div>&lt;/body>&lt;/html>\n",
  "payment_id": 437532,
  "order_id": 106369,
  "amount_in_paise": 200,
  "response_code": 1,
  "response_message": "Payment Successful!"
}
```

## Check Status

\[[API Reference](https://developer.pluralonline.com/reference/inquiry-payment)]  
To get the latest status of the order or transaction, merchant can call Inquiry APIs. There are 3 types of Inquiry calls which a merchant can call, which are as follows:

- Fetch status of a specific payment

#### Curl for Status Inquiry API

```curl
curl --location 'https://api-staging.pluralonline.com/api/v1/inquiry/order/156096/payment/8069673' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic MTIyNzY6ZTAwZGYzYjItNWY1Ni00ZTZkLTgwY2UtZWI1NGVkNDBhNzJh'
```

#### Response from Status Inquiry

```json
{
  "merchant_data": {
    "merchant_id": 11435,
    "order_id": "2626L31LB41P9BS"
  },
  "order_data": {
    "order_status": "CHARGED",
    "plural_order_id": 105771,
    "amount": 1000,
    "order_desc": "One shirt",
    "refund_amount": "0"
  },
  "payment_info_data": {
    "acquirer_name": "RazorPay",
    "auth_code": "NA",
    "captured_amount_in_paisa": "1000",
    "card_holder_name": "NA",
    "masked_card_number": "NA",
    "merchant_return_url": "http://192.168.101.205:9073/chargingrespnew.aspx,https://www.google.com,",
    "mobile_no": "NA",
    "payment_completion_date_time": "2021-09-15T10:43:55.673Z",
    "payment_id": "431723",
    "payment_status": "CAPTURED",
    "payment_response_code": 1,
    "payment_response_message": "NA",
    "product_code": "NA",
    "rrn": "NA",
    "refund_amount_in_paisa": "0",
    "salted_card_hash": "NA",
    "udf_field_1": "NA",
    "udf_field_2": "NA",
    "udf_field_3": "NA",
    "udf_field_4": "NA",
    "payment_mode": "NETBANKING",
    "issuer_name": "NONE",
    "gateway_payment_id": "pay_HxcaJfiAUV5bOL"
  }
}
```

Next step is to encode the above JSON into base64 format. [Then generate SHA256 hash according to this logic ](https://developer.pluralonline.com/docs/hash-generation-logic) and then verify this hash with `x-verify` received in the response of Status Inquiry call

> 🚧 Important
> 
> Verifying the SHA with `x-verify` is an important step and should not be skipped to prevent any security issues.
