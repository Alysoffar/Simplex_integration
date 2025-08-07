"""
Enhanced Business Integration Dashboard with OAuth2 Authentication

This module provides OAuth2-enabled integrations for various business systems.
All API calls now use OAuth2 tokens for secure authentication.
"""

from dataclasses import dataclass, field
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import xmlrpc.client
from datetime import datetime
import logging
from typing import Optional, Dict, Any
from oauth2_auth import OAuth2Manager, OAuth2Token, ServiceOAuth2Configs

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OAuth2APIConfig:
    """Enhanced API configuration with OAuth2 support"""
    
    # OAuth2 Configuration
    oauth2_manager: OAuth2Manager = field(default_factory=OAuth2Manager)
    redirect_uri: str = "http://localhost:8000/oauth/callback"
    
    # Service-specific OAuth2 client credentials
    # CRM Configuration (Salesforce)
    crm_client_id: Optional[str] = None
    crm_client_secret: Optional[str] = None
    crm_is_sandbox: bool = False
    crm_base_url: str = "https://api.salesforce.com"
    
    # ERP Configuration (for non-OAuth2 systems like Odoo)
    erp_api_key: Optional[str] = None
    erp_client_id: Optional[str] = None
    erp_base_url: Optional[str] = None
    erp_db: Optional[str] = None
    erp_username: Optional[str] = None
    erp_password: Optional[str] = None
    
    # E-commerce Configuration (Shopify)
    shopify_client_id: Optional[str] = None
    shopify_client_secret: Optional[str] = None
    shopify_shop_domain: Optional[str] = None
    
    # Scheduling Configuration (Calendly)
    calendly_client_id: Optional[str] = None
    calendly_client_secret: Optional[str] = None
    
    # Learning Management (Custom API)
    learning_base_url: Optional[str] = None
    learning_api_key: Optional[str] = None  # If not using OAuth2
    
    # Marketing Configuration (HubSpot)
    hubspot_client_id: Optional[str] = None
    hubspot_client_secret: Optional[str] = None
    
    # Support Configuration (Zendesk)
    zendesk_client_id: Optional[str] = None
    zendesk_client_secret: Optional[str] = None
    zendesk_subdomain: Optional[str] = None
    
    # Communication Configuration (Slack)
    slack_client_id: Optional[str] = None
    slack_client_secret: Optional[str] = None
    slack_channel: str = "#general"
    
    def __post_init__(self):
        """Initialize OAuth2 configurations after dataclass creation"""
        self.setup_oauth2_configs()
    
    def setup_oauth2_configs(self):
        """Setup OAuth2 configurations for all services"""
        
        # Salesforce/CRM
        if self.crm_client_id and self.crm_client_secret:
            config = ServiceOAuth2Configs.salesforce(
                self.crm_client_id,
                self.crm_client_secret,
                f"{self.redirect_uri}/salesforce",
                self.crm_is_sandbox
            )
            self.oauth2_manager.add_service_config("salesforce", config)
        
        # Shopify
        if self.shopify_client_id and self.shopify_client_secret and self.shopify_shop_domain:
            config = ServiceOAuth2Configs.shopify(
                self.shopify_client_id,
                self.shopify_client_secret,
                f"{self.redirect_uri}/shopify",
                self.shopify_shop_domain
            )
            self.oauth2_manager.add_service_config("shopify", config)
        
        # HubSpot
        if self.hubspot_client_id and self.hubspot_client_secret:
            config = ServiceOAuth2Configs.hubspot(
                self.hubspot_client_id,
                self.hubspot_client_secret,
                f"{self.redirect_uri}/hubspot"
            )
            self.oauth2_manager.add_service_config("hubspot", config)
        
        # Slack
        if self.slack_client_id and self.slack_client_secret:
            config = ServiceOAuth2Configs.slack(
                self.slack_client_id,
                self.slack_client_secret,
                f"{self.redirect_uri}/slack"
            )
            self.oauth2_manager.add_service_config("slack", config)
        
        # Calendly
        if self.calendly_client_id and self.calendly_client_secret:
            config = ServiceOAuth2Configs.calendly(
                self.calendly_client_id,
                self.calendly_client_secret,
                f"{self.redirect_uri}/calendly"
            )
            self.oauth2_manager.add_service_config("calendly", config)
        
        # Zendesk
        if self.zendesk_client_id and self.zendesk_client_secret and self.zendesk_subdomain:
            config = ServiceOAuth2Configs.zendesk(
                self.zendesk_client_id,
                self.zendesk_client_secret,
                f"{self.redirect_uri}/zendesk",
                self.zendesk_subdomain
            )
            self.oauth2_manager.add_service_config("zendesk", config)


