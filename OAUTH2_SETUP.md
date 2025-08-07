# OAuth2 Integration Setup Guide

This guide will help you implement OAuth2 authentication for your Business Integration Dashboard, allowing secure access to user data across multiple business systems.

## 🔐 Overview

OAuth2 is implemented for the following services:
- **Salesforce** (CRM)
- **Shopify** (E-commerce)
- **HubSpot** (Marketing)
- **Slack** (Communication)
- **Calendly** (Scheduling)
- **Zendesk** (Support)

**Note**: Odoo (ERP) still uses traditional username/password authentication as it may not support OAuth2 in all configurations.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in your project root:

```env
# Flask Configuration
FLASK_SECRET_KEY=your-super-secret-key-change-this

# OAuth2 Redirect URI Base
OAUTH_REDIRECT_URI=http://localhost:8000/oauth/callback

# Salesforce
SALESFORCE_CLIENT_ID=your_salesforce_client_id
SALESFORCE_CLIENT_SECRET=your_salesforce_client_secret
SALESFORCE_SANDBOX=false

# Shopify
SHOPIFY_CLIENT_ID=your_shopify_client_id
SHOPIFY_CLIENT_SECRET=your_shopify_client_secret
SHOPIFY_SHOP_DOMAIN=your-shop.myshopify.com

# HubSpot
HUBSPOT_CLIENT_ID=your_hubspot_client_id
HUBSPOT_CLIENT_SECRET=your_hubspot_client_secret

# Slack
SLACK_CLIENT_ID=your_slack_client_id
SLACK_CLIENT_SECRET=your_slack_client_secret

# Calendly
CALENDLY_CLIENT_ID=your_calendly_client_id
CALENDLY_CLIENT_SECRET=your_calendly_client_secret

# Zendesk
ZENDESK_CLIENT_ID=your_zendesk_client_id
ZENDESK_CLIENT_SECRET=your_zendesk_client_secret
ZENDESK_SUBDOMAIN=your_zendesk_subdomain

# ERP (Odoo) - Traditional Auth
ERP_BASE_URL=http://your-odoo-instance.com
ERP_DB=your_database_name
ERP_USERNAME=your_username
ERP_PASSWORD=your_password
```

### 3. Run the OAuth2 Web Application

```bash
python oauth2_webapp.py
```

Visit http://localhost:8000 to authenticate with services.

### 4. Use the Integration

```python
from oauth2_integration import OAuth2APIConfig, OAuth2DashboardManager

# The configuration will be loaded from environment variables
config = OAuth2APIConfig()
dashboard = OAuth2DashboardManager(config)

# Check authentication status
auth_status = dashboard.get_authentication_status()
print(auth_status)

# Use authenticated services
if dashboard.crm.is_authenticated():
    leads = dashboard.crm.get_all_leads(limit=10)
    print(leads)
```

## 🔧 OAuth2 Application Setup

### Salesforce

1. **Create Connected App**:
   - Go to Setup → App Manager → New Connected App
   - Enable OAuth Settings
   - Callback URL: `http://localhost:8000/oauth/callback/salesforce`
   - Scopes: `api`, `refresh_token`, `offline_access`

2. **Get Credentials**:
   - Consumer Key → `SALESFORCE_CLIENT_ID`
   - Consumer Secret → `SALESFORCE_CLIENT_SECRET`

### Shopify

1. **Create App**:
   - Go to Partners Dashboard → Apps → Create App
   - App type: Public App
   - Callback URL: `http://localhost:8000/oauth/callback/shopify`

2. **Configure Scopes**:
   - `read_orders`, `write_orders`
   - `read_products`, `write_products`
   - `read_customers`, `write_customers`

3. **Get Credentials**:
   - Client ID → `SHOPIFY_CLIENT_ID`
   - Client Secret → `SHOPIFY_CLIENT_SECRET`

### HubSpot

1. **Create App**:
   - Go to Developer Portal → Create App
   - Redirect URL: `http://localhost:8000/oauth/callback/hubspot`

2. **Configure Scopes**:
   - `contacts`
   - `crm.objects.contacts.read`
   - `crm.objects.contacts.write`

3. **Get Credentials**:
   - App ID → `HUBSPOT_CLIENT_ID`
   - Client Secret → `HUBSPOT_CLIENT_SECRET`

### Slack

1. **Create App**:
   - Go to api.slack.com → Create New App
   - From scratch
   - Redirect URL: `http://localhost:8000/oauth/callback/slack`

2. **OAuth Scopes**:
   - `chat:write`
   - `channels:read`
   - `files:write`

3. **Get Credentials**:
   - Client ID → `SLACK_CLIENT_ID`
   - Client Secret → `SLACK_CLIENT_SECRET`

### Calendly

1. **Create App**:
   - Go to Calendly Developer Portal
   - Create New App
   - Redirect URI: `http://localhost:8000/oauth/callback/calendly`

