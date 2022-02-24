from . import __version__ as app_version  # noqa

app_name = "pms_app_frappe"
app_title = "PMS App Frappe"
app_publisher = "Leam Technology Systems"
app_description = "PMS Frappe App"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@leam.ae"
app_license = "MIT"

# Includes in <head>
# ------------------
renovation_app = "pms_app"

graphql_sdl_dir = [
    "pms_app/utils/graphql/types",
    "pms_app/pms_core/graphql/types",
    "pms_app/properties/graphql/types",
]

graphql_schema_processors = [
    "pms_app.pms_core.graphql.bind_resolvers"
]

# include js, css files in header of desk.html
# app_include_css = "/assets/pms_app_frappe/css/pms_app_frappe.css"
# app_include_js = "/assets/pms_app_frappe/js/pms_app_frappe.js"

# include js, css files in header of web template
# web_include_css = "/assets/pms_app_frappe/css/pms_app_frappe.css"
# web_include_js = "/assets/pms_app_frappe/js/pms_app_frappe.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "pms_app_frappe/public/scss/website"

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

# Installation
# ------------

# before_install = "pms_app_frappe.install.before_install"
# after_install = "pms_app_frappe.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "pms_app_frappe.uninstall.before_uninstall"
# after_uninstall = "pms_app_frappe.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "pms_app_frappe.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"pms_app_frappe.tasks.all"
# 	],
# 	"daily": [
# 		"pms_app_frappe.tasks.daily"
# 	],
# 	"hourly": [
# 		"pms_app_frappe.tasks.hourly"
# 	],
# 	"weekly": [
# 		"pms_app_frappe.tasks.weekly"
# 	]
# 	"monthly": [
# 		"pms_app_frappe.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "pms_app_frappe.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "pms_app_frappe.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "pms_app_frappe.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {
        "doctype": "{doctype_4}"
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"pms_app_frappe.auth.validate"
# ]
