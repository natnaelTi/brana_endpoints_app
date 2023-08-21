import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, getdate, add_days

@frappe.whitelist()
def subscribe_user(subscription_level, user):
    # Check if the Subscription Level exists
    if not frappe.db.exists("Subscription Level", subscription_level):
        frappe.throw(_("Subscription Level {0} does not exist").format(subscription_level))

    # Check if the User Profile exists
    if not frappe.db.exists("User Profile", user):
        frappe.throw(_("User Profile {0} does not exist").format(user))

    # Check if the user is already subscribed to the Subscription Level
    if frappe.db.exists("Subscription Plan", {"subscription_level": subscription_level, "user_profile": user}):
        frappe.throw(_("User {0} is already subscribed to the Subscription Level {1}").format(user, subscription_level))

    # Create a new Subscription Plan document
    subscription_plan = frappe.new_doc("Subscription Plan")
    subscription_plan.subscription_level = subscription_level
    subscription_plan.user_profile = user
    subscription_plan.start_date = nowdate()
    subscription_plan.end_date = add_days(nowdate(), 30)  # Assuming a 30-day subscription period
    subscription_plan.payment_amount = frappe.get_value("Subscription Level", subscription_level, "monthly_price")
    subscription_plan.insert()

    frappe.msgprint(_("User {0} subscribed successfully to the Subscription Level {1}").format(user, subscription_level))

@frappe.whitelist()
def create_subscription_plan(data):
    data = frappe.parse_json(data)

    subscription_plan = frappe.new_doc("Subscription Plan")
    subscription_plan.update(data)
    subscription_plan.insert()

    frappe.msgprint(_("Subscription Plan {0} created successfully").format(subscription_plan.name))

@frappe.whitelist()
def update_subscription_plan(data):
    data = frappe.parse_json(data)

    subscription_plan = frappe.get_doc("Subscription Plan", data.get("name"))
    subscription_plan.update(data)
    subscription_plan.save()

    frappe.msgprint(_("Subscription Plan {0} updated successfully").format(subscription_plan.name))

@frappe.whitelist()
def cancel_subscription_plan(name):
    subscription_plan = frappe.get_doc("Subscription Plan", name)
    
    # Check if the subscription plan is already cancelled
    if subscription_plan.status == "Cancelled":
        frappe.throw(_("Subscription Plan {0} is already cancelled").format(name))

    # Set the subscription plan as cancelled
    subscription_plan.status = "Cancelled"
    subscription_plan.save()

    frappe.msgprint(_("Subscription Plan {0} cancelled successfully").format(name))