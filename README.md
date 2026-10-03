https://rapidapi.com/studio/api_d157d033-5c8a-4516-8b1a-77b973df37de/publish/general




Isaac Rogelio Gonzlez Zavala

Port Lookup API
Port Lookup API is a lightweight REST API for querying port information programmatically.

It is designed for businesses, developers, and teams that need fast and reliable access to port data in logistics, shipping, import/export operations, and international trade workflows.

Features
REST API interface
JSON responses
API key authentication
Easy integration with web and mobile apps
Scalable architecture for production use
Clean documentation and examples
Use Cases
Logistics platforms
Freight and shipping systems
International trade tools
ERP and operational dashboards
Port and route data integrations
API Access
The API is available through secure authentication using an API key.

Example request:

curl -X GET "https://your-api-domain.com/api/ports?code=YOUR_API_KEY" \
  -H "Accept: application/json"
Example response:

{
  "status": "success",
  "data": {
    "id": "PORT-001",
    "name": "Port of Rotterdam",
    "country": "Netherlands",
    "region": "Europe",
    "code": "NLRTM"
  }
}
Pricing
SaaS Plans
Starter: $29 USD/month
Pro: $99 USD/month
Business: $599 MXN/month
Enterprise: Custom pricing
Commercial License
Commercial License: $499
Pro Commercial License: $1,499
Enterprise License: Custom pricing
Documentation
Endpoint examples and integration guides are available in the project documentation.

Support
Support is available for:

installation
deployment
authentication setup
custom integrations
production troubleshooting
License
This project is available under a commercial license. Contact the maintainer for licensing and commercial use details.

Contact
For business inquiries, custom integrations, or licensing:

Email: sales@yourcompany.com
Website: https://yourcompany.com

Stripe Billing Setup
--------------------

The checkout creates monthly subscriptions:

- Starter: $29 USD/month, 1,000 port lookups per billing cycle.
- Pro: $99 USD/month, 5,000 port lookups per billing cycle.
- Business: $599 MXN/month, 20,000 port lookups per billing cycle.

Configure these environment variables in Render (or your hosting provider):

- `STRIPE_SECRET_KEY`: Stripe secret API key.
- `STRIPE_WEBHOOK_SECRET`: signing secret for the webhook endpoint.
- `PUBLIC_BASE_URL`: public base URL of this API, for example
  `https://port-lookup-api-sb9w.onrender.com`.
- `DATABASE_URL`: persistent database URL. SQLite is suitable only when the
  host provides persistent disk storage.
- `ADMIN_KEY`: secret used by `/admin/stats`.

In Stripe, add a webhook pointing to
`https://<your-api-domain>/stripe-webhook` and subscribe it to:

- `checkout.session.completed`
- `checkout.session.async_payment_succeeded`
- `invoice.paid`
- `invoice.payment_failed`
- `customer.subscription.updated`
- `customer.subscription.deleted`

The static page starts checkout at `/checkout?plan=starter` or
`/checkout?plan=pro`. Stripe collects payment details and charges the first
monthly payment when the customer completes Checkout; the subscription saves
the payment method for automatic renewal charges. No charge is made merely by
visiting the checkout page. After payment, the confirmation endpoint returns
the subscription status and API Key. Renewal invoices reset the plan's monthly
query allowance; canceled, paused, or unpaid subscriptions disable their API
Key. Failed renewal payments are marked `past_due` while Stripe retries
payment.

To let a customer manage or cancel their subscription, enable the Stripe
Customer Portal in the Stripe Dashboard, then call `POST /billing-portal` with
their API key in the `X-API-Key` header. The response contains the portal URL.
