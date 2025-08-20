import frappe
from datetime import datetime # type: ignore
from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  # type: ignore


def get_context(context):
  is_guest()
  is_employee()
  context.employee = get_employee

  # Fetch announcements
  context.announcements = frappe.get_all(
    "Announcement",
    fields=["name", "title", "content", "published_on", "image"],
    order_by="published_on desc"
  )

  # Fetch upcoming events
  context.events = frappe.get_all(
    "Event",
    filters={"starts_on": [">=", frappe.utils.nowdate()]},
    fields=["name", "subject", "starts_on", "ends_on"],
    order_by="starts_on asc"
  )

  # Get modules for the portal
  

  # Fetch employee details
  try:
    user = frappe.get_doc("User", frappe.session.user)
    employee = frappe.get_doc("Employee", {"user_id": user.name})
    context.employee = employee
  except frappe.DoesNotExistError:
    raise frappe.PermissionError("You are not authorized to access this page.")

  return context
