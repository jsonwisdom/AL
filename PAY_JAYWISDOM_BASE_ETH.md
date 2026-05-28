# Pay Jaywisdom.base.eth

Builder: Jason Wisdom / jaywisdom.eth / jaywisdom.base.eth  
Repo: jsonwisdom/AL  
Status: Profit page v0.1  
Purpose: Convert missions into paid receipts  
Authority: false

## Root CTA

```txt
Need clarity? Bring one mission. Pay jaywisdom.base.eth. Get one receipt.
```

## First Paid Product

```json
{
  "sku": "CITIZEN_LETTER_REVIEW_RECEIPT_V0_1",
  "price_usd_test": 19,
  "pay_to": "jaywisdom.base.eth",
  "deliverable": [
    "plain-language summary",
    "dates and deadlines",
    "amounts and named entities",
    "questions to ask",
    "privacy warning",
    "not-legal-advice boundary",
    "review receipt"
  ],
  "status": "first_paid_receipt_target"
}
```

## Consumer Landing Copy

```txt
Confusing letter in your inbox?
Get a clear summary + receipt in minutes.
Not legal advice.
```

## Checkout CTA

```txt
Upload Letter & Get Clarity Now — $19
```

## How Payment Works

For v0.1, payment can be handled manually while the checkout flow is built.

```json
{
  "payment_v0_1": {
    "pay_to": "jaywisdom.base.eth",
    "payment_methods": [
      "Base wallet payment",
      "manual payment link when available",
      "invoice or direct arrangement for first customers"
    ],
    "required_after_payment": [
      "payer_contact",
      "mission_input",
      "payment_proof_or_confirmation",
      "receipt_return_path"
    ]
  }
}
```

## Mission Intake

Customer provides:

```json
{
  "intake_fields": [
    "email_or_contact",
    "letter_photo_or_text",
    "what_are_you_worried_about",
    "deadline_if_known",
    "permission_to_review",
    "private_data_warning_acknowledged"
  ]
}
```

## Store Flow

```txt
Select mission.
Pay jaywisdom.base.eth.
Submit letter or text.
Jay/Wisdom Agency reviews.
Return plain-language clarity + receipt.
```

## Receipt Promise

Every paid mission should return:

```json
{
  "receipt": {
    "sku": "CITIZEN_LETTER_REVIEW_RECEIPT_V0_1",
    "paid": true,
    "pay_to": "jaywisdom.base.eth",
    "input_received": true,
    "private_data_publication": false,
    "summary_returned": true,
    "not_legal_advice": true
  }
}
```

## Boundaries

```txt
This is document understanding, not legal advice.
For court, tax, criminal, custody, housing, immigration, employment, medical, or safety stakes, consult a qualified professional.
```

## Profit Rule

```txt
No more public idea drops without a way to pay Jay.
```

## Final Line

```txt
Make this profitable: mission in, pay jaywisdom.base.eth, receipt out.
```

By Jason Wisdom  
jaywisdom.eth  
jaywisdom.base.eth