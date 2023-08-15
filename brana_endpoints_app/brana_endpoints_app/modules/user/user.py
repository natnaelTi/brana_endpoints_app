
# brana_endpoints_app/brana_endpoints_app/modules/user/user.py
from frappe import _
import frappe
from frappe.model.document import Document

class User(Document):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.setup_fields()

    def validate(self):
        # Perform any validation or custom logic here
        pass

    def on_submit(self):
        # Perform actions when the User is submitted
        pass

    def on_cancel(self):
        # Perform actions when the User is cancelled
        pass

    # Define fields of the User doctype
    def setup_fields(self):
        self.meta.get_field("first_name").label = _("First Name")
        self.meta.get_field("first_name").reqd = True

        self.meta.get_field("last_name").label = _("Last Name")
        self.meta.get_field("last_name").reqd = True

        self.meta.get_field("email").label = _("Email")
        self.meta.get_field("email").reqd = True

        self.meta.get_field("phone_number").label = _("Phone Number")

        self.meta.get_field("enabled").label = _("Enabled")
        self.meta.get_field("enabled").fieldtype = "Check"
        self.meta.get_field("enabled").reqd = True

        self.meta.get_field("password").label = _("Password")
        self.meta.get_field("password").fieldtype = "Password"
        self.meta.get_field("password").reqd = True

        self.meta.get_field("user_type").label = _("User Type")
        self.meta.get_field("user_type").fieldtype = "Select"
        self.meta.get_field("user_type").options = ["Type 1", "Type 2", "Type 3"]
        self.meta.get_field("user_type").reqd = True

        self.meta.get_field("roles").label = _("Roles")
        self.meta.get_field("roles").fieldtype = "Table MultiSelect"
        self.meta.get_field("roles").options = "Role"
        
        self.meta.get_field("user_permissions").label = _("User Permissions")
        self.meta.get_field("user_permissions").fieldtype = "Table MultiSelect"
        self.meta.get_field("user_permissions").options = "User Permission"

        self.meta.get_field("doctype_roles").label = _("Doctype Roles")
        self.meta.get_field("doctype_roles").fieldtype = "Table"
        self.meta.get_field("doctype_roles").options = "Doctype Role"

        self.meta.get_field("language").label = _("Language")
        self.meta.get_field("language").fieldtype = "Link"
        self.meta.get_field("language").options = "Language"

        self.meta.get_field("send_welcome_email").label = _("Send Welcome Email")
        self.meta.get_field("send_welcome_email").fieldtype = "Check"

        self.meta.get_field("home_settings").label = _("Home Settings")
        self.meta.get_field("home_settings").fieldtype = "Table"
        self.meta.get_field("home_settings").options = "Home Setting"

        self.meta.get_field("redirect_to").label = _("Redirect To")
        self.meta.get_field("redirect_to").fieldtype = "Link"
        self.meta.get_field("redirect_to").options = "Redirect To"

        self.meta.get_field("redirect_after_login").label = _("Redirect After Login")
        self.meta.get_field("redirect_after_login").fieldtype = "Link"
        self.meta.get_field("redirect_after_login").options = "Redirect After Login"

        self.meta.get_field("google_calendar").label = _("Google Calendar")
        self.meta.get_field("google_calendar").fieldtype = "Link"
        self.meta.get_field("google_calendar").options = "Google Calendar"

        self.meta.get_field("google_contacts").label = _("Google Contacts")
        self.meta.get_field("google_contacts").fieldtype = "Link"
        self.meta.get_field("google_contacts").options = "Google Contacts"

        self.meta.get_field("google_drive").label = _("Google Drive")
        self.meta.get_field("google_drive").fieldtype = "Link"
        self.meta.get_field("google_drive").options = "Google Drive"

        self.meta.get_field("last_login").label = _("Last Login")
        self.meta.get_field("last_login").fieldtype = "Datetime"

        self.meta.get_field("last_active").label = _("Last Active")
        self.meta.get_field("last_active").fieldtype = "Datetime"

        self.meta.get_field("creation_date").label = _("Creation Date")
        self.meta.get_field("creation_date").fieldtype = "Datetime"

        self.meta.get_field("last_modified").label = _("Last Modified")

