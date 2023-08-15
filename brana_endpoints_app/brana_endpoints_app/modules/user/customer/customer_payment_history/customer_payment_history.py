
# user/customer/customer_payment_history/customer_payment_history.py
from frappe import _
from frappe.model.document import Document

class CustomerPaymentHistory(Document):
    def validate(self):
        # Perform any validation or custom logic here
        pass

    # Define fields of the Customer Payment History doctype
    def setup_fields(self):
        self.meta.get_field("customer").label = _("Customer")
        self.meta.get_field("customer").fieldtype = "Link"
        self.meta.get_field("customer").options = "Customer"
        self.meta.get_field("customer").reqd = True

        self.meta.get_field("transaction_date").label = _("Transaction Date")
        self.meta.get_field("transaction_date").fieldtype = "Date"
        self.meta.get_field("transaction_date").reqd = True

        self.meta.get_field("transaction_amount").label = _("Transaction Amount")
        self.meta.get_field("transaction_amount").fieldtype = "Currency"
        self.meta.get_field("transaction_amount").reqd = True

        self.meta.get_field("transaction_status").label = _("Transaction Status")
        self.meta.get_field("transaction_status").fieldtype = "Select"
        self.meta.get_field("transaction_status").options = [
            {"label": _("Pending"), "value": "pending"},
            {"label": _("Paid"), "value": "paid"},
            {"label": _("Failed"), "value": "failed"},
            {"label": _("Reversed"), "value": "reversed"}
        ]
        self.meta.get_field("transaction_status").reqd = True

        self.meta.get_field("payment_method").label = _("Payment Method")
        self.meta.get_field("payment_method").fieldtype = "Select"
        self.meta.get_field("payment_method").options = [
            {"label": _("Credit Card"), "value": "Credit Card"},
            {"label": _("PayPal"), "value": "PayPal"},
            {"label": _("Stripe"), "value": "Stripe"},
            {"label": _("Bank Transfer"), "value": "Bank Transfer"}
        ]
        self.meta.get_field("payment_method").reqd = True

        self.meta.get_field("invoice_number").label = _("Invoice Number")
        self.meta.get_field("invoice_number").fieldtype = "Data"
        self.meta.get_field("invoice_number").reqd = True

        self.meta.get_field("description").label = _("Description")
        self.meta.get_field("description").fieldtype = "Text Editor"
        self.meta.get_field("description").reqd = True

    # Define other methods and properties as needed

