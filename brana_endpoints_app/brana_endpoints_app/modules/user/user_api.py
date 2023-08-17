# brana_endpoints_app/brana_endpoints_app/modules/user/user_api.py
import frappe
from frappe import _
from frappe.utils import cstr, get_url, random_string, validate_email_add
import requests
import logging

logger = logging.getLogger(__name__)

# Constants for rate limiting
MAX_REQUESTS_PER_MINUTE = 10

@frappe.whitelist(allow_guest=True)
def login(identifier, password, captcha_response):
    # Validate the identifier and password
    if not identifier or not password:
        frappe.throw(_("Please enter the identifier and password."))

    # Rate Limiting: Check if the client has exceeded the maximum number of requests per minute
    if is_rate_limited():
        frappe.throw(_("Too many requests. Please try again later."))

    # CAPTCHA Verification: Check if the CAPTCHA response is valid
    if not verify_captcha(captcha_response):
        frappe.throw(_("Invalid CAPTCHA. Please try again."))

    # Find the user based on the identifier
    users = frappe.get_all(
        "User",
        filters={"enabled": 1},
        fields=["name", "email", "phone"]
    )

    matching_users = []

    for user in users:
        if user.name == identifier or user.email == identifier or user.phone == identifier:
            matching_users.append(user)

    if not matching_users:
        frappe.throw(_("Invalid identifier or password."))

    user = None

    for matching_user in matching_users:
        if frappe.local.login_manager.check_password(matching_user.name, password):
            user = matching_user
            break

    if not user:
        # Rate Limiting: Increment the request count for failed login attempts
        increment_request_count()

        frappe.throw(_("Invalid identifier or password."))

    user_doc = frappe.get_doc("User", user.name)

    # Retrieve the User Profile document
    user_profile = frappe.get_value("User Profile", {"user": user_doc.name}, ["name", "wish_list", "listening_history"], as_dict=True)

    # Create a new session for the user
    frappe.local.login_manager.login_as(user_doc.name)

    # Log the successful login
    logger.info(f"User '{user_doc.name}' logged in successfully.")

    # Reset the request count for successful login
    reset_request_count()

    return {
        "user": user_doc.name,
        "first_name": user_doc.get_first_name(),
        "last_name": user_doc.get_last_name(),
        "email": user_doc.email,
        "user_profile": user_profile
        # Add other user details as needed
    }

@frappe.whitelist()
def logout():
    # Perform logout logic
    frappe.local.login_manager.logout()

    # Log the logout
    logger.info("User logged out successfully.")

    return {
        "message": "Logged out successfully."
    }

def is_rate_limited():
    # Get the client's IP address (assuming Frappe request object is available)
    client_ip = frappe.request_ip

    # Get the current timestamp
    current_time = frappe.utils.now_datetime()

    # Get the rate limit data for the client
    rate_limit_data = frappe.cache().hget("rate_limit", client_ip) or {}

    # Check if the client has exceeded the maximum number of requests per minute
    if rate_limit_data.get("count", 0) >= MAX_REQUESTS_PER_MINUTE:
        return True

    return False

def increment_request_count():
    # Get the client's IP address (assuming Frappe request object is available)
    client_ip = frappe.request_ip

    # Get the current timestamp
    current_time = frappe.utils.now_datetime()

    # Get the rate limit data for the client
    rate_limit_data = frappe.cache().hget("rate_limit", client_ip) or {}

    # Increment the request count
    rate_limit_data["count"] = rate_limit_data.get("count", 0) + 1

    # Update the rate limit data in the cache
    frappe.cache().hset("rate_limit", client_ip, rate_limit_data)

def reset_request_count():
    # Get the client's IP address (assuming Frappe request object is available)
    client_ip = frappe.request_ip

    # Remove the rate limit data for the client
    frappe.cache().hdel("rate_limit", client_ip)

def verify_captcha(captcha_response):
    # Implement CAPTCHA verification logic here
    # Return True if the CAPTCHA response is valid, False otherwise
    # You can use a third-party CAPTCHA service or your own implementation

    # Set your reCAPTCHA secret key
    recaptcha_secret_key = "YOUR_RECAPTCHA_SECRET_KEY"
    
    payload = {
        "secret": recaptcha_secret_key,
        "response": captcha_response
    }

    response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    recaptcha_result = response.json()

    if recaptcha_result.get("success"):
        return True
    else:
        return False