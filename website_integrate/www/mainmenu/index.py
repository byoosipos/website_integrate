import frappe

def get_context(context):
    context.hero_slides = frappe.get_all(
        "Blog Post",
        filters={
            "blog_category": "hero-slider",
            "published": 1
        },
        fields=["title", "blog_intro", "meta_image", "creation", "name"],
        order_by="creation asc",
        limit_page_length=5  # Limit to 5 most recent posts
    )
    return context