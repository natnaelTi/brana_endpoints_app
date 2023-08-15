# brana_endpoints_app/brana_endpoints_app/modules/user/user_profile/user_profile.py
from frappe import _
import frappe
from frappe.model.document import Document

class UserProfile(Document):
    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        self.setup_fields()

    def validate(self):
        # Perform any validation or custom logic here
        pass

    def on_submit(self):
        # Perform actions when the User Profile is submitted
        pass

    def on_cancel(self):
        # Perform actions when the User Profile is cancelled
        pass

    # Define fields of the User Profile doctype
    def setup_fields(self):
        self.meta.get_field("user").label = _("User")
        self.meta.get_field("user").fieldtype = "Link"
        self.meta.get_field("user").options = "User"
        self.meta.get_field("user").reqd = True

        self.meta.get_field("wish_list").label = _("Wish List")
        self.meta.get_field("wish_list").fieldtype = "Table"
        self.meta.get_field("wish_list").options = "Wish List Item"

        self.meta.get_field("listening_history").label = _("Listening History")
        self.meta.get_field("listening_history").fieldtype = "Table"
        self.meta.get_field("listening_history").options = "User Listening History"
