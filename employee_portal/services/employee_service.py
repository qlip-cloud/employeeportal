import frappe
from frappe import _
from frappe.utils import getdate, now_datetime
from employee_portal.utils.permissions import get_employee_or_throw
from employee_portal.utils.calculations import (
    calculate_mentum_hours
)


class EmployeeService:

    
    @staticmethod
    def get_employee_profile(employee_id=None):
        """
        Obtiene el perfil completo del empleado
        
        Args:
            employee_id: ID del empleado (opcional, usa el actual si no se especifica)
            
        Returns:
            dict: Datos del perfil del empleado
        """
        if not employee_id:
            employee = get_employee_or_throw()
            employee_id = employee.name
        else:
            employee = frappe.get_doc("Employee", employee_id)
        
        # Calcular métricas
        mentum_hours = calculate_mentum_hours(employee_id)
        
        return {
            'employee': employee.as_dict(),
            'mentum_hours': mentum_hours,
            'department': employee.department,
            'designation': employee.designation,
            'reports_to': employee.reports_to,
            'joining_date': employee.date_of_joining,
        }
    
    @staticmethod
    def update_employee_profile(data):
        """
        Actualiza el perfil del empleado
        
        Args:
            data: Diccionario con los campos a actualizar
            
        Returns:
            dict: Resultado de la operación
        """
        # 1. Obtener el empleado actual (automáticamente del usuario logueado)
        employee = get_employee_or_throw()
        
        # 2. Validar campos requeridos
        required_fields = ['first_name', 'last_name', 'dob', 'gender', 'employee_id_number']
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            frappe.throw(
                _("Los siguientes campos son obligatorios: {0}").format(
                    ", ".join(missing_fields)
                )
            )
        
        # 3. Validar formato de datos
        try:
            if data.get('dob'):
                data['dob'] = getdate(data['dob'])
        except:
            frappe.throw(_("Formato de fecha de nacimiento inválido"))
        
        # 4. Campos que el empleado puede actualizar
        allowed_fields = [
            'first_name',
            'middle_name', 
            'last_name',
            'employee_id_number',
            'dob',
            'gender',
            'cell_number',
            'emergency_phone_number',
            'person_to_be_contacted',
            'relation',
            'current_accommodation_type',
            'current_address',
            'health_details',
            'family_background'
        ]
        
        # 5. Actualizar solo campos permitidos
        updated_fields = []
        for field in allowed_fields:
            if field in data:
                old_value = employee.get(field)
                new_value = data[field]
                
                if old_value != new_value:
                    employee.set(field, new_value)
                    updated_fields.append(field)
        
        # 6. Si no hay cambios, retornar sin guardar
        if not updated_fields:
            return {
                'success': True,
                'message': _('No se detectaron cambios'),
                'employee': employee.as_dict()
            }
        
        # 7. Guardar cambios
        try:
            employee.save(ignore_permissions=True)
            frappe.db.commit()
            
            # 8. Log de auditoría (opcional)
            frappe.log_error(
                f"Empleado {employee.name} actualizó campos: {', '.join(updated_fields)}",
                "Employee Profile Update"
            )
            
        except Exception as e:
            frappe.db.rollback()
            frappe.log_error(frappe.get_traceback(), "Error saving employee profile")
            frappe.throw(_("Error al guardar los cambios: {0}").format(str(e)))
        
        # 9. Retornar resultado exitoso
        return {
            'success': True,
            'message': _('Perfil actualizado exitosamente'),
            'employee': employee.as_dict(),
            'updated_fields': updated_fields
        }