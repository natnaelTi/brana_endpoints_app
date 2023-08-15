
from frappe import _
from frappe.model.document import Document

class SubscriptionLevel(Document):
    def validate(self):
        # Perform any validation or custom logic here
        pass

    # Define fields of the Subscription Level doctype
    def setup_fields(self):
        self.meta.get_field("name").label = _("Name")
        self.meta.get_field("name").reqd = True

        self.meta.get_field("monthly_price").label = _("Monthly Price")
        self.meta.get_field("monthly_price").fieldtype = "Currency"
        self.meta.get_field("monthly_price").reqd = True

        self.meta.get_field("annual_price").label = _("Annual Price")
        self.meta.get_field("annual_price").fieldtype = "Currency"
        self.meta.get_field("annual_price").reqd = True

        self.meta.get_field("access_frequency").label = _("Access Frequency")
        self.meta.get_field("access_frequency").fieldtype = "Int"
        self.meta.get_field("access_frequency").reqd = True

    # Define other methods and properties as needed

