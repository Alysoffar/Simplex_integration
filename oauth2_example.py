"""
Example Usage of OAuth2 Business Integration Dashboard

This example demonstrates how to use the OAuth2-enabled business integration
dashboard to authenticate and interact with various business systems.
"""

import os
from datetime import datetime
from oauth2_integration import OAuth2APIConfig, OAuth2DashboardManager
from oauth2_auth import OAuth2Manager

def setup_oauth2_dashboard():
    """Setup the OAuth2 dashboard with configuration"""
    
    # Load configuration from environment variables
    config = OAuth2APIConfig(
        # Salesforce/CRM
        crm_client_id=os.environ.get('SALESFORCE_CLIENT_ID'),
        crm_client_secret=os.environ.get('SALESFORCE_CLIENT_SECRET'),
        crm_is_sandbox=os.environ.get('SALESFORCE_SANDBOX', 'false').lower() == 'true',
        
        # Shopify
        shopify_client_id=os.environ.get('SHOPIFY_CLIENT_ID'),
        shopify_client_secret=os.environ.get('SHOPIFY_CLIENT_SECRET'),
        shopify_shop_domain=os.environ.get('SHOPIFY_SHOP_DOMAIN'),
        
        # HubSpot
        hubspot_client_id=os.environ.get('HUBSPOT_CLIENT_ID'),
        hubspot_client_secret=os.environ.get('HUBSPOT_CLIENT_SECRET'),
        
        # Slack
        slack_client_id=os.environ.get('SLACK_CLIENT_ID'),
        slack_client_secret=os.environ.get('SLACK_CLIENT_SECRET'),
        
        # Calendly
        calendly_client_id=os.environ.get('CALENDLY_CLIENT_ID'),
        calendly_client_secret=os.environ.get('CALENDLY_CLIENT_SECRET'),
        
        # Zendesk
        zendesk_client_id=os.environ.get('ZENDESK_CLIENT_ID'),
        zendesk_client_secret=os.environ.get('ZENDESK_CLIENT_SECRET'),
        zendesk_subdomain=os.environ.get('ZENDESK_SUBDOMAIN'),
        
        # ERP (Odoo) - Traditional authentication
        erp_base_url=os.environ.get('ERP_BASE_URL'),
        erp_db=os.environ.get('ERP_DB'),
        erp_username=os.environ.get('ERP_USERNAME'),
        erp_password=os.environ.get('ERP_PASSWORD'),
    )
    
    return OAuth2DashboardManager(config)

def demonstrate_authentication_flow():
    """Demonstrate OAuth2 authentication flow"""
    
    dashboard = setup_oauth2_dashboard()
    
    print("=== OAuth2 Business Integration Dashboard ===")
    print()
    
    # Check current authentication status
    auth_status = dashboard.get_authentication_status()
    print("Current Authentication Status:")
    for service, is_authenticated in auth_status.items():
        status = "✅ Authenticated" if is_authenticated else "❌ Not Authenticated"
        print(f"  {service.title()}: {status}")
    print()
    
    # Get authorization URLs for non-authenticated services
    auth_urls = dashboard.get_authorization_urls()
    if auth_urls:
        print("Authorization URLs (visit these to authenticate):")
        for service, url in auth_urls.items():
            if not auth_status.get(service, False):
                print(f"  {service.title()}: {url}")
        print()
    
    return dashboard

