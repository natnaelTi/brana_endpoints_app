import frappe
from frappe import _
from frappe.utils.response import build_response

@frappe.whitelist(allow_guest=False)
def get_subscription_levels():
    # Fetch the list of Subscription Levels
    subscription_levels = frappe.get_all(
        "Subscription Level",
        fields=["name", "monthly_price", "annual_price", "access_frequency"],
        filters={"disabled": 0}
    )

    # Construct the response object
    response = {
        "subscription_levels": subscription_levels,
        "total_count": len(subscription_levels)
    }

    # Build and return the JSON response
    return build_response(response)