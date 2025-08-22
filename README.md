# Business Integration Dashboard API

A comprehensive Python-based integration platform that connects and manages multiple business systems including CRM, ERP, e-commerce, scheduling, learning management, marketing automation, and customer support tools. Now featuring **secure OAuth2 authentication** for industry-standard access to user data.

## 🌟 Features

- **Multi-System Integration**: Seamlessly connect to 8+ different business platforms
- **OAuth2 Authentication**: Secure, industry-standard authentication for all supported services
- **Unified API Management**: Single interface for managing all your business tools
- **Real-time Synchronization**: Keep customer data synchronized across all platforms
- **Dashboard Overview**: Get a complete status overview of all connected systems
- **Web-Based Authentication**: User-friendly web interface for OAuth2 flows
- **Automatic Token Management**: Handles token refresh and expiration automatically
- **Error Handling**: Robust error handling and logging for reliable operations
- **Slack Integration**: Real-time notifications and alerts via Slack
- **PKCE Security**: Enhanced OAuth2 security with Proof Key for Code Exchange
- **MCP / LLM Tooling**: Expose business operations as Model Context Protocol tools for LangGraph / LLM agents

## 🔧 Supported Integrations

### 1. CRM Integration (Salesforce) - OAuth2 ✅

- Create and manage leads
- Customer data management
- Opportunity tracking
- Task management
- Lead conversion
- **Authentication**: OAuth2 with automatic token refresh

### 2. ERP Integration (Odoo) - Traditional Auth ⚙️

- Inventory management
- Purchase order creation
- Sales order tracking
- Vendor management
- Stock level updates
- **Authentication**: Username/Password (legacy system)

### 3. E-commerce Integration (Shopify) - OAuth2 ✅

- Order management
- Product catalog management
- Inventory synchronization
- Customer management
- Discount code creation
- Order fulfillment
- **Authentication**: OAuth2 with store-specific permissions

### 4. Appointment Scheduling (Calendly) - OAuth2 ✅

- Event management
- Event type configuration
- Appointment cancellation
- Invitee management
- **Authentication**: OAuth2 with user consent

### 5. Learning Management System - API Key 🔑

- Student enrollment
- Course management
- Progress tracking
- Assignment creation
- **Authentication**: API Key or custom authentication

### 6. Marketing Automation (HubSpot) - OAuth2 ✅

- Contact management
- Campaign creation
- Email marketing
- Analytics and reporting
- List management
- **Authentication**: OAuth2 with granular scopes

### 7. Customer Support (Zendesk) - OAuth2 ✅

- Ticket management
- Customer support workflows
- User management
- Ticket search and filtering
- **Authentication**: OAuth2 with subdomain-specific access

### 8. Communication (Slack) - OAuth2 ✅

- Message sending
- Channel management
- File uploads
- Scheduled messages
- Alert notifications
- **Authentication**: OAuth2 with workspace permissions

## 🔐 Authentication Methods

This integration platform supports multiple authentication methods:

### **OAuth2 (Recommended)** 🛡️
- **Services**: Salesforce, Shopify, HubSpot, Slack, Calendly, Zendesk
- **Security**: Industry-standard with PKCE enhancement
- **User Experience**: Web-based consent flow
- **Token Management**: Automatic refresh and expiration handling

### **Traditional Authentication** ⚙️
- **Services**: Odoo/ERP (username/password)
- **Usage**: Legacy systems that don't support OAuth2

### **API Key Authentication** �
- **Services**: Custom LMS or other services
- **Usage**: Simple token-based authentication

## �📋 Prerequisites

Before running this application, ensure you have:

- Python 3.7 or higher
- Valid OAuth2 app credentials for the services you want to integrate
- Network access to the respective APIs
- (Optional) Web browser for OAuth2 authentication flows

## 🚀 Installation

