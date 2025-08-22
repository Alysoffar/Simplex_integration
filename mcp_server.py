"""MCP Server exposing Business Integration Dashboard operations.

Implements a Model Context Protocol (MCP) server so LLM frameworks (e.g. LangGraph,
OpenAI assistants with MCP client support) can call integration functions as tools.

Transport: stdio (default) or WebSocket (optional future enhancement).

Run:
  python mcp_server.py

Tools Exposed (initial set):
  - get_dashboard_summary
  - get_authentication_status
  - get_authorization_urls
  - complete_oauth2_flow(service_name, code, state)
  - revoke_service_authentication(service_name)
  - crm_create_lead(FirstName, LastName, Company, Email)
  - crm_get_leads(limit)
  - store_get_orders(status, limit)
  - marketing_get_contacts(limit)
  - support_get_tickets(status, priority)
  - appointments_get_events(count)
  - erp_fetch_inventory(item_id, item_name)
  - slack_send_message(channel, text)

Returns JSON-friendly dicts.
"""
import asyncio
import json
import os
import traceback
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Attempt to import MCP server primitives
try:
    from mcp.server import Server
    from mcp.types import Tool, ToolInputSchema, ToolResult
except ImportError:  # Fallback lightweight shim to avoid runtime crash if lib missing
    class Tool:  # type: ignore
        def __init__(self, name: str, description: str, input_schema: Dict[str, Any]):
            self.name = name
            self.description = description
            self.input_schema = input_schema
    class ToolResult(dict):
        pass
    class Server:
        def __init__(self, name: str):
            self.name = name
            self._tools = {}
        def tool(self, name: str, description: str, input_schema: Dict[str, Any]):
            def decorator(fn):
                self._tools[name] = (fn, description, input_schema)
                return fn
            return decorator
        async def run_stdio(self):  # Minimal dev helper
            print(json.dumps({"event": "server_started", "name": self.name}))
            # Simple REPL loop for manual testing
            while True:
                line = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
                if not line:
                    continue
                if line in ("exit", "quit"):
                    break
                try:
                    payload = json.loads(line)
                    tool_name = payload.get("tool")
                    args = payload.get("args", {})
                    if tool_name in self._tools:
                        fn, _, _ = self._tools[tool_name]
                        if asyncio.iscoroutinefunction(fn):
                            result = await fn(**args)
                        else:
                            result = fn(**args)
                        print(json.dumps({"ok": True, "result": result}))
                    else:
                        print(json.dumps({"ok": False, "error": "unknown tool"}))
                except Exception as e:  # noqa
                    print(json.dumps({"ok": False, "error": str(e)}))
            print("Server stopped")

# Local imports after path setup
from oauth2_integration import (
    OAuth2APIConfig,
    OAuth2DashboardManager,
)

load_dotenv()

# Instantiate config from environment variables

def build_config() -> OAuth2APIConfig:
    cfg = OAuth2APIConfig(
        crm_client_id=os.getenv("SALESFORCE_CLIENT_ID"),
        crm_client_secret=os.getenv("SALESFORCE_CLIENT_SECRET"),
        crm_is_sandbox=os.getenv("SALESFORCE_SANDBOX", "false").lower() == "true",
        shopify_client_id=os.getenv("SHOPIFY_CLIENT_ID"),
        shopify_client_secret=os.getenv("SHOPIFY_CLIENT_SECRET"),
        shopify_shop_domain=os.getenv("SHOPIFY_SHOP_DOMAIN"),
        hubspot_client_id=os.getenv("HUBSPOT_CLIENT_ID"),
        hubspot_client_secret=os.getenv("HUBSPOT_CLIENT_SECRET"),
        slack_client_id=os.getenv("SLACK_CLIENT_ID"),
        slack_client_secret=os.getenv("SLACK_CLIENT_SECRET"),
        calendly_client_id=os.getenv("CALENDLY_CLIENT_ID"),
        calendly_client_secret=os.getenv("CALENDLY_CLIENT_SECRET"),
        zendesk_client_id=os.getenv("ZENDESK_CLIENT_ID"),
        zendesk_client_secret=os.getenv("ZENDESK_CLIENT_SECRET"),
        zendesk_subdomain=os.getenv("ZENDESK_SUBDOMAIN"),
        erp_base_url=os.getenv("ERP_BASE_URL"),
        erp_db=os.getenv("ERP_DB"),
        erp_username=os.getenv("ERP_USERNAME"),
        erp_password=os.getenv("ERP_PASSWORD"),
    )
    return cfg

