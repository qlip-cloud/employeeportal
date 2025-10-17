import frappe
from frappe.utils import getdate, nowdate, date_diff, add_days, cstr, cint  # type: ignore
from employee_portal.employee_portal.utils.validation import is_guest, is_employee, get_employee  # type: ignore


def get_context(context):
  is_guest()
  is_employee()
  context.employee = get_employee()
  leave_types = frappe.get_all("Leave Type", fields=["*"])
  context.leave_types = leave_types

  # Validación 32 horas MENTUM
  today = getdate(nowdate())  
  current_year = (
      today.year if today >= getdate(f"{today.year}-09-27") else today.year - 1
  )
  mentum_start_date = getdate(f"{current_year}-09-27")

  employee = context.employee
  date_of_joining = frappe.get_value("Employee", employee.name, "date_of_joining")

  if date_of_joining:
      date_of_joining = getdate(date_of_joining) 

      days_worked = date_diff(today, max(date_of_joining, mentum_start_date))
      mentum_percentage = min(days_worked / 365, 1)

      max_mentum_hours = 32 * mentum_percentage

      used_mentum_hours = frappe.db.sql(
          """
          SELECT COALESCE(SUM(leave_balance), 0) 
          FROM `tabLeave Application`
          WHERE employee = %s 
          AND leave_type != 'Vacaciones' 
          AND status = 'Approved'
          AND from_date >= %s
      """,
          (employee.name, mentum_start_date),
      )[0][0]

      remaining_mentum_hours = max(0, max_mentum_hours - used_mentum_hours)
      context.remaining_mentum_hours = round(remaining_mentum_hours, 2)
  else:
      context.remaining_mentum_hours = 0

  return context


