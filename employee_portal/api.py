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
