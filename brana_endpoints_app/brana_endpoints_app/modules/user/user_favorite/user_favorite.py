
# brana_endpoints_app/brana_endpoints_app/modules/user/user_favorite/user_favorite.py
from frappe import _
import frappe
from frappe.model.document import Document

class UserFavorite(Document):
    def __init__(self, *args, **kwargs):
        super(UserFavorite, self).__init__(*args, **kwargs)
        self.setup_fields()

    def validate(self):
        # Perform any validation or custom logic here
        pass

    def on_submit(self):
        # Perform actions when the User Favorite is submitted
        pass

    def on_cancel(self):
        # Perform actions when the User Favorite is cancelled
        pass

    # Define fields of the User Favorite doctype
    def setup_fields(self):
        self.meta.get_field("user").label = _("User")
        self.meta.get_field("user").fieldtype = "Link"
        self.meta.get_field("user").options = "User Profile"
        self.meta.get_field("user").reqd = True

        self.meta.get_field("audio_content").label = _("Audio Content")
        self.meta.get_field("audio_content").fieldtype = "Link"
        self.meta.get_field("audio_content").options = "Audiobook or Podcast"

