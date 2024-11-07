import frappe
from datetime import datetime
from employee_portal.utils.utils import get_modules, get_employee# type: ignore
def get_context(context):
  announcements = frappe.get_all("Announcement", fields=["name", "title", "content", "published_on", "image"], order_by="published_on desc")
  context.announcements = announcements
  events = frappe.get_all(
        "Event",
        filters={"starts_on": [">=", datetime.now().date()]},
        fields=["name", "subject", "starts_on", "ends_on"],
        order_by="starts_on asc"
    )
  context.events = events
  get_employee(context)
  get_modules(context)
  return context