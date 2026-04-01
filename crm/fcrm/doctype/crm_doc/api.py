import frappe

from crm.api.doc import get_assigned_users, get_fields_meta
from crm.fcrm.doctype.crm_form_script.crm_form_script import get_form_script


@frappe.whitelist()
def get_doc(name):
	doc = frappe.get_doc("CRM Doc", name)
	doc.check_permission("read")

	doc = doc.as_dict()

	doc["fields_meta"] = get_fields_meta("CRM Doc")
	doc["_form_script"] = get_form_script("CRM Doc")
	return doc
