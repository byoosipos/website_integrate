import frappe
import requests
from frappe import _

@frappe.whitelist(allow_guest=True)
def request_payment():
    try:
        # Get request data
        data = frappe.request.get_json()
        
        # Relworx API configuration
        RELWORX_CONFIG = {
            'BASE_URL': 'https://payments.relworx.com/api',
            'API_KEY': '45ecb53c81fead.Rta8MNVQQhDS7s1J_hqIYw',
            'ACCOUNT_NO': 'RELC23A5AB148'
        }
        
        # Forward request to Relworx
        response = requests.post(
            f"{RELWORX_CONFIG['BASE_URL']}/mobile-money/request-payment",
            json=data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.relworx.v2',
                'Authorization': f"Bearer {RELWORX_CONFIG['API_KEY']}"
            }
        )
        
        return response.json()
        
    except Exception as e:
        frappe.log_error(f"Relworx Payment Error: {str(e)}")
        return {
            'success': False,
            'message': str(e)
        }

@frappe.whitelist(allow_guest=True)
def check_status(reference):
    try:
        # Relworx API configuration
        RELWORX_CONFIG = {
            'BASE_URL': 'https://payments.relworx.com/api',
            'API_KEY': '45ecb53c81fead.Rta8MNVQQhDS7s1J_hqIYw',
            'ACCOUNT_NO': 'RELC23A5AB148'
        }
        
        # Check payment status
        response = requests.get(
            f"{RELWORX_CONFIG['BASE_URL']}/mobile-money/transaction-status/{reference}",
            headers={
                'Accept': 'application/vnd.relworx.v2',
                'Authorization': f"Bearer {RELWORX_CONFIG['API_KEY']}"
            }
        )
        
        return response.json()
        
    except Exception as e:
        frappe.log_error(f"Relworx Status Check Error: {str(e)}")
        return {
            'success': False,
            'message': str(e)
        }

@frappe.whitelist(allow_guest=True)
def webhook():
    try:
        data = frappe.request.get_json()
        frappe.log_error(f"Relworx Webhook: {str(data)}", "Payment Webhook")
        return {'success': True}
    except Exception as e:
        frappe.log_error(f"Relworx Webhook Error: {str(e)}")
        return {
            'success': False,
            'message': str(e)
        } 