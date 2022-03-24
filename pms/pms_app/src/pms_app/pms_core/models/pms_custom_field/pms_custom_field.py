
from renovation import RenovationModel, scrub
from .pms_custom_field_types import PMSCustomFieldMeta


class PMSCustomField(RenovationModel["PMSCustomField"], PMSCustomFieldMeta):
    def validate(self):
        if not self.fieldname:
            self.fieldname = scrub(self.label)
