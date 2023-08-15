
from frappe import _
from frappe.model.document import Document

class SubscriptionPlan(Document):
    def validate(self):
        # Perform any validation or custom logic here
        pass

    # Define fields of the Subscription Plan doctype
    def setup_fields(self):
        self.meta.get_field("name").label = _("Name")
        self.meta.get_field("name").reqd = True

        self.meta.get_field("subscription_level").label = _("Subscription Level")
        self.meta.get_field("subscription_level").fieldtype = "Link"
        self.meta.get_field("subscription_level").options = "Subscription Level"
        self.meta.get_field("subscription_level").reqd = True

        self.meta.get_field("user_profile").label = _("User Profile")
        self.meta.get_field("user_profile").fieldtype = "Link"
        self.meta.get_field("user_profile").options = "User Profile"
        self.meta.get_field("user_profile").reqd = True

        self.meta.get_field("start_date").label = _("Start Date")
        self.meta.get_field("start_date").fieldtype = "Date"
        self.meta.get_field("start_date").reqd = True

        self.meta.get_field("end_date").label = _("End Date")
        self.meta.get_field("end_date").fieldtype = "Date"
        self.meta.get_field("end_date").reqd = True

        self.meta.get_field("payment_amount").label = _("Payment Amount")
        self.meta.get_field("payment_amount").fieldtype = "Currency"
        self.meta.get_field("payment_amount").reqd = True

    # Define other methods and properties as needed

