Source: https://docs.stripe.com/payments/ach-direct-debit

# ACH Direct Debit payments

Accept payments from US bank accounts using ACH Direct Debit.

ACH Direct Debit lets you accept payments from customers with a US bank account. There are two ways to accept US bank debits on Stripe: ACH Direct Debit and [Instant Bank Payments](https://docs.stripe.com/payments/link/instant-bank-payments.md). ACH Direct Debit is a [reusable](https://docs.stripe.com/payments/payment-methods.md#usage), [delayed notification](https://docs.stripe.com/payments/payment-methods.md#payment-notification) payment method that can take [up to 4 business days](https://docs.stripe.com/payments/ach-direct-debit.md#timing) to receive acknowledgement of success or failure. Because ACH Direct Debit isn’t a guaranteed payment method, there’s a risk of failed payments and [disputes](https://docs.stripe.com/payments/ach-direct-debit.md#disputes).

Accepting bank accounts is slightly different from accepting cards:

1. Your customer must [authorize](https://docs.stripe.com/payments/ach-direct-debit.md#mandates) the payment terms.
2. Bank accounts must be [verified](https://docs.stripe.com/payments/ach-direct-debit.md#verification).
3. `billing_details` must include the account holder’s name and, if the *merchant of record* (The legal entity responsible for facilitating the sale of products to a customer that handles any applicable regulations and liabilities, including sales taxes. In a Connect integration, it can be the platform or a connected account) is outside the US, a complete [`address`](https://docs.stripe.com/api/payment_methods/object.md#payment_method_object-billing_details-address).
Payment method family: Bank Debits
Usability: Reusable
Access type: Instant provisional access
Payment confirmation timing: Delayed
Settlement timing: Up to 4 business days (T+4)
Pricing: https://stripe.com/en-us/pricing/local-payment-methods#ach-direct-debit
## US bank debit comparison 

| Option | Confirmation time | Payment failure protection | Additional information |
| --- | --- | --- | --- |
| [Instant Bank Payments](https://docs.stripe.com/payments/link/instant-bank-payments.md) | Instant | Bank-initiated returns guaranteed by Stripe | For businesses looking for instant confirmation and faster settlement, Instant Bank Payments provides a card-like payment flow with the cost savings of bank debits. Instant Bank Payments are available only as a part of [Link](https://docs.stripe.com/payments/link.md). |
| ACH Direct Debit | Up to 4 business days | Use [Financial Connections](https://docs.stripe.com/financial-connections/ach-direct-debit-payments.md) data to optimize payments. | For businesses that don’t need instant confirmation, ACH Direct Debit has lower costs than Instant Bank Payments. ACH Direct Debit is popular for businesses with large or recurring transactions. |

## Timing 

With ACH Direct Debit, it can take time for funds to become available in your Stripe balance. The amount of time it takes for funds to become available is referred to as the settlement timing. The following tables describe the settlement timings for ACH Direct Debit payments that Stripe offers.

You can access the `expected_debit_date` for ACH Direct Debit under [payment_method_details](https://docs.stripe.com/api/charges/object.md#charge_object-payment_method_details-us_bank_account-expected_debit_date) for [Charges](https://docs.stripe.com/api/charges/object.md). This is an estimated date of when the funds might be debited. This estimate isn’t guaranteed and the actual date might vary. This information is available in API responses and in [charge.updated](https://docs.stripe.com/api/events/types.md#event_types-charge.updated), [charge.succeeded](https://docs.stripe.com/api/events/types.md#event_types-charge.succeeded), and [charge.failed](https://docs.stripe.com/api/events/types.md#event_types-charge.failed) webhook events when the debit date can be determined.

Initial payments made from select bank accounts that use temporary account numbers with Financial Connections might be subject to settlement delays.

| Settlement type | Timing | Cutoff time | Additional information |
| --- | --- | --- | --- |
| Standard settlement (T+4) | 4 business days from payment creation | 21:00 US/Eastern | After ACH Direct Debit payments settle to your Stripe account balance, we make payouts to your bank account according to your set payout schedule. |
| Faster settlement (T+2) | 2 business days from payment creation | 14:00 US/Eastern | This option is available only to eligible US users. You can check your eligibility and activate this option on the [Payment methods settings](https://dashboard.stripe.com/settings/payment_methods). For more information on faster settlement, see the [Support](https://support.stripe.com/questions/two-day-settlement-for-ach-direct-debit) page. |

![](https://b.stripecdn.com/docs-statics-srv/assets/settlement-timings.a7d03de51dbe6630245b69df27038ce1.svg)
 A diagram showing the two settlement timings for ACH Direct Debit: standard (4 days) and faster (2 days). 

For information on how to cancel payments, see [Refund and cancel payments](https://docs.stripe.com/refunds.md#cancel-payment).

## Connect and settlement 

Settlement speed is generally controlled at the platform level. The table below shows a comprehensive view of settlement timing by account and charge type.

| Account Type | Direct Charges | Destination Charges | Separate Charges and Transfers |
| --- | --- | --- | --- |
| **Standard with Platform Control** | The platform controls the settlement speed. | The platform controls the settlement speed. | The platform controls the settlement speed. |
| **Standard without Platform Control** | The connected account controls the settlement speed. | The connected account controls the settlement speed. | The platform controls the settlement speed. |
| **Express** | The platform controls the settlement speed. | The platform controls the settlement speed. | The platform controls the settlement speed. |
| **Custom** | The platform controls the settlement speed. | The platform controls the settlement speed. | The platform controls the settlement speed. |

## Eligibility and availability 

### Account eligibility
Business location: AT, BE, BG, CH, CY, CZ, DE, DK, EE, ES, FI, FR, GB, GI, GR, HR, HU, IE, IT, LI, LT, LU, LV, MT, NL, NO, PL, PT, RO, SE, SI, SK, US; Private preview: CA
Account type: ✓ Merchant, ✓ Platform or marketplace (Connect)
Business model: ✓ B2B, ✓ B2C
In addition to the industry and business categories listed in Stripe’s [Prohibited and restricted businesses](https://stripe.com/restricted-businesses) list, the following restrictions apply to ACH Direct Debit:

- In the UK, businesses selling CBD products are prohibited from using ACH Direct Debit.
- In the EU, the following business categories are restricted:
  - NFT businesses
  - Crowdfunding businesses
  - Charities
  - Pawn shops
  - Stamp and coin stores
  - Precious stones and metals, watches, and jewelry businesses
  - Antique shops, including sales, repairs, and restoration services
  - Jewelry stores, including watches, clocks, and silverware
  - Government-licensed online casinos
  - Betting and gambling businesses
  - Video game and arcade establishments
  - Digital goods businesses

Your account might be reviewed after activation to confirm eligibility. While ACH Direct Debit doesn’t enforce any additional website requirements, make sure that you provide a website that meets the [Stripe account activation requirements](https://support.stripe.com/questions/business-website-for-account-activation-faq). You can contact [Stripe support](https://support.stripe.com/) to appeal any ACH Direct Debit capability restrictions.

Stripe accounts in the following countries can accept ACH Direct Debit payments with local currency settlement.

AMER: US, [Preview] CA

EMEA: AT, BE, BG, CH, CY, CZ, DE, DK, EE, ES, FI, FR, GB, GI, GR, HR, HU, IE, IT, LI, LT, LU, LV, MT, NL, NO, PL, PT, RO, SE, SI, SK

Customers in the following countries can use ACH Direct Debit.

AMER: US

### Payment support
Buyer location: US
Presentment currency: USD
Geographic coverage: ✓ Domestic, ✓ Crossborder
Transaction limits: Minimum amount: 0.50 USD
### Blocked bank accounts 

To comply with Nacha regulations, Stripe might block bank accounts when a blockable ACH return is received until we can confirm that the issue causing the returns has been resolved. When this happens, Stripe sends the [payment_method.automatically_updated](https://docs.stripe.com/api/events/types.md#event_types-payment_method.automatically_updated) event for all saved payment methods.

Consuming these events can provide advance notice if your business model relies on recurring payments that need to be processed before a certain date. Inspect the event data for the `us_bank_account.status_details.blocked` field, then work with your customer to unblock or switch bank accounts before initiating future payments.

You receive equivalent events when the block is removed, indicating that payment methods can be reused immediately if an active mandate exists or you re-collect one.

For more information on blocked bank accounts and how to deal with them, see [Blocked bank accounts](https://docs.stripe.com/payments/ach-direct-debit/blocked-bank-accounts.md).

## Capabilities 
Recurring payments: ✓ Supported

Payment authorizations:
  ✗ Extended authorizations
  ✗ Flexible extended authorizations
  ✗ Incremental authorizations
  ✗ Decremental authorizations
  ✗ Re-authorizations

Payment captures:
  ✗ Manual capture
  ✗ Partial capture
  ✗ Multi-capture
  ✗ Over-capture

Refunds:
  ✗ Partial refunds
  ✓ Full refunds
  Submission window: 180 days
  Processing time: 3 business days

Disputes:
  ✗ Partial disputes
  ✓ Full disputes
  Submission window: 60 days
### Refunds 

You have up to 180 days from the original payment to submit a refund using the [Dashboard](https://dashboard.stripe.com/payments) or [Refunds API.](https://docs.stripe.com/api/refunds/create.md) This is the maximum the payment method allows-your return policy determines what you offer customers.

Refunds for ACH Direct Debit payments are asynchronous and take up to 3 business days to complete. ACH Direct Debit refunds can’t be canceled. 

#### Refund process 



ACH Direct Debit refunds are always processed as a separate credit to the customer’s bank account. Unlike card payments, they’re never issued as a reversal. The refund won’t be explicitly labeled as a refund on the customer’s bank statement. Instead, it appears as a credit referencing the original payment’s statement descriptor. We recommend notifying your customer when you issue a refund so they can identify the incoming credit.

#### Tracking refunds 

You can view refund status in the [Dashboard](https://dashboard.stripe.com/payments). Open the payment and click **View Details** on the refund entry, or [retrieve the Refund object](https://docs.stripe.com/api/refunds/retrieve.md) and check its `status` field. Stripe also notifies you of the final refund status using the `refund.updated` or `refund.failed` *webhook* (A webhook is a real-time push notification sent to your application as a JSON payload through HTTPS requests) event. When a refund succeeds, the status of the [Refund](https://docs.stripe.com/api/refunds/object.md) object transitions to `succeeded`. If a refund fails, the status transitions to `failed`, Stripe returns the amount to your Stripe balance, and you must arrange an alternative way to provide your customer with a refund.

Stripe waits for the original payment to succeed before submitting the refund.

> Issuing a refund does not prevent a dispute from being processed. To reduce the risk of a double credit, confirm with your customer that you’re processing the refund so they don’t independently file a dispute with their bank. Inform your customer of the expected processing time so they don’t escalate to their bank.

### Disputes 

Customers have up to 60 calendar days from the date of purchase to file ACH Direct Debit disputes.

ACH Direct Debit payments can only be disputed once.

#### Dispute process 

ACH Direct Debit provides a dispute process for bank account holders to dispute
payments. Customers can generally dispute a payment through their bank for up to
60 calendar days after a debit on a personal account, or up to two business days
for a business account. Disputes received within these timeframes are considered
final and uncontestable through the ACH network.

Consequently, you can't challenge these disputes and must resolve them directly
with your customers. In rare instances, a debit payment can be successfully
disputed outside these timelines. This is called a late return. The late return
process is primarily managed by and ultimately decided at the discretion of the
banks involved in the transaction.

Unlike credit card disputes, all ACH Direct Debit disputes are final with no
process for appeal. If a customer successfully disputes a payment, you must
contact them directly to resolve the situation. If you suspect that disputes are
fraudulent, Stripe Radar might help you reduce risk.

If you proactively issue your customer a refund while the customer's bank also
initiates the dispute process, your customer might receive two credits for the
same transaction.

When a customer disputes an ACH Direct Debit payment, it invalidates the mandate
associated with the payment method and you can't reuse it. To attempt a charge
again, you must resolve the dispute with the customer and collect a new mandate
authorization. If they dispute a subsequent payment, Stripe blocks the bank
account from further re-use.


#### Dispute notifications 

When a ACH Direct Debit dispute is opened, Stripe notifies you through:

- Email
- The [Stripe Dashboard](https://dashboard.stripe.com/disputes)
- A [charge.dispute.created](https://docs.stripe.com/api/events/types.md#event_types-charge.dispute.created) webhook event

The dispute reason is available in the Dashboard and in the `reason` field of the [Dispute object](https://docs.stripe.com/api/disputes/object.md). The evidence submission deadline is available in the Dashboard and in the `evidence_due_by` field of the Dispute object.

#### Responding to disputes 

You have 60 calendar days from dispute creation to submit evidence.

We request that you upload compelling evidence proving that you fulfilled the purchase order [using the Stripe Dashboard](https://docs.stripe.com/disputes/responding.md#respond). This evidence can include the:

- Tracking ID
- Shipping date
- Record of purchase for intangible goods, such as IP address or email receipt
- Record of purchase for services or physical goods, such as phone number or proof of receipt
- Record of refund (for purchases you’ve already refunded)

You can submit evidence and manage ACH Direct Debit disputes in the [Dashboard](https://dashboard.stripe.com/disputes) or programmatically using the [Disputes API](https://docs.stripe.com/api/disputes/update.md). In the Dashboard, go to the **Needs Response** tab, click the disputed payment, then click **Counter dispute** to submit your evidence, or **Accept dispute** to accept the loss. To submit evidence through the API, upload supporting files using the [Files API](https://docs.stripe.com/api/files/create.md) and include the returned file IDs when you update the [Dispute Evidence object](https://docs.stripe.com/api/disputes/update.md).

#### Dispute outcomes 

If ACH Direct Debit resolves the dispute in your favor, Stripe returns the disputed amount   to your Stripe balance.

If they rule in favor of the customer, the balance charge becomes permanent. Dispute fees are non-refundable regardless of the outcome.

ACH Direct Debit disputes allow only a single round of evidence submission. Make sure to gather all necessary evidence before submitting—you won’t be able to supplement it afterward.

### Proof of authorization 

In some rare circumstances, a customer’s bank initiates an inquiry to request proof of authorization for an ACH Debit. If you use custom mandates through the [Payment Intents API](https://docs.stripe.com/api/payment_intents.md), Stripe creates a dispute inquiry for your business to provide evidence for the payment in question. If you use Stripe-hosted ACH mandates, Stripe automatically responds to the customer’s bank with a copy of the debit authorization.

When Stripe receives an ACH Debit authorization inquiry, a [charge.dispute.created](https://docs.stripe.com/api/events/types.md#event_types-charge.dispute.created) event is triggered with the status `warning_needs_response` and a new dispute inquiry is shown in the Dashboard. To comply with Nacha rules, you must upload evidence of the customer’s authorization upon request.

#### Evidence to submit for an ACH inquiry

Here is the evidence you need to submit for an ACH inquiry:

- **Mandate authorization (required)**: A copy of the authorization proving that the customer or bank account holder agreed to the debit on their bank account.
- **Sales receipt**: Documentation of the goods or services purchased by the customer.
- **Customer information**: Information on the customer’s identity proving that the accountholder authorized the payment and received the good or service.

You can upload evidence through the Stripe Dashboard or the [Files API](https://docs.stripe.com/api/files.md). You can only submit evidence for a dispute inquiry once. If you don’t submit evidence before the deadline, the dispute is accepted and closed.

#### Submit evidence through the Dashboard

To submit evidence to contest a late return dispute through the Dashboard:

1. Go to [the payments page](https://dashboard.stripe.com/payments) and look for a payment with an inquiry icon.
2. Click **Respond to the inquiry** to provide more details about the transaction. You can upload an image or PDF of the proof of authorization.

#### Post-submission

After receiving evidence submissions, Stripe sends a [charge.dispute.updated](https://docs.stripe.com/api/events/types.md#event_types-charge.dispute.created) event and a message appears in your timeline confirming receipt of the evidence. After you submit evidence, the bank reviews the evidence and makes a determination. If the evidence is sufficient, the dispute inquiry closes in your favor and is marked as `won`. If the bank determines that the authorization is insufficient, the dispute closes and is marked as `lost`.

### Mandates 

ACH Direct Debit payments require customer authorization before you can debit their bank account. To obtain authorization, present a mandate to your customer. Stripe collects and stores mandate acceptance on your behalf when you use Stripe’s payment front-end products, such as [Checkout](https://docs.stripe.com/payments/checkout.md). If you build a custom payment form, you’re responsible for displaying the required mandate language before confirming the payment.

#### What customers authorize 

When a customer provides their bank details, they authorize your business to debit their account under the agreed terms. Stripe stores this authorization and associates it with the PaymentMethod object.

The mandate records:

- The business name
- Whether the authorization is one-time or recurring
- The date and method of acceptance (IP address, user agent, and timestamp for online flows)

#### Collect mandates 

When you use Checkout or the Payment Element, Stripe displays the required
mandate language and records acceptance automatically. No additional integration
is required.

If you collect payment details outside of Stripe's hosted flows, see
Online and offline mandates below for the recommended mandate text to display
to your customer before confirming the payment.


#### Manage mandates 

Active mandates appear in the Dashboard under a customer’s saved payment methods. Each mandate displays the accepted text, acceptance date, and IP address. To retrieve mandate details programmatically, use the [Mandate API](https://docs.stripe.com/api/mandates.md).

#### Cancel mandates 

Customers can revoke a mandate at any time by contacting you directly. When a customer notifies you of a cancellation:

1. Cancel or capture any pending payments associated with the mandate.
2. Detach the `PaymentMethod` from the customer or mark the mandate as inactive using the [Detach API](https://docs.stripe.com/api/payment_methods/detach.md).

If you debit an account after a mandate is canceled, the payment will fail.

#### Online and offline mandates 

There are two types of mandates: online and offline. Online mandates appear as part of the payment flow on a website and customers accept them through a user interface element such as clicking an Accept or Pay button. Offline mandates require that you present the specific terms to your customer in writing or over the phone. Stripe supports several offline mandate types for ACH Direct Debit.

Stripe displays an online mandate on the payment page for you if you use [Checkout](https://docs.stripe.com/payments/checkout.md), [Payment Element](https://docs.stripe.com/payments/payment-element.md), or the [Hosted Invoice Page](https://docs.stripe.com/invoicing/hosted-invoice-page.md).

If you build a custom payment form that integrates directly with the [Payment Intents API](https://docs.stripe.com/api/payment_intents.md), you must display the mandate terms on your payment page before confirming the PaymentIntent or SetupIntent. You only need to display a mandate the first time you collect a customer’s bank account. We recommend using the following mandate text:

|  |
| By clicking [accept], you authorize [Business Name] to debit the bank account specified above for any amount owed for charges arising from your use of [Business Name]'s services and/or purchase of products from [Business Name], pursuant to [Business Name]'s website and terms, until this authorization is revoked. You may amend or cancel this authorization at any time by providing notice to [Business Name] with 30 (thirty) days notice. |

If you plan to use the customer’s bank account for future payments with the [setup_future_usage](https://docs.stripe.com/api/payment_intents/create.md#create_payment_intent-setup_future_usage) parameter or by [saving bank details](https://docs.stripe.com/payments/ach-direct-debit/set-up-payment.md) for a future payment, also include the following authorization:

|  |
| If you use [Business Name]'s services or purchase additional products periodically pursuant to [Business Name]'s terms, you authorize [Business Name] to debit your bank account periodically. Payments that fall outside of the regular debits authorized above will only be debited after your authorization is obtained. |

If you originate recurring preauthorized debits, you must disclose to your customers how these amounts are calculated or a range the customer can anticipate. You must also give your customer at least 7 calendar days notice if you change the timing of any recurring preauthorized debits.

#### Mandate and microdeposit emails 

To comply with Nacha rules, you must provide each customer with an electronic or hard copy of the mandate. By default, if your customer provides a [billing email address](https://docs.stripe.com/api/payment_methods/object.md#payment_method_object-billing_details-email), Stripe automatically emails your customer the following information:

- Confirmation of the mandate, per Nacha requirements.
- Notification if Stripe needs to use microdeposits to verify your customer’s bank account. These notification emails link to a hosted verification page.

##### Sending custom mandate notifications

You can send custom mandate notifications to customers. To send custom mandate notifications:

1. Turn off Stripe emails in the Stripe Dashboard [email settings](https://dashboard.stripe.com/settings/emails).
2. Send a mandate confirmation email when you receive your customer’s bank account and mandate authorization.

In the email, include the following information:

- Authorization date
- Account holder name
- Financial institution
- Routing number
- Last four digits of the account number

The following is a sample mandate confirmation email that you can send.

|  |
| Agreement Date | **June 28, 2021** |
| Account Holder Name | **Jenny Rosen** |
| Financial Institution | **Chase Bank** |
| Routing Number | **021000021** |
| Account Number | \******6789 |

|  |
| Thank you for signing up for direct debits from [Business Name]. You have authorized [Business Name] to debit the bank account specified above for any amount owed for charges arising from your use of [Business Name]'s services and/or purchase of products from [Business Name], pursuant to [Business Name]'s website and terms, until this authorization is revoked. You can amend or cancel this authorization at any time by providing notice to [Business Name] with 30 (thirty) days notice. |

If you collected the customer’s bank account for future payments with the [setup_future_usage](https://docs.stripe.com/api/payment_intents/create.md#create_payment_intent-setup_future_usage) parameter or by [saving bank details](https://docs.stripe.com/payments/ach-direct-debit/set-up-payment.md), also include:

|  |
| You have authorized [Business Name] to debit your bank account periodically if and when you use [Business Name]'s services or purchase more than one of [Business Name]'s products periodically pursuant to [Business Name]'s terms. Payments that fall outside of the regular debits authorized above will only be debited after your authorization is obtained. |

> If you choose to send custom emails, you also need to send microdeposit reminder emails. For detailed instructions, see [Custom microdeposit email and verification page](https://docs.stripe.com/payments/ach-direct-debit/accept-a-payment.md?web-or-mobile=web&payment-ui=direct-api#optional-send-custom-email-notifications).

#### When mandates become inactive 

ACH Direct Debit mandates can become inactive, which renders the payment method unusable. This can occur when a customer disputes a payment, when certain [payment failures](https://docs.stripe.com/payments/ach-direct-debit.md#transaction-failures) occur, or when Stripe becomes aware that the payment method is no longer valid, such as when a [bank account is blocked](https://docs.stripe.com/payments/ach-direct-debit.md#blocked-bank-accounts).

### Transaction failures 

ACH Direct Debit transactions can fail any time after the payment is initiated through payment confirmation. These failures can occur for a number of reasons, such as:

- Insufficient funds
- An invalid account number
- A customer disabling debits from their bank account

If a payment fails after funds have been made available in your Stripe balance, Stripe immediately removes funds from your Stripe account.

In rare situations, Stripe might receive an ACH failure from the bank after a PaymentIntent has transitioned to `succeeded`. If this happens, Stripe creates a dispute with a `reason` of:

- `insufficient_funds`
- `incorrect_account_details`
- `bank_cannot_process`

Stripe charges a failure fee in this situation.

### Verification 

Learn about [validation and verification](https://support.stripe.com/questions/nacha-bank-account-validation-rule) requirements.

Stripe lets your customers securely share their financial data by linking their financial accounts to your business. Use [Financial Connections](https://docs.stripe.com/financial-connections.md) to access customer-permissioned financial data such as tokenized account and routing numbers, balance data, ownership details, and transaction data.

Your customers might enter their bank account manually instead of authenticating with Stripe Financial Connections. In these cases, Stripe provides a fully-hosted flow for collecting bank account details and verifies them with microdeposits. Customers have 10 days to verify their bank account with microdeposits. If they don’t verify within this timeframe, the PaymentIntent or SetupIntent reverts to requiring new payment method details.

When you use [Stripe.js](https://docs.stripe.com/payments/elements.md), our JavaScript library for building payment flows, Stripe provides a fully-hosted collection of bank account details, instant bank verification, and (if needed) delayed verification using microdeposits. This verification process is a requirement for many businesses, and it helps reduce payment failures and fraudulent activities.

## Stripe product support 
Products:
  ✓ Checkout
  ✓ Payment Links
  ✓ Payment Element
  ✗ Express Checkout Element
  ✗ Mobile Payment Element
  ✗ Managed Payments
  ✓ Billing
  ✓ Invoicing
  ✓ Adaptive Pricing
  ✗ Customer Portal
  ✓ Radar
  ✗ Terminal
  ✓ Connect

APIs:
  ✓ PaymentIntents
  ✓ PaymentIntents with setup_future_usage
  ✓ SetupIntents
  ✓ CheckoutSessions
If you use *Connect* (Connect is Stripe's solution for multi-party businesses, such as marketplace or software platforms, to route payments between sellers, customers, and other recipients), you must take the following into consideration before you enable and use ACH Direct Debits.

### Request ACH Debit capabilities for your connected accounts

Set the `us_bank_account_ach_payments` capability to `active` on your platform account, and for any connected accounts you want to enable for ACH debits. You can also [request more account capabilities](https://docs.stripe.com/connect/account-capabilities.md#requesting-unrequesting).

> Stripe automatically refunds the application fee to your platform account when the [destination charge](https://docs.stripe.com/connect/charges.md#destination) for an ACH debit fails. Learn about [fees for failed payments](https://stripe.com/pricing/local-payment-methods#ach-direct-debit).

### Merchant of record 

The [charge type](https://docs.stripe.com/connect/charges.md) of Connect payments might change the merchant of record. The charge type can also change:

- The *merchant of record* (The legal entity responsible for facilitating the sale of products to a customer that handles any applicable regulations and liabilities, including sales taxes. In a Connect integration, it can be the platform or a connected account) shown on the mandate
- The business shown on confirmation emails
- The business shown on microdeposit reminder emails

The merchant of record determines the Stripe account authorized to create payments with a particular [PaymentMethod](https://docs.stripe.com/api/payment_methods/object.md). To learn more about sharing this authorization across multiple connected accounts, see [PaymentMethod and Mandate cloning](https://docs.stripe.com/payments/ach-direct-debit.md#payment-method-and-mandate-cloning).

### PaymentMethod and mandate cloning 

You can collect customer bank accounts on the platform account and [clone](https://docs.stripe.com/connect/direct-charges-multiple-accounts.md#clone-and-create-direct-charges) ACH Direct Debit payment methods. Cloning these methods allows you to save customer bank accounts for later use on connected accounts. When you clone ACH Direct Debit payment methods, Stripe duplicates the mandate authorization to the connected account, but we don’t send any new mandate confirmation emails.

> If a mandate is authorized for a PaymentIntent or SetupIntent [on_behalf_of](https://docs.stripe.com/connect/charges.md#on_behalf_of) a connected account, you can’t use that mandate with a different connected account.

When collecting a bank account that you intend to clone to connected accounts, you must communicate to the customer that their authorization extends to connected accounts on your platform. For example, you can communicate this message to a customer through the mandate terms. Failure to communicate this message to your customers could result in customer confusion and increase the risk of disputed payments.

### Fraud protection for ACH with Radar 

[Stripe Radar](https://stripe.com/radar) provides fraud protection capabilities for ACH Direct Debits without any additional development time, performing real-time evaluation using machine learning algorithms to help identify and block high-risk transactions. Our machine learning trains specifically for ACH, so it’s effective at detecting fraud that might be unique to ACH Direct Debit payments.

For Radar users, Radar might be on by default for all supported payment methods.

### Billing retries 

Enable [Direct Debit retries](https://docs.stripe.com/billing/revenue-recovery/smart-retries.md#direct-debit-retries) to have Stripe automatically retry failed Direct Debit payments caused by insufficient funds. You can turn on retries for [recurring subscription invoices](https://dashboard.stripe.com/revenue_recovery/retries), [one-off invoices](https://dashboard.stripe.com/settings/billing/invoices/general), or both.

Stripe can automatically retry each failed ACH Direct Debit payment a maximum of 2 times, no more than 40 days after the original payment attempt. These limits differ from card retries because ACH Direct Debit payments are asynchronous and can take several business days to complete.

## Customer experience 

#### 1. Select ACH Direct Debit

The customer selects ACH Direct Debit at checkout.

#### 2. Sign in to bank account

The customer signs into their bank account to provide account information in a pop up window. On mobile, customers are redirected to the bank login. On desktop, bank login appears in a pop-up window.

#### 3. Accept mandate

The business presents the mandate. The customer accepts it by completing the purchase.

#### 4. Payment complete

The customer is redirected to the checkout once the payment is confirmed.

### Statement descriptors 

Every ACH Direct Debit payment shows up on customers’ bank statements with the name of the merchant. For payments created with Stripe, the name of the merchant is your Stripe account’s [statement descriptor](https://docs.stripe.com/get-started/account/statement-descriptors.md). You can override this default behavior for every transaction independently by using a [dynamic statement descriptor](https://docs.stripe.com/payments/payment-intents.md#dynamic-statement-descriptor). To do so, specify the [statement_descriptor](https://docs.stripe.com/api/payment_intents/create.md#create_payment_intent-statement_descriptor) parameter when creating the PaymentIntent.

> Your statement descriptor truncates to the first 16 alphanumeric characters on the bank statement. For example, if your statement descriptor is `ROCKETRIDESLIMITED`, the customer sees `ROCKETRIDESLIMIT`. Additionally, statement descriptors can’t use the special characters `<`, `>`, `'`, or `"`.

The following table illustrates the merchant name behavior you can expect on the customer’s bank statement:

| Default statement descriptor | Dynamic statement descriptor | Bank statement descriptor |
| --- | --- | --- |
| Rocket Rides | Unspecified | `Rocket Rides` |
| Rocket Rides | `Sunday Ride` | `Sunday Ride` |

Each bank formats these fields differently. Depending on your customer’s bank, some fields might appear in all lowercase or all uppercase.

When using [Connect](https://docs.stripe.com/connect.md), the charge type determines which Stripe account’s statement descriptor appears on the customer’s bank statement:

| Charge type | Descriptor taken from |
| --- | --- |
| Direct | Connected account |
| Destination | Platform |
| Separate charge and transfer | Platform |
| Destination (with `on_behalf_of`) | Connected account |
| Separate charge and transfer (with `on_behalf_of`) | Connected account |

## Enable ACH Direct Debit 

If you use our front-end products, you can enable ACH Direct Debit directly from your [payment method settings](https://dashboard.stripe.com/settings/payment_methods). Stripe then automatically determines the most relevant payment methods to display to your customers.

If your integration requires manually listing payment methods, learn how to [manually configure ACH Direct Debit as a payment](https://docs.stripe.com/payments/ach-direct-debit/accept-a-payment.md).