### Option 1: OAuth2-Enabled Installation (Recommended)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd business-integration-dashboard
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

    (Optional) To enable full MCP protocol support (instead of fallback REPL) also install a compatible MCP server library (example placeholder):

    ```bash
    # Example (uncomment corresponding line in requirements.txt if you add a real library)
    # pip install mcp
    ```

3. **Set up OAuth2 environment variables**

   Create a `.env` file with your OAuth2 app credentials:

   ```env
   # Flask Configuration
   FLASK_SECRET_KEY=your-super-secret-key-change-this

   # OAuth2 Redirect URI Base
   OAUTH_REDIRECT_URI=http://localhost:8000/oauth/callback

   # Salesforce OAuth2
   SALESFORCE_CLIENT_ID=your_salesforce_client_id
   SALESFORCE_CLIENT_SECRET=your_salesforce_client_secret
   SALESFORCE_SANDBOX=false

   # Shopify OAuth2
   SHOPIFY_CLIENT_ID=your_shopify_client_id
   SHOPIFY_CLIENT_SECRET=your_shopify_client_secret
   SHOPIFY_SHOP_DOMAIN=your-shop.myshopify.com

   # HubSpot OAuth2
   HUBSPOT_CLIENT_ID=your_hubspot_client_id
   HUBSPOT_CLIENT_SECRET=your_hubspot_client_secret

   # Slack OAuth2
   SLACK_CLIENT_ID=your_slack_client_id
   SLACK_CLIENT_SECRET=your_slack_client_secret

   # Calendly OAuth2
   CALENDLY_CLIENT_ID=your_calendly_client_id
   CALENDLY_CLIENT_SECRET=your_calendly_client_secret

   # Zendesk OAuth2
   ZENDESK_CLIENT_ID=your_zendesk_client_id
   ZENDESK_CLIENT_SECRET=your_zendesk_client_secret
   ZENDESK_SUBDOMAIN=your_zendesk_subdomain

   # ERP (Traditional Auth)
   ERP_BASE_URL=http://your-odoo-instance.com
   ERP_DB=your_database_name
   ERP_USERNAME=your_username
   ERP_PASSWORD=your_password
   ```

4. **Set up OAuth2 applications**

   Follow the detailed setup guide in [`OAUTH2_SETUP.md`](OAUTH2_SETUP.md) to create OAuth2 applications for each service.

5. **Run the OAuth2 web application**

   ```bash
   python oauth2_webapp.py
   ```

   Visit http://localhost:8000 to authenticate with services.

### Option 2: Legacy Installation (API Keys/Tokens)

1. **Clone and install** (same as above)

2. **Set up legacy environment variables**

   ```env
   # CRM Configuration (Legacy)
   CRM_API_KEY=your_salesforce_api_key
   CRM_BASE_URL=https://api.salesforce.com

   # ERP Configuration
   ERP_API_KEY=your_odoo_api_key
   ERP_CLIENT_ID=your_odoo_client_id
   ERP_BASE_URL=your_odoo_base_url
   ERP_DB=your_odoo_database
   ERP_USERNAME=your_odoo_username
   ERP_PASSWORD=your_odoo_password

   # E-commerce Configuration (Legacy Tokens)
   SHOPIFY_ACCESS_TOKEN=your_shopify_token
   SHOPIFY_STORE_URL=your_shopify_store_url

   # Other services... (use legacy tokens)
   ```

## 📖 Usage

### 🤖 LLM / MCP Server Integration

This project ships with an optional **MCP server** (`mcp_server.py`) that exposes the dashboard’s capabilities as callable tools for Large Language Model agents (e.g. LangGraph, OpenAI Assistants with MCP client support).