def demonstrate_crm_operations(dashboard):
    """Demonstrate CRM operations with OAuth2"""
    
    print("=== CRM Operations (Salesforce) ===")
    
    if not dashboard.crm.is_authenticated():
        print("❌ CRM not authenticated. Please complete OAuth2 flow first.")
        print(f"   Authorization URL: {dashboard.crm.get_authorization_url()}")
        return
    
    try:
        # Create a lead
        lead_data = {
            "FirstName": "John",
            "LastName": "Doe",
            "Company": "Example Corp",
            "Email": "john.doe@example.com",
            "Phone": "555-1234"
        }
        
        print("Creating new lead...")
        result = dashboard.crm.create_lead(lead_data)
        if result.get('success'):
            print("✅ Lead created successfully")
            lead_id = result['data'].get('id')
        else:
            print(f"❌ Failed to create lead: {result.get('error')}")
            return
        
        # Get all leads
        print("Fetching leads...")
        result = dashboard.crm.get_all_leads(limit=5)
        if result.get('success'):
            leads = result['data']['records']
            print(f"✅ Retrieved {len(leads)} leads")
            for lead in leads[:3]:  # Show first 3
                print(f"   - {lead.get('FirstName')} {lead.get('LastName')} ({lead.get('Company')})")
        else:
            print(f"❌ Failed to fetch leads: {result.get('error')}")
        
        # Create a task
        if lead_id:
            task_data = {
                "Subject": "Follow up with new lead",
                "WhoId": lead_id,
                "ActivityDate": datetime.now().strftime("%Y-%m-%d")
            }
            
            print("Creating task...")
            result = dashboard.crm.create_task(task_data)
            if result.get('success'):
                print("✅ Task created successfully")
            else:
                print(f"❌ Failed to create task: {result.get('error')}")
        
    except Exception as e:
        print(f"❌ CRM operations failed: {str(e)}")
    
    print()

def demonstrate_marketing_operations(dashboard):
    """Demonstrate marketing operations with OAuth2"""
    
    print("=== Marketing Operations (HubSpot) ===")
    
    if not dashboard.marketing.is_authenticated():
        print("❌ Marketing not authenticated. Please complete OAuth2 flow first.")
        print(f"   Authorization URL: {dashboard.marketing.get_authorization_url()}")
        return
    
    try:
        # Create a contact
        contact_data = {
            "email": "jane.smith@example.com",
            "firstname": "Jane",
            "lastname": "Smith",
            "company": "Example Corp",
            "phone": "555-5678"
        }
        
        print("Creating new contact...")
        result = dashboard.marketing.create_contact(contact_data)
        if result.get('success'):
            print("✅ Contact created successfully")
        else:
            print(f"❌ Failed to create contact: {result.get('error')}")
        
        # Get contacts
        print("Fetching contacts...")
        result = dashboard.marketing.get_contacts(limit=5)
        if result.get('success'):
            contacts = result['data']['results']
            print(f"✅ Retrieved {len(contacts)} contacts")
            for contact in contacts[:3]:  # Show first 3
                props = contact.get('properties', {})
                email = props.get('email', 'No email')
                name = f"{props.get('firstname', '')} {props.get('lastname', '')}".strip()
                print(f"   - {name or 'No name'} ({email})")
        else:
            print(f"❌ Failed to fetch contacts: {result.get('error')}")
        
        # Get analytics
        print("Fetching analytics...")
        result = dashboard.marketing.get_analytics()
        if result.get('success'):
            print("✅ Analytics retrieved successfully")
        else:
            print(f"❌ Failed to fetch analytics: {result.get('error')}")
        
    except Exception as e:
        print(f"❌ Marketing operations failed: {str(e)}")
    
    print()

def demonstrate_ecommerce_operations(dashboard):
    """Demonstrate e-commerce operations with OAuth2"""
    
    print("=== E-commerce Operations (Shopify) ===")
    
    if not dashboard.store.is_authenticated():
        print("❌ Store not authenticated. Please complete OAuth2 flow first.")
        print(f"   Authorization URL: {dashboard.store.get_authorization_url()}")
        return
    
    try:
        # Get orders
        print("Fetching recent orders...")
        result = dashboard.store.get_orders(limit=5)
        if result.get('success'):
            orders = result['data']['orders']
            print(f"✅ Retrieved {len(orders)} orders")
            for order in orders[:3]:  # Show first 3
                print(f"   - Order #{order.get('order_number')} - ${order.get('total_price')}")
        else:
            print(f"❌ Failed to fetch orders: {result.get('error')}")
        
        # Get products
        print("Fetching products...")
        result = dashboard.store.get_products()
        if result.get('success'):
            products = result['data']['products']
            print(f"✅ Retrieved {len(products)} products")
            for product in products[:3]:  # Show first 3
                print(f"   - {product.get('title')} - ${product.get('variants', [{}])[0].get('price', 'N/A')}")
        else:
            print(f"❌ Failed to fetch products: {result.get('error')}")
        
        # Get customers
        print("Fetching customers...")
        result = dashboard.store.get_customers()
        if result.get('success'):
            customers = result['data']['customers']
            print(f"✅ Retrieved {len(customers)} customers")
            for customer in customers[:3]:  # Show first 3
                name = f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip()
                print(f"   - {name or 'No name'} ({customer.get('email', 'No email')})")
        else:
            print(f"❌ Failed to fetch customers: {result.get('error')}")
        
    except Exception as e:
        print(f"❌ E-commerce operations failed: {str(e)}")
    
    print()

