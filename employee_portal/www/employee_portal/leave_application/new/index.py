import frappe
from frappe.utils import getdate, nowdate, date_diff, add_days, cstr, cint # type: ignore
from employee_portal.utils.utils import get_modules, get_employee_from_user
from employee_portal.employee_portal.services.employee.leave_application import save_application  # type: ignore


def get_context(context):
    get_employee_from_user(context)
    get_modules(context)
    leave_types = frappe.get_all("Leave Type", fields=["*"])

    # Validación 32 horas MENTUM
    today = getdate(nowdate())  # Obtiene la fecha actual en formato correcto
    current_year = today.year if today >= getdate(f"{today.year}-09-27") else today.year - 1
    mentum_start_date = getdate(f"{current_year}-09-27")

    employee = context.employee
    date_of_joining = frappe.get_value("Employee", employee.name, "date_of_joining")

    if date_of_joining:
        date_of_joining = getdate(date_of_joining)  # Convertir la fecha de ingreso

        # Calcular el tiempo trabajado desde el inicio de MENTUM o la fecha de ingreso
        days_worked = date_diff(today, max(date_of_joining, mentum_start_date))
        mentum_percentage = min(days_worked / 365, 1)

        # Horas de MENTUM disponibles según el tiempo trabajado
        max_mentum_hours = 32 * mentum_percentage

        # Obtener las horas ya usadas desde el inicio del año MENTUM
        used_mentum_hours = frappe.db.sql("""
            SELECT COALESCE(SUM(total_leave_hours), 0) 
            FROM `tabLeave Application`
            WHERE employee = %s 
            AND leave_type != 'Vacaciones' 
            AND status = 'Approved'
            AND from_date >= %s
        """, (employee.name, mentum_start_date))[0][0]

        remaining_mentum_hours = max(0, max_mentum_hours - used_mentum_hours)
        context.remaining_mentum_hours = round(remaining_mentum_hours, 2)
    else:
        context.remaining_mentum_hours = 0

    context.leave_types = leave_types
    return context


@frappe.whitelist()
def send_application(data):
  try:
    if isinstance(data, str):
      data = frappe.parse_json(data)

    required_fields = ["leave_type", "from_date", "to_date", "department"]
    for field in required_fields:
      if not data.get(field):
        raise Exception(f"{field.replace('_', ' ').title()} is required")

    response = save_application(data) 

    if response.get("status") == "error":
      frappe.log_error(f"Error saving leave application: {response.get('message')}")
      return {"status": "error", "message": response.get("message")}

    return {"status": "success", "message": "Leave Application saved successfully :)"}

  except Exception as e:
    frappe.log_error(f"Exception in send_application: {str(e)}")
    return {"status": "error", "message": str(e)}


    