#### What It Provides
| Tool | Purpose |
|------|---------|
| `get_dashboard_summary` | High-level system & auth status snapshot |
| `get_authentication_status` | Boolean auth flags per service |
| `get_authorization_urls` | URLs to start OAuth2 flows |
| `complete_oauth2_flow` | Exchanges code+state for tokens |
| `revoke_service_authentication` | Revokes stored token |
| `crm_create_lead` / `crm_get_leads` / `crm_convert_lead` | Salesforce CRM operations |
| `store_get_orders` | Shopify order retrieval |
| `marketing_get_contacts` | HubSpot contacts |
| `support_get_tickets` / `support_create_ticket` | Zendesk tickets |
| `appointments_get_events` | Calendly events |
| `erp_fetch_inventory` | Odoo inventory (legacy auth) |
| `slack_send_message` / `slack_send_alert` | Slack messaging |
| `introspect_tools` | List currently registered tools |

#### Running the MCP Server

```bash
python mcp_server.py
```

If a real MCP library is not installed, a lightweight JSON-line REPL is available. Type JSON requests like:

```json
{"tool": "get_authentication_status"}
```

Example OAuth2 initiation followed by token exchange (after user completed browser auth):

```json
{"tool": "get_authorization_urls"}
{"tool": "complete_oauth2_flow", "args": {"service_name": "salesforce", "authorization_code": "<code>", "state": "<state>"}}
```

#### Using with LangGraph (Conceptual Snippet)

```python
from some_mcp_client import MCPClient

client = MCPClient(command=["python", "mcp_server.py"])  # Launch server

auth_status = client.call_tool("get_authentication_status")
if not auth_status["salesforce"]:
    urls = client.call_tool("get_authorization_urls")
    print("Visit:", urls["salesforce"])  # Complete browser flow then continue

leads = client.call_tool("crm_get_leads", {"limit": 5})
print(leads)
```

#### Token Persistence
Tokens are cached to a JSON file (`.oauth_tokens.json` by default) so LLM / agent sessions can resume without re-authentication.

Configure a custom path via:
```env
OAUTH2_TOKEN_STORE=.secure_tokens/tokens.json
```

Security recommendations:
- Add the token store file to `.gitignore`
- Restrict filesystem permissions (700 / Windows equivalent)
- Consider encrypting at rest (future enhancement)

---

### OAuth2-Enabled Usage (Recommended)

```python
from oauth2_integration import OAuth2APIConfig, OAuth2DashboardManager

# Configuration loaded from environment variables
config = OAuth2APIConfig()
dashboard = OAuth2DashboardManager(config)

# Check authentication status
auth_status = dashboard.get_authentication_status()
print("Authentication Status:")
for service, is_authenticated in auth_status.items():
    status = "✅ Authenticated" if is_authenticated else "❌ Not Authenticated"
    print(f"  {service}: {status}")

# Get authorization URLs for unauthenticated services
if not dashboard.crm.is_authenticated():
    print(f"Authenticate Salesforce: {dashboard.crm.get_authorization_url()}")

# Use authenticated services (same interface as before!)
if dashboard.crm.is_authenticated():
    leads = dashboard.crm.get_all_leads(limit=10)
    print(f"Found {len(leads.get('data', {}).get('records', []))} leads")

# System status with authentication info
summary = dashboard.get_dashboard_summary()
print(summary)
```

### Legacy Usage (API Keys/Tokens)

```python
from FirstBluePrint import APIConfig, DashboardManager

# Configure API credentials manually
config = APIConfig(
    crm_api_key="your_crm_key",
    erp_api_key="your_erp_key",
    # ... other legacy credentials
    shopify_access_token="your_shopify_token",
    shopify_store_url="your_shopify_url",
    calendly_access_token="your_calendly_token",
    learning_access_token="your_lms_token",
    learning_base_url="your_lms_url",
    hubspot_access_token="your_hubspot_token",
    zendesk_access_token="your_zendesk_token",
    zendesk_subdomain="your_zendesk_subdomain",
    zendesk_email="your_zendesk_email"
)

# Initialize dashboard manager
dashboard = DashboardManager(config)

# Get system status overview
summary = dashboard.get_dashboard_summary()
print(summary)
```

### Web Interface Usage

For easy OAuth2 authentication, run the web interface:

```bash
python oauth2_webapp.py
```