class OAuth2BaseIntegration:
    """Enhanced base class for all integrations with OAuth2 support"""
    
    def __init__(self, config: OAuth2APIConfig, service_name: str):
        self.config = config
        self.service_name = service_name
        self.session = requests.Session()
        
    def _get_oauth2_headers(self) -> Dict[str, str]:
        """Get OAuth2 authorization headers"""
        token = self.config.oauth2_manager.get_valid_token(self.service_name)
        if not token:
            raise ValueError(f"No valid OAuth2 token for {self.service_name}. Please authenticate first.")
        
        return {
            'Authorization': f'{token.token_type} {token.access_token}',
            'Content-Type': 'application/json'
        }
    
    def _make_oauth2_request(self, method: str, url: str, **kwargs) -> dict:
        """Make HTTP request with OAuth2 authentication"""
        try:
            headers = self._get_oauth2_headers()
            if 'headers' in kwargs:
                headers.update(kwargs['headers'])
            kwargs['headers'] = headers
            
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            
            # Handle different response types
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                return {"success": True, "data": response.json()}
            else:
                return {"success": True, "data": response.text}
                
        except requests.RequestException as e:
            logger.error(f"OAuth2 API request failed for {self.service_name}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _validate_required_fields(self, data: dict, required_fields: list) -> bool:
        """Validate that required fields are present in data"""
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            return False
        return True
    
    def is_authenticated(self) -> bool:
        """Check if the service is properly authenticated"""
        return self.config.oauth2_manager.is_authenticated(self.service_name)
    
    def get_authorization_url(self) -> str:
        """Get OAuth2 authorization URL for this service"""
        auth_url, state = self.config.oauth2_manager.generate_authorization_url(self.service_name)
        return auth_url


class OAuth2CRMIntegration(OAuth2BaseIntegration):
    """Enhanced CRM integration with OAuth2 authentication"""
    
    def __init__(self, config: OAuth2APIConfig):
        super().__init__(config, "salesforce")
        
    def create_lead(self, lead_data: dict) -> dict:
        """Create a new lead in the CRM system"""
        required_fields = ['FirstName', 'LastName', 'Company', 'Email']
        if not self._validate_required_fields(lead_data, required_fields):
            return {"error": "Missing required fields for lead creation"}
        
        url = f"{self.config.crm_base_url}/services/data/v55.0/sobjects/Lead"
        return self._make_oauth2_request('POST', url, json=lead_data)
    
    def get_customer_data(self, customer_id: str) -> dict:
        """Fetch customer data from CRM"""
        url = f"{self.config.crm_base_url}/services/data/v55.0/sobjects/Account/{customer_id}"
        return self._make_oauth2_request('GET', url)
    
    def update_customer(self, customer_id: str, update_data: dict) -> dict:
        """Update existing customer information"""
        url = f"{self.config.crm_base_url}/services/data/v55.0/sobjects/Account/{customer_id}"
        return self._make_oauth2_request('PATCH', url, json=update_data)
    
    def get_all_leads(self, limit: int = 100) -> dict:
        """Fetch all leads with pagination"""
        url = f"{self.config.crm_base_url}/services/data/v55.0/query"
        query = f"SELECT Id, FirstName, LastName, Company, Email, Status FROM Lead LIMIT {limit}"
        params = {'q': query}
        return self._make_oauth2_request('GET', url, params=params)
    
    def convert_lead(self, lead_id: str) -> dict:
        """Convert a lead to an opportunity"""
        url = f"{self.config.crm_base_url}/services/data/v55.0/sobjects/Lead/{lead_id}/convert"
        return self._make_oauth2_request('POST', url)
    
    def get_opportunities(self, stage: str = None) -> dict:
        """Fetch opportunities, optionally filtered by stage"""
        query = "SELECT Id, Name, StageName, Amount, CloseDate FROM Opportunity"
        if stage:
            query += f" WHERE StageName = '{stage}'"
        
        url = f"{self.config.crm_base_url}/services/data/v55.0/query"
        params = {'q': query}
        return self._make_oauth2_request('GET', url, params=params)
    
    def create_task(self, task_data: dict) -> dict:
        """Create a task in CRM"""
        required_fields = ['Subject', 'WhoId']
        if not self._validate_required_fields(task_data, required_fields):
            return {"error": "Missing required fields for task creation"}
        
        url = f"{self.config.crm_base_url}/services/data/v55.0/sobjects/Task"
        return self._make_oauth2_request('POST', url, json=task_data)


class OAuth2OnlineStoreIntegration(OAuth2BaseIntegration):
    """Enhanced online store integration with OAuth2 authentication"""
    
    def __init__(self, config: OAuth2APIConfig):
        super().__init__(config, "shopify")
        self.base_url = f"https://{config.shopify_shop_domain}/admin/api/2023-10"
    
    def get_orders(self, status: str = None, limit: int = 50) -> dict:
        """Fetch orders from Shopify with optional filtering"""
        url = f"{self.base_url}/orders.json"
        params = {'limit': limit}
        if status:
            params['status'] = status
        
        return self._make_oauth2_request('GET', url, params=params)
    
    def get_products(self, published_status: str = None) -> dict:
        """Fetch products from store"""
        url = f"{self.base_url}/products.json"
        params = {}
        if published_status:
            params['published_status'] = published_status
        
        return self._make_oauth2_request('GET', url, params=params)
    
    def update_product_inventory(self, variant_id: str, quantity: int) -> dict:
        """Update product inventory quantity"""
        url = f"{self.base_url}/inventory_levels/set.json"
        data = {
            'location_id': 1,  # Main location
            'inventory_item_id': variant_id,
            'available': quantity
        }
        return self._make_oauth2_request('POST', url, json=data)
    
    def create_discount_code(self, discount_data: dict) -> dict:
        """Create a discount code"""
        required_fields = ['code', 'value', 'value_type']
        if not self._validate_required_fields(discount_data, required_fields):
            return {"error": "Missing required fields for discount code"}
        
        url = f"{self.base_url}/discount_codes.json"
        return self._make_oauth2_request('POST', url, json={'discount_code': discount_data})
    
    def get_customers(self) -> dict:
        """Fetch customer list from store"""
        url = f"{self.base_url}/customers.json"
        return self._make_oauth2_request('GET', url)
    
    def fulfill_order(self, order_id: str, tracking_number: str = None) -> dict:
        """Fulfill an order"""
        url = f"{self.base_url}/orders/{order_id}/fulfillments.json"
        data = {'fulfillment': {'notify_customer': True}}
        if tracking_number:
            data['fulfillment']['tracking_number'] = tracking_number
        
        return self._make_oauth2_request('POST', url, json=data)


class OAuth2AppointmentTools(OAuth2BaseIntegration):
    """Enhanced appointment scheduling tools with OAuth2"""

    def __init__(self, config: OAuth2APIConfig):
        super().__init__(config, "calendly")
        self.base_url = "https://api.calendly.com"

    def get_events(self, user_uri: str = None, count: int = 20) -> dict:
        """Fetch upcoming scheduled events"""
        url = f"{self.base_url}/scheduled_events"
        params = {'count': count}
        if user_uri:
            params['user'] = user_uri
        
        return self._make_oauth2_request('GET', url, params=params)
    
    def get_event_types(self, user_uri: str = None) -> dict:
        """Fetch available event types"""
        url = f"{self.base_url}/event_types"
        params = {}
        if user_uri:
            params['user'] = user_uri
        
        return self._make_oauth2_request('GET', url, params=params)
    
    def cancel_event(self, event_uuid: str, reason: str = None) -> dict:
        """Cancel a scheduled event"""
        url = f"{self.base_url}/scheduled_events/{event_uuid}/cancellation"
        data = {}
        if reason:
            data['reason'] = reason
        
        return self._make_oauth2_request('POST', url, json=data)
    
    def get_invitees(self, event_uuid: str) -> dict:
        """Get invitees for a specific event"""
        url = f"{self.base_url}/scheduled_events/{event_uuid}/invitees"
        return self._make_oauth2_request('GET', url)


class OAuth2MarketingTools(OAuth2BaseIntegration):
    """Enhanced marketing automation tools with OAuth2"""
    
    def __init__(self, config: OAuth2APIConfig):
        super().__init__(config, "hubspot")
        self.base_url = "https://api.hubapi.com"

    def get_contacts(self, limit: int = 100) -> dict:
        """Fetch contacts from HubSpot"""
        url = f"{self.base_url}/crm/v3/objects/contacts"
        params = {'limit': limit}
        return self._make_oauth2_request('GET', url, params=params)
    
    def create_contact(self, contact_data: dict) -> dict:
        """Create a new contact"""
        required_fields = ['email']
        if not self._validate_required_fields(contact_data, required_fields):
            return {"error": "Email is required for contact creation"}
        
        url = f"{self.base_url}/crm/v3/objects/contacts"
        data = {'properties': contact_data}
        return self._make_oauth2_request('POST', url, json=data)
    
    def create_campaign(self, campaign_data: dict) -> dict:
        """Create a marketing campaign"""
        url = f"{self.base_url}/marketing/v3/campaigns"
        return self._make_oauth2_request('POST', url, json=campaign_data)
    
    def get_email_campaigns(self) -> dict:
        """Fetch email campaigns"""
        url = f"{self.base_url}/marketing/v3/campaigns"
        return self._make_oauth2_request('GET', url)
    
    def add_contact_to_list(self, contact_id: str, list_id: str) -> dict:
        """Add contact to a marketing list"""
        url = f"{self.base_url}/crm/v3/lists/{list_id}/memberships/add"
        data = {'objectIds': [contact_id]}
        return self._make_oauth2_request('PUT', url, json=data)
    
    def get_analytics(self, object_type: str = 'contacts', time_range: str = '30d') -> dict:
        """Get marketing analytics data"""
        url = f"{self.base_url}/analytics/v2/reports/{object_type}"
        params = {'timeRange': time_range}
        return self._make_oauth2_request('GET', url, params=params)


class OAuth2SupportTools(OAuth2BaseIntegration):
    """Enhanced customer support tools with OAuth2"""
    
    def __init__(self, config: OAuth2APIConfig):
        super().__init__(config, "zendesk")
        self.base_url = f"https://{config.zendesk_subdomain}.zendesk.com/api/v2"

    def get_tickets(self, status: str = None, priority: str = None) -> dict:
        """Fetch support tickets from Zendesk"""
        url = f"{self.base_url}/tickets.json"
        params = {}
        if status:
            params['status'] = status
        if priority:
            params['priority'] = priority
        
        return self._make_oauth2_request('GET', url, params=params)
    
    def create_ticket(self, ticket_data: dict) -> dict:
        """Create a new support ticket"""
        required_fields = ['subject', 'comment']
        if not self._validate_required_fields(ticket_data, required_fields):
            return {"error": "Subject and comment are required for ticket creation"}
        
        url = f"{self.base_url}/tickets.json"
        data = {'ticket': ticket_data}
        return self._make_oauth2_request('POST', url, json=data)
    
    def update_ticket(self, ticket_id: str, update_data: dict) -> dict:
        """Update an existing ticket"""
        url = f"{self.base_url}/tickets/{ticket_id}.json"
        data = {'ticket': update_data}
        return self._make_oauth2_request('PUT', url, json=data)
    
    def add_ticket_comment(self, ticket_id: str, comment: str, public: bool = True) -> dict:
        """Add a comment to a ticket"""
        url = f"{self.base_url}/tickets/{ticket_id}.json"
        data = {
            'ticket': {
                'comment': {
                    'body': comment,
                    'public': public
                }
            }
        }
        return self._make_oauth2_request('PUT', url, json=data)
    
    def get_users(self) -> dict:
        """Fetch users from Zendesk"""
        url = f"{self.base_url}/users.json"
        return self._make_oauth2_request('GET', url)
    
    def search_tickets(self, query: str) -> dict:
        """Search tickets using Zendesk search API"""
        url = f"{self.base_url}/search.json"
        params = {'query': f'type:ticket {query}'}
        return self._make_oauth2_request('GET', url, params=params)


class OAuth2SlackIntegration(OAuth2BaseIntegration):
    """Enhanced Slack API interactions with OAuth2"""

    def __init__(self, config: OAuth2APIConfig):
        super().__init__(config, "slack")
        self.config = config
        # Initialize WebClient with OAuth2 token
        token = self.config.oauth2_manager.get_valid_token("slack")
        if token:
            self.client = WebClient(token=token.access_token)
        else:
            self.client = None

    def _refresh_slack_client(self):
        """Refresh Slack client with new token"""
        token = self.config.oauth2_manager.get_valid_token("slack")
        if token:
            self.client = WebClient(token=token.access_token)

    def send_message(self, channel: str, text: str, blocks: list = None) -> dict:
        """Send a message to a Slack channel"""
        if not self.client:
            self._refresh_slack_client()
            
        if not self.client:
            return {"error": "Slack not authenticated. Please complete OAuth2 flow."}
            
        try:
            payload = {
                'channel': channel or self.config.slack_channel,
                'text': text
            }
            if blocks:
                payload['blocks'] = blocks
            
            response = self.client.chat_postMessage(**payload)
            return {"success": True, "message_ts": response['ts']}
        except SlackApiError as e:
            return {"error": f"Slack API error: {e.response['error']}"}
    
    def send_alert(self, message: str, urgent: bool = False, channel: str = None) -> dict:
        """Send an alert message with optional urgency"""
        alert_message = f"🚨 ALERT: {message}" if urgent else f"ℹ️ {message}"
        return self.send_message(channel or self.config.slack_channel, alert_message)
    
    def create_channel(self, name: str, is_private: bool = False) -> dict:
        """Create a new Slack channel"""
        if not self.client:
            self._refresh_slack_client()
            
        if not self.client:
            return {"error": "Slack not authenticated. Please complete OAuth2 flow."}
            
        try:
            if is_private:
                response = self.client.conversations_create(name=name, is_private=True)
            else:
                response = self.client.conversations_create(name=name)
            return {"success": True, "channel_id": response['channel']['id']}
        except SlackApiError as e:
            return {"error": f"Slack API error: {e.response['error']}"}
    
    def get_channel_history(self, channel: str, limit: int = 100) -> dict:
        """Get message history from a channel"""
        if not self.client:
            self._refresh_slack_client()
            
        if not self.client:
            return {"error": "Slack not authenticated. Please complete OAuth2 flow."}
            
        try:
            response = self.client.conversations_history(channel=channel, limit=limit)
            return {"success": True, "messages": response['messages']}
        except SlackApiError as e:
            return {"error": f"Slack API error: {e.response['error']}"}


# Legacy ERP Integration (Non-OAuth2)
class ERPIntegration:
    """ERP integration using traditional authentication (Odoo)"""
    
    def __init__(self, config: OAuth2APIConfig):
        self.config = config
        self.url = config.erp_base_url
        self.db = config.erp_db
        self.username = config.erp_username
        self.password = config.erp_password
        
        # Initialize Odoo connection
        try:
            common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
            self.uid = common.authenticate(self.db, self.username, self.password, {})
            self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        except Exception as e:
            logger.error(f"ERP connection failed: {str(e)}")
            self.uid = None
            self.models = None

    def fetch_inventory(self, item_id: str = None, item_name: str = None) -> dict:
        """Fetch inventory data from the ERP system"""
        if not self.uid:
            return {"error": "ERP connection not established"}
        
        try:
            domain = []
            if item_id:
                domain.append(['id', '=', int(item_id)])
            elif item_name:
                domain.append(['name', 'ilike', item_name])
            
            result = self.models.execute_kw(
                self.db, self.uid, self.password,
                'product.product', 'search_read',
                [domain], 
                {'fields': ['name', 'qty_available', 'list_price', 'default_code', 'categ_id']}
            )
            return {"success": True, "data": result}
        except Exception as e:
            return {"error": f"ERP API error: {str(e)}"}
    
    # ... (other ERP methods remain the same)


class OAuth2DashboardManager:
    """Enhanced dashboard manager with OAuth2 authentication"""
    
    def __init__(self, config: OAuth2APIConfig):
        self.config = config
        self.crm = OAuth2CRMIntegration(config)
        self.erp = ERPIntegration(config)  # Still uses traditional auth
        self.store = OAuth2OnlineStoreIntegration(config)
        self.appointments = OAuth2AppointmentTools(config)
        self.marketing = OAuth2MarketingTools(config)
        self.support = OAuth2SupportTools(config)
        self.slack = OAuth2SlackIntegration(config)
    
    def get_authorization_urls(self) -> Dict[str, str]:
        """Get OAuth2 authorization URLs for all services"""
        urls = {}
        
        services = [
            ("salesforce", self.crm),
            ("shopify", self.store),
            ("calendly", self.appointments),
            ("hubspot", self.marketing),
            ("zendesk", self.support),
            ("slack", self.slack)
        ]
        
        for service_name, integration in services:
            try:
                if hasattr(integration, 'get_authorization_url'):
                    urls[service_name] = integration.get_authorization_url()
            except Exception as e:
                logger.error(f"Failed to get auth URL for {service_name}: {str(e)}")
                
        return urls
    
    def complete_oauth2_flow(self, service_name: str, authorization_code: str, state: str) -> bool:
        """Complete OAuth2 flow for a service"""
        try:
            token = self.config.oauth2_manager.exchange_code_for_token(
                service_name, authorization_code, state
            )
            
            # Refresh service clients if needed
            if service_name == "slack":
                self.slack._refresh_slack_client()
                
            logger.info(f"Successfully completed OAuth2 flow for {service_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to complete OAuth2 flow for {service_name}: {str(e)}")
            return False
    
    def get_authentication_status(self) -> Dict[str, bool]:
        """Get authentication status for all services"""
        services = ["salesforce", "shopify", "calendly", "hubspot", "zendesk", "slack"]
        return {
            service: self.config.oauth2_manager.is_authenticated(service)
            for service in services
        }
    
    def revoke_service_authentication(self, service_name: str):
        """Revoke authentication for a specific service"""
        self.config.oauth2_manager.revoke_token(service_name)
        
        # Reset service client if needed
        if service_name == "slack":
            self.slack.client = None
    
    def get_dashboard_summary(self) -> dict:
        """Get a summary of all connected systems"""
        summary = {
            "timestamp": datetime.now().isoformat(),
            "authentication_status": self.get_authentication_status(),
            "systems": {}
        }
        
        # Test each integration only if authenticated
        integrations = [
            ("CRM", self.crm.get_all_leads, {"limit": 1}, "salesforce"),
            ("ERP", self.erp.fetch_inventory, {}, None),  # No OAuth2
            ("Store", self.store.get_orders, {"limit": 1}, "shopify"),
            ("Appointments", self.appointments.get_events, {"count": 1}, "calendly"),
            ("Marketing", self.marketing.get_contacts, {"limit": 1}, "hubspot"),
            ("Support", self.support.get_tickets, {}, "zendesk"),
        ]
        
        for name, method, kwargs, auth_service in integrations:
            try:
                if auth_service and not self.config.oauth2_manager.is_authenticated(auth_service):
                    summary["systems"][name] = {
                        "status": "not_authenticated",
                        "last_check": datetime.now().isoformat()
                    }
                else:
                    result = method(**kwargs)
                    summary["systems"][name] = {
                        "status": "connected" if result.get("success") else "error",
                        "last_check": datetime.now().isoformat()
                    }
            except Exception as e:
                summary["systems"][name] = {
                    "status": "error",
                    "error": str(e),
                    "last_check": datetime.now().isoformat()
                }
        
        return summary
