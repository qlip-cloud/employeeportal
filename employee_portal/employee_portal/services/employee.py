import frappe 
from frappe import _

@frappe.whitelist()
def update_employee_info(**kwargs):
  employee = frappe.get_doc("Employee", kwargs.get("name"))
  try:
    employee.first_name = kwargs.get("first_name")
    employee.middle_name = kwargs.get("middle_name")
    employee.last_name = kwargs.get("last_name")
    employee.date_of_birth = kwargs.get("dob")
    employee.gender = kwargs.get("gender")
    employee.employee_number = kwargs.get("employee_number")
    employee.emergency_phone_number = kwargs.get("emergency_phone")
    employee.person_to_be_contacted = kwargs.get("emergency_contact")
  except Exception as e:
    frappe.throw(_("Error: {0}").format(e))
  else:
    employee.flags.ignore_permissions = True
    employee.save()
    frappe.db.commit() 