Then visit `http://localhost:8000` to:
- See authentication status for all services
- Authenticate with each service using OAuth2  
- View connection health and system overview
- Access API endpoints through web interface

### Programmatic OAuth2 Flow

```python
from oauth2_auth import OAuth2Manager

# Initialize OAuth2 manager
oauth2_manager = OAuth2Manager()

# Get authorization URL for a service
auth_url = oauth2_manager.get_authorization_url('salesforce')
print(f"Visit: {auth_url}")

# After user visits URL and gets code, exchange for tokens
tokens = oauth2_manager.exchange_code_for_tokens(
    service='salesforce',
    authorization_code='received_code',
    code_verifier='your_verifier'  # Store this from get_authorization_url call
)

# Tokens are automatically stored for future use
```

## 🔧 Service Configuration

Each service requires specific OAuth2 configuration. See [OAUTH2_SETUP.md](OAUTH2_SETUP.md) for detailed setup instructions.

### Quick Configuration Example

```python
from oauth2_auth import ServiceOAuth2Configs

# Get configuration for a service
salesforce_config = ServiceOAuth2Configs.get_config('salesforce')
print(f"Authorization URL: {salesforce_config['auth_url']}")
print(f"Required Scopes: {salesforce_config['scopes']}")

# Check if service supports OAuth2
services = ServiceOAuth2Configs.get_supported_services()
print(f"OAuth2 Supported: {services}")
```

### CRM Operations

```python
# Create a new lead
lead_data = {
    "FirstName": "John",
    "LastName": "Doe", 
    "Company": "Acme Corp",
    "Email": "john.doe@acme.com"
}
result = dashboard.crm.create_lead(lead_data)

# Get customer data
customer = dashboard.crm.get_customer_data("customer_id")

# Get all leads
leads = dashboard.crm.get_all_leads(limit=50)

# Convert lead to opportunity
conversion = dashboard.crm.convert_lead("lead_id")

# Create a task
task_data = {
    "Subject": "Follow up call",
    "WhoId": "contact_id"
}
task = dashboard.crm.create_task(task_data)
```

### ERP Operations

```python
# Fetch inventory
inventory = dashboard.erp.fetch_inventory(item_name="Product Name")

# Create purchase order
order_data = {
    "partner_id": 123,
    "order_line": [
        {"product_id": 456, "quantity": 10, "price_unit": 50.0}
    ]
}
result = dashboard.erp.create_purchase_order(order_data)

# Get sales orders
sales_orders = dashboard.erp.get_sales_orders(state="draft")

# Update inventory
inventory_update = dashboard.erp.update_inventory(product_id=456, new_quantity=100)

# Get vendors
vendors = dashboard.erp.get_vendors()
```

### E-commerce Operations

```python
# Get orders
orders = dashboard.store.get_orders(status="pending", limit=25)

# Get products
products = dashboard.store.get_products(published_status="published")

# Update product inventory
result = dashboard.store.update_product_inventory("variant_id", 100)

# Create discount code
discount_data = {
    "code": "SAVE20",
    "value": 20,
    "value_type": "percentage"
}
result = dashboard.store.create_discount_code(discount_data)

# Fulfill order
fulfillment = dashboard.store.fulfill_order("order_id", tracking_number="123456")
```

### Appointment Scheduling

```python
# Get events
events = dashboard.appointments.get_events(count=10)

# Get event types
event_types = dashboard.appointments.get_event_types()

# Cancel event
cancellation = dashboard.appointments.cancel_event("event_uuid", reason="Reschedule needed")

# Get invitees
invitees = dashboard.appointments.get_invitees("event_uuid")
```

### Learning Management

```python
# Get students
students = dashboard.learning.get_students(course_id="course_123")

# Get courses
courses = dashboard.learning.get_courses(published_only=True)

# Enroll student
enrollment = dashboard.learning.enroll_student("student_id", "course_id")

# Get progress
progress = dashboard.learning.get_student_progress("student_id", "course_id")

# Create assignment
assignment_data = {
    "title": "Week 1 Assignment",
    "course_id": "course_123",
    "due_date": "2025-08-15"
}
assignment = dashboard.learning.create_assignment(assignment_data)
```