CONFIG = build_config()
DASHBOARD = OAuth2DashboardManager(CONFIG)

server = Server("business-integration-mcp")

# Utility wrappers

def _serialize(result: Any) -> Dict[str, Any]:
    if isinstance(result, dict):
        return result
    return {"data": result}

def _safe_call(fn, *args, **kwargs):
    try:
        data = fn(*args, **kwargs)
        return {"success": True, **_serialize(data)}
    except Exception as e:  # noqa
        return {"success": False, "error": str(e), "trace": traceback.format_exc().splitlines()[-5:]}

# Tool registrations
@server.tool(
    name="get_dashboard_summary",
    description="Return a summary of all connected systems and their status.",
    input_schema={"type": "object", "properties": {}, "required": []},
)
async def get_dashboard_summary_tool():
    return _safe_call(DASHBOARD.get_dashboard_summary)

@server.tool(
    name="get_authentication_status",
    description="Return auth status (True/False) for each OAuth2 service.",
    input_schema={"type": "object", "properties": {}, "required": []},
)
async def get_authentication_status_tool():
    return _safe_call(DASHBOARD.get_authentication_status)

@server.tool(
    name="get_authorization_urls",
    description="Return authorization URLs for services needing authentication.",
    input_schema={"type": "object", "properties": {}, "required": []},
)
async def get_authorization_urls_tool():
    return _safe_call(DASHBOARD.get_authorization_urls)

@server.tool(
    name="complete_oauth2_flow",
    description="Complete OAuth2 for a service using code + state.",
    input_schema={
        "type": "object",
        "properties": {
            "service_name": {"type": "string"},
            "authorization_code": {"type": "string"},
            "state": {"type": "string"},
        },
        "required": ["service_name", "authorization_code", "state"],
    },
)
async def complete_oauth2_flow_tool(service_name: str, authorization_code: str, state: str):
    ok = DASHBOARD.complete_oauth2_flow(service_name, authorization_code, state)
    if ok:
        return {"success": True, "message": f"OAuth2 flow completed for {service_name}"}
    return {"success": False, "error": f"Failed OAuth2 flow for {service_name}"}

@server.tool(
    name="revoke_service_authentication",
    description="Revoke stored OAuth2 token for a service.",
    input_schema={"type": "object", "properties": {"service_name": {"type": "string"}}, "required": ["service_name"]},
)
async def revoke_service_authentication_tool(service_name: str):
    DASHBOARD.revoke_service_authentication(service_name)
    return {"success": True, "message": f"Revoked {service_name}"}

def _auth_guard(service_name: str):
    if not DASHBOARD.config.oauth2_manager.is_authenticated(service_name):
        return {"success": False, "error": f"Service '{service_name}' not authenticated"}
    return None

@server.tool(
    name="crm_create_lead",
    description="Create a CRM lead (Salesforce).",
    input_schema={
        "type": "object",
        "properties": {
            "FirstName": {"type": "string"},
            "LastName": {"type": "string"},
            "Company": {"type": "string"},
            "Email": {"type": "string"},
        },
        "required": ["FirstName", "LastName", "Company", "Email"],
    },
)
async def crm_create_lead_tool(FirstName: str, LastName: str, Company: str, Email: str):  # noqa
    guard = _auth_guard("salesforce")
    if guard:
        return guard
    return _safe_call(DASHBOARD.crm.create_lead, {
        "FirstName": FirstName,
        "LastName": LastName,
        "Company": Company,
        "Email": Email,
    })

@server.tool(
    name="crm_get_leads",
    description="List CRM leads (limit).",
    input_schema={"type": "object", "properties": {"limit": {"type": "integer", "default": 20}}, "required": []},
)
async def crm_get_leads_tool(limit: int = 20):
    guard = _auth_guard("salesforce")
    if guard:
        return guard
    return _safe_call(DASHBOARD.crm.get_all_leads, limit=limit)

@server.tool(
    name="store_get_orders",
    description="Fetch Shopify orders.",
    input_schema={
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "limit": {"type": "integer", "default": 20},
        },
        "required": [],
    },
)
async def store_get_orders_tool(status: Optional[str] = None, limit: int = 20):
    guard = _auth_guard("shopify")
    if guard:
        return guard
    return _safe_call(DASHBOARD.store.get_orders, status=status, limit=limit)

