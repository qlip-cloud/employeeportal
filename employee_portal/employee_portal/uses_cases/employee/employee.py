import frappe, json
from frappe import _

def get_announcements():
  query = """
    SELECT
      name, title, content, published_on, image
    FROM
      `tabAnnouncement`
    WHERE
      published_on <= CURDATE()
    ORDER BY
      published_on DESC
  """
  return frappe.db.sql(query, as_dict=True)


def get_events():
  query = """
    SELECT
      name, subject, starts_on, ends_on
    FROM
      `tabEvent`
    WHERE
      starts_on >= CURDATE()
    ORDER BY
      starts_on ASC
  """
  return frappe.db.sql(query, as_dict=True)


@frappe.whitelist()
def save_profile(employee_id, data):
  try:
    current_user = frappe.session.user

    employee = frappe.get_doc("Employee", employee_id)

    if employee.user_id.lower() != current_user.lower():
      return {
        "status": "error",
        "error": "No tienes permiso para editar este perfil.",
      }

    if isinstance(data, str):
      data=json.loads(data)

    employee = frappe.get_doc("Employee", employee_id)
    employee.update(data)
    employee.save(ignore_permissions=True)
    return {"status": "success"}
  except Exception as e:
    return {"status": "error", "error": str(e)}

@frappe.whitelist()
def create_leave_application(data):
    """
    Crea una solicitud de permiso usando frappe.get_doc()
    pero con validaciones y limpieza previas.
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)

        # Limpieza básica de campos
        for key in ["from_datetime", "to_datetime"]:
            if data.get(key):
                data[key] = data[key].strip()
        
        # Extraer fechas (solo parte date)
        data["from_date"] = data["from_datetime"].split("T")[0] if data.get("from_datetime") else None
        data["to_date"] = data["to_datetime"].split("T")[0] if data.get("to_datetime") else None

        # Validación mínima
        required_fields = ["employee", "employee_name", "leave_type", "from_datetime", "to_datetime"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": _(f"Falta el campo requerido: {field}")}

        # Crear doc
        doc = frappe.get_doc({
            "doctype": "Leave Application",
            "employee": data["employee"],
            "employee_name": data["employee_name"],
            "company": data.get("company"),
            "department": data.get("department"),
            "leave_approver": data.get("leave_approver"),
            "leave_type": data["leave_type"],
            "posting_date": data.get("posting_date"),
            "from_date": data.get("from_date"),
            "to_date": data.get("to_date"),
            "from_datetime": data.get("from_datetime"),
            "to_datetime": data.get("to_datetime"),
            "description": data.get("description"),
            "status": data.get("status", "Open")
        })

        # Inserta e ignora permisos (útil si lo hace el propio empleado)
        doc.insert(ignore_permissions=True, ignore_validate=True)
        frappe.db.commit()

        # Devuelve respuesta
        return {
            "status": "success",
            "message": _("Solicitud creada correctamente."),
            "name": doc.name
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "Error en create_leave_application")
        return {
            "status": "error",
            "message": f"Ocurrió un error: {str(e)}"
        }

    
@frappe.whitelist()
def create_leave_application_vacation_type(data):
    """
    Crea una solicitud de vacaciones validando días, anticipación, etc.
    Similar a create_leave_application pero ajustado para 'Vacaciones'.
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)

        # Limpieza de espacios
        for key in ["from_date", "to_date"]:
            if data.get(key):
                data[key] = data[key].strip()

        # Validaciones básicas
        required_fields = [
            "employee", "employee_name", "from_date", "to_date",
            "company", "department", "status", "description"
        ]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": _(f"Falta el campo requerido: {field}")}

        # Convertir fechas a objetos date
        from_date = frappe.utils.getdate(data["from_date"])
        to_date = frappe.utils.getdate(data["to_date"])
        today = frappe.utils.getdate()

        # Validar duración mínima de 6 días
        diff_days = (to_date - from_date).days
        if diff_days < 6:
            return {"status": "error", "message": _("El período de vacaciones debe ser de al menos 6 días.")}

        # Validar solicitud con 2 meses de anticipación
        min_request_date = frappe.utils.add_days(today, 60)
        if from_date < min_request_date:
            return {"status": "error", "message": _("La solicitud debe hacerse con al menos 2 meses de anticipación.")}

        # Crear el documento
        doc = frappe.get_doc({
            "doctype": "Leave Application",
            "employee": data["employee"],
            "employee_name": data["employee_name"],
            "company": data["company"],
            "department": data["department"],
            "leave_approver": data.get("leave_approver"),
            "leave_type": "Vacaciones",
            "posting_date": data.get("posting_date"),
            "from_date": data["from_date"],
            "to_date": data["to_date"],
            "period_from": data.get("period_from"),
            "period_to": data.get("period_to"),
            "replacement": data.get("replacement"),
            "description": data.get("description"),
            "follow_via_email": data.get("follow_via_email", True),
            "status": data.get("status", "Open"),
        })

        # Guardar
        doc.insert(ignore_permissions=True, ignore_validate=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Solicitud de vacaciones creada correctamente."),
            "name": doc.name
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "Error en create_leave_application_vacation_type")
        return {
            "status": "error",
            "message": f"Ocurrió un error al crear la solicitud de vacaciones: {str(e)}"
        }