### Marketing Operations

```python
# Get contacts
contacts = dashboard.marketing.get_contacts(limit=100)

# Create contact
contact_data = {
    "email": "new@customer.com",
    "firstname": "New",
    "lastname": "Customer"
}
contact = dashboard.marketing.create_contact(contact_data)

# Create campaign
campaign_data = {
    "name": "Summer Sale Campaign",
    "type": "EMAIL"
}
campaign = dashboard.marketing.create_campaign(campaign_data)

# Get analytics
analytics = dashboard.marketing.get_analytics(object_type="contacts", time_range="30d")
```

### Support Operations

```python
# Get tickets
tickets = dashboard.support.get_tickets(status="open", priority="high")

# Create ticket
ticket_data = {
    "subject": "Product inquiry",
    "comment": "Customer needs help with setup"
}
ticket = dashboard.support.create_ticket(ticket_data)

# Update ticket
update_data = {"status": "pending"}
update = dashboard.support.update_ticket("ticket_id", update_data)

# Add comment
comment = dashboard.support.add_ticket_comment("ticket_id", "Following up on this issue")

# Search tickets
search_results = dashboard.support.search_tickets("login issues")
```

### Slack Integration

```python
# Send a message
dashboard.slack.send_message("#general", "Hello team!")

# Send an alert
dashboard.slack.send_alert("System maintenance scheduled", urgent=True)

# Create channel
channel = dashboard.slack.create_channel("project-updates")

# Upload a file
file_upload = dashboard.slack.upload_file("/path/to/file.pdf", "#general", "Monthly Report")

# Schedule message
import time
future_time = int(time.time()) + 3600  # 1 hour from now
scheduled = dashboard.slack.schedule_message("#general", "Reminder: Meeting in 1 hour", future_time)
```

### Customer Data Synchronization

```python
# Sync customer data across all platforms
sync_result = dashboard.sync_customer_data("customer@example.com")
print(sync_result)
```

## 🏗️ Architecture

### OAuth2-Enhanced Architecture

The platform now supports both OAuth2 and legacy authentication methods with a three-layer architecture:

#### Layer 1: OAuth2 Authentication Engine (`oauth2_auth.py`)
- **OAuth2Manager**: Core OAuth2 protocol implementation with PKCE security
- **OAuth2Token**: Token storage and automatic refresh management
- **ServiceOAuth2Configs**: Pre-configured OAuth2 settings for all supported services
- Handles authorization flows, token exchanges, and credential storage

#### Layer 2: Business Integration Layer (`oauth2_integration.py`)
- **OAuth2BaseIntegration**: Enhanced base class with OAuth2 authentication
- **OAuth2CRMIntegration**, **OAuth2ERPIntegration**, etc.: Service-specific implementations
- **OAuth2DashboardManager**: Unified dashboard with OAuth2 capabilities
- Maintains same API interface as legacy classes for backward compatibility

#### Layer 3: Web Interface (`oauth2_webapp.py`)
- **Flask web application**: User-friendly OAuth2 authentication interface
- **Dashboard routes**: Authentication status, service management, API testing
- **OAuth2 callback handling**: Secure authorization code exchange
- **System overview**: Real-time connection status and health monitoring

### Legacy Architecture

```
DashboardManager (FirstBluePrint.py)
├── CRMIntegration (Salesforce)
├── ERPIntegration (Odoo)
├── OnlineStoreIntegration (Shopify)
├── AppointmentTools (Calendly)
├── LearningTools (LMS)
├── MarketingTools (HubSpot)
├── SupportTools (Zendesk)
└── SlackIntegration (Slack)
```

### Base Integration Class

All integrations inherit from `BaseIntegration` which provides:

