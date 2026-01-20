import frappe
from frappe.utils import getdate # type: ignore
from frappe import _


@frappe.whitelist()
def get_evaluation_details(evaluation_id):
    try:
        evaluation = frappe.get_doc("Performance Review", evaluation_id)
        return {
            "feedback": evaluation.feedback,
            "actionplan": evaluation.actionplan
        }
    except frappe.DoesNotExistError:
        frappe.throw("La evaluación no existe.")

@frappe.whitelist()
def update_employee_info(employee_id, **kwargs):
    try:
        employee = frappe.get_doc("Employee", employee_id)
        
        # Iterar sobre los campos que se pasan como argumento
        for field, value in kwargs.items():
            # Validar que el campo sea válido
            if hasattr(employee, field):
                employee.set(field, value)
        
        employee.save()
        return {"status": "success", "message": _("Información actualizada con éxito.")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def bulk_create_appraisals(employees, appraisal_template, start_date, end_date):
    """
    Crear evaluaciones masivas en estado de borrador
    
    Args:
        employees: Lista de IDs de empleados (JSON string)
        appraisal_template: ID de la plantilla de evaluación
        start_date: Fecha de inicio
        end_date: Fecha final
    
    Returns:
        dict: Resultado de la operación con los nombres de las evaluaciones creadas
    """
    import json
    
    try:
        # Convertir employees de string JSON a lista si es necesario
        if isinstance(employees, str):
            employees = json.loads(employees)
        
        created_appraisals = []
        errors = []
        
        for employee_id in employees:
            try:
                # Crear nuevo documento de Appraisal
                appraisal = frappe.get_doc({
                    "doctype": "Appraisal",
                    "kra_template": appraisal_template,
                    "employee": employee_id,
                    "start_date": start_date,
                    "end_date": end_date,
                    "status": "Draft"
                })
                
                # Obtener los goals de la plantilla usando el método existente
                from erpnext.hr.doctype.appraisal.appraisal import fetch_appraisal_template
                template_doc = fetch_appraisal_template(appraisal_template)
                
                # Copiar los goals al appraisal
                if template_doc and template_doc.goals:
                    appraisal.goals = template_doc.goals
                
                # Guardar el documento (quedará en estado Draft)
                appraisal.insert(ignore_permissions=True)
                created_appraisals.append(appraisal.name)
                
            except Exception as e:
                employee_name = frappe.db.get_value("Employee", employee_id, "employee_name")
                errors.append(f"Error para {employee_name}: {str(e)}")
        
        return {
            "status": "success",
            "created": created_appraisals,
            "errors": errors,
            "message": _("Se crearon {0} evaluaciones exitosamente.").format(len(created_appraisals))
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Bulk Appraisal Creation Error")
        return {
            "status": "error",
            "message": str(e)
        }
