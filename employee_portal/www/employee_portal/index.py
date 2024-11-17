import frappe
from datetime import datetime
from employee_portal.utils.utils import get_modules  # type: ignore

def get_context(context):
  """
  Fetches announcements, events, and employee data (if logged in as an employee)
  for the employee portal context.

  Raises PermissionError if the user is not logged in or is not an employee.

  Args:
      context (dict): The context dictionary to update.

  Returns:
      dict: The updated context dictionary.
  """

  # Check for logged-in user and permissions early
  if frappe.session.user == "Guest":
    raise frappe.PermissionError("Log in to access this page.")

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
  get_modules(context)

  # Fetch employee details
  try:
    user = frappe.get_doc("User", frappe.session.user)
    employee = frappe.get_doc("Employee", {"user_id": user.name})
    context.employee = employee
  except frappe.DoesNotExistError:
    raise frappe.PermissionError("You are not authorized to access this page.")

  return context
