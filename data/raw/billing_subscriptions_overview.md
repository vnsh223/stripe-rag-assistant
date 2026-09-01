Source: https://docs.stripe.com/billing/subscriptions/overview

# How subscriptions work

Manage recurring payments and subscription lifecycles.

Subscriptions let customers make recurring payments to access a product or service. When you create a subscription, Stripe automatically generates invoices, attempts payment collection, and manages the subscription status throughout its lifecycle. A subscription moves through a predictable set of states, from creation to cancellation.

Unlike one-time payments, subscriptions require storing customer and payment method information for future billing cycles. Stripe handles the payment retry logic, dunning, and status transitions.

## Subscription lifecycle 

Each of the following subscription lifecycle phases maps to a status change on the [Subscription object](https://docs.stripe.com/api/subscriptions/object.md). Understanding these statuses helps you know when to provision access, notify customers, and handle errors. You can use [webhook events](https://docs.stripe.com/billing/subscriptions/webhooks.md#state-changes) to monitor and handle transitions between statuses.

### Create the subscription

Create a new subscription in the [Dashboard](https://dashboard.stripe.com/subscriptions?status=active) or with the [Subscriptions API](https://docs.stripe.com/api/subscriptions/create.md). The resulting [Subscription object](https://docs.stripe.com/api/subscriptions/object.md) contains the subscribed customer, [product](https://docs.stripe.com/api/products.md), and [price](https://docs.stripe.com/api/prices/object.md), and the `status` reflecting the subscription’s current lifecycle state.

When you create a subscription that requires an immediate payment, Stripe also creates an [Invoice](https://docs.stripe.com/billing/invoices/subscription.md) and a [PaymentIntent](https://docs.stripe.com/payments/payment-intents.md). The subscription’s initial status is `incomplete`, then becomes `active` after the customer pays the first invoice.

> Payment methods with *delayed* (A payment method that can't immediately return payment status when a customer attempts a transaction (for example, ACH debits). Businesses commonly hold an order in a pending state until payment is successful with these payment methods) payment confirmation timing, such as ACH Direct Debit, might have a different status. For more details, see [Delayed payment confirmation](https://docs.stripe.com/billing/subscriptions/overview.md#delayed-payment-confirmation).

Default subscription payment collection and failure handling depends on the payment method. In the API, you can configure a subscription’s [payment_behavior](https://docs.stripe.com/api/subscriptions/create.md#create_subscription-payment_behavior) to override the default.

If you create a [trial period](https://docs.stripe.com/billing/subscriptions/trials.md) to delay the first charge for the subscription, the initial status is `trialing`, and the subscription automatically transitions to `active` when the trial ends and payment succeeds.

### Handle the invoice

For subscriptions with `collection_method` set to `charge_automatically`, Stripe creates an [invoice](https://docs.stripe.com/billing/invoices/subscription.md) with the status `open` when you create the subscription. Your customer has 23 hours to pay. During this time, the subscription status is `incomplete` and the invoice status remains `open`. This 23-hour window accommodates customers who pay while *on-session* (A payment is described as on-session if it occurs while the customer is actively in your checkout flow and able to authenticate the payment method). If the customer returns to your application after 23 hours, create a new subscription for them.

For subscriptions with `collection_method` set to `send_invoice`, Stripe emails the customer a link to the invoice with a configurable due date. The subscription remains `incomplete` until the customer pays.

To learn more, see [Subscription invoices](https://docs.stripe.com/billing/invoices/subscription.md).

### Confirm payment

If your customer pays the invoice, the subscription updates to `active` and the invoice to `paid`. Listen for the [invoice.paid](https://docs.stripe.com/billing/subscriptions/webhooks.md#events) event or confirm that the subscription status is `active`.

If the customer doesn’t pay within 23 hours, the subscription updates to `incomplete_expired` and the invoice becomes `void`. To reactivate their access, create a new subscription.

For more details, see [Subscription statuses](https://docs.stripe.com/billing/subscriptions/overview.md#subscription-statuses) and [Payment statuses](https://docs.stripe.com/billing/subscriptions/overview.md#payment-status).

### Provision access to your product 

When a subscription becomes `active`, Stripe creates an active [entitlement](https://docs.stripe.com/billing/entitlements.md) for each feature associated with the subscribed product. When a customer accesses your services, use their active entitlements to grant them access to the features included in their subscription.

Alternatively, [track active subscriptions](https://docs.stripe.com/billing/subscriptions/webhooks.md#active-subscriptions) with webhook events and provision the product for the customer based on that activity.

### Update the subscription

You can [modify existing subscriptions](https://docs.stripe.com/billing/subscriptions/change.md) as needed without having to cancel and recreate them. Some of the most significant changes you might make are [upgrading or downgrading](https://docs.stripe.com/billing/subscriptions/change-price.md) the subscription price or [pausing payment collection](https://docs.stripe.com/billing/subscriptions/pause-payment.md) for an active subscription.

For [Stripe Checkout](https://docs.stripe.com/payments/checkout.md) integrations, you can’t update the subscription or its invoice if the session’s subscription is `incomplete`. You can listen to the [checkout.session.completed](https://docs.stripe.com/api/events/types.md#event_types-checkout.session.completed) event to make the update after the session has completed. You can also [expire the session](https://docs.stripe.com/api/checkout/sessions/expire.md) instead if you want to cancel the session’s subscription, void the subscription invoice, or mark the invoice as uncollectible.

### Handle unpaid subscriptions 

If the customer doesn’t pay a subscription invoice, Stripe pauses further collection attempts. The subscription continues to generate invoices each billing period, which remain in `draft` status. The subscription’s status (`past_due` or `unpaid`) depends on your [failed payment settings](https://dashboard.stripe.com/settings/billing/automatic#manage-failed-payments) in the Dashboard.

Voided invoices don’t affect subscription status. Stripe determines the status from the most recent non-voided invoice. To learn more, see [Failed subscription payments](https://docs.stripe.com/billing/collection-method.md#failed-subscription-payments).

### Cancel the subscription 

You can [cancel](https://docs.stripe.com/billing/subscriptions/cancel.md) a subscription at any time, including at the [end of a billing cycle](https://docs.stripe.com/billing/subscriptions/cancel.md#cancel-at-the-end-of-the-current-billing-period) or after a [set number of billing cycles](https://docs.stripe.com/billing/subscriptions/cancel.md#subscription-schedules).

By default, canceling a subscription disables creating new invoices and [stops automatic collection](https://docs.stripe.com/billing/subscriptions/cancel.md#handle-invoice-items-when-canceling-subscriptions) of all outstanding invoices from the subscription. It also deletes the subscription and you can no longer update it except for its [metadata](https://docs.stripe.com/metadata.md) and `cancellation_details`. If your customer wants to resubscribe, you need to collect new payment information from them and create a new subscription.

## Subscription statuses 

Subscriptions can have the following statuses. The actions you can take on a subscription depend on its status.

| Status | Description |
| --- | --- |
| `trialing` | The subscription is currently in a trial period and you can safely provision your product for your customer. The subscription transitions automatically to `active` when a customer makes the first payment. |
| `active` | The subscription is in good standing. For `past_due` subscriptions, paying the latest associated invoice or marking it uncollectible transitions the subscription to `active`.

`active` doesn’t indicate that all outstanding invoices associated with the subscription have been paid. You can leave other outstanding invoices open for payment, mark them as uncollectible, or void them as you see fit. |
| `incomplete` | The customer must make a successful payment within 23 hours to activate the subscription. Or the payment [requires action](https://docs.stripe.com/billing/subscriptions/overview.md#requires-action), such as customer authentication. Subscriptions can also be `incomplete` if there’s a pending payment and the PaymentIntent status is `processing`. |
| `incomplete_expired` | The initial payment on the subscription failed and the customer didn’t make a successful payment within 23 hours of subscription creation. These subscriptions don’t bill customers. This status exists so you can track customers that failed to activate their subscriptions. |
| `past_due` | Payment on the latest *finalized* invoice either failed or wasn’t attempted. The subscription continues to create invoices. Your Dashboard [subscription settings](https://dashboard.stripe.com/settings/billing/automatic) determine the subscription’s next status. If the invoice is still unpaid after all attempted [smart retries](https://docs.stripe.com/billing/revenue-recovery/smart-retries.md), you can configure the subscription to move to `canceled`, `unpaid`, or leave it as `past_due`.

To reactivate the subscription, have your customer pay the most recent invoice. The subscription status becomes `active` regardless of whether the payment is done before or after the latest invoice due date. |
| `canceled` | The subscription was canceled. During cancellation, automatic collection for all unpaid invoices is disabled (`auto_advance=false`). This is a terminal state that can’t be updated. |
| `unpaid` | The latest invoice hasn’t been paid but the subscription remains in place. The latest invoice remains open and invoices continue to generate, but payments aren’t attempted. Revoke access to your product when the subscription is `unpaid` because payments were already attempted and retried while `past_due`. To move the subscription to `active`, pay the most recent invoice before its due date. |
| `paused` | The subscription has ended its trial period without a default payment method and the [trial_settings.end_behavior.missing_payment_method](https://docs.stripe.com/billing/subscriptions/trials/free-trials.md#create-free-trials-without-payment) is set to `pause`. Invoices are no longer created for the subscription. After attaching a default payment method to the customer, you can [resume the subscription](https://docs.stripe.com/billing/subscriptions/trials/free-trials.md#resume-a-paused-subscription). |

## Payment statuses 

A [PaymentIntent](https://docs.stripe.com/payments/payment-intents.md) tracks the lifecycle of every payment. Whenever a payment is due for a subscription, Stripe generates an [invoice](https://docs.stripe.com/billing/invoices/subscription.md) and a PaymentIntent. The PaymentIntent ID attaches to the invoice and you can access it from the Invoice and Subscription objects.

The status of the PaymentIntent affects the status of the invoice and the subscription. Here’s how the different outcomes of a payment map to the different statuses:

| Payment outcome | PaymentIntent status | Invoice status | Subscription status |
| --- | --- | --- | --- |
| Success | `succeeded` | `paid` | `active` |
| Fails because of a card error | `requires_payment_method` | `open` | `incomplete` |
| Fails because of authentication | `requires_action` | `open` | `incomplete` |

### Payment methods with delayed payment confirmation 

Payment methods that can’t immediately return payment status when a customer attempts a transaction (for example, ACH Direct Debit) handle subscription status transitions differently. When you use these types of payment methods, a subscription can move directly to `active` after creation and bypass `incomplete`. If the payment fails later, Stripe voids the invoice but the subscription remains `active`. Use this behavior when you design your access control and retry logic.

The following sections explain these statuses and the actions to take for each.

### Payment succeeded 

When the customer’s payment is successful:

- The `status` of the PaymentIntent moves to `succeeded`.
- The `status` of the subscription is `active`.
- The `status` of the invoice is `paid`.
- Stripe sends an `invoice.paid` event to your configured webhook endpoints.

For [payment methods](https://docs.stripe.com/payments/payment-methods/integration-options.md) with longer processing periods, subscriptions are immediately activated. In these cases, the status of the PaymentIntent might be `processing` for an `active` subscription until the payment succeeds.

With your subscription now activated, [provision access](https://docs.stripe.com/billing/subscriptions/overview.md#provision-access) to your product.

### Requires payment method 

If payment fails because of a [card error](https://docs.stripe.com/api/errors.md#errors-card_error) such as a [decline](https://docs.stripe.com/declines.md#issuer-declines):

- The `status` of the PaymentIntent is `requires_payment_method`.
- The `status` of the subscription is `incomplete`.
- The `status` of the invoice is `open`.

To handle these scenarios:

- Notify the customer.
- Collect new payment information and [confirm the PaymentIntent](https://docs.stripe.com/api/payment_intents/confirm.md).
- Update the [default payment method](https://docs.stripe.com/api/subscriptions/object.md#subscription_object-default_payment_method) on the subscription.
- Stripe re-attempts payment using [Smart Retries](https://docs.stripe.com/invoicing/automatic-collection.md#smart-retries) or based on your custom [retry rules](https://dashboard.stripe.com/account/billing/automatic).
- Use the [invoice.payment_failed](https://docs.stripe.com/billing/revenue-recovery/smart-retries.md#invoice-payment-failed-webhook) event to monitor subscription payment failure events and retry attempt updates. After a payment attempt on an invoice, its [next_payment_attempt](https://docs.stripe.com/api.md#invoice_object-next_payment_attempt) value is set using the current subscription settings in your Dashboard.

Learn how to [handle payment failures for subscriptions](https://docs.stripe.com/billing/subscriptions/webhooks.md#payment-failures).

### Handle failed recurring payments 

When a recurring subscription payment fails, listen for `invoice.payment_failed`. [Monitor subscription status changes](https://docs.stripe.com/billing/subscriptions/webhooks.md#state-changes) to detect transitions to `past_due` or `unpaid`. Notify the customer so they can update their payment method or pay the open invoice. [Verify webhook signatures](https://docs.stripe.com/webhooks.md#verify-events) before you process events.

Configure [Smart Retries or custom retry rules](https://docs.stripe.com/billing/revenue-recovery/smart-retries.md) to retry failed payments. In your [failed payment settings](https://dashboard.stripe.com/settings/billing/automatic), choose what happens to the subscription after the final retry. Use the [subscription status table](https://docs.stripe.com/billing/subscriptions/overview.md#subscription-statuses) to determine when to revoke access and how to reactivate `past_due` and `unpaid` subscriptions. See [Failed recurring charges](https://docs.stripe.com/billing/collection-method.md#handle-recurring-charge-failures) for more details.

### Requires action 

Some payment methods require customer authentication with [3D Secure](https://docs.stripe.com/payments/3d-secure.md) (3DS). Whether authentication is required depends on your [Radar rules](https://docs.stripe.com/payments/3d-secure/authentication-flow.md#three-ds-radar) and the issuing bank for the card.

If payment fails because the customer needs to authenticate a payment:

- The `status` of the PaymentIntent is `requires_action`.
- The `status` of the subscription is `incomplete`.
- The `status` of the invoice is `open`.

To handle these scenarios:

- Monitor for the `invoice.payment_action_required` event notification with [webhook endpoints](https://docs.stripe.com/billing/subscriptions/webhooks.md). This indicates that authentication is required.
- Notify your customer that they must authenticate. Retrieve the PaymentIntent’s client secret and pass it to [stripe.handleNextAction](https://docs.stripe.com/js/payment_intents/handle_next_action). This guides the customer through any required steps and returns the result to your application.
- Monitor the `invoice.paid` event on your event destination to verify that the payment succeeded. Users can leave your application before `handleNextAction()` finishes. Verifying whether the payment succeeded allows you to correctly provision your product.

## See also

- [Design a subscriptions integration](https://docs.stripe.com/billing/subscriptions/design-an-integration.md)
- [Build a subscriptions integration](https://docs.stripe.com/billing/subscriptions/build-subscriptions.md)
- [Subscriptions quickstart](https://docs.stripe.com/billing/quickstart.md)
