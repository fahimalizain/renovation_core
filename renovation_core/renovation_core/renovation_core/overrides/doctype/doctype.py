


import frappe
from frappe.core.doctype.doctype.doctype import DocType
from renovation_app.model.modelcontroller import generate_controller_for_model
from renovation_core.utils.doctype import check_for_renovation_doctype, get_external_app, make_wrapper_app_boilerplate_controller

# renovation_core (frappe) knows -> about renovation (agnostic)
# So what we can do is have renovation_core override DocType and do frappe internal generation here
# Then, it can call a generic util function in renovation that will generate the doctype.py and doctype_fields.py

class DocTypeOverride(DocType):

    def on_update(self):

        # If doctype is part of a wrapper app, perform checks to make sure everything is kosher from our side
        check_for_renovation_doctype(self)
        super().on_update()

    def make_controller_template(self):
        super().make_controller_template()

        # TODO This part should only run once on doctype creation, like how frappe does it.
        # We do not want to overrite the business logic everytime the doctype is updated. 😅
        
        # Have a small check to see if the doctype belongs to a wrapper app.
        external_app = get_external_app(frappe.get_doctype_app(self.name))
        if external_app:

            # Generate the extrenal model files

            # TODO Instead of calling the function with a doctype object, 
            # we should prolly pass in our own "model" object 

            generate_controller_for_model(self, external_app)

            # Replace the internal doctype controller with our own custom one
            make_wrapper_app_boilerplate_controller(self, external_app)




























####################################

