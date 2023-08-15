
# modules/audiobook_listening_history/audiobook_listening_history.py
from frappe import _
from frappe.model.document import Document

class AudiobookListeningHistory(Document):
    def validate(self):
        # Perform any validation or custom logic here
        pass

    # Define fields of the Audiobook Listening History doctype
    def setup_fields(self):
        self.meta.get_field("audiobook").label = _("Audiobook")
        self.meta.get_field("audiobook").fieldtype = "Link"
        self.meta.get_field("audiobook").options = "Audiobook"
        self.meta.get_field("audiobook").reqd = True

        self.meta.get_field("start_time").label = _("Start Time")
        self.meta.get_field("start_time").fieldtype = "Datetime"
        self.meta.get_field("start_time").reqd = True

        self.meta.get_field("end_time").label = _("End Time")
        self.meta.get_field("end_time").fieldtype = "Datetime"
        self.meta.get_field("end_time").reqd = True

        self.meta.get_field("total_listening_time").label = _("Total Listening Time")
        self.meta.get_field("total_listening_time").fieldtype = "Time"
        self.meta.get_field("total_listening_time").reqd = True

    # Define other methods and properties as needed

