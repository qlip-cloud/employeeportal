import frappe
from employee_portal.utils.utils import get_modules # type: ignore
def get_context(context):
  user = frappe.get_doc("User", frappe.session.user)
  employee = frappe.get_doc("Employee", {"user_id": user.name})
  announcements = frappe.get_all("Announcement", fields=["name", "title", "content", "published_on", "image"], order_by="published_on desc")
  context.employee = employee
  context.announcements = announcements
  get_modules(context)
  return context