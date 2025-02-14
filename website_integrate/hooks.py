app_name = "website_integrate"
app_title = "Website Integration"
app_publisher = "DeKoolar"
app_description = "Website Integration for DeKoolar"
app_email = "info@dekoolar.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/website_integrate/css/website_integrate.css"
# app_include_js = "/assets/website_integrate/js/website_integrate.js"

# include js, css files in header of web template
# web_include_css = "/assets/website_integrate/css/website_integrate.css"
# web_include_js = "/assets/website_integrate/js/website_integrate.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "website_integrate/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Whitelist Blog Post for website
website_route_rules = [
    {"from_route": "/blog/<category>", "to_route": "Blog Post"},
]

has_website_permission = {
    "Blog Post": "frappe.website.doctype.blog_post.blog_post.has_website_permission"
}

# Allow guest access to Blog Post
website_generators = ["Blog Post"]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "website_integrate.utils.jinja_methods",
#	"filters": "website_integrate.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "website_integrate.install.before_install"
# after_install = "website_integrate.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "website_integrate.uninstall.before_uninstall"
# after_uninstall = "website_integrate.uninstall.after_uninstall"

# Integration Setup
# ------------------

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"website_integrate.tasks.all"
#	],
#	"daily": [
#		"website_integrate.tasks.daily"
#	],
#	"hourly": [
#		"website_integrate.tasks.hourly"
#	],
#	"weekly": [
#		"website_integrate.tasks.weekly"
#	],
#	"monthly": [
#		"website_integrate.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "website_integrate.install.before_tests"

