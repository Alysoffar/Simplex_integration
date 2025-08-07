"""
Flask Web Application for OAuth2 Authentication Flow

This application handles the OAuth2 callback flows for all integrated services
and provides a web interface for authentication management.
"""

from flask import Flask, request, redirect, render_template_string, session, jsonify, url_for
import os
import logging
from oauth2_integration import OAuth2APIConfig, OAuth2DashboardManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-change-this')

# Global dashboard manager
dashboard = None

def init_dashboard():
    """Initialize the dashboard with OAuth2 configuration"""
    global dashboard
    
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
        
        # Redirect URI base
        redirect_uri=os.environ.get('OAUTH_REDIRECT_URI', 'http://localhost:8000/oauth/callback')
    )
    
    dashboard = OAuth2DashboardManager(config)

@app.route('/')
def index():
    """Main dashboard page"""
    if not dashboard:
        init_dashboard()
    
    auth_status = dashboard.get_authentication_status()
    auth_urls = dashboard.get_authorization_urls()
    
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Business Integration Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .service { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            .authenticated { background-color: #e8f5e8; }
            .not-authenticated { background-color: #ffe8e8; }
            .auth-button { 
                background-color: #007bff; 
                color: white; 
                padding: 10px 15px; 
                text-decoration: none; 
                border-radius: 3px; 
                display: inline-block;
                margin: 5px 0;
            }
            .revoke-button { 
                background-color: #dc3545; 
                color: white; 
                padding: 5px 10px; 
                text-decoration: none; 
                border-radius: 3px; 
                display: inline-block;
                margin-left: 10px;
            }
            .status-connected { color: green; font-weight: bold; }
            .status-error { color: red; font-weight: bold; }
            .status-not-auth { color: orange; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Business Integration Dashboard</h1>
        <p>Manage your OAuth2 authentication for integrated business services.</p>
        
        <h2>Service Authentication Status</h2>
        
        {% for service, is_auth in auth_status.items() %}
        <div class="service {{ 'authenticated' if is_auth else 'not-authenticated' }}">
            <h3>{{ service.title() }}</h3>
            <p>Status: 
                <span class="{{ 'status-connected' if is_auth else 'status-not-auth' }}">
                    {{ 'Authenticated' if is_auth else 'Not Authenticated' }}
                </span>
            </p>
            
            {% if not is_auth and service in auth_urls %}
                <a href="{{ auth_urls[service] }}" class="auth-button">
                    Authenticate {{ service.title() }}
                </a>
            {% endif %}
            
            {% if is_auth %}
                <a href="{{ url_for('revoke_auth', service=service) }}" class="revoke-button">
                    Revoke Authentication
                </a>
            {% endif %}
        </div>
        {% endfor %}
        
        <h2>System Status</h2>
        <div id="system-status">
            <button onclick="checkSystemStatus()">Check System Status</button>
            <div id="status-results"></div>
        </div>
        
        <script>
            function checkSystemStatus() {
                fetch('/api/status')
                    .then(response => response.json())
                    .then(data => {
                        let html = '<h3>System Status Results</h3>';
                        for (const [system, status] of Object.entries(data.systems)) {
                            const statusClass = status.status === 'connected' ? 'status-connected' : 
                                              status.status === 'not_authenticated' ? 'status-not-auth' : 'status-error';
                            html += `<p><strong>${system}:</strong> <span class="${statusClass}">${status.status}</span></p>`;
                        }
                        document.getElementById('status-results').innerHTML = html;
                    })
                    .catch(error => {
                        document.getElementById('status-results').innerHTML = 
                            '<p class="status-error">Error checking status: ' + error + '</p>';
                    });
            }
        </script>
    </body>
    </html>
    """
    
    return render_template_string(template, 
                                auth_status=auth_status, 
                                auth_urls=auth_urls, 
                                url_for=url_for)

@app.route('/oauth/callback/<service>')
def oauth_callback(service):
    """Handle OAuth2 callback for any service"""
    if not dashboard:
        init_dashboard()
    
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    if error:
        logger.error(f"OAuth2 error for {service}: {error}")
        return f"Authentication failed for {service}: {error}", 400
    
    if not code or not state:
        logger.error(f"Missing code or state parameter for {service}")
        return "Missing required parameters", 400
    
    # Complete OAuth2 flow
    success = dashboard.complete_oauth2_flow(service, code, state)
    
    if success:
        return redirect(url_for('index') + f'?auth_success={service}')
    else:
        return redirect(url_for('index') + f'?auth_error={service}')

@app.route('/revoke/<service>')
def revoke_auth(service):
    """Revoke authentication for a service"""
    if not dashboard:
        init_dashboard()
    
    dashboard.revoke_service_authentication(service)
    return redirect(url_for('index') + f'?revoked={service}')

@app.route('/api/status')
def api_status():
    """API endpoint to get system status"""
    if not dashboard:
        init_dashboard()
    
    return jsonify(dashboard.get_dashboard_summary())

@app.route('/api/auth-urls')
def api_auth_urls():
    """API endpoint to get authentication URLs"""
    if not dashboard:
        init_dashboard()
    
    return jsonify(dashboard.get_authorization_urls())

@app.route('/api/test/<service>')
def api_test_service(service):
    """Test a specific service integration"""
    if not dashboard:
        init_dashboard()
    
    try:
        if service == 'crm':
            result = dashboard.crm.get_all_leads(limit=1)
        elif service == 'store':
            result = dashboard.store.get_orders(limit=1)
        elif service == 'marketing':
            result = dashboard.marketing.get_contacts(limit=1)
        elif service == 'support':
            result = dashboard.support.get_tickets()
        elif service == 'appointments':
            result = dashboard.appointments.get_events(count=1)
        elif service == 'erp':
            result = dashboard.erp.fetch_inventory()
        else:
            return jsonify({"error": "Unknown service"}), 400
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error testing {service}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/setup')
def setup():
    """Setup page with environment variable instructions"""
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OAuth2 Setup Instructions</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            pre { background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
            .service-section { margin: 30px 0; }
        </style>
    </head>
    <body>
        <h1>OAuth2 Setup Instructions</h1>
        
        <p>To use this integration dashboard, you need to set up OAuth2 applications for each service and configure environment variables.</p>
        
        <div class="service-section">
            <h2>Environment Variables</h2>
            <p>Create a <code>.env</code> file with the following variables:</p>
            <pre>
# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here

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
            </pre>
        </div>
        
        <div class="service-section">
            <h2>OAuth2 Application Setup</h2>
            
            <h3>Salesforce</h3>
            <ol>
                <li>Go to Setup → App Manager → New Connected App</li>
                <li>Set callback URL to: <code>http://localhost:8000/oauth/callback/salesforce</code></li>
                <li>Enable OAuth Settings and add required scopes</li>
            </ol>
            
            <h3>Shopify</h3>
            <ol>
                <li>Go to your Partner Dashboard → Apps → Create App</li>
                <li>Set redirect URL to: <code>http://localhost:8000/oauth/callback/shopify</code></li>
                <li>Configure required scopes for your app</li>
            </ol>
            
            <h3>HubSpot</h3>
            <ol>
                <li>Go to HubSpot Developer Portal → Create App</li>
                <li>Set redirect URL to: <code>http://localhost:8000/oauth/callback/hubspot</code></li>
                <li>Configure required scopes</li>
            </ol>
            
            <h3>Slack</h3>
            <ol>
                <li>Go to api.slack.com → Create New App</li>
                <li>Set redirect URL to: <code>http://localhost:8000/oauth/callback/slack</code></li>
                <li>Configure OAuth scopes</li>
            </ol>
            
            <h3>Calendly</h3>
            <ol>
                <li>Go to Calendly Developer Portal → Create App</li>
                <li>Set redirect URL to: <code>http://localhost:8000/oauth/callback/calendly</code></li>
            </ol>
            
            <h3>Zendesk</h3>
            <ol>
                <li>Go to Admin Center → Apps and integrations → APIs → OAuth Clients</li>
                <li>Set redirect URL to: <code>http://localhost:8000/oauth/callback/zendesk</code></li>
            </ol>
        </div>
        
        <a href="/">← Back to Dashboard</a>
    </body>
    </html>
    """
    return render_template_string(template)

if __name__ == '__main__':
    # Load environment variables from .env file if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("python-dotenv not installed. Please install it or set environment variables manually.")
    
    app.run(host='localhost', port=8000, debug=True)
