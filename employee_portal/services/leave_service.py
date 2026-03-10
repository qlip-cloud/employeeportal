from datetime import timedelta
import frappe
import json
from frappe import _
from frappe.utils import getdate, now_datetime
from employee_portal.utils.permissions import get_employee_or_throw
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from employee_portal.utils.calculations import (
    calculate_mentum_hours,
    calculate_vacation_days_remaining
)

class LeaveService:
  
    @staticmethod
    def get_employee_leaves(employee_id=None):
        """
        Obtiene los datos relacionados con permisos/ausencias del empleado
        
        Args:
            employee_id: ID del empleado (opcional, usa el actual si no se especifica)
            
        Returns:
            dict: Datos relacionados con permisos/ausencias
        """
        print(f"Fetching leaves for employee_id: {employee_id}")
        if not employee_id:
            employee = get_employee_or_throw()
            employee_id = employee.name
        else:
            employee = frappe.get_doc("Employee", employee_id)
        
        leaves = frappe.get_all(
            "Leave Application",
            filters={"employee": employee_id,  "leave_type": ["!=", "Vacaciones"]},
            fields=["name", "leave_type", "from_date", "to_date", "from_datetime", "to_datetime", "status", "total_leave_days", "total_leave_hours"]
        )
        return leaves
    
    @staticmethod
    def get_employee_vacations(employee_id=None):
        """
        Obtiene los datos relacionados con vacaciones del empleado
        
        Args:
            employee_id: ID del empleado (opcional, usa el actual si no se especifica)
            
        Returns:
            dict: Datos relacionados con vacaciones
        """
        if not employee_id:
            employee = get_employee_or_throw()
            employee_id = employee.name
        else:
            employee = frappe.get_doc("Employee", employee_id)
        
        vacations = frappe.get_all(
            "Leave Application",
            filters={"employee": employee_id,  "leave_type": "Vacaciones"},
            fields=["name", "from_date", "to_date", "status", "total_leave_days"]
        )
        return vacations
    @staticmethod
    def get_my_employees_leaves():
        """
        Obtiene los datos relacionados con permisos/ausencias de los empleados que reportan al usuario actual
        
        Returns:
            dict: Datos relacionados con permisos/ausencias de los empleados
        """
        all_leaves = frappe.get_all(
            "Leave Application",
            filters={"leave_approver": frappe.session.user,  "leave_type": ["!=", "Vacaciones"]},
            fields=["name", "employee_name", "leave_type", "from_date", "to_date", "from_datetime", "to_datetime", "status", "total_leave_days", "total_leave_hours"]
        )
        return all_leaves
    
    @staticmethod
    def get_leave_types():
        """
        Obtiene todos los tipos de permisos/ausencias disponibles
        
        Returns:
            list: Lista de tipos de permisos/ausencias
        """
        leave_types = frappe.get_all("Leave Type", fields=["*"])
        return leave_types
    
    @staticmethod
    def get_leave_details(leave_application_id):
        """
        Obtiene los detalles de una solicitud de permiso/ausencia específica
        
        Args:
            leave_application_id: ID de la solicitud de permiso/ausencia
            
        Returns:
            dict: Detalles de la solicitud de permiso/ausencia
        """
        leave_application = frappe.get_doc("Leave Application", leave_application_id)
        return leave_application.as_dict()
    
    @staticmethod
    def has_permission_to_approve(user, leave_application):
        """
        Verifica si un usuario tiene permiso para aprobar una solicitud de permiso/ausencia
        
        Args:
            user: Usuario a verificar
            leave_application: Solicitud de permiso/ausencia
            
        Returns:
            bool: True si el usuario tiene permiso, False en caso contrario
        """
        if not leave_application:
            return False
        
        approver = leave_application.get("leave_approver")
        return approver == user
    
    @staticmethod
    def approve_leave_application(leave_application_name, approver_user):
        """
        Aprueba una solicitud de permiso/ausencia
        
        Args:
            leave_application_name: Nombre de la solicitud de permiso/ausencia
            approver_user: Usuario que aprueba la solicitud
            
        Returns:
            dict: Resultado de la operación
        """
        leave_application = frappe.get_doc("Leave Application", leave_application_name)
        
        if not LeaveService.has_permission_to_approve(approver_user, leave_application):
            frappe.throw(_("No tienes permiso para aprobar esta solicitud de permiso/ausencia."))
        
        leave_application.status = "Approved"
        leave_application.approved_by = approver_user
        leave_application.approved_on = now_datetime()
        leave_application.save()
        
        return {"message": _("Solicitud de permiso/ausencia aprobada exitosamente.")}
    
    @staticmethod
    def create_leave_application(data, mentum_hours):
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

    
          # Validación de horas de Mentum para permisos personales y calamidades domésticas
          if data["leave_type"].lower() == "permiso personal" or data["leave_type"].lower() == "calamidad doméstica":
            
            # Calcular duración en horas
            from_datetime = frappe.utils.get_datetime(data["from_datetime"])
            to_datetime = frappe.utils.get_datetime(data["to_datetime"])
            requested_hours = (to_datetime - from_datetime).total_seconds() / 3600
            if requested_hours > float(mentum_hours):
                return {
                    "status": "error",
                    "message": _(f"No tienes suficientes horas de Mentum disponibles. Horas disponibles: {mentum_hours}, Horas solicitadas: {requested_hours}."),
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
            'success': True,
            'message': _('Solicitud de permiso/ausencia creada exitosamente.'),
          }

        except Exception as e:
          frappe.db.rollback()
          frappe.log_error(frappe.get_traceback(), "Error en create_leave_application")

    @staticmethod
    def create_vacation_leave_application(data):
        """
        Crea una nueva solicitud de vacaciones
        
        Args:
            data: Datos de la solicitud de vacaciones
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            if isinstance(data, str):
                data = json.loads(data)

            # Limpieza básica de campos
            for key in ["from_date", "to_date"]:
                if data.get(key):
                    data[key] = data[key].strip()

            # Calcular duración en días
            from_date = frappe.utils.getdate(data["from_date"])
            to_date = frappe.utils.getdate(data["to_date"])
            diff_days = (to_date - from_date).days + 1  # Incluir día final

            # Validar mínimo 6 días hábiles de vacaciones
            holiday_list = get_holiday_list_for_employee(data["employee"])
            holidays = frappe.get_all(
              "Holiday",
              filters={
                  "parent": holiday_list,
                  "holiday_date": ["between", [data["from_date"], data["to_date"]]]
              },
              fields=["holiday_date"]
            )
            business_days = diff_days - len(holidays)
            if business_days < 6:
                return {
                    'success': False,
                    'message': _('La solicitud de vacaciones debe ser de al menos 6 días hábiles. Días hábiles solicitados: {0}').format(business_days),
                }
            
            # Validar mínimo de 5 días de vacaciones restantes después de esta solicitud
            allocation_data = frappe.db.get_value(
                "Leave Allocation",
                {"employee": data["employee"], "leave_type": "Vacaciones", "docstatus": 1},
                ["from_date", "to_date"],
                as_dict=True
            )
            if not allocation_data:
                return {
                    'success': False,
                    'message': _('No se encontró una asignación de vacaciones activa para este empleado.'),
                }
            taken_leaves = frappe.db.sql("""
                SELECT COALESCE(SUM(total_leave_days), 0) as total
                FROM `tabLeave Application`
                WHERE employee = %s
                AND leave_type = 'Vacaciones'
                AND status = 'Approved'
                AND from_date >= %s
                AND to_date <= %s
                AND docstatus = 1
            """, (data["employee"], allocation_data.from_date, allocation_data.to_date), as_dict=True)[0].total
            allocated_leaves = frappe.db.get_value(
                "Leave Allocation",
                {"employee": data["employee"], "leave_type": "Vacaciones", "docstatus": 1},
                "total_leaves_allocated"
            ) or 0
            remaining_leaves_after_request = allocated_leaves - taken_leaves - business_days
            if remaining_leaves_after_request < 5:
                return {
                    'success': False,
                    'message': _('No puedes solicitar estas vacaciones ya que te quedarían menos de 5 días hábiles restantes. Días hábiles restantes después de la solicitud: {0}').format(remaining_leaves_after_request),
                }
            data["total_leave_days"] = business_days
            data["total_leave_hours"] = 0

            doc = frappe.get_doc(
                {
                    "doctype": "Leave Application",
                    "employee": data["employee"],
                    "employee_name": data["employee_name"],
                    "company": data.get("company"),
                    "department": data.get("department"),
                    "leave_approver": data.get("leave_approver"),
                    "leave_type": "Vacaciones",
                    "posting_date": data.get("posting_date"),
                    "from_date": data.get("from_date"),
                    "to_date": data.get("to_date"),
                    "total_leave_days": data.get("total_leave_days"),
                    "total_leave_hours": data.get("total_leave_hours"),
                    "description": data.get("description"),
                    "status": data.get("status", "Open"),
                }
            )

            doc.insert(ignore_permissions=True)
            frappe.db.commit()

            return {
                'success': True,
                'message': _('Solicitud de vacaciones creada exitosamente.'),
            }

        except Exception as e:
            frappe.db.rollback()
            frappe.log_error(frappe.get_traceback(), "Error en create_vacation_application")
            return {
                'success': False,
                'message': _('Error al crear la solicitud de vacaciones: {0}').format(str(e)),
            }
          

