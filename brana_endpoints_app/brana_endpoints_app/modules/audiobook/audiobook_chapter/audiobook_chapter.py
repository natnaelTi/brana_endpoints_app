
from frappe import _
import frappe
from frappe.model.document import Document

class AudiobookChapter(Document):
    def __init__(self, *args, **kwargs):
        super(AudiobookChapter, self).__init__(*args, **kwargs)
        self.setup_fields()

    def validate(self):
        # Perform any validation or custom logic here
        pass

    def on_submit(self):
        # Perform actions when the Audiobook Chapter is submitted
        pass

    def on_cancel(self):
        # Perform actions when the Audiobook Chapter is cancelled
        pass

    # Define fields of the Audiobook Chapter doctype
    def setup_fields(self):
        self.meta.get_field("title").label = _("Title")
        self.meta.get_field("title").reqd = True

        self.meta.get_field("description").label = _("Description")
        self.meta.get_field("description").fieldtype = "Text Editor"

        self.meta.get_field("audiobook").label = _("Audiobook")
        self.meta.get_field("audiobook").fieldtype = "Link"
        self.meta.get_field("audiobook").options = "Audiobook"
        self.meta.get_field("audiobook").reqd = True

        self.meta.get_field("audio_file").label = _("Audio File")
        self.meta.get_field("audio_file").fieldtype = "Link"
        self.meta.get_field("audio_file").options = "File"
        self.meta.get_field("audio_file").reqd = True

        self.meta.get_field("total_listening_time").label = _("Total Listening Time")
        self.meta.get_field("total_listening_time").fieldtype = "Time"
        self.meta.get_field("total_listening_time").reqd = True

    # Define other methods and properties as needed

def get_audiobook_chapter_list(audiobook):
    # Custom function to retrieve a list of Audiobook Chapters for a given Audiobook
    chapters = frappe.get_all(
        "Audiobook Chapter",
        filters={"audiobook": audiobook},
        fields=["name", "title", "description", "audiobook", "audio_file", "total_listening_time"]
    )
    return chapters

