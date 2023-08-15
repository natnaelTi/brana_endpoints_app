
# modules/address/address.py
from frappe import _
from frappe.model.document import Document

class Address(Document):
    def validate(self):
        # Perform any validation or custom logic here
        pass

    # Define fields of the Address doctype
    def setup_fields(self):
        self.meta.get_field("address_line_1").label = _("Address Line 1")
        self.meta.get_field("address_line_1").fieldtype = "Data"
        self.meta.get_field("address_line_1").reqd = True

        self.meta.get_field("address_line_2").label = _("Address Line 2")
        self.meta.get_field("address_line_2").fieldtype = "Data"

        self.meta.get_field("city").label = _("City")
        self.meta.get_field("city").fieldtype = "Data"
        self.meta.get_field("city").reqd = True

        self.meta.get_field("state").label = _("State")
        self.meta.get_field("state").fieldtype = "Data"

        self.meta.get_field("postal_code").label = _("Postal Code")
        self.meta.get_field("postal_code").fieldtype = "Data"
        self.meta.get_field("postal_code").reqd = True

        self.meta.get_field("country").label = _("Country")
        self.meta.get_field("country").fieldtype = "Data"
        self.meta.get_field("country").reqd = True

    # Define other methods and properties as needed

