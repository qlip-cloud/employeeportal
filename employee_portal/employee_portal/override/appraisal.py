import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

@frappe.whitelist()
def fetch_supervisor_template(source_name, target_doc=None):
	target_doc = get_mapped_doc("Appraisal Template", source_name, {
		"Appraisal Template": {
			"doctype": "Appraisal",
		},
		"Appraisal Template Goal": {
			"doctype": "Appraisal Supervisor Goal",
		}
	}, target_doc)

	return target_doc