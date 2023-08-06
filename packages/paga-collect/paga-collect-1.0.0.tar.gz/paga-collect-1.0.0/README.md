# Paga Collect Python library
The Paga Collect API allows anyone to initiate a payment request to a third party and automatically get notified when the payment request is fulfilled. This library makes it easier and faster for developers to integrate the API

### 1. Installation
Make sure you have `pip` installed, then run the command below
```sh
pip install paga-collect
```


### 2. Usage
Once installed to use the library see sample code below:
```sh
from paga_collect import Collect;

principal = "public_key"
credentials = "private"
hash_key = "hash_key"

collect = Collect(principal, credentials, hash_key, False)
```


### Paga Collect API Operations
Now that you have created a collect api object you easily call its operations

<br>

#### Request Payment
Register a new request for payment between a payer and a payee. Once a payment request is initiated successfully, the payer is notified by the platform (this can be suppressed) and can proceed to authorize/execute the payment. Once the payment is fulfilled, a notification is sent to the supplied callback URL. See the callback notification section for more details.
<br>
To make a payment request see sample code below:
```sh
payment_request_payload = {
    "referenceNumber": "6020000011z",
    "amount": "100",
    "currency": "NGN",
    "payer": {
        "name": "John Doe",
        "phoneNumber": "07033333333",
        "bankId": "3E94C4BC-6F9A-442F-8F1A-8214478D5D86"
    },
    "payee": {
        "name": "Payee Tom",
        "accountNumber": "1188767464",
        "bankId": "40090E2F-7446-4217-9345-7BBAB7043C4C",
        "bankAccountNumber": "0000000000",
        "financialIdentificationNumber": "03595843212"
    },
    "expiryDateTimeUTC": "2021-05-27T00:00:00",
    "isSuppressMessages": "true",
    "payerCollectionFeeShare": "0.5",
    "recipientCollectionFeeShare": "0.5",
    "isAllowPartialPayments": "true",
    "callBackUrl": "http://localhost:9091/test-callback",
    "paymentMethods": ["BANK_TRANSFER", "FUNDING_USSD"]
}

response = collect.payment_request(payment_request_payload)
```

<br>

#### Register Persistent Payment Account

An operation for business to create Persistent Payment Account Numbers that can be assigned to their customers for payment collection.
<br>
To create a persistent payment account see sample code below:
```sh
register_persistent_payment_account_payload = {
    "referenceNumber": "test123451",
    "phoneNumber": "07022222222",
    "accountName": "Joh Doe",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@doe.com",
    "accountReference": "22222222222220",
    "financialIdentificationNumber": "22182799077",
    "callbackUrl": "http://localhost:9091/test-callback"
}

response = collect.register_persistent_payment_account(register_persistent_payment_account_payload)
```

<br>

#### Query Status
Query the current status of a submitted request
<br>
To check the status of a submitted request see sample code below:
```sh
status_payload = {"referenceNumber": "82000001109", }

response = collect.get_status(status_payload)
```

<br>

#### Query History
Get payment requests for a period between given start and end dates. The period window should not exceed 1 month.
<br>
See sample code below:
```sh
history_payload = {
    "referenceNumber": "82000001109",
    "startDateTimeUTC" : "2021-05-13T19:15:22",
    "endDateTimeUTC" : "2021-05-20T19:15:22"
}

response = collect.get_history(history_payload)
```

<br>

#### Get Banks
Retrieve a list of supported banks and their complementary unique ids on the bank. This is required for populating the payer (optional) and payee objects in the payment request model.
<br>
See usage sample code below:
```sh
banks_payload = {"referenceNumber": "0001109"}

response = collect.get_banks(status_payload)
```

