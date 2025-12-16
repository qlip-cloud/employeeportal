import frappe
from datetime import datetime # type: ignore
from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  # type: ignore
from employee_portal.employee_portal.uses_cases.employee.employee import get_announcements, get_events  # type: ignore


def get_context(context):
  is_guest()
  is_employee()
  context.employee = get_employee()

  # Fetch announcements
  context.announcements = get_announcements()
  # Fetch upcoming events
  context.events = get_events()

  return context
