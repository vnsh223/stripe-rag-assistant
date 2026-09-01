Source: https://docs.stripe.com/payments/payment-methods/overview

# Supported payment methods

Learn about the types of payment methods that your Stripe integration can support.

Stripe supports the following categories of payment methods:

- [Cards](https://docs.stripe.com/payments/payment-methods/overview.md#cards)
- [Bank debits](https://docs.stripe.com/payments/payment-methods/overview.md#bank-debits)
- [Bank redirects](https://docs.stripe.com/payments/payment-methods/overview.md#bank-redirects)
- [Bank transfers](https://docs.stripe.com/payments/payment-methods/overview.md#bank-transfers)
- [Buy now, pay later](https://docs.stripe.com/payments/payment-methods/overview.md#buy-now-pay-later)
- [Real-time payments](https://docs.stripe.com/payments/payment-methods/overview.md#real-time-payments)
- [Vouchers](https://docs.stripe.com/payments/payment-methods/overview.md#vouchers)
- [Wallets](https://docs.stripe.com/payments/payment-methods/overview.md#wallets)

Different payment methods are more dominant in certain regions, meaning not all customers have or prefer a card payment method. Offering more options can help reduce the chance of losing a customer at checkout. Each payment method has its own restrictions around supported currencies, countries, products, and API options. To learn more see, [Payment method support](https://docs.stripe.com/payments/payment-methods/payment-method-support.md).

For information on payment method transaction fees, refer to [pricing details](https://stripe.com/pricing/local-payment-methods).

Each category has similar features, a single integration, and common checkout experiences. After you integrate one payment method, you can add another within the same category with minimal changes to your integration.
[Watch on YouTube](https://www.youtube.com/watch?v=tJin1R6KLyA)
## Cards 

Cards are a common way for customers and businesses to pay online or in person. Stripe supports global and local card networks. See the [card brands](https://docs.stripe.com/payments/cards.md#supported-card-brands) that Stripe supports.

| Global | US and Canada | Europe | Asia Pacific | Latin America |
| --- | --- | --- | --- | --- |
| [Visa](https://docs.stripe.com/payments/cards.md#supported-card-brands) | [Discover](https://docs.stripe.com/payments/cards.md#supported-card-brands) | [Cartes Bancaires](https://docs.stripe.com/payments/cartes-bancaires.md) | [eftpos](https://docs.stripe.com/payments/cards.md#supported-card-brands) | — |
| [Mastercard](https://docs.stripe.com/payments/cards.md#supported-card-brands) | [Interac (In-person only)](https://docs.stripe.com/terminal/payments/regional.md?country=CA) |  | [JCB](https://docs.stripe.com/payments/cards.md#supported-card-brands) |  |
| [American Express](https://docs.stripe.com/payments/cards.md#supported-card-brands) |  |  | [China Union Pay](https://docs.stripe.com/payments/cards.md#supported-card-brands) |  |
| [Diners](https://docs.stripe.com/payments/cards.md#supported-card-brands) |  |  | [South Korean Cards](https://docs.stripe.com/payments/countries/korea.md) |  |

In-person payments support different card brands, depending on the country and reader type. For more information, see Terminal’s [supported card brands](https://docs.stripe.com/terminal/payments/collect-card-payment/supported-card-brands.md#payment-method-availability).

## Bank debits 

By debiting your customer’s bank account directly, you can save on transaction fees when compared to cards. For details, see the [bank debits documentation](https://docs.stripe.com/payments/bank-debits.md).

| Global | US and Canada | Europe | Asia Pacific | Latin America |
| --- | --- | --- | --- | --- |
| — | [Instant Bank Payments](https://docs.stripe.com/payments/link/instant-bank-payments.md) | [Bacs Direct Debit](https://docs.stripe.com/payments/payment-methods/bacs-debit.md) | [AU BECS Direct Debit](https://docs.stripe.com/payments/au-becs-debit.md) | — |
| — | [ACH Direct Debit](https://docs.stripe.com/payments/ach-direct-debit.md) | [SEPA Direct Debit](https://docs.stripe.com/payments/sepa-debit.md) | [NZ BECS Direct Debit](https://docs.stripe.com/payments/nz-bank-account.md) | — |
| — | [Canadian PADs](https://docs.stripe.com/payments/acss-debit.md) | — | — |

## Bank redirects 

Bank redirects let customers pay online using their bank account, using a secure checkout flow. They’re popular among European and Asian customers and can improve conversion and reduce fraud. See [bank redirects](https://docs.stripe.com/payments/bank-redirects.md) to learn more.

| Global | US and Canada | Europe | Asia Pacific | Latin America |
| --- | --- | --- | --- | --- |
| — | — | [Bancontact](https://docs.stripe.com/payments/bancontact.md) | [FPX](https://docs.stripe.com/payments/fpx.md) | — |
| — | — | [BLIK](https://docs.stripe.com/payments/blik.md) | [PayNow](https://docs.stripe.com/payments/paynow.md) | — |
| — | — | [EPS](https://docs.stripe.com/payments/eps.md) | [UPI](https://docs.stripe.com/payments/upi.md) | — |
| — | — | [iDEAL | Wero](https://docs.stripe.com/payments/ideal.md) | — |
| — | — | [P24](https://docs.stripe.com/payments/p24.md) | — | — |
| — | — | [TWINT](https://docs.stripe.com/payments/twint.md) | — | — |

To request access to one of our invite only payment methods, [contact us](https://support.stripe.com/contact).

## Bank transfers 

Customers or other businesses can use bank transfers to send money directly to your bank account and are common for accepting large payments from other businesses. In some countries, bank transfers are popular for consumer payments as well. See [bank transfers](https://docs.stripe.com/payments/bank-transfers.md) to learn more.

| Global | US and Canada | Europe | Asia Pacific | Latin America |
| --- | --- | --- | --- | --- |
| — | [USD Bank Transfer](https://docs.stripe.com/payments/bank-transfers.md) | [SEPA Bank Transfer](https://docs.stripe.com/payments/bank-transfers.md) | [Japan Bank Transfer (Furikomi)](https://docs.stripe.com/payments/bank-transfers.md) | [Mexico Bank Transfer](https://docs.stripe.com/payments/bank-transfers.md) |
| — | — | [UK Bank Transfer](https://docs.stripe.com/payments/bank-transfers.md) | — | — |

## Buy now, pay later 

Buy now, pay later payment methods help retailers reach customers who want to pay in installments. Your business is paid immediately and in full, and your customer pays nothing or a portion of the total cost at checkout. See [buy now, pay later](https://docs.stripe.com/payments/buy-now-pay-later.md) to learn more.

| Payment method | US and Canada | Europe | Asia Pacific | Latin America |
| --- | --- | --- | --- | --- |
| [Affirm](https://docs.stripe.com/payments/affirm.md) | ✓ Supported | ✓ Supported UK Only
(Invite only) | ✗ Not supported | ✗ Not supported |
| [Afterpay / Clearpay](https://docs.stripe.com/payments/afterpay-clearpay.md) | ✓ Supported | ✓ Supported | ✓ Supported | ✗ Not supported |
| [Klarna](https://docs.stripe.com/payments/klarna.md) | ✓ Supported | ✓ Supported | ✓ Supported | ✗ Not supported |
| [Meses sin intereses](https://docs.stripe.com/payments/mx-installments.md) | ✗ Not supported | ✗ Not supported | ✗ Not supported | ✓ Supported |
| [Zip](https://docs.stripe.com/payments/zip.md) | ✓ Supported (US Only) US Only | ✗ Not supported | ✓ Supported | ✗ Not supported |

To request access to one of our invite only payment methods, [contact us](https://support.stripe.com/contact).

## Real-time payments 

Real-time payments let customers send money directly from their bank account or other funding source using an intermediary to authenticate, such as a phone number or other account. They’re a common payment type in Asia and Latin America. See [real-time payments](https://docs.stripe.com/payments/real-time.md) to learn more.

| Global | US and Canada | Europe | Asia Pacific | Latin America |
| --- | --- | --- | --- | --- |
| — | — | [Swish (Invite only)](https://docs.stripe.com/payments/swish.md) | [PayTo](https://docs.stripe.com/payments/payto.md) | [Pix](https://docs.stripe.com/payments/pix.md) |
| — | — | — | [PayNow](https://docs.stripe.com/payments/paynow.md) | — |
| — | — | — | [PromptPay](https://docs.stripe.com/payments/promptpay.md) | — |

To request access to one of our invite only payment methods, [contact us](https://support.stripe.com/contact).

## Vouchers 

Vouchers are a popular way for customers in Asia and Latin America to complete online purchases in-person. At checkout, customers receive a digital voucher with pending transaction details and then complete the payment at local stores. See [vouchers](https://docs.stripe.com/payments/vouchers.md) to learn more.

| Global | US and Canada | Europe | Asia | Latin America |
| --- | --- | --- | --- | --- |
| — | — | [Multibanco](https://docs.stripe.com/payments/multibanco.md) | [Konbini](https://docs.stripe.com/payments/konbini.md) | [OXXO](https://docs.stripe.com/payments/oxxo.md) |
| — | — | — | — | [Boleto](https://docs.stripe.com/payments/boleto.md) | — |

## Wallets 

Wallets provide a fast and secure way for customers to pay with a saved card or a stored balance. Wallets can help increase conversion and reduce fraud. To learn more, see [Wallets](https://docs.stripe.com/payments/wallets.md).

| Global | US and Canada | Europe | Asia | Latin America |
| --- | --- | --- | --- | --- |
| [Apple Pay (Not available in India)](https://docs.stripe.com/apple-pay.md) | [Cash App Pay](https://docs.stripe.com/payments/cash-app-pay.md) | [PayPal](https://docs.stripe.com/payments/paypal.md) | [Alipay](https://docs.stripe.com/payments/alipay.md) | — |
| [Google Pay (Not available in India)](https://docs.stripe.com/google-pay.md) |  | [MobilePay](https://docs.stripe.com/payments/mobilepay.md) | [WeChat Pay](https://docs.stripe.com/payments/wechat-pay.md) |  |
| [Link](https://docs.stripe.com/payments/link.md) |  |  | [PayPay](https://docs.stripe.com/payments/paypay.md) |  |
| [Secure Remote Commerce](https://docs.stripe.com/secure-remote-commerce.md) |  | [Revolut Pay](https://docs.stripe.com/payments/revolut-pay.md) | [GrabPay](https://docs.stripe.com/payments/grabpay.md) |  |
| [Stablecoins and crypto](https://docs.stripe.com/payments/stablecoin-payments.md) |  | [Satispay](https://docs.stripe.com/payments/satispay.md) | [Kakao Pay](https://docs.stripe.com/payments/countries/korea.md) |  |
|  |  | [MB WAY](https://docs.stripe.com/payments/mb-way.md) | [Naver Pay](https://docs.stripe.com/payments/countries/korea.md) |  |
|  |  |  | [Samsung Pay](https://docs.stripe.com/payments/countries/korea.md) |  |
|  |  |  | [PayCo](https://docs.stripe.com/payments/countries/korea.md) |  |

To request access to one of our invite only payment methods, [contact us](https://support.stripe.com/contact).

## Custom payment methods 

If you need a payment method that’s not on this page, see [custom payment methods](https://docs.stripe.com/payments/payment-methods/custom-payment-methods.md).

## See also

- [Guide to Payment Methods](https://stripe.com/payments/payment-methods-guide)
- [Supported card brands](https://docs.stripe.com/payments/cards.md#supported-card-brands)
- [Faster checkout with Link](https://docs.stripe.com/payments/link.md)
- [Wallets](https://docs.stripe.com/payments/wallets.md)
- [Vouchers](https://docs.stripe.com/payments/vouchers.md)