- HTTP request handling with error management
- Field validation utilities
- Session management
- Consistent error responses

## 🔒 OAuth2 User Data Access Flow

### How OAuth2 Enables Secure User Data Access

With OAuth2 implementation, users can securely grant your application access to their data across all integrated systems **without sharing their passwords**:

1. **User Authentication Request**: User clicks "Connect [Service]" in your app
2. **Redirect to Service**: User is redirected to the service's official login page (e.g., Salesforce, Shopify)
3. **User Grants Permission**: User logs in with their own credentials and grants specific permissions
4. **Secure Token Exchange**: Service redirects back with authorization code, app exchanges it for access tokens
5. **Data Access**: App can now access user's data in that service using the token
6. **Automatic Refresh**: Tokens are automatically refreshed to maintain access

### Benefits for Users

- **No Password Sharing**: Users never give their passwords to your app
- **Granular Permissions**: Users control exactly what data your app can access
- **Revocable Access**: Users can revoke access anytime from their service settings
- **Secure**: Industry-standard security with PKCE enhancement
- **Transparent**: Users see exactly what permissions are being requested

### Example User Experience

```python
# User workflow with OAuth2
dashboard = OAuth2DashboardManager(config)

# Check what services need user authentication
auth_status = dashboard.get_authentication_status()
for service, authenticated in auth_status.items():
    if not authenticated:
        print(f"User needs to authenticate with {service}")
        # User visits the authorization URL to grant access
        auth_url = getattr(dashboard, service).get_authorization_url()
        print(f"Visit: {auth_url}")

# Once authenticated, access user's data seamlessly
if dashboard.crm.is_authenticated():
    # Access user's Salesforce data
    user_leads = dashboard.crm.get_all_leads()
    
if dashboard.store.is_authenticated():
    # Access user's Shopify store data
    user_orders = dashboard.store.get_orders()
```

## 📊 User Data Access Capabilities

Once users authenticate through OAuth2, your application can access their data across all registered systems:

### What Users Can Access Through Your App

| Service | User Data Available | Permissions Required |
|---------|-------------------|---------------------|
| **Salesforce CRM** | Leads, Contacts, Opportunities, Tasks, Accounts | `api`, `refresh_token` |
| **Shopify Store** | Orders, Products, Customers, Inventory, Analytics | `read_orders`, `read_products`, `write_inventory` |
| **HubSpot Marketing** | Contacts, Companies, Deals, Email Campaigns | `contacts`, `content` |
| **Slack Workspace** | Channels, Messages, Files, Team Members | `channels:read`, `chat:write`, `files:write` |
| **Calendly Scheduling** | Events, Event Types, Invitees, Availability | `read`, `write` |
| **Zendesk Support** | Tickets, Users, Organizations, Knowledge Base | `read`, `write` |

### User Control & Privacy

- **Granular Permissions**: Users choose exactly what data to share
- **Real-time Revocation**: Users can disconnect any service instantly
- **Audit Trail**: All API calls are logged for transparency
- **Data Ownership**: Users retain full ownership of their data
- **No Data Storage**: App accesses data in real-time, doesn't store personal data

### Multi-User Support

```python
# Each user gets their own authenticated session
user1_dashboard = OAuth2DashboardManager(user1_config)
user2_dashboard = OAuth2DashboardManager(user2_config)

# Users can access their own data independently
user1_leads = user1_dashboard.crm.get_all_leads()  # User 1's Salesforce data
user2_orders = user2_dashboard.store.get_orders()  # User 2's Shopify data
```

## 🔒 Security Best Practices

### OAuth2 Security
- **PKCE Implementation**: Enhanced security with Proof Key for Code Exchange
- **Secure Token Storage**: Tokens encrypted and stored securely
- **Automatic Token Refresh**: Prevents expired token issues
- **Scope Limitation**: Request only necessary permissions from users
- **State Parameter**: Prevents CSRF attacks during OAuth2 flow

