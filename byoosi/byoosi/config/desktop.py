# Configuration settings for the desktop interface of the Frappe application

from frappe import _

def get_data():
    return [
        {
            "module_name": "Byoosi",
            "type": "module",
            "label": _("Byoosi"),
            "icon": "octicon octicon-file-directory",
            "color": "grey",
            "description": _("Manage your Byoosi website."),
            "permissions": [{"permission": "read", "role": "All"}],
        }
    ]