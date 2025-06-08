---
title: "Tokenisation"
slug: "tokenisation"
excerpt: "Welcome to Tokenisation. This is a comprehensive reference for integrating with Plural for Tokenisation."
hidden: true
createdAt: "Wed Jul 27 2022 17:19:27 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jun 25 2024 11:00:34 GMT+0000 (Coordinated Universal Time)"
---
# RBI Mandate

To ensure greater security to end customers and lower the risks of cyber-crimes, the Reserve Bank of India (RBI) passed a mandate prohibiting businesses, payment gateways, and payment aggregators from storing customer card details on their servers. 

The deadline, which was earlier set to 30 June 2022, has now been extended to 30 Sep 2022, giving businesses more time to make the required changes. 

The RBI has only permitted card networks to store card details while all stakeholders, including businesses, payment gateways, and payment aggregators, must adopt the tokenisation guidelines and have compliant solutions in place by the deadline. 

With tokenisation, a customer’s card details would be masked behind a token, facilitating transactions only through the token.

# Tokenisation

Tokenization is the process of replacing sensitive card data into a form of unique identification token that retain all the essential information about the card data without compromising its security. 

Tokenization, which seeks to minimize the amount of card data a business needs to keep on hand, has become a popular way for small and midsize businesses to support the security and compliance with industry standards and government regulations.

