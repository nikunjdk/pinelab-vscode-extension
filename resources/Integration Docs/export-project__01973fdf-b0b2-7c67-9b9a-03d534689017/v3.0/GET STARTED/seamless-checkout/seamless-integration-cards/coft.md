---
title: "COFT (Card on File Tokenisation) / Save Cards / COFT-Compliant Payments"
slug: "coft"
excerpt: "Learn how you can save your customer card details using Plural tokenization to process payments."
hidden: true
createdAt: "Mon Feb 17 2025 09:53:25 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Feb 18 2025 10:06:15 GMT+0000 (Coordinated Universal Time)"
---
With the implementation of Card on File Tokenization (COFT) compliance, Payment Aggregators (PAs) and Payment Gateways (PGs) can no longer store card details in any encrypted format within their databases. Currently, Plural processes transactions using cards and tokens but does not support a saved card feature due to these regulatory constraints.

To address this limitation, card networks have introduced token provisioning. In this process, a token is generated by the network for a card after obtaining the customer’s consent. This token is then securely stored and managed in the customer vault by the platform, enabling saved card functionality while ensuring compliance with COFT regulations. The stored token can be used for future transactions, ensuring both security and regulatory adherence.

## How It Works

**First Transaction**: A token is provisioned for the customer’s card after successful authorization of a GCT (Generic Card Transaction). Customers must provide explicit consent via Plural’s checkout (redirect/iFrame) or the merchant’s checkout page (seamless). 

**Subsequent Transactions**: At checkout, all saved tokens are displayed for the customer to choose from. Before initiating payment, a cryptogram is generated against the selected token. The transaction is then processed via COFT (Card on File Tokenization), ensuring compliance and security.

## Key Entities in Card on File Tokenization (COFT)

COFT involves multiple stakeholders working together to enable secure token-based transactions. Each entity plays a critical role in ensuring seamless tokenization, storage, and processing. Below are the key participants in this ecosystem: 

1. **Token Requestor (TR)** 

**Definition**: An entity, such as a merchant or payment service provider (PSP), that initiates a request to replace a Primary Account Number (PAN) with a token. 

**Role**: Sends the original card details to the Token Service Provider (TSP) to generate a token. For example, when a merchant saves a card for future transactions, they act as the Token Requestor. 

**Plural’s Role**: Plural functions as the Token Requestor. 

2. **Token Service Provider (TSP) **

**Definition**: The entity responsible for generating and managing tokens within the tokenization ecosystem. 

**Role**: Receives token requests from the Token Requestor, replaces the card’s PAN with a token, and securely maps it to the original card. The TSP also translates the token back to the PAN during payment processing. 

**Examples**: VISA, Mastercard, RuPay, Diners, AMEX act as TSPs. 

3. **Token Provisioner (TP)** 

**Definition**: The entity responsible for provisioning the tokenized card information to merchants. 

**Role**: Ensures tokens are securely assigned to the correct merchant account and customer-card combination. 

**Plural’s Role**: Plural also functions as the Token Provisioner. 

4. **Card Issuer (Issuing Bank)** 

**Definition**: The financial institution that issues the payment card to the cardholder. 

**Role**: Authorizes and settles transactions. When a tokenization request is made, the issuer may approve or decline it based on customer account status and fraud considerations. 

5. **Cardholder** 

**Definition**: The individual who holds and uses the payment card issued by the bank. 

**Role**: Can enroll their card in the tokenization process, typically when saving a card for future transactions. 

6. **Acquirer (Acquiring Bank)** 

**Definition**: The financial institution that processes card transactions on behalf of merchants. 

**Role**: Receives tokenized transaction requests from merchants and forwards them to the card network for authorization. 

7. **Card Network (Payment Networks)** 

**Definition**: The entity (e.g., Visa, Mastercard, American Express) that facilitates communication between the acquirer and issuer. 

**Role**: Routes tokenized transaction requests from the merchant or acquirer to the Token Service Provider and subsequently to the issuer for authorization.
