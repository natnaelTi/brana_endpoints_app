import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, add_days

class SubscriptionLevel(Document):
    def __init__(self, *args, **kwargs):
        super(SubscriptionLevel, self).__init__(*args, **kwargs)
        self.setup_fields()

    def send_notification_email(user, remaining_days):
        email_domain = frappe.get_value("Email Domain", None, "domain_name")
        sender = frappe.session.user
        recipient = frappe.get_value("User", user, "email_id")
        subject = "Subscription Level Change Notification"
        message = "Your subscription level has been updated. You have {} days remaining in your current subscription plan.".format(remaining_days)

        frappe.sendmail(
            recipients=recipient,
            sender=sender,
            subject=subject,
            message=message,
            delayed=False,
            retry=False,
            email_id=None,
            reference_doctype=None,
            reference_name=None,
            unsubscribe_message=False,
            unsubscribe_option=False,
            inline_images=[],
            header=[],
            print_letterhead=False,
            communication=None,
            now=False,
            email_account=None,
            email_domain=email_domain
        )

    def validate(self):
        # Check if all fields have values
        if not self.monthly_price or not self.annual_price or not self.access_frequency:
            frappe.throw("Please enter values for all fields")

    def on_submit(self):
        # Set the document as active
        self.status = "Active"

    def on_cancel(self):
        # Check if the Subscription Level is linked to any Audiobooks or Podcasts
        if frappe.db.exists("Audiobook", {"subscription_level": self.name}) or frappe.db.exists("Podcast", {"subscription_level": self.name}):
            frappe.throw("Cannot cancel the Subscription Level as it is linked to Audiobooks or Podcasts")
        
        # Check if any users are currently subscribed to this Subscription Level
        if frappe.db.exists("Subscription Plan", {"subscription_level": self.name, "status": "Active"}):
            frappe.throw("Cannot cancel the Subscription Level as there are active subscribers")

        # Set the document as cancelled
        self.status = "Cancelled"

    def on_trash(self):
        # Check if the Subscription Level is linked to any Audiobooks or Podcasts
        if frappe.db.exists("Audiobook", {"subscription_level": self.name}) or frappe.db.exists("Podcast", {"subscription_level": self.name}):
            frappe.throw("Cannot delete the Subscription Level as it is linked to Audiobooks or Podcasts")
        
        # Check if any users are currently subscribed to this Subscription Level
        if frappe.db.exists("Subscription Plan", {"subscription_level": self.name, "status": "Active"}):
            frappe.throw("Cannot delete the Subscription Level as there are active subscribers")

        # Delete related Subscription Plans
        frappe.delete_doc("Subscription Plan", {"subscription_level": self.name})

    def on_update(self):
        # Update the Access Frequency in Subscription Level whenever a User subscribes to it
        users_subscribed = frappe.get_all(
            "Subscription Plan",
            filters={"subscription_level": self.name, "status": "Active"},
            fields=["user_profile"]
        )
        access_frequency = len(users_subscribed)
        frappe.db.set_value(
            "Subscription Level",
            self.name,
            "access_frequency",
            access_frequency
        )

        # Get the currently subscribed users
        subscribed_users = frappe.get_all(
            "Subscription Plan",
            filters={"subscription_level": self.name, "status": "Active"},
            fields=["user_profile"]
        )

        # Notify the subscribed users about the change via email and allow them to continue using the app until their subscription plan expires
        for user in subscribed_users:
            user_profile_doc = frappe.get_doc("User Profile", user.user_profile)
            remaining_days = (user_profile_doc.end_date - nowdate()).days
            if remaining_days > 0:
                send_notification_email(user_profile_doc.user, remaining_days)

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

