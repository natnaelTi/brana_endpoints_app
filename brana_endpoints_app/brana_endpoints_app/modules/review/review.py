
# modules/review/review.py
from frappe import _
from frappe.model.document import Document

class Review(Document):
    def validate(self):
        # Perform any validation or custom logic here
        pass

    # Define fields of the Review doctype
    def setup_fields(self):
        self.meta.get_field("user").label = _("User")
        self.meta.get_field("user").fieldtype = "Link"
        self.meta.get_field("user").options = "User Profile"
        self.meta.get_field("user").reqd = True

        self.meta.get_field("audio_content").label = _("Audio Content")
        self.meta.get_field("audio_content").fieldtype = "Link"
        self.meta.get_field("audio_content").options = "Audiobook,Podcast"
        self.meta.get_field("audio_content").reqd = True

        self.meta.get_field("rating").label = _("Rating")
        self.meta.get_field("rating").fieldtype = "Float"
        self.meta.get_field("rating").reqd = True
        self.meta.get_field("rating").precision = 1
        self.meta.get_field("rating").min_value = 0
        self.meta.get_field("rating").max_value = 5

        self.meta.get_field("review_text").label = _("Review Text")
        self.meta.get_field("review_text").fieldtype = "Text"

        self.meta.get_field("date_created").label = _("Date Created")
        self.meta.get_field("date_created").fieldtype = "Date"
        self.meta.get_field("date_created").read_only = True

        self.meta.get_field("review_id").label = _("Review ID")
        self.meta.get_field("review_id").fieldtype = "Data"
        self.meta.get_field("review_id").read_only = True

    # Define other methods and properties as needed

