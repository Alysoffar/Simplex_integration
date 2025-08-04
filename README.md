# Business Integration Dashboard API

A comprehensive Python-based integration platform that connects and manages multiple business systems including CRM, ERP, e-commerce, scheduling, learning management, marketing automation, and customer support tools.

## 🌟 Features

- **Multi-System Integration**: Seamlessly connect to 8+ different business platforms
- **Unified API Management**: Single interface for managing all your business tools
- **Real-time Synchronization**: Keep customer data synchronized across all platforms
- **Dashboard Overview**: Get a complete status overview of all connected systems
- **Error Handling**: Robust error handling and logging for reliable operations
- **Slack Integration**: Real-time notifications and alerts via Slack

## 🔧 Supported Integrations

### 1. CRM Integration (Salesforce)

- Create and manage leads
- Customer data management
- Opportunity tracking
- Task management
- Lead conversion

### 2. ERP Integration (Odoo)

- Inventory management
- Purchase order creation
- Sales order tracking
- Vendor management
- Stock level updates

### 3. E-commerce Integration (Shopify)

- Order management
- Product catalog management
- Inventory synchronization
- Customer management
- Discount code creation
- Order fulfillment

### 4. Appointment Scheduling (Calendly)

- Event management
- Event type configuration
- Appointment cancellation
- Invitee management

### 5. Learning Management System

- Student enrollment
- Course management
- Progress tracking
- Assignment creation

### 6. Marketing Automation (HubSpot)

- Contact management
- Campaign creation
- Email marketing
- Analytics and reporting
- List management

### 7. Customer Support (Zendesk)

- Ticket management
- Customer support workflows
- User management
- Ticket search and filtering

### 8. Communication (Slack)

- Message sending
- Channel management
- File uploads
- Scheduled messages
- Alert notifications

## 📋 Prerequisites

Before running this application, ensure you have:

- Python 3.7 or higher
- Valid API credentials for the services you want to integrate
- Network access to the respective APIs

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd business-integration-dashboard
   ```

2. **Install dependencies**

   ```bash
   pip install requests slack-sdk python-dotenv
   ```

3. **Set up environment variables**

   Create a `.env` file with your API credentials:

   ```env
   # CRM Configuration
   CRM_API_KEY=your_salesforce_api_key
   CRM_BASE_URL=https://api.salesforce.com

   # ERP Configuration
   ERP_API_KEY=your_odoo_api_key
   ERP_CLIENT_ID=your_odoo_client_id
   ERP_BASE_URL=your_odoo_base_url
   ERP_DB=your_odoo_database
   ERP_USERNAME=your_odoo_username
   ERP_PASSWORD=your_odoo_password

   # E-commerce Configuration
   SHOPIFY_ACCESS_TOKEN=your_shopify_token
   SHOPIFY_STORE_URL=your_shopify_store_url

   # Scheduling Configuration
   CALENDLY_ACCESS_TOKEN=your_calendly_token

   # Learning Management Configuration
   LEARNING_ACCESS_TOKEN=your_lms_token
   LEARNING_BASE_URL=your_lms_base_url

   # Marketing Configuration
   HUBSPOT_ACCESS_TOKEN=your_hubspot_token

   # Support Configuration
   ZENDESK_ACCESS_TOKEN=your_zendesk_token
   ZENDESK_SUBDOMAIN=your_zendesk_subdomain
   ZENDESK_EMAIL=your_zendesk_email

   # Communication Configuration
   SLACK_BOT_TOKEN=your_slack_bot_token
   SLACK_CHANNEL=#general
   ```

## 📖 Usage

### Basic Setup

```python
from FirstBluePrint import APIConfig, DashboardManager

# Configure API credentials
config = APIConfig(
    crm_api_key="your_crm_key",
    erp_api_key="your_erp_key",
    erp_client_id="your_erp_client_id",
    erp_base_url="your_erp_url",
    erp_db="your_erp_db",
    erp_username="your_erp_username",
    erp_password="your_erp_password",
    slack_bot_token="your_slack_token",
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

### Class Structure

```
DashboardManager
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

## 🔒 Security Best Practices

- Store API credentials securely using environment variables
- Use HTTPS for all API communications
- Implement proper authentication for each service
- Regularly rotate API keys and tokens
- Monitor API usage and access logs
- Never commit credentials to version control

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

Key dependencies include:

- `requests` - HTTP library for API calls
- `slack-sdk` - Official Slack SDK for Python
- `python-dotenv` - Environment variable management
- `xmlrpc.client` - XML-RPC client for Odoo integration

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
