import frappe


@frappe.whitelist()
def get_sidebar_items():
  sidebar_items = frappe.get_all("Sidebar Item", filters={"disable":0}, fields=['document'])
  return sidebar_items
