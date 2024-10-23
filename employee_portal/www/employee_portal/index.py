import frappe
from employee_portal.utils.utils import get_modules, get_employee# type: ignore
def get_context(context):
  announcements = frappe.get_all("Announcement", fields=["name", "title", "content", "published_on", "image"], order_by="published_on desc")
  context.announcements = announcements
  get_employee(context)
  get_modules(context)
  return context