2. **Get Credentials**:
   - Client ID → `CALENDLY_CLIENT_ID`
   - Client Secret → `CALENDLY_CLIENT_SECRET`

### Zendesk

1. **Create OAuth Client**:
   - Admin Center → Apps and integrations → APIs → OAuth Clients
   - Add OAuth Client
   - Redirect URL: `http://localhost:8000/oauth/callback/zendesk`

2. **Get Credentials**:
   - Unique identifier → `ZENDESK_CLIENT_ID`
   - Secret → `ZENDESK_CLIENT_SECRET`

## 📝 Usage Examples

### Basic Authentication Check

```python
from oauth2_integration import OAuth2APIConfig, OAuth2DashboardManager

config = OAuth2APIConfig()
dashboard = OAuth2DashboardManager(config)

# Check which services are authenticated
auth_status = dashboard.get_authentication_status()
for service, is_auth in auth_status.items():
    print(f"{service}: {'✅' if is_auth else '❌'}")
```

### CRM Operations

```python
# Create a lead (requires Salesforce authentication)
if dashboard.crm.is_authenticated():
    lead_data = {
        "FirstName": "John",
        "LastName": "Doe",
        "Company": "Acme Corp",
        "Email": "john@acme.com"
    }
    result = dashboard.crm.create_lead(lead_data)
    print(result)
else:
    print("Please authenticate Salesforce first")
    print(f"Auth URL: {dashboard.crm.get_authorization_url()}")
```

### E-commerce Operations

```python
# Get recent orders (requires Shopify authentication)
if dashboard.store.is_authenticated():
    orders = dashboard.store.get_orders(limit=10)
    print(f"Found {len(orders.get('data', {}).get('orders', []))} orders")
else:
    print("Please authenticate Shopify first")
```

### Marketing Operations

```python
# Create a contact (requires HubSpot authentication)
if dashboard.marketing.is_authenticated():
    contact_data = {
        "email": "jane@example.com",
        "firstname": "Jane",
        "lastname": "Smith"
    }
    result = dashboard.marketing.create_contact(contact_data)
    print(result)
```

### Slack Notifications

```python
# Send a message (requires Slack authentication)
if dashboard.slack.is_authenticated():
    dashboard.slack.send_message("#general", "Hello from OAuth2 integration!")
    dashboard.slack.send_alert("System status: All systems operational")
```

## 🔒 Security Best Practices

### 1. Secure Token Storage
- Store tokens securely (consider using a database or encrypted storage)
- Never commit tokens to version control
- Implement token rotation

### 2. Environment Variables
- Use strong, unique secrets
- Never expose credentials in code
- Use different credentials for development/production

### 3. HTTPS in Production
- Always use HTTPS for production OAuth2 flows
- Update redirect URIs to use HTTPS
- Implement proper SSL certificate validation

### 4. Token Management
- Implement automatic token refresh
- Handle token expiration gracefully
- Provide clear authentication status to users

## 🛠️ Troubleshooting

### Common Issues

1. **"Invalid redirect URI" error**:
   - Ensure redirect URI in OAuth app matches exactly
   - Check for trailing slashes
   - Verify HTTP vs HTTPS

2. **"Invalid client" error**:
   - Check client ID and secret are correct
   - Verify they're properly set in environment variables

3. **Token expiration**:
   - Tokens are automatically refreshed when possible
   - Re-authenticate if refresh token is missing

4. **Scope permissions**:
   - Ensure your OAuth app has required scopes
   - Check user has granted necessary permissions

### Debug Mode

Run with debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your integration code here
```

## 🚀 Production Deployment

### 1. Update Redirect URIs
Change redirect URIs in your OAuth apps to production URLs:
- Development: `http://localhost:8000/oauth/callback/{service}`
- Production: `https://yourdomain.com/oauth/callback/{service}`

### 2. Secure Environment Variables
- Use secure environment variable management
- Consider services like AWS Secrets Manager, Azure Key Vault, etc.

### 3. Database Storage
Consider storing tokens in a database instead of memory:

```python
# Example: Store tokens in database
class DatabaseTokenStorage:
    def store_token(self, service_name, token):
        # Store in your database
        pass
    
    def get_token(self, service_name):
        # Retrieve from database
        pass
```

### 4. Load Balancing
If using multiple instances, ensure token storage is shared across instances.

## 📚 API Reference

### OAuth2DashboardManager

- `get_authentication_status()` - Check auth status for all services
- `get_authorization_urls()` - Get OAuth2 auth URLs
- `complete_oauth2_flow(service, code, state)` - Complete OAuth2 flow
- `revoke_service_authentication(service)` - Revoke service auth

### Service Integrations

Each service integration has:
- `is_authenticated()` - Check if service is authenticated
- `get_authorization_url()` - Get OAuth2 authorization URL
- Service-specific methods (create_lead, get_orders, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new OAuth2 providers
4. Submit a pull request

---

For more detailed information, see the individual service documentation and OAuth2 specifications.