def demonstrate_slack_operations(dashboard):
    """Demonstrate Slack operations with OAuth2"""
    
    print("=== Communication Operations (Slack) ===")
    
    if not dashboard.slack.is_authenticated():
        print("❌ Slack not authenticated. Please complete OAuth2 flow first.")
        print(f"   Authorization URL: {dashboard.slack.get_authorization_url()}")
        return
    
    try:
        # Send a message
        print("Sending test message...")
        result = dashboard.slack.send_message(
            "#general",
            "🚀 OAuth2 integration test successful!"
        )
        if result.get('success'):
            print("✅ Message sent successfully")
        else:
            print(f"❌ Failed to send message: {result.get('error')}")
        
        # Send an alert
        print("Sending alert...")
        result = dashboard.slack.send_alert(
            "System integration test completed",
            urgent=False
        )
        if result.get('success'):
            print("✅ Alert sent successfully")
        else:
            print(f"❌ Failed to send alert: {result.get('error')}")
        
    except Exception as e:
        print(f"❌ Slack operations failed: {str(e)}")
    
    print()

def demonstrate_system_status(dashboard):
    """Demonstrate system status checking"""
    
    print("=== System Status Summary ===")
    
    try:
        summary = dashboard.get_dashboard_summary()
        
        print(f"Status checked at: {summary['timestamp']}")
        print()
        
        print("Authentication Status:")
        for service, is_auth in summary['authentication_status'].items():
            status = "✅ Authenticated" if is_auth else "❌ Not Authenticated"
            print(f"  {service.title()}: {status}")
        print()
        
        print("System Health:")
        for system, status_info in summary['systems'].items():
            status = status_info['status']
            if status == 'connected':
                icon = "✅"
            elif status == 'not_authenticated':
                icon = "🔐"
            else:
                icon = "❌"
            
            print(f"  {system}: {icon} {status.replace('_', ' ').title()}")
            if 'error' in status_info:
                print(f"    Error: {status_info['error']}")
        
    except Exception as e:
        print(f"❌ Failed to get system status: {str(e)}")
    
    print()

def main():
    """Main demonstration function"""
    
    print("OAuth2 Business Integration Dashboard Demo")
    print("==========================================")
    print()
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded from .env file")
    except ImportError:
        print("⚠️  python-dotenv not installed. Make sure environment variables are set manually.")
    except Exception as e:
        print(f"⚠️  Could not load .env file: {str(e)}")
    
    print()
    
    # Setup dashboard
    try:
        dashboard = demonstrate_authentication_flow()
    except Exception as e:
        print(f"❌ Failed to setup dashboard: {str(e)}")
        return
    
    # Demonstrate system status
    demonstrate_system_status(dashboard)
    
    # Demonstrate operations for authenticated services
    demonstrate_crm_operations(dashboard)
    demonstrate_marketing_operations(dashboard)
    demonstrate_ecommerce_operations(dashboard)
    demonstrate_slack_operations(dashboard)
    
    print("=== Demo Complete ===")
    print("To authenticate services, run the Flask web app:")
    print("  python oauth2_webapp.py")
    print("Then visit: http://localhost:8000")

if __name__ == "__main__":
    main()
