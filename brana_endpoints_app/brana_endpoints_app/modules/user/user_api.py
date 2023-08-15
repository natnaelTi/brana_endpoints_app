# brana_endpoints_app/brana_endpoints_app/modules/user/user_api.py
import frappe
from frappe import _
from frappe.utils import cstr, get_url, random_string, validate_email_add

@frappe.whitelist(allow_guest=True)
def login(identifier, password):
    # Validate the identifier and password
    if not identifier or not password:
        frappe.throw(_("Please enter the identifier and password."))

    # Find the user based on the identifier
    user = frappe.get_all(
        "User",
        filters={"enabled": 1, "name": identifier},
        fields=["name", "email", "phone"]
    )

    if not user:
        user = frappe.get_all(
            "User",
            filters={"enabled": 1, "email": identifier},
            fields=["name", "email", "phone"]
        )

    if not user:
        user = frappe.get_all(
            "User",
            filters={"enabled": 1, "phone": identifier},
            fields=["name", "email", "phone"]
        )

    if not user or not frappe.local.login_manager.check_password(user[0].name, password):
        frappe.throw(_("Invalid identifier or password."))

    user = frappe.get_doc("User", user[0].name)

    # Create a new session for the user
    frappe.local.login_manager.login_as(user.name)

    return {
        "user": user.name,
        "full_name": user.get_full_name(),
        "email": user.email,
        # Add other user details as needed
    }

@frappe.whitelist()
def logout():
    # Perform logout logic
    frappe.local.login_manager.logout()

    return {
        "message": "Logged out successfully."
    }