import frappe
from frappe import _
from employee_portal.services.evaluation_service import EvaluationService


@frappe.whitelist()
def bulk_create_appraisals(company, kra_template, second_kra_template, start_date, end_date, is_performance_review=False, **kwargs):
    try:
        return EvaluationService.bulk_create_appraisals(company, kra_template, second_kra_template, start_date, end_date, is_performance_review)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error creating bulk appraisals")
        frappe.throw(_("Error al crear evaluaciones masivas: {0}").format(str(e)))

@frappe.whitelist()
def update_employee_appraisal(appraisal_name, goals, remarks, stop_action, continue_action, start_action, supervisor_feedback, **kwargs):
    try:
        return EvaluationService.update_employee_appraisal(appraisal_name, goals, remarks, stop_action, continue_action, start_action, supervisor_feedback)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error updating employee appraisal")
        return {
            "success": False,
            "message": _("Ocurrió un error al actualizar la evaluación: {0}").format(str(e))
        }