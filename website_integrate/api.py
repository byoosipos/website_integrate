import frappe
import json
from frappe import _

@frappe.whitelist(allow_guest=True)
def create_quotation(**kwargs):
    """Create a new quotation from website form submission
    
    Args:
        kwargs: Dictionary containing form_data with the following fields:
            - firstName (str): First name of the customer
            - lastName (str): Last name of the customer 
            - email (str): Email address
            - phone (str): Phone number
            - company (str, optional): Company name
            - productCategory (str): Product category
            - requirements (str): Customer requirements
            
    Returns:
        dict: Response containing:
            - success (bool): Whether request was successful
            - message (str): Response message
            - quotation_id (str, optional): ID of created quotation
    """
    # Add rate limiting
    if not frappe.cache().get_value(f"quote_request_{frappe.local.request.remote_addr}"):
        frappe.cache().set_value(
            f"quote_request_{frappe.local.request.remote_addr}",
            1,
            expires_in_sec=300  # 5 minutes
        )
    else:
        return {
            "success": False,
            "message": "Please wait before submitting another request"
        }

    try:
        # Get form data from kwargs
        form_data = kwargs
        
        # Remove any None or empty values
        form_data = {k: v for k, v in form_data.items() if v}
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'phone', 'productCategory', 'requirements']
        for field in required_fields:
            if field not in form_data:
                return {
                    'success': False,
                    'message': f'Missing required field: {field}'
                }

        # Validate form data
        valid, message = validate_form_data(form_data)
        if not valid:
            return {
                "success": False,
                "message": message
            }

        # Create a new lead
        lead = frappe.get_doc({
            "doctype": "Lead",
            "first_name": form_data.get('firstName'),
            "last_name": form_data.get('lastName'),
            "lead_name": f"{form_data.get('firstName')} {form_data.get('lastName')}",  # Required field
            "email_id": form_data.get('email'),
            "mobile_no": form_data.get('phone'),
            "company_name": form_data.get('company', ''),
            "source": "Website",
            "status": "Lead",
            "request_type": "Product Enquiry",
            "industry": map_industry(form_data.get('productCategory')),
            "_user_tags": form_data.get('productCategory'),  # Add product category as a tag
        })

        # Add notes about requirements
        if form_data.get('requirements'):
            lead.add_comment('Comment', text=f"""
Product Category: {form_data.get('productCategory')}
Requirements: {form_data.get('requirements')}
            """)

        lead.insert(ignore_permissions=True)
        frappe.db.commit()

        # Create opportunity
        opportunity = frappe.get_doc({
            "doctype": "Opportunity",
            "opportunity_from": "Lead",
            "party_name": lead.name,
            "title": f"Website Quote Request - {form_data.get('productCategory')}",
            "opportunity_type": "Sales",
            "source": "Website",
            "status": "Open",
            "with_items": 0  # Changed to 0 since no items are being added
        })
        opportunity.insert(ignore_permissions=True)
        frappe.db.commit()

        # Create quotation
        quotation = frappe.get_doc({
            "doctype": "Quotation",
            "quotation_to": "Lead",
            "party_name": lead.name,
            "order_type": "Sales",
            "opportunity": opportunity.name,
            "status": "Draft"
        })
        quotation.insert(ignore_permissions=True)
        frappe.db.commit()

        # Send notification
        send_quote_request_notification(quotation.name, form_data)

        return {
            "success": True,
            "message": "Quote request submitted successfully",
            "quotation_id": quotation.name
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Quote Request Error")
        return {
            "success": False,
            "message": str(e) if frappe.conf.developer_mode else "Error processing quote request"
        }

def send_quote_request_notification(quotation_id, form_data):
    try:
        # Add HTML formatting for better email presentation
        message = frappe.render_template(
            "templates/emails/quote_request.html",
            {
                "form_data": form_data,
                "quotation_id": quotation_id,
                "site_url": frappe.utils.get_url()
            }
        )
        
        # Get recipients from DocType instead of hardcoded roles
        recipients = frappe.get_all(
            "Sales Team Member",
            filters={"enabled": 1},
            fields=["email"]
        )
        
        if not recipients:
            recipients = [{"email": frappe.get_value("System Settings", None, "admin_email_address")}]
            
        frappe.sendmail(
            recipients=[r.email for r in recipients],
            subject=f"New Quote Request: {form_data.get('firstName')} {form_data.get('lastName')}",
            message=message,
            now=True,
            send_priority=1,
            reference_doctype="Quotation",
            reference_name=quotation_id
        )
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Quote Request Notification Error")

def validate_form_data(form_data):
    # Validate email format
    if not frappe.utils.validate_email_address(form_data.get('email')):
        return False, "Invalid email address"
        
    # Validate phone number (Nigerian format)
    phone = form_data.get('phone', '').strip()
    if not phone or len(phone) < 10:
        return False, "Invalid phone number. Please enter a valid Nigerian phone number"
    
    # Validate name length
    if len(form_data.get('firstName', '')) < 2:
        return False, "First name is too short"
    if len(form_data.get('lastName', '')) < 2:
        return False, "Last name is too short"
    
    # Validate product category
    valid_categories = ["Cold Room Solutions", "Blast Freezers", "Additional Products", "Support Products"]
    if form_data.get('productCategory') not in valid_categories:
        return False, "Invalid product category"
    
    # Validate requirements length
    if len(form_data.get('requirements', '')) < 10:
        return False, "Please provide more details about your requirements"
        
    return True, ""

def map_industry(product_category):
    """Map product category to appropriate industry"""
    industry_map = {
        "Cold Room Solutions": "Cold Chain",
        "Blast Freezers": "Food Processing",
        "Additional Products": "General",
        "Support Products": "Services"
    }
    return industry_map.get(product_category, "Other Industry")

# Add any other necessary helper functions here 