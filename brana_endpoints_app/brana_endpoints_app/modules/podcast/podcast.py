
from frappe import _
import frappe
from frappe.model.document import Document

class Podcast(Document):
    def __init__(self, *args, **kwargs):
        super(Podcast, self).__init__(*args, **kwargs)
        self.setup_fields()

    def validate(self):
        # Perform any validation or custom logic here
        pass

    def on_submit(self):
        # Perform actions when the Podcast is submitted
        pass

    def on_cancel(self):
        # Perform actions when the Podcast is cancelled
        pass

    # Define fields of the Podcast doctype
    def setup_fields(self):
        self.meta.get_field("title").label = _("Title")
        self.meta.get_field("title").reqd = True

        self.meta.get_field("description").label = _("Description")
        self.meta.get_field("description").fieldtype = "Text Editor"

        self.meta.get_field("host").label = _("Host")
        self.meta.get_field("host").fieldtype = "Link"
        self.meta.get_field("host").options = "User"
        self.meta.get_field("host").reqd = True

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

def get_podcast_list():
    # Custom function to retrieve a list of Podcasts
    podcasts = frappe.get_all(
        "Podcast",
        fields=["name", "title", "description", "host", "publisher", "subscription_level",
                "audio_file", "total_listening_time", "licensing_cost", "production_cost", "royalty_percentage"]
    )
    return podcasts