### General Security
- Store OAuth2 app credentials securely using environment variables
- Use HTTPS for all API communications and OAuth2 redirects
- Implement proper authentication for each service
- Regularly rotate OAuth2 app secrets
- Monitor API usage and access logs
- Never commit credentials to version control
- Validate all OAuth2 callback parameters

## 📊 Monitoring & Logging

The application includes comprehensive logging:

```python
import logging

# Configure logging level
logging.basicConfig(level=logging.INFO)

# Access logs
logger = logging.getLogger(__name__)
```

## 🛠️ Error Handling

Each integration includes robust error handling:

- **Connection Errors**: Automatic retry mechanisms
- **Authentication Errors**: Clear error messages for credential issues
- **Rate Limiting**: Proper handling of API rate limits
- **Data Validation**: Field validation before API calls

## 📝 API Rate Limits

Be aware of rate limits for each service:

- **Salesforce**: 1,000 calls per hour (varies by plan)
- **Shopify**: 2 calls per second
- **HubSpot**: 100 calls per 10 seconds
- **Zendesk**: 700 requests per minute
- **Slack**: 1+ requests per minute per channel
- **Calendly**: 100 requests per minute

## 🔄 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-integration`)
3. Commit your changes (`git commit -am 'Add new integration'`)
4. Push to the branch (`git push origin feature/new-integration`)
5. Create a Pull Request

## 🧪 Testing

To test the integrations:

```python
# Test dashboard summary
summary = dashboard.get_dashboard_summary()
for system, status in summary["systems"].items():
    print(f"{system}: {status['status']}")
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:

- Create an issue in the repository
- Check the documentation for each integrated service
- Review the error logs for troubleshooting

## 🔮 Future Enhancements

- [ ] Add more e-commerce platforms (WooCommerce, Magento)
- [ ] Implement webhook support for real-time updates
- [ ] Add data analytics and reporting dashboard
- [ ] Create web-based configuration interface
- [ ] Add support for custom integrations
- [ ] Implement automated testing suite
- [ ] Add backup and recovery mechanisms
- [ ] Create Docker containerization
- [ ] Add GraphQL API support

## 📚 Dependencies

### Core Dependencies

- `requests` - HTTP library for API calls  
- `python-dotenv` - Environment variable management
- `xmlrpc.client` - XML-RPC client for Odoo integration

### OAuth2 Dependencies

- `flask` - Web framework for OAuth2 callback handling
- `secrets` - Secure token generation for PKCE
- `hashlib` - SHA256 hashing for PKCE code challenges
- `base64` - URL-safe encoding for OAuth2 parameters
- `urllib.parse` - URL parameter encoding/decoding

### Service-Specific Dependencies

- `slack-sdk` - Official Slack SDK for Python (optional, can use requests)

### Optional Dependencies

- `cryptography` - Enhanced security for token storage
- `keyring` - Secure credential storage (future enhancement)
- `mcp` - (Optional) Real MCP protocol implementation for `mcp_server.py`

---

**Note**: This integration platform requires valid API credentials for each service you wish to connect. Ensure you have the necessary permissions and API access before implementation.

## 🚀 Quick Start Example

```python
from FirstBluePrint import APIConfig, DashboardManager

# Minimal configuration for testing
config = APIConfig(
    crm_api_key="test_key",
    erp_api_key="test_key", 
    erp_client_id="test_id",
    erp_base_url="http://localhost:8069",
    erp_db="test_db",
    erp_username="admin",
    erp_password="admin",
    slack_bot_token="xoxb-test-token",
    shopify_access_token="test_token",
    shopify_store_url="https://test-store.myshopify.com",
    calendly_access_token="test_token",
    learning_access_token="test_token",
    learning_base_url="https://test-lms.com",
    hubspot_access_token="test_token",
    zendesk_access_token="test_token",
    zendesk_subdomain="test",
    zendesk_email="admin@test.com"
)

dashboard = DashboardManager(config)
print("Dashboard initialized successfully!")
```
