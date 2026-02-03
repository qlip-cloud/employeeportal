
(function () {

  function updateAppraisal() {
    var appraisal_name = $('#appraisal-name').val();
    var is_employee_view = $('#is-employee-view').val() === 'true';
    var is_appraiser_view = $('#is-appraiser-view').val() === 'true';
    
    var goals = [];
    
    // Si es vista del empleado, recoger self_assessment
    if (is_employee_view) {
      $('.goal-self-assessment').each(function() {
        goals.push({
          name: $(this).data('goal-name'),
          self_assessment: parseFloat($(this).val()) || 0
        });
      });
    }
    // Si es vista del evaluador, recoger score
    else if (is_appraiser_view) {
      $('.goal-score').each(function() {
        goals.push({
          name: $(this).data('goal-name'),
          score: parseFloat($(this).val()) || 0
        });
      });
    }
    
    console.log(goals);
    console.log(is_employee_view);
    console.log(is_appraiser_view);
    var supervisor_feedback = [];
    // Solo el empleado puede llenar la evaluación del supervisor
    if (is_employee_view) {
      $('.supervisor-score').each(function() {
        supervisor_feedback.push({
          name: $(this).data('supervisor-name'),
          score_earned: parseFloat($(this).val()) || 0
        });
      });
    }
    
    var remarks = $('#remarks').val();
    var stop_action = $('#stop-action').val();
    var continue_action = $('#continue-action').val();
    var start_action = $('#start-action').val();
    var valid = true;
    
    // Validar puntuaciones
    goals.forEach(function(goal) {
      var score = goal.self_assessment || goal.score || 0;
      if (score < 0 || score > 5) {
        valid = false;
      }
    });
    supervisor_feedback.forEach(function(feedback) {
      if (feedback.score_earned < 0 || feedback.score_earned > 5) {
        valid = false;
      }
    });
    
    if (!valid) {
      frappe.msgprint({
        title: 'Error',
        message: 'Las puntuaciones deben estar entre 0 y 5',
        indicator: 'red',
      });
      return;
    }
    
    // Enviar datos al backend
    frappe.call({
      method: 'employee_portal.api.evaluation.update_employee_appraisal',
      freeze: true,
      args: {
        appraisal_name: appraisal_name,
        goals: goals,
        remarks: remarks,
        stop_action: stop_action,
        continue_action: continue_action,
        start_action: start_action,
        supervisor_feedback: supervisor_feedback
      },
      callback: function(r) {
        var response = r.message;
        if (response.success == true) {
          frappe.msgprint({
            title: 'Notificación',
            message: 'La evaluación ha sido actualizada correctamente',
            indicator: 'green',
          });
        } else {
          frappe.msgprint({
            title: 'Error',
            message: response.message || 'Ocurrió un error al guardar',
            indicator: 'red',
          });
        }
      }
    });
  }

  setTimeout(function() {
    $('#appraisal-save').off('click').on('click', updateAppraisal);
  }, 0);
})();