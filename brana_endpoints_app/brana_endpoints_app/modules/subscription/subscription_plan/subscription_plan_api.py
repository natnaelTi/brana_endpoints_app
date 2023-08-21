import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, getdate, add_days
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry

@frappe.whitelist()
def subscribe_user(subscription_level, user, payment_option):
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

    # Set the payment amount based on the chosen payment option
    monthly_price = frappe.get_value("Subscription Level", subscription_level, "monthly_price")
    annual_price = frappe.get_value("Subscription Level", subscription_level, "annual_price")

    if payment_option == "monthly":
        subscription_plan.payment_amount = monthly_price
    elif payment_option == "annual":
        subscription_plan.payment_amount = annual_price
    else:
        frappe.throw(_("Invalid payment option"))

    # Make Payment using ERPNext's payment processing methods
    payment_entry = get_payment_entry(
        doctype="Subscription Plan",
        docname=subscription_plan.name,
        party_type="Customer",
        party=subscription_plan.user_profile,
        mode_of_payment=payment_option,
        paid_amount=subscription_plan.payment_amount,
        reference_dt="Subscription Plan",
        reference_dn=subscription_plan.name,
        reference_name=subscription_plan.name,
        account=None,
        company=frappe.defaults.get_user_default("company"),
    )

    try:
        payment_entry.submit()
        subscription_plan.status = "Active"
        frappe.msgprint(_("Payment processed successfully. User {0} subscribed to the Subscription Level {1}").format(user, subscription_level))
    except frappe.exceptions.ValidationError:
        subscription_plan.status = "Disabled"
        frappe.msgprint(_("Payment failed. User {0} subscription to the Subscription Level {1} is disabled").format(user, subscription_level))
        send_payment_failure_notification(user, subscription_level)

    subscription_plan.insert()

def send_payment_failure_notification(user, subscription_level):
    # Email notification logic for payment failure
    pass

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