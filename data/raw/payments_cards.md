Source: https://docs.stripe.com/payments/cards

# Cards

Learn more about accepting card payments with Stripe.

Cards are linked to a debit or credit account at a bank. To complete a payment online, customers enter their card information at checkout. Cards are enabled by default and are supported by [online payments integration paths](https://docs.stripe.com/payments/online-payments.md#compare-features-and-availability). You can manage payment methods from the [Dashboard](https://dashboard.stripe.com/settings/payment_methods). Stripe handles the return of eligible payment methods based on factors such as the transaction’s amount, currency, and payment flow.

## Payment flow 

A customer initiates a card payment at checkout by entering their credit card information. Depending on their card network and country location, customers might have additional security verification steps.
![A flowchart showing the three required and one optional step for a customer to pay with card.](https://b.stripecdn.com/docs-statics-srv/assets/pay-with-card.059eb99f8cad148c1aea3bb2a29b8284.svg)

Cards can act as the funding source for other Stripe payment products and methods like [Link](https://docs.stripe.com/payments/link.md) and [wallets](https://docs.stripe.com/payments/wallets.md). For instance, customers can use Link to save their card payment data for fast checkout with any business that has Link enabled.

With wallets, customers can store their card details in a *digital wallet* (A digital wallet is a contactless payment method that stores payment options, such as credit and debit cards, allowing customers to use a smart device to make a purchase). From your end, their payment method is managed using a `wallet`, but for the customer, the transaction shows up in their card history as a charge from their digital wallet provider.

## Supported card brands 

Stripe supports several card brands, from large global networks like Visa and Mastercard to local networks like Cartes Bancaires in France or Interac in Canada. When you integrate Stripe, you can begin accepting a diversity of card brands without any additional configurations, including:

- American Express
- China UnionPay (CUP)
- Discover & Diners Club
- eftpos Australia
- Japan Credit Bureau (JCB)
- Mastercard
- Visa

Some card brands require additional configuration, such as [Cartes Bancaires](https://docs.stripe.com/payments/cartes-bancaires.md) and [Interac](https://docs.stripe.com/terminal/payments/regional.md?integration-country=CA#interac-payments).

> In integrations that [handle Link payments as card payments](https://docs.stripe.com/payments/link/link-payment-integrations.md?link-integrations=link-card-integrations), non-card payment methods saved to Link can have a card brand of `link`.

### Online card brand capabilities 

The following table describes some of the different features and restrictions of each card brand online, including limitations on countries where Stripe users can accept the brand (Stripe Account Country), countries where most cardholders of the brand are located (Customer Country) and support for key features like 3D Secure Authentication, and [Wallets](https://docs.stripe.com/payments/wallets.md) (like Apple Pay and Google Pay).

> Other payment scenarios like setting up [future payments](https://docs.stripe.com/payments/save-and-reuse.md), [saving a card](https://docs.stripe.com/payments/save-during-payment.md) or [placing a hold](https://docs.stripe.com/payments/place-a-hold-on-a-payment-method.md) are supported across all card brands.

Stripe supports processing payments in [135+ currencies](https://docs.stripe.com/currencies.md), but some card brand networks have limitations on [supported currencies](https://docs.stripe.com/currencies.md#presentment-currencies) that charges can be made with.

| Card Brand | Stripe Account Country | Customer Country | 3D Secure Authentication | Wallets |
| --- | --- | --- | --- | --- |
| **Visa** | All countries | Global | ✓ Supported | ✓ Supported |
| **Mastercard** | All countries | Global | ✓ Supported | ✓ Supported |
| **American Express** | All countries except Brazil, Malaysia, Thailand, and the United Arab Emirates | Global, except India1 | ✓ Supported | ✓ Supported |
| **Discover & Diners Club** | Canada, Japan, United Kingdom, United States, and the following European Economic Area countries: Austria, Belgium, Cyprus, Denmark, Estonia, Finland, France, Germany, Greece, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Norway, Poland, Portugal, Slovakia, Slovenia, Spain, Sweden, and Switzerland | Global | ✓ Supported | ✓ Supported |
| **China UnionPay** | Australia, Canada, Hong Kong, Malaysia, New Zealand, Singapore, United Kingdom, United States, Switzerland, and all countries in the European Economic Area except Iceland | Global | ✓ Supported | Not supported |
| **Japan Credit Bureau (JCB)** | Australia, Canada, Hong Kong, Japan, New Zealand, Singapore, Switzerland, United Kingdom, United States, and all countries in the European Economic Area except Iceland | Global | Hong Kong, Japan, Singapore, Switzerland, United Kingdom, and all countries in the European Economic Area except Iceland | ✓ Supported |
| **Cartes Bancaires** | All countries in the [SEPA](https://en.wikipedia.org/wiki/Single_Euro_Payments_Area) region, as well as Canada Australia, Hong Kong, Japan, Mexico, New Zealand, Singapore, and United States | France | ✓ Supported | ✓ Supported2 |
| **eftpos** | Australia | Australia | ✓ Supported | Not supported |

1 For more information, see [American Express card support for India-based businesses](https://support.stripe.com/questions/american-express-card-support-for-india-based-businesses).

2 Supports Apple Pay. For more information, see [Cartes Bancaires with Apple Pay](https://docs.stripe.com/apple-pay/cartes-bancaires.md).

### Exclude card brands 

You can disallow the use of specific card brands in the following ways:

- If you use Stripe Radar, [set up a rule](https://docs.stripe.com/radar/rules.md) to reject the desired brands.
- Add custom client-side code that checks the [brand](https://docs.stripe.com/api/cards/object.md#card_object-brand) of a card.

## Geographic considerations 

Stripe, along with other platforms, offer a solid infrastructure that handles secure payments and complies with specific regulations from different regions. This becomes particularly important with the roll-out of Strong Customer Authentication (SCA) rules in regulated markets like Europe and India, wherein additional verification steps are usually necessary.

It’s essential to ensure your Stripe integration is lined up with SCA rules and 3D Secure (3DS) criteria. Moreover, adjusting your approach to suit regional nuances—like installment payments and card brand preferences—is vital for seamless, compliant, and user-centered transactions.

### SCA and 3D Secure 

Some banks, especially in regulated regions like Europe and India, might prompt the customer to authenticate a purchase (for example, by texting the customer a code to enter on the bank’s website). This authentication step is part of *Strong Customer Authentication* (Strong Customer Authentication (SCA) is a regulatory requirement in effect as of September 14, 2019, that impacts many European online payments. It requires customers to use two-factor authentication like 3D Secure to verify their purchase) (SCA) Requirements. Making sure that your integration meets SCA requirements for 3DS can sometimes require extra steps.

[SCA](https://docs.stripe.com/strong-customer-authentication.md), a rule in effect as of September 14, 2019, as part of PSD2 regulation in Europe, requires changes to how your European customers authenticate online payments. Card payments require a different type of user authentication ([3DS](https://docs.stripe.com/payments/3d-secure.md) specifically) to meet SCA requirements.

Stripe supports 3DS by default in Stripe Checkout, Payment Links, and a Hosted Invoice Page. You can configure your integration to use 3DS with Subscriptions and *Connect* (Connect is Stripe's solution for multi-party businesses, such as marketplace or software platforms, to route payments between sellers, customers, and other recipients) with the following:

- *Payment Intents API* (The Payment Intents API tracks the lifecycle of a customer checkout flow and triggers additional authentication steps when required by regulatory mandates, custom Radar fraud rules, or redirect-based payment methods)
- *Setup Intents API* (The Setup Intents API lets you build dynamic flows for collecting payment method details for future payments. It tracks the lifecycle of a payment setup flow and can trigger additional authentication steps if required by law or by the payment method)
- Elements
- Mobile SDKs

### Installments 

Some regions have card brands that support installment payments managed by the card issuer. In such cases, you can’t use Subscriptions or SetupIntents to create installments.

If you want to create recurring payments and your region or card network doesn’t support [Meses sin intereses](https://docs.stripe.com/payments/mx-installments.md), see how to [set up future payments](https://docs.stripe.com/payments/save-and-reuse.md) or [Subscriptions](https://docs.stripe.com/billing/subscriptions/overview.md).

### Card brand choice 

The European Union requires businesses to allow their customers the option to pick which card brand processes their transaction because cards in the EU might have both a local network, like Cartes Bancaires, and an affiliated card network, like Visa or Mastercard. You can enable this choice using Elements or Payments APIs so that [customers can choose which card brand](https://docs.stripe.com/co-badged-cards-compliance.md) processes their payment.

### Accept card payments in India 

The Reserve Bank of India (RBI) has specific regulations for online transactions that apply to Stripe accounts in India. Stripe Support includes a consolidated list of important resources, for many payment methods in the [India FAQs](https://support.stripe.com/questions/india-faq).

## See also

- [Integrate card payment methods](https://docs.stripe.com/payments/payment-methods/integration-options.md)
- [Understand card updates and change default payment methods](https://docs.stripe.com/payments/cards/overview.md#card-updates)
- [Customize the way PaymentElements handle cards](https://docs.stripe.com/payments/customize-payment-methods.md)
