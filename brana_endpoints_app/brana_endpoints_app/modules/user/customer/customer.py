
# brana_endpoints_app/brana_endpoints_app/modules/user/customer/customer.py
from frappe import _
import frappe
from frappe.model.document import Document

class Customer(Document):
    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)
        self.setup_fields()

    def validate(self):
        # Perform any validation or custom logic here
        pass

    def on_submit(self):
        # Perform actions when the Customer is submitted
        pass

    def on_cancel(self):
        # Perform actions when the Customer is cancelled
        pass

    # Define fields of the Customer doctype
    def setup_fields(self):
        self.meta.get_field("user_profile").label = _("User Profile")
        self.meta.get_field("user_profile").fieldtype = "Link"
        self.meta.get_field("user_profile").options = "User Profile"
        self.meta.get_field("user_profile").reqd = True

        self.meta.get_field("billing_address").label = _("Billing Address")
        self.meta.get_field("billing_address").fieldtype = "Link"
        self.meta.get_field("billing_address").options = "Address"

        self.meta.get_field("shipping_address").label = _("Shipping Address")
        self.meta.get_field("shipping_address").fieldtype = "Link"
        self.meta.get_field("shipping_address").options = "Address"

