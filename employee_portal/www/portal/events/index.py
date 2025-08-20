import frappe
from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  

def get_context(context):
  is_guest()
  is_employee()
  context.employee = get_employee()
  return context

@frappe.whitelist()
def get_events():
  events = frappe.get_all('Event', fields=['name', 'subject as title', 'starts_on as start', 'ends_on as end', 'status'])
  return events
