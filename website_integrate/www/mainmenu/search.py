import frappe
from frappe import _

def get_context(context):
    try:
        search_query = frappe.form_dict.get('q', '').strip()
        context.search_query = search_query
        context.no_cache = 1
        
        if not search_query:
            context.results = []
            return context
        
        # Search in products
        products = frappe.get_all(
            "Item",
            filters=[
                ["name", "like", f"%{search_query}%"],
                ["is_published", "=", 1]
            ],
            fields=["name", "item_name", "description", "image", "route"],
            limit=10
        )
        
        # Search in blog posts
        blog_posts = frappe.get_all(
            "Blog Post",
            filters=[
                ["published", "=", 1],
                ["title", "like", f"%{search_query}%"]
            ],
            fields=["title", "blog_intro", "route", "published_on"],
            limit=5
        )
        
        # Search in services
        services = frappe.get_all(
            "Service",
            filters=[
                ["title", "like", f"%{search_query}%"],
                ["published", "=", 1]
            ],
            fields=["title", "description", "route"],
            limit=5
        )
        
        context.results = {
            "products": products,
            "blog_posts": blog_posts,
            "services": services,
            "total_count": len(products) + len(blog_posts) + len(services)
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Search Error")
        context.error = _("An error occurred while searching. Please try again.")
        
    return context 