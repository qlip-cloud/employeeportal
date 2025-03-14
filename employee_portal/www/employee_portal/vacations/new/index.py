import frappe
from frappe.utils import getdate, nowdate, date_diff # type: ignore
from employee_portal.utils.utils import get_modules, get_employee_from_user
from employee_portal.employee_portal.services.employee.leave_application import save_application # type: ignore

def get_context(context):
  get_employee_from_user(context)
  get_modules(context)
  context.employees = frappe.get_all(
      "Employee",
      filters=[["user_id", "!=", frappe.session.user]],  
      fields=["*"]
  )
  # Validación 15 días de vacaciones
  today = getdate(nowdate()) 
  current_year = today.year

  employee = context.employee
  date_of_joining = frappe.get_value("Employee", employee.name, "date_of_joining")

  if date_of_joining:
      date_of_joining = getdate(date_of_joining)

      start_of_year = getdate(f"{current_year}-01-01")
      days_worked = date_diff(today, max(date_of_joining, start_of_year))

      max_vacation_days = (days_worked / 365) * 15

      used_vacation_days = frappe.db.sql("""
          SELECT COALESCE(SUM(total_leave_days), 0) 
          FROM `tabLeave Application`
          WHERE employee = %s 
          AND leave_type = 'Vacaciones' 
          AND status = 'Approved'
          AND from_date >= %s
      """, (employee.name, start_of_year))[0][0]

      remaining_vacation_days = max(0, max_vacation_days - used_vacation_days)
      context.remaining_vacation_days = round(remaining_vacation_days, 2)
  else:
      context.remaining_vacation_days = 0
  return context