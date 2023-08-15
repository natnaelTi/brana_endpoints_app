
from frappe import _
import frappe
from frappe.model.document import Document

class Audiobook(Document):
    def __init__(self, *args, **kwargs):
        super(Audiobook, self).__init__(*args, **kwargs)
        self.setup_fields()

def validate(self):
        # Check if at least one Audiobook Chapter is associated
        if not self.get("chapters"):
            frappe.throw("At least one Audiobook Chapter is required.")

        # Validate required fields
        if not self.title:
            frappe.throw("Title is required.")
        if not self.author:
            frappe.throw("Author is required.")
        if not self.narrator:
            frappe.throw("Narrator is required.")
        if not self.subscription_level:
            frappe.throw("Subscription Level is required.")
        if not self.get(“audio_file”):
            frappe.throw("Sample Audio is required.")
        if not self.title:
            frappe.throw("Title is required.")
        if not self.total_listening_time:
            frappe.throw("Total Listening Time is required.")
        if not self.title:
            frappe.throw("Title is required.")
        if not self.licensing_cost:
            frappe.throw("Licensing Cost is required.")
        if not self.production_cost:
            frappe.throw("Production Cost is required.")
        if not self.royalty_percentage:
            frappe.throw("Royalty Percentage is required.")

        # Validate data types
        if not isinstance(self.licensing_cost, (int, float)):
            frappe.throw("Licensing Cost must be a number.")
        if not isinstance(self.production_cost, (int, float)):
            frappe.throw("Production Cost must be a number.")
        
        # Perform other validation checks
    
    def on_submit(self):
        # Add Licensing Cost and Production Cost to Direct Expenses account
        direct_expenses_account = "Direct Expenses"  # Replace with the appropriate account name
        
        # Create a Journal Entry
        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.voucher_type = "Journal Entry"
        journal_entry.company = self.company
        journal_entry.posting_date = frappe.utils.nowdate()
        journal_entry.append("accounts", {
            "account": direct_expenses_account,
            "debit_in_account_currency": self.licensing_cost + self.production_cost
        })
        journal_entry.append("accounts", {
            "account": direct_expenses_account,
            "credit_in_account_currency": self.licensing_cost
        })
        journal_entry.append("accounts", {
            "account": direct_expenses_account,
            "credit_in_account_currency": self.production_cost
        })
        journal_entry.save()
        journal_entry.submit()
    
    def on_cancel(self):
        # Subtract Licensing Cost and Production Cost from Direct Expenses account
        direct_expenses_account = "Direct Expenses"  # Replace with the appropriate account name
        
        # Create a Journal Entry for cancellation
        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.voucher_type = "Journal Entry"
        journal_entry.company = self.company
        journal_entry.posting_date = frappe.utils.nowdate()
        journal_entry.append("accounts", {
            "account": direct_expenses_account,
            "credit_in_account_currency": self.licensing_cost + self.production_cost
        })
        journal_entry.append("accounts", {
            "account": direct_expenses_account,
            "debit_in_account_currency": self.licensing_cost
        })
        journal_entry.append("accounts", {
            "account": direct_expenses_account,
            "debit_in_account_currency": self.production_cost
        })
        journal_entry.save()
        journal_entry.submit()

    def on_trash(self):
        # Perform necessary cleanup tasks before deleting the document
        # For example, delete related Audiobook Chapter documents
        frappe.delete_doc("Audiobook Chapter", filters={"audiobook": self.name})

def on_update(audiobook_id, new_title=None, new_author=None, new_narrator=None, new_subscription_level=None,
                     new_audio_file=None, new_total_listening_time=None, new_licensing_cost=None,
                     new_production_cost=None, new_royalty_percentage=None, new_chapters=None):
    audiobook = frappe.get_doc("Audiobook", {"audiobook_id": audiobook_id})

    if not audiobook:
        frappe.throw("Audiobook not found.")

    if new_title:
        audiobook.title = new_title
    if new_author:
        audiobook.author = new_author
    if new_narrator:
        audiobook.narrator = new_narrator
    if new_subscription_level:
        audiobook.subscription_level = new_subscription_level
    if new_audio_file:
        audiobook.audio_file = new_audio_file
    if new_total_listening_time:
        audiobook.total_listening_time = new_total_listening_time
    if new_licensing_cost:
        audiobook.licensing_cost = new_licensing_cost
    if new_production_cost:
        audiobook.production_cost = new_production_cost
    if new_royalty_percentage:
        audiobook.royalty_percentage = new_royalty_percentage
    if new_chapters:
        audiobook.chapters = []
        for chapter in new_chapters:
            audiobook.append("chapters", chapter)

    audiobook.save()

    # Define fields of the Audiobook doctype
    def setup_fields(self):
        self.meta.get_field("title").label = _("Title")
        self.meta.get_field("title").reqd = True

        self.meta.get_field("description").label = _("Description")

        self.meta.get_field("author").label = _("Author")
        self.meta.get_field("author").fieldtype = "Link"
        self.meta.get_field("author").options = "User Profile"
        self.meta.get_field("author").reqd = True

        self.meta.get_field("narrator").label = _("Narrator")
        self.meta.get_field("narrator").fieldtype = "Link"
        self.meta.get_field("narrator").options = "User Profile"
        self.meta.get_field("narrator").reqd = True

        self.meta.get_field("publisher").label = _("Publisher")
        self.meta.get_field("publisher").fieldtype = "Link"
        self.meta.get_field("publisher").options = "Publisher"

        self.meta.get_field("subscription_level").label = _("Subscription Level")
        self.meta.get_field("subscription_level").fieldtype = "Link"
        self.meta.get_field("subscription_level").options = "Subscription Level"
        self.meta.get_field("subscription_level").reqd = True

        self.meta.get_field("audio_file").label = _("Audio File")
        self.meta.get_field("audio_file").fieldtype = "Link"
        self.meta.get_field("audio_file").options = "File"
        self.meta.get_field("audio_file").reqd = True

        self.meta.get_field("total_listening_time").label = _("Total Listening Time")
        self.meta.get_field("total_listening_time").fieldtype = "Time"
        self.meta.get_field("total_listening_time").reqd = True

        self.meta.get_field("licensing_cost").label = _("Licensing Cost")
        self.meta.get_field("licensing_cost").fieldtype = "Currency"
        self.meta.get_field("licensing_cost").reqd = True

        self.meta.get_field("production_cost").label = _("Production Cost")
        self.meta.get_field("production_cost").fieldtype = "Currency"
        self.meta.get_field("production_cost").reqd = True

        self.meta.get_field("royalty_percentage").label = _("Royalty Percentage")
        self.meta.get_field("royalty_percentage").fieldtype = "Float"
        self.meta.get_field("royalty_percentage").reqd = True

    # Define other methods and properties as needed

    def get_listening_history(self):
        # Get the Audiobook Listening History records associated with this Audiobook
        listening_history = frappe.get_all(
            "Audiobook Listening History",
            filters={"audiobook": self.name},
            fields=["name", "user", "timestamp"]
        )
        return listening_history

    # Define other methods and properties as needed

def get_audiobook_list():
    # Custom function to retrieve a list of Audiobooks
    audiobooks = frappe.get_all(
        "Audiobook",
        filters={},
        fields=["name", "title", "author", "publisher"]
    )
    return audiobooks

