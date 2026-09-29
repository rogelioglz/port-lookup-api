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
Starter: $29/month
Pro: $99/month
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
