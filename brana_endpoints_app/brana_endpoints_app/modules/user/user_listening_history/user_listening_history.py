
# user/user_listening_history/user_listening_history.py
from frappe import _
from frappe.model.document import Document

class UserListeningHistory(Document):
    def validate(self):
        # Perform any validation or custom logic here
        pass

    # Define fields of the User Listening History doctype
    def setup_fields(self):
        self.meta.get_field("user").label = _("User")
        self.meta.get_field("user").fieldtype = "Link"
        self.meta.get_field("user").options = "User"
        self.meta.get_field("user").reqd = True

        self.meta.get_field("audio_content").label = _("Audio Content")
        self.meta.get_field("audio_content").fieldtype = "Link"
        self.meta.get_field("audio_content").options = "Audiobook,Podcast"
        self.meta.get_field("audio_content").reqd = True

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

