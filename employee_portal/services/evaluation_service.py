from datetime import timedelta
import frappe
import json
from frappe import _
from frappe.utils import getdate, now_datetime # type: ignore
from employee_portal.utils.permissions import get_employee_or_throw


class EvaluationService:
  @staticmethod
  def bulk_create_appraisals(company, kra_template, second_kra_template, start_date, end_date, is_performance_review=False):
    """
    Crea evaluaciones masivas para empleados seleccionados
    """
    try:
      employees = frappe.get_all(
        "Employee",
        filters={
          "company": company,
          "status": "Active"
        },
        fields=["name", "employee_name","reports_to", "branch", "designation"]
      )
      created_appraisals = []
      for emp in employees:
        appraisal = frappe.new_doc("Appraisal")
      
        # Establecer los datos específicos del empleado
        appraisal.employee = emp.name
        appraisal.employee_name = emp.employee_name
        appraisal.designation = emp.designation
        appraisal.branch = emp.branch
        appraisal.appraiser = emp.reports_to
        appraisal.company = company
        appraisal.kra_template = kra_template
        appraisal.supervisor_template = second_kra_template
        appraisal.start_date = start_date
        appraisal.end_date = end_date
        appraisal.status = "Draft"
        appraisal.is_performance_review = is_performance_review
        if kra_template:
          template_doc = frappe.get_doc("Appraisal Template", kra_template)
          
          for template_goal in template_doc.goals:
            appraisal.append("goals", {
              "kra": template_goal.kra,
              "per_weightage": template_goal.per_weightage
            })
        if is_performance_review and second_kra_template:
          supervisor_template_doc = frappe.get_doc("Appraisal Template", second_kra_template)
          
          for template_goal in supervisor_template_doc.goals:
            appraisal.append("supervisor_feedback", {
              "kra": template_goal.kra,
              "per_weightage": template_goal.per_weightage
            })
        
        appraisal.insert()
        
        created_appraisals.append(appraisal.name)
      
      return {
        'success': True,
        'created_appraisals': created_appraisals
      }
    except Exception as e:
      frappe.log_error(frappe.get_traceback(), "Error en bulk_create_appraisals")
      raise e
    
  def get_active_evaluations_for_employee(employee_name):
    """
    Obtiene las evaluaciones activas para un empleado específico
    """
    try:
      appraisals = frappe.get_all(
        "Appraisal",
        filters={
          "employee": employee_name,
          "status": ["in", ["Draft"]]
        },
        fields=["*"]
      )
      return appraisals
    except Exception as e:
      frappe.log_error(frappe.get_traceback(), "Error en get_active_evaluations_for_employee")
      raise e
  
  def get_active_evaluations_for_supervisor(supervisor_name):
    """
    Obtiene las evaluaciones activas para un supervisor específico
    """
    try:
      appraisals = frappe.get_all(
        "Appraisal",
        filters={
          "appraiser": supervisor_name,
          "status": ["in", ["Draft"]]
        },
        fields=["*"]
      )
      return appraisals
    except Exception as e:
      frappe.log_error(frappe.get_traceback(), "Error en get_active_evaluations_for_supervisor")
      raise e
  def get_completed_evaluations_for_employee(employee_name):
    """
    Obtiene las evaluaciones completadas para un empleado específico
    """
    try:
      appraisals = frappe.get_all(
        "Appraisal",
        filters={
          "employee": employee_name,
          "status": "Completed"
        },
        fields=["*"]
      )
      return appraisals
    except Exception as e:
      frappe.log_error(frappe.get_traceback(), "Error en get_completed_evaluations_for_employee")
      raise e
    
  def update_employee_appraisal(appraisal_name, goals, remarks, stop_action, continue_action, start_action, supervisor_feedback):
    """
    Actualiza la autoevaluación del empleado o la puntuación del evaluador en un Appraisal.
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
                "success": False,
                "message": _("La evaluación no existe."),
            }

        # Obtener el documento sin validar
        appraisal = frappe.get_doc("Appraisal", appraisal_name)

        # Actualizar autoevaluaciones o puntuaciones de los objetivos
        for goal_data in goals:
            for goal in appraisal.goals:
                if goal.name == goal_data.get("name"):
                    # Si viene self_assessment, es el empleado
                    if "self_assessment" in goal_data:
                        goal.self_assessment = goal_data.get("self_assessment", 0)
                    # Si viene score, es el evaluador
                    if "score" in goal_data:
                        goal.score = goal_data.get("score", 0)
                    break

        # Actualizar puntuaciones del supervisor feedback (solo empleado)
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
            "success": True,
            "message": _("Evaluación actualizada correctamente."),
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(
            frappe.get_traceback(), "Error en update_employee_appraisal"
        )
        return {
            "success": False,
            "message": f"Ocurrió un error al actualizar la evaluación: {str(e)}",
        }