@server.tool(
    name="marketing_get_contacts",
    description="Fetch HubSpot contacts.",
    input_schema={"type": "object", "properties": {"limit": {"type": "integer", "default": 20}}, "required": []},
)
async def marketing_get_contacts_tool(limit: int = 20):
    guard = _auth_guard("hubspot")
    if guard:
        return guard
    return _safe_call(DASHBOARD.marketing.get_contacts, limit=limit)

@server.tool(
    name="support_get_tickets",
    description="Fetch Zendesk tickets.",
    input_schema={
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "priority": {"type": "string"},
        },
        "required": [],
    },
)
async def support_get_tickets_tool(status: Optional[str] = None, priority: Optional[str] = None):
    guard = _auth_guard("zendesk")
    if guard:
        return guard
    return _safe_call(DASHBOARD.support.get_tickets, status=status, priority=priority)

@server.tool(
    name="appointments_get_events",
    description="Fetch Calendly events.",
    input_schema={"type": "object", "properties": {"count": {"type": "integer", "default": 10}}, "required": []},
)
async def appointments_get_events_tool(count: int = 10):
    guard = _auth_guard("calendly")
    if guard:
        return guard
    return _safe_call(DASHBOARD.appointments.get_events, count=count)

@server.tool(
    name="erp_fetch_inventory",
    description="Fetch ERP inventory (by item_id or item_name).",
    input_schema={
        "type": "object",
        "properties": {
            "item_id": {"type": "string"},
            "item_name": {"type": "string"},
        },
        "required": [],
    },
)
async def erp_fetch_inventory_tool(item_id: Optional[str] = None, item_name: Optional[str] = None):
    return _safe_call(DASHBOARD.erp.fetch_inventory, item_id=item_id, item_name=item_name)

@server.tool(
    name="slack_send_message",
    description="Send Slack message (requires Slack OAuth2).",
    input_schema={
        "type": "object",
        "properties": {
            "channel": {"type": "string", "default": "#general"},
            "text": {"type": "string"},
        },
        "required": ["text"],
    },
)
async def slack_send_message_tool(text: str, channel: Optional[str] = None):
    guard = _auth_guard("slack")
    if guard:
        return guard
    return _safe_call(DASHBOARD.slack.send_message, channel or CONFIG.slack_channel, text)

# Additional tools
@server.tool(
    name="crm_convert_lead",
    description="Convert a Salesforce lead to an opportunity.",
    input_schema={"type": "object", "properties": {"lead_id": {"type": "string"}}, "required": ["lead_id"]},
)
async def crm_convert_lead_tool(lead_id: str):
    guard = _auth_guard("salesforce")
    if guard:
        return guard
    return _safe_call(DASHBOARD.crm.convert_lead, lead_id)

@server.tool(
    name="support_create_ticket",
    description="Create a Zendesk ticket.",
    input_schema={
        "type": "object",
        "properties": {
            "subject": {"type": "string"},
            "comment": {"type": "string"},
        },
        "required": ["subject", "comment"],
    },
)
async def support_create_ticket_tool(subject: str, comment: str):
    guard = _auth_guard("zendesk")
    if guard:
        return guard
    return _safe_call(DASHBOARD.support.create_ticket, {"subject": subject, "comment": comment})

@server.tool(
    name="slack_send_alert",
    description="Send a Slack alert message (urgent optional).",
    input_schema={
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "urgent": {"type": "boolean", "default": False},
            "channel": {"type": "string"},
        },
        "required": ["message"],
    },
)
async def slack_send_alert_tool(message: str, urgent: bool = False, channel: Optional[str] = None):
    guard = _auth_guard("slack")
    if guard:
        return guard
    return _safe_call(DASHBOARD.slack.send_alert, message, urgent, channel or CONFIG.slack_channel)

@server.tool(
    name="introspect_tools",
    description="List available tools (static metadata).",
    input_schema={"type": "object", "properties": {}, "required": []},
)
async def introspect_tools_tool():
    # Minimal metadata; if using real MCP library it may already expose this.
    return {
        "success": True,
        "tools": [
            "get_dashboard_summary","get_authentication_status","get_authorization_urls","complete_oauth2_flow","revoke_service_authentication",
            "crm_create_lead","crm_get_leads","crm_convert_lead","store_get_orders","marketing_get_contacts","support_get_tickets","support_create_ticket",
            "appointments_get_events","erp_fetch_inventory","slack_send_message","slack_send_alert"
        ]
    }

async def main():
    # Prefer real MCP server run loop if available
    if hasattr(server, "run_stdio"):
        await server.run_stdio()
    else:  # Fallback
        print("MCP server object missing run_stdio")

if __name__ == "__main__":
    asyncio.run(main())
