# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SalesInvoice(Document):
	
	@staticmethod
	def default_list_data():
		columns = [
			{
				"label": "Name",
				"type": "Data",
				"key": "customer",
				"width": "12rem",
			},
			{
				"label": "Customer",
				"type": "Data",
				"key": "customer",
				"options": "",
				"width": "10rem",
			},
			{
				"label": "Last Modified",
				"type": "Datetime",
				"key": "modified",
				"width": "8rem",
			},
		]
		rows = [
			"name",
			"customer",
			"modified"
		]
		return {"columns": columns, "rows": rows}
