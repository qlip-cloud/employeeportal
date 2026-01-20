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
            data = json.loads(data)

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
        data["from_date"] = (
            data["from_datetime"].split("T")[0] if data.get("from_datetime") else None
        )
        data["to_date"] = (
            data["to_datetime"].split("T")[0] if data.get("to_datetime") else None
        )

        # Validación mínima
        required_fields = [
            "employee",
            "employee_name",
            "leave_type",
            "from_datetime",
            "to_datetime",
        ]
        for field in required_fields:
            if not data.get(field):
                return {
                    "status": "error",
                    "message": _(f"Falta el campo requerido: {field}"),
                }
            
        if data["leave_type"].lower() == "permiso personal" or data["leave_type"].lower() == "calamidad doméstica":
            mentum_hours = 32
            existing_leaves = frappe.db.get_all(
                "Leave Application",
                filters={
                    "employee": data["employee"],
                    "leave_type": ["in", ["Permiso Personal", "Calamidad Doméstica"]],
                    "status": ["in", ["Approved"]],
                },
                fields=["total_leave_hours"],
            )
            used_hours = sum(leave.total_leave_hours for leave in existing_leaves)
            available_hours = mentum_hours - used_hours
            if available_hours <= 0:
                return {
                    "status": "error",
                    "message": _("No tienes horas de Mentum disponibles para este tipo de permiso."),
                }
            # Calcular duración en horas
            from_datetime = frappe.utils.get_datetime(data["from_datetime"])
            to_datetime = frappe.utils.get_datetime(data["to_datetime"])
            requested_hours = (to_datetime - from_datetime).total_seconds() / 3600
            if requested_hours > available_hours:
                return {
                    "status": "error",
                    "message": _(f"No tienes suficientes horas de Mentum disponibles. Horas disponibles: {available_hours}, Horas solicitadas: {requested_hours}."),
                }
            
            if not data.get("description"):
                return {
                    "status": "error",
                    "message": _("La descripción es obligatoria para Permiso Personal."),
                }

        # Calcular duración de solicitud en días u horas, segun corresponda
        if data.get("from_date") and data.get("to_date"):
            from_date = frappe.utils.getdate(data["from_date"])
            to_date = frappe.utils.getdate(data["to_date"])
            diff_days = (to_date - from_date).days

            if diff_days >= 1:
                data["total_leave_days"] = diff_days
                data["total_leave_hours"] = 0
            else:
                # Mismo día - calcular en horas
                from_datetime = frappe.utils.get_datetime(data["from_datetime"])
                to_datetime = frappe.utils.get_datetime(data["to_datetime"])
                diff_hours = (to_datetime - from_datetime).total_seconds() / 3600
                data["total_leave_hours"] = diff_hours
                data["total_leave_days"] = 0
        # Crear doc
        doc = frappe.get_doc(
            {
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
                "total_leave_days": data.get("total_leave_days"),
                "total_leave_hours": data.get("total_leave_hours"),
                "description": data.get("description"),
                "status": data.get("status", "Open"),
            }
        )

        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        # Devuelve respuesta
        return {
            "status": "success",
            "message": _("Solicitud creada correctamente."),
            "name": doc.name,
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "Error en create_leave_application")
        return {"status": "error", "message": f"Ocurrió un error: {str(e)}"}


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
            "employee",
            "employee_name",
            "from_date",
            "to_date",
            "company",
            "department",
            "status",
            "description",
        ]
        for field in required_fields:
            if not data.get(field):
                return {
                    "status": "error",
                    "message": _(f"Falta el campo requerido: {field}"),
                }
        existing_allocation = frappe.db.exists(
            "Leave Allocation",
            {
                "employee": data["employee"],
                "leave_type": "Vacaciones",
                "from_date": ["<=", data["from_date"]],
                "to_date": [">=", data["to_date"]],
            },
        )

        if not existing_allocation:
            allocation = frappe.get_doc(
                {
                    "doctype": "Leave Allocation",
                    "employee": data["employee"],
                    "leave_type": data["leave_type"],
                    "from_date": frappe.utils.getdate("2025-01-01"),
                    "to_date": frappe.utils.getdate("2025-12-31"),
                    "new_leaves_allocated": 15,
                }
            )
            allocation.insert(ignore_permissions=True)

        # Convertir fechas a objetos date
        from_date = frappe.utils.getdate(data["from_date"])
        to_date = frappe.utils.getdate(data["to_date"])
        today = frappe.utils.getdate()

    
        # Crear el documento
        doc = frappe.get_doc(
            {
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
            }
        )

        # Guardar
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Solicitud de vacaciones creada correctamente."),
            "name": doc.name,
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(
            frappe.get_traceback(), "Error en create_leave_application_vacation_type"
        )
        return {
            "status": "error",
            "message": f"Ocurrió un error al crear la solicitud de vacaciones: {str(e)}",
        }


@frappe.whitelist()
def update_employee_appraisal(appraisal_name, goals, remarks, stop_action, continue_action, start_action, supervisor_feedback):
    """
    Actualiza la autoevaluación del empleado en un Appraisal.
    Solo actualiza los campos sin validar el documento.
    """
    try:
        if isinstance(goals, str):
            goals = json.loads(goals)
        if isinstance(supervisor_feedback, str):
            supervisor_feedback = json.loads(supervisor_feedback)

        # Validar que el appraisal existe
        if not frappe.db.exists("Appraisal", appraisal_name):
            return {
                "status": "error",
                "message": _("La evaluación no existe."),
            }

        # Obtener el documento sin validar
        appraisal = frappe.get_doc("Appraisal", appraisal_name)

        # Actualizar autoevaluaciones de los objetivos
        for goal_data in goals:
            for goal in appraisal.goals:
                if goal.name == goal_data.get("name"):
                    goal.self_assessment = goal_data.get("self_assessment", 0)
                    break

        # Actualizar puntuaciones del supervisor feedback
        for feedback_data in supervisor_feedback:
            for feedback in appraisal.supervisor_feedback:
                if feedback.name == feedback_data.get("name"):
                    feedback.score_earned = feedback_data.get("score_earned", 0)
                    break
    
        # Actualizar otros campos
        appraisal.remarks = remarks
        appraisal.stop_action = stop_action
        appraisal.continue_action = continue_action
        appraisal.start_action = start_action
        
        # Guardar sin validar
        appraisal.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Evaluación actualizada correctamente."),
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(
            frappe.get_traceback(), "Error en update_employee_appraisal"
        )
        return {
            "status": "error",
            "message": f"Ocurrió un error al actualizar la evaluación: {str(e)}",
        }