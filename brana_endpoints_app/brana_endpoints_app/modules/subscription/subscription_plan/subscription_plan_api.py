import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, getdate, add_days
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
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

    # Get the current subscription plan of the user
    current_subscription_plan = frappe.get_all(
        "Subscription Plan",
        filters={"user_profile": user},
        fields=["name", "subscription_level", "start_date", "end_date", "payment_amount"],
        order_by="start_date desc",
        limit=1,
    )

    # Check if the user has an existing subscription plan
    if current_subscription_plan:
        current_subscription_plan = frappe.get_doc("Subscription Plan", current_subscription_plan[0].name)
        remaining_days = (getdate(current_subscription_plan.end_date) - getdate(nowdate())).days

        # Handle upgrade to a higher subscription level
        if subscription_level != current_subscription_plan.subscription_level:
            upgrade_payment_amount = calculate_upgrade_payment(
                current_subscription_plan.subscription_level,
                subscription_level,
                current_subscription_plan.payment_amount,
                remaining_days,
            )

            # Make Payment for the upgrade
            payment_entry = get_payment_entry(
                doctype="Subscription Plan",
                docname=current_subscription_plan.name,
                party_type="Customer",
                party=current_subscription_plan.user_profile,
                mode_of_payment=payment_option,
                paid_amount=upgrade_payment_amount,
                reference_dt="Subscription Plan",
                reference_dn=current_subscription_plan.name,
                reference_name=current_subscription_plan.name,
                account=None,
                company=frappe.defaults.get_user_default("company"),
            )

            try:
                payment_entry.submit()
                current_subscription_plan.status = "Disabled"
                current_subscription_plan.save(ignore_permissions=True)

                # Create a new Subscription Plan document for the upgraded level
                subscription_plan = frappe.new_doc("Subscription Plan")
                subscription_plan.subscription_level = subscription_level
                subscription_plan.user_profile = user
                subscription_plan.start_date = nowdate()
                subscription_plan.end_date = add_days(nowdate(), remaining_days)
                subscription_plan.payment_amount = upgrade_payment_amount
                subscription_plan.status = "Active"
                subscription_plan.insert(ignore_permissions=True)

                frappe.msgprint(_("Payment processed successfully. User {0} upgraded to Subscription Level {1}").format(user, subscription_level))
            except frappe.exceptions.ValidationError:
                frappe.msgprint(_("Payment failed. User {0} remains on the current Subscription Level {1}").format(user, current_subscription_plan.subscription_level))
                return

        # Handle downgrade to a lower subscription level
        elif subscription_level == current_subscription_plan.subscription_level:
            downgrade_payment_amount = calculate_downgrade_payment(
                current_subscription_plan.subscription_level,
                current_subscription_plan.payment_amount,
                remaining_days,
            )

            # Make Payment for the downgrade
            payment_entry = get_payment_entry(
                doctype="Subscription Plan",
                docname=current_subscription_plan.name,
                party_type="Customer",
                party=current_subscription_plan.user_profile,
                mode_of_payment=payment_option,
                paid_amount=downgrade_payment_amount,
                reference_dt="Subscription Plan",
                reference_dn=current_subscription_plan.name,
                reference_name=current_subscription_plan.name,
                account=None,
                company=frappe.defaults.get_user_default("company"),
            )

            try:
                payment_entry.submit()
                current_subscription_plan.status = "Disabled"
                current_subscription_plan.save(ignore_permissions=True)

                # Create a new Subscription Plan document for the downgraded level
                subscription_plan = frappe.new_doc("Subscription Plan")
                subscription_plan.subscription_level = subscription_level
                subscription_plan.user_profile = user
                subscription_plan.start_date = nowdate()
                subscription_plan.end_date = add_days(nowdate(), remaining_days)
                subscription_plan.payment_amount = downgrade_payment_amount
                subscription_plan.status = "Active"
                subscription_plan.insert(ignore_permissions=True)

                frappe.msgprint(_("Payment processed successfully. User {0} downgraded to Subscription Level {1}").format(user, subscription_level))
            except frappe.exceptions.ValidationError:
                frappe.msgprint(_("Payment failed. User {0} remains on the current Subscription Level {1}").format(user, current_subscription_plan.subscription_level))
                return

    else:
        # Create a new Subscription Plan document for the user
        subscription_plan = frappe.new_doc("Subscription Plan")
        subscription_plan.subscription_level = subscription_level
        subscription_plan.user_profile = user
        subscription_plan.start_date = nowdate()
        subscription_plan.end_date = add_days(nowdate(), 30)  # Assuming a 30-day subscription period
        subscription_plan.payment_amount = calculate_payment_amount(subscription_level, payment_option)
        subscription_plan.status = "Active"
        subscription_plan.insert(ignore_permissions=True)

        frappe.msgprint(_("Payment processed successfully. User {0} subscribed to Subscription Level {1}").format(user, subscription_level))

def calculate_upgrade_payment(current_subscription_level, new_subscription_level, current_payment_amount, remaining_days):
    # Perform necessary calculations based on payment frequency, remaining days, etc.
    # ...

    upgrade_payment_amount = 0  # Calculate the required payment amount
    return upgrade_payment_amount

def calculate_downgrade_payment(current_subscription_level, current_payment_amount, remaining_days):
    # Perform necessary calculations based on payment frequency, remaining days, etc.
    # ...

    downgrade_payment_amount = 0  # Calculate the required payment amount
    return downgrade_payment_amount

def calculate_payment_amount(subscription_level, payment_option):
    # Perform necessary calculations based on subscription level and payment option
    # ...

    payment_amount = 0  # Calculate the payment amount
    return payment_amount

def send_payment_failure_notification(user, subscription_level):
    email_subject = "Payment Failure Notification"
    email_content = f"Dear {user},\n\nWe regret to inform you that the payment for your subscription to Subscription Level {subscription_level} has failed. Please update your payment information to continue enjoying your subscription.\n\nThank you,\nThe Subscription Management Team"

    frappe.sendmail(
        recipients=user,
        subject=email_subject,
        message=email_content,
    )

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