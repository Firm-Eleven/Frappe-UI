import frappe

@frappe.whitelist()
def create_doc():
    data = frappe.form_dict
    doctype = data.get("doctype")
    #frappe.throw(f"Doctype : {doctype}")
    args = data.get("args")

    if isinstance(args, str):
        args = frappe.parse_json(args)

    doc_data = args.get("doc") if args else {}
    if not doc_data:
        frappe.throw("No document data received")

    if not doctype:
        frappe.throw("Doctype is required")

    doc_data = {
        "doctype": doctype,
        **doc_data
    }

    doc = frappe.get_doc(doc_data)
    doc.insert()
    frappe.db.commit()

    return doc.name

@frappe.whitelist()
def get_doc():
    doctype = frappe.form_dict.get("doctype")
    doc_id = frappe.form_dict.get("doc_id")

    if not doctype or not doc_id:
        frappe.throw("doctype and doc_id are required")

    return frappe.get_doc(doctype, doc_id).as_dict()

@frappe.whitelist()
def update_doc():
    data = frappe.form_dict

    doctype = data.get("doctype")
    doc_id = data.get("doc_id")
    args = data.get("args")

    if isinstance(args, str):
        args = frappe.parse_json(args)

    if not doctype or not doc_id:
        frappe.throw("doctype and doc_id are required")

    if not args:
        frappe.throw("No update data received")

    doc = frappe.get_doc(doctype, doc_id)

    for key, value in args.items():
        setattr(doc, key, value)

    doc.save()
    frappe.db.commit()

    return doc.name

@frappe.whitelist()
def get_list_view_columns(doctype, limit=3):
    meta = frappe.get_meta(doctype)
    
    if not meta or not meta.fields:
        
        return []

    # 🔹 In List View fields filter
    fields = [f for f in meta.fields if f.in_list_view]

    # 🔹 limit apply
    fields = fields[:int(limit)]

    # 🔹 columns format
    columns = [
        {
            "key": f.fieldname,
            "label": f.label,
            "align": "left"
        }
        for f in fields
    ]

    # 🔹 modified add
    columns.append({
        "key": "modified",
        "label": "Modified",
        "align": "left"
    })

    return columns


@frappe.whitelist()   
def get_list_view_rows(doctype):
    # Columns jo list view me visible hain
    fields = [f.fieldname for f in frappe.get_meta(doctype).fields if f.in_list_view] + ["modified"]

    # rows fetch karo
    docs = frappe.get_list(doctype, fields=fields)
    return docs
