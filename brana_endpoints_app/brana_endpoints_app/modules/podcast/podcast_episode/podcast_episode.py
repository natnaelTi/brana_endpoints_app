
from frappe import _
import frappe
from frappe.model.document import Document

class PodcastEpisode(Document):
    def validate(self):
        # Perform any validation or custom logic here
        pass

    def on_submit(self):
        # Perform actions when the Podcast Episode is submitted
        pass

    def on_cancel(self):
        # Perform actions when the Podcast Episode is cancelled
        pass

    # Define fields of the Podcast Episode doctype
    def setup_fields(self):
        self.meta.get_field("title").label = _("Title")
        self.meta.get_field("title").reqd = True

        self.meta.get_field("description").label = _("Description")
        self.meta.get_field("description").fieldtype = "Text Editor"

        self.meta.get_field("episode_number").label = _("Episode Number")
        self.meta.get_field("episode_number").reqd = True

        self.meta.get_field("air_date").label = _("Air Date")
        self.meta.get_field("air_date").fieldtype = "Date"
        self.meta.get_field("air_date").reqd = True

        self.meta.get_field("audio_file").label = _("Audio File")
        self.meta.get_field("audio_file").fieldtype = "Link"
        self.meta.get_field("audio_file").options = "File"
        self.meta.get_field("audio_file").reqd = True

        self.meta.get_field("podcast").label = _("Podcast")
        self.meta.get_field("podcast").fieldtype = "Link"
        self.meta.get_field("podcast").options = "Podcast"
        self.meta.get_field("podcast").reqd = True

        self.meta.get_field("total_listening_time").label = _("Total Listening Time")
        self.meta.get_field("total_listening_time").fieldtype = "Time"
        self.meta.get_field("total_listening_time").reqd = True

    # Define other methods and properties as needed

def get_podcast_episode_list(podcast):
    # Custom function to retrieve a list of Podcast Episodes for a given Podcast
    episodes = frappe.get_all(
        "Podcast Episode",
        filters={"podcast": podcast},
        fields=["name", "title", "description", "episode_number", "air_date", "audio_file", "total_listening_time"]
    )
    return episodes

