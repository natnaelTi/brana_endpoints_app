
# modules/file/file.py
from frappe import _
from frappe.model.document import Document

class File(Document):
    def validate(self):
        # Perform any validation or custom logic here
        pass

    # Define fields of the File doctype
    def setup_fields(self):
        self.meta.get_field("name").label = _("Name")
        self.meta.get_field("name").fieldtype = "Data"
        self.meta.get_field("name").reqd = True

        self.meta.get_field("file_name").label = _("File Name")
        self.meta.get_field("file_name").fieldtype = "Data"
        self.meta.get_field("file_name").reqd = True

        self.meta.get_field("file").label = _("File")
        self.meta.getfield("file").fieldtype = "Attachment"
        self.meta.get_field("file").reqd = True

        self.meta.get_field("file_type").label = _("File Type")
        self.meta.get_field("file_type").fieldtype = "Data"
        self.meta.get_field("file_type").reqd = True

        self.meta.get_field("attached_to").label = _("Attached To")
        self.meta.get_field("attached_to").fieldtype = "Dynamic Link"
        self.meta.get_field("attached_to").reqd = True

        self.meta.get_field("file_size").label = _("File Size")
        self.meta.get_field("file_size").fieldtype = "Data"
        self.meta.get_field("file_size").reqd = True

        self.meta.get_field("is_private").label = _("Is Private")
        self.meta.get_field("is_private").fieldtype = "Check"
        self.meta.get_field("is_private").reqd = True

        self.meta.get_field("folder").label = _("Folder")
        self.meta.get_field("folder").fieldtype = "Link"
        self.meta.get_field("folder").options = "Folder"

        self.meta.get_field("thumbnail").label = _("Thumbnail")
        self.meta.get_field("thumbnail").fieldtype = "Attachment"

        self.meta.get_field("thumbnail_small").label = _("Thumbnail Small")
        self.meta.get_field("thumbnail_small").fieldtype = "Attachment"

        self.meta.get_field("sha256").label = _("SHA256")
        self.meta.get_field("sha256").fieldtype = "Data"
        self.meta.get_field("sha256").reqd = True

        self.meta.get_field("media_type").label = _("Media Type")
        self.meta.get_field("media_type").fieldtype = "Data"
        self.meta.get_field("media_type").reqd = True

        self.meta.get_field("content_type").label = _("Content Type")
        self.meta.get_field("content_type").fieldtype = "Data"
        self.meta.get_field("content_type").reqd = True

        self.meta.get_field("parenttype").label = _("Parenttype")
        self.meta.get_field("parenttype").fieldtype = "Data"
        self.meta.get_field("parenttype").reqd = True

        self.meta.get_field("parent").label = _("Parent")
        self.meta.get_field("parent").fieldtype = "Dynamic Link"
        self.meta.get_field("parent").reqd = True

    # Define other methods and properties as needed