![](https://files.readme.io/8602656-Tokenisation.png "Tokenisation.png")

# Types of Tokenisation

## Device Based Tokens

Device-based tokens are bound with the card and the device, and the card networks generate the token. 

Example:  
A customer with an HDFC credit card gets it enrolled for a token on his mobile’s Amazon app. In this example, the customer can transact on the Amazon app using his mobile phone only. 

Device-based tokens are generally used in NFC based phones where the card details are mimicked onto the NFC chip. E.g. Samsung Pay, Apple Pay, etc and for offline use cases.

## Account Based Tokens / Card on File (COF) Tokens

Account-based tokens are like saved cards on a specific merchant. The customer needs to log in on the merchant’s app/web platform to continue with the transaction and be interoperable and used across devices.

> 📘 Important Information
> 
> Plural supports only Account Based Tokenisation / Card on File (COF) Tokenisation.

# Stakeholders in the tokenisation ecosystem

Stakeholders involved in e-commerce card-on-file tokenisation are,  
o	Token Requestors  
o	Acquirers  
o	Issuers  
o	Card Networks

# Benefits of Tokenization

Largely designed to counter online frauds and curb digital payment breaches, tokenisation comes with a slew of benefits. Some of them are:

## Enhanced safety and security

Tokens generated will be unique to a single card at a specific merchant and this will take up the overall security of making card-based transactions. It eliminates the risk of storing card details online and ensures the uncompromised convenience of storing your token details on the merchant site. 

## Lifecycle Management

Tokens can be deleted/updated by issuer in real time. Issuer visibility to where tokens are stored

## Quicker checkouts

Tokenised card will also allow you the convenience of quick checkouts as you won't need to punch in your card number for each purchase which helps to achieve better Approval Rates. Save your card once and you'll have the ease of transaction at all times.

## No more 'False Declines'

Many times, your legitimate online payments using your valid cards are declined on the grounds of the transaction looking like a fraud. With tokenisation, this becomes a thing of the past as the usage of tokens for payments confirms security of the highest order.

## Dynamic Cryptogram

With tokenisation, unique cryptogram verified for every transaction.

## Domain Restriction

Tokens are issued to merchant for a particular use case. Cannot be used outside domain

# Impact of Tokenisation

## Impact to Merchant

‘Tokenization’ might significantly disrupt the existing merchants’ platform since it needs to develop a system that supports tokenised transactions (PCI-DSS merchants only). However, their functionality will remain unchanged for small merchants (redirect model).

Merchant will need to partner with card networks or leverage payment aggregators to have a ‘save card details’ feature for existing and future customers.  

According to CII's Media and Entertainment Committee, this could lead to 20-50% of revenue losses for businesses that fail to comply by the deadline.  

## Impact to customers

Not just businesses, an estimated 5 million customers who have stored their card details on ecommerce and online stores could also face difficulties if the online platforms/businesses they frequently visit have not made the changes to their backend.  

Imagine that for each purchase customers make, they need to input the card number, name, expiry date, CVV. This hassle may cause customers to abandon cart & drop off if the business has not made the changes on the backend

# Tokenisation Flow

## Token Provisioning

1. Customer saves card details at merchant site or initiate the purchase transaction and provide the consent to save card
2. Merchant does penny drop transaction or purchase transaction to authentication and authorization the card.
3. Post successful authentication and authorization of the Penny drop transaction or purchase transaction, merchant request to tokenise the card to Plural tokeniser
4. Plural initiate the enrolment request to network for card tokenisation
5. Network validate the request and create card token and cryptogram and sends back to Plural
6. Plural generate the token reference id and map it with token, merchant, customer details
7. Plural sends the token reference id back to merchant for repeat transaction to fetch the token, cryptogram (TAVV) and other token details

![](https://files.readme.io/50cb9d1-Token_Provisioning.png "Token Provisioning.png")

## Token Payment Processing

1. Consumer initiates purchase on the merchant platform via saved card.
2. Merchant fetches the token, cryptogram (TAVV) and other token details from the Plural Tokenizer to perform authentication.
3. Plural Tokenizer fetches the token, cryptogram (TAVV) and other token details from Network and send the details back to merchant
4. Merchant initiates the authentication request to Plural PG to process the token payment 
5. Plural PG forwards the authentication request to Acquirer and network 
6. Network converts the token to PAN and passes to issuer 
7. Issuers authenticate or decline the transaction and send the response back to Network
8. Network forwards the response back to Acquirer and Acquirer back to Plural
9. Plural forwards the response back to Merchant and Merchant forwards the final response back to customer

![](https://files.readme.io/2a5e622-Token_Payment_Processing.png "Token Payment Processing.png")

# Integration Model

## External Tokeniser for Token Provisioning and Plural as Payment Aggregator for Token Payment Processing

When a consumer initiates purchase on an online transaction with consent to save card, post successful authentication and authorization the external token service integrates with respective network to tokenise the card and notifies the token reference merchant. Payment processing of the tokenised card can be done by plural and merchant will work with the external token service to get the token related information like token, cryptogram, and expiry.

![](https://files.readme.io/79d8029-External_Tokeniser_for_Token_Provisioning_and_Plural_as_Payment_Aggregator_for_Token_Payment_Processing.png "External Tokeniser for Token Provisioning and Plural as Payment Aggregator for Token Payment Processing.png")

## Plural Tokeniser for Token Provisioning and Plural as Payment Aggregator for Token Payment Processing

When a consumer initiates purchase on an online transaction with consent to save card, post successful authentication and authorization Plural Tokenizer integrates with respective network to tokenise the card and notifies the token reference merchant. Payment processing of the Tokenised card can be done by Plural in conjunction with Plural Tokenizer to get the token related information like token, cryptogram, and expiry.

![](https://files.readme.io/091e380-Plural_Tokeniser_for_Token_Provisioning_and_Plural_as_Payment_Aggregator_for_Token_Payment_Processing.png "Plural Tokeniser for Token Provisioning and Plural as Payment Aggregator for Token Payment Processing.png")

## Plural Tokeniser for Token Provisioning and other Payment Aggregator for Token Payment Processing

When a consumer initiates purchase on an online transaction with consent to save card, post successful authentication and authorisation, Plural Tokenizer integrates with respective network to tokenise the card and notifies the token reference to merchant. Payment processing of the tokenised card can be done by any of the merchant specific payment aggregator and merchant will work with Plural Tokenizer to get the token related information like token, cryptogram and expiry.

![](https://files.readme.io/50f83c0-Plural_Tokeniser_for_Token_Provisioning_and_other_Payment_Aggregator_for_Token_Payment_Processing.png "Plural Tokeniser for Token Provisioning and other Payment Aggregator for Token Payment Processing.png")

## Standalone Plural Tokeniser for Token Provisioning

When a consumer saves card at merchant web/app, Plural Tokenizer integrates with respective network directly to the network specific gateways or third-party gateways to tokenise the card and notifies the token reference to merchant.

![](https://files.readme.io/4a3b588-Standalone_Plural_Tokeniser_for_Token_Provisioning.png "Standalone Plural Tokeniser for Token Provisioning.png")
