# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CrmDoc(Document):

    def validate(self):
    	if self.id:
        	existing = frappe.db.exists("CRM Doc", {"id": self.id})
        
        	if existing and existing != self.name:
            		frappe.throw(f"ID '{self.id}' already exists")

    def before_save(self):
        # Optional: trim whitespace from name1
        if self.name1:
            self.name1 = self.name1.strip()
            
    @staticmethod
    def default_list_data():
        
        columns = [
            {
                "label": "ID",
                "type": "Data",
                "key": "id",
                #"width": "15rem",
            },
            {
                "label": "Name",
                "type": "Data",
                "key": "name1",
                #"width": "25rem",
            },
            {
		"label": "Last Modified",
		"type": "Datetime",
		"key": "modified",
		#"width": "10rem",
	    },
        ]

        # rows = order of fields when displayed in table view
        rows = ["id", "name1","modified",]

        return {"columns": columns, "rows": rows}
    
    @staticmethod
    def default_kanban_settings():
        return {
            "column_field": "id",          # which field defines the Kanban columns
            "title_field": "name1",        # what to display on the card
            "kanban_fields": '["id","name1"]'
        }
    
@frappe.whitelist()
def create_crm_doc():
    data = frappe.form_dict
    doctype = data.get("doctype")
    args = data.get("args")

    if isinstance(args, str):
        args = frappe.parse_json(args)

    doc_data = args.get("doc") if args else {}
    if not doc_data:
        frappe.throw("No document data received")

    doc_data = {
        "doctype": doctype,
        **doc_data
    }

    new_doc = frappe.get_doc(doc_data)
    new_doc.insert()
	frappe.db.commit()
    return new_doc.name


@frappe.whitelist()
def get_crm_doc(doc_id):
    return frappe.get_doc("CRM Doc", doc_id).as_dict()


@frappe.whitelist()
def update_crm_doc(doc_id, name1=None):
    doc = frappe.get_doc("CRM Doc", doc_id)
    if name1 is not None:
        doc.name1 = name1
    if type1 is not None:
        doc.type1 = type1
    doc.save()
    return doc.name
