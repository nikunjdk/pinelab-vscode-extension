---
title: "Create Customer"
slug: "create-customer"
excerpt: ""
hidden: true
metadata: 
  image: []
  robots: "index"
createdAt: "Tue Feb 08 2022 07:08:47 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Mon Jul 11 2022 11:42:54 GMT+0000 (Coordinated Universal Time)"
---
**Response Body** 

[block:parameters]
{
  "data": {
    "h-0": "",
    "h-1": "",
    "h-2": "",
    "h-3": "",
    "h-4": "",
    "h-5": "",
    "0-0": "pineTokenidentifier",
    "0-1": "",
    "0-2": "string",
    "0-3": "Max Length 36",
    "0-4": "Unique non-guessable Guid sent during token provisioning API call",
    "0-5": "M",
    "1-0": "last4Digits",
    "1-1": "",
    "1-2": "string",
    "1-3": "Max Length 4",
    "1-4": "The customer’s last 4 digits of payment card number, also known as the Primary Account Number (PAN)",
    "1-5": "M",
    "2-0": "networkType",
    "2-1": "",
    "2-2": "string",
    "2-3": "Max Length 20",
    "2-4": "Visa/MasterCard/RuPay",
    "2-5": "M",
    "3-0": "cardExpiry",
    "3-1": "",
    "3-2": "string",
    "3-3": "Max Length 7",
    "3-4": "Payment card expiry.  \nFormat: MM/YYYY",
    "3-5": "M",
    "4-0": "panBIN",
    "4-1": "",
    "4-2": "string",
    "4-3": "Max Length 6",
    "4-4": "Card's bin 6 digits",
    "4-5": "M",
    "5-0": "issuer_name",
    "5-1": "",
    "5-2": "string",
    "5-3": "",
    "5-4": "Card's issuer name",
    "5-5": "M",
    "6-0": "is_debit_card",
    "6-1": "",
    "6-2": "string",
    "6-3": "Is debit card. Possible values is one of true/false",
    "6-4": "Card is debit or credit",
    "6-5": "M",
    "7-0": "issuerId",
    "7-1": "",
    "7-2": "integer",
    "7-3": "",
    "7-4": "For internal use only",
    "7-5": "",
    "8-0": "cardMetaData",
    "8-1": "",
    "8-2": "Complex Type",
    "8-3": "",
    "8-4": "A cardMetaData object structure",
    "8-5": "M",
    "9-0": "",
    "9-1": "backgroundColor",
    "9-2": "string",
    "9-3": "Max length 20",
    "9-4": "Card meta–Data BackgroundColor",
    "9-5": "O",
    "10-0": "",
    "10-1": "foregroundColor",
    "10-2": "string",
    "10-3": "Max length 20",
    "10-4": "Card meta–Data ForegroundColor",
    "10-5": "O",
    "11-0": "",
    "11-1": "labelColor",
    "11-2": "string",
    "11-3": "Max length 20",
    "11-4": "Card meta–Data Label Color",
    "11-5": "O",
    "12-0": "",
    "12-1": "ImageHeight",
    "12-2": "string",
    "12-3": "Max length 20",
    "12-4": "Card Image content height",
    "12-5": "O",
    "13-0": "",
    "13-1": "ImageWidth",
    "13-2": "string",
    "13-3": "Max length 20",
    "13-4": "Card Image content width",
    "13-5": "O",
    "14-0": "",
    "14-1": "contentMimeType",
    "14-2": "string",
    "14-3": "Max length 20",
    "14-4": "Mime Content-Type of the asset  \nEx image/png, image/jpeg",
    "14-5": "O"
  },
  "cols": 6,
  "rows": 15,
  "align": [
    "left",
    "left",
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]
