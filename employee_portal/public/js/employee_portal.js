function initEmployeePortalEvents() {
  function approve_leave_application(leave_application_name) {
    // Mostrar loader
    $("#loader-overlay").fadeIn(200);
    
    frappe.call({
      method: 'employee_portal.api.leave_application.approve_leave_application',
      freeze: true,
      args: {
        'leave_application_name': leave_application_name,
        'approver_user': frappe.session.user
      },
      callback: function (r) {
        $("#loader-overlay").fadeOut(200);
        
        if (r.message?.success) {
          frappe.msgprint({
            title: __('Éxito'),
            message: r.message.message,
            indicator: 'green',
          });
          // Recargar la página para reflejar los cambios
          location.reload();
          
        } else {
          frappe.msgprint({
            title: __('Error'),
            message: r.message?.message || __('Error al aprobar la solicitud de permiso'),
            indicator: 'red',
          });
        }
      },
      error: function (r) {
        $("#loader-overlay").fadeOut(200);
        frappe.msgprint({
          title: __('Error'),
          message: __('Error de conexión'),
          indicator: 'red',
        });
        console.error('Error:', r);
      }
    });
  }

  function sendVacationRequest() {
    var employee_id = $('#employee-name').val();

    // Validación días mínimos de vacaciones
    var fromDate = new Date($('#from-datetime').val());
    var toDate = new Date($('#to-datetime').val());

    var diffMs = toDate - fromDate;
    var diffDays = diffMs / (1000 * 60 * 60 * 24);

    // Validación días disponibles de vacaciones
    var remainigVacationDays = parseInt($('#remaining-vacation-days').val());
    if (diffDays > remainigVacationDays) {
      frappe.msgprint({
        title: 'Error',
        message: 'Solo tienes ' + remainigVacationDays + ' días de vacaciones disponibles durante el período seleccionado.',
        indicator: 'red',
      });
      return;
    }

    // Validación solicitud realizada con al menos un mes de anticipación
    var today = new Date();
    var requestedDate = new Date($('#from-datetime').val());
    var minRequestDate = new Date();
    minRequestDate.setDate(today.getDate() + 30);
    if (requestedDate < minRequestDate) {
      frappe.msgprint({
        title: 'Error',
        message: 'La solicitud debe ser realizada con al menos 1 mes de anticipación.',
        indicator: 'red',
      });
      return;
    }

   
    // Solicitud
    var data = {
      'employee': $('#employee-name').val(),
      'employee_name': $('#employee-full-name').val(),
      'company': $('input[name="company"]').val(),
      'department': $('#department').val(),
      'leave_approver': $('#leave-approver').val(),
      'leave_type': 'Vacaciones',
      'posting_date': $('#posting-date').val(),
      'from_date': $('#from-datetime').val(),
      'to_date': $('#to-datetime').val(),
      'description': $('#description').val(),
      'status': $('#leave-status').val(),
      'replacement': $('#replacement').val(),
      'follow_via_email': true,
    };

    if (!data.employee || !data.posting_date || !data.department || !data.employee_name || !data.status || !data.from_date || !data.to_date || !data.description) {
      console.log(data);
      frappe.msgprint({
        title: 'Error',
        message: 'Por favor, completa los campos obligatorios',
        indicator: 'red',
      });
      return;
    }

    frappe.call({
      method: 'employee_portal.api.leave_application.create_vacation_leave_application',
      args: {
        data: data
      },
      callback: function (r) {
        $("#loader-overlay").fadeOut(200);

        if (r.message?.success) {
          frappe.msgprint({
            title: __('Éxito'),
            message: r.message.message,
            indicator: 'green',
          });

        } else {
          frappe.msgprint({
            title: __('Error'),
            message: r.message?.message || __('Error al enviar la solicitud de permiso'),
            indicator: 'red',
          });
        }
      }
    });
  }

   function updateEmployeeProfile() {
    const requiredFields = ['first_name', 'last_name', 'dob', 'gender', 'employee_id_number'];

    const data = {
      'first_name': $('#first_name').val()?.trim(),
      'middle_name': $('#middle_name').val()?.trim(),
      'last_name': $('#last_name').val()?.trim(),
      'employee_id_number': $('#employee_id_number').val()?.trim(),
      'dob': $('#dob').val(),
      'gender': $('#gender').val(),
      'cell_number': $('#employee-number').val()?.trim(),
      'emergency_phone_number': $('#emergency-phone').val()?.trim(),
      'person_to_be_contacted': $('#emergency-contact').val()?.trim(),
      'relation': $('#relation').val(),
      'current_accommodation_type': $('#current_accommodation_type').val(),
      'current_address': $('#current_address').val()?.trim(),
      'health_details': $('#health_details').val()?.trim(),
      'family_background': $('#family_background').val()?.trim()
    };

    const missingFields = requiredFields.filter(field => !data[field]);

    if (missingFields.length > 0) {
      frappe.msgprint({
        title: __('Error'),
        message: __('Por favor, completa los campos obligatorios'),
        indicator: 'red',
      });
      return;
    }

    // Mostrar loader
    $("#loader-overlay").fadeIn(200);

    // Llamar API
    frappe.call({
      method: 'employee_portal.api.employee.update_profile',
      freeze: true,
      args: data,
      callback: function (r) {
        $("#loader-overlay").fadeOut(200);

        if (r.message?.success) {
          frappe.msgprint({
            title: __('Éxito'),
            message: r.message.message,
            indicator: 'green',
          });

        } else {
          frappe.msgprint({
            title: __('Error'),
            message: r.message?.message || __('Error al actualizar'),
            indicator: 'red',
          });
        }
      },
      error: function (r) {
        $("#loader-overlay").fadeOut(200);
        frappe.msgprint({
          title: __('Error'),
          message: __('Error de conexión'),
          indicator: 'red',
        });
        console.error('Error:', r);
      }
    });
  }
  function saveLeaveApplication() {
    
    var employee_id = $('#employee-name').val();
    var mentum_hours = parseFloat($('#mentum_hours').val()) || 0;
    var fromDatetime = new Date($('#from-datetime').val());
    var toDatetime = new Date($('#to-datetime').val());
    
    // Validar que las fechas sean válidas
    if (!isNaN(fromDatetime.getTime())){
      var fromDate = fromDatetime.toISOString().split('T')[0];
    } else{
      var fromDate = null;
    }
    if (!isNaN(toDatetime.getTime())){
      var toDate = toDatetime.toISOString().split('T')[0];
    }else{
      var toDate = null;
    }

    var diffMs = toDatetime - fromDatetime;
    var diffHours = diffMs / (1000 * 60 * 60);

    if (diffHours < 1) {
      frappe.msgprint({
        title: 'Error',
        message: 'El permiso debe ser de al menos 1 hora.',
        indicator: 'red',
      });
      return;
    }

    leave_type = $('#leave-type').val();
    if (leave_type == 'Permiso Personal' && diffHours>24) {
      frappe.msgprint({
        title: 'Error',
        message: 'El permiso de Horas Mentum no puede exceder 24 horas.',
        indicator: 'red',
      });
      return;
    }


    var data = {
      'employee': $('#employee-name').val(),
      'employee_name': $('#employee-full-name').val(),
      'company': $('#company').val(),
      'department': $('#department').val(),
      'leave_approver': $('#leave-approver').val(),
      'leave_type': $('#leave-type').val(),
      'posting_date': $('#posting-date').val(),
      'from_date': fromDate,
      'to_date': toDate,
      'from_datetime': $('#from-datetime').val(),
      'to_datetime': $('#to-datetime').val(),
      'description': $('#description').val(),
      'status': $('#leave-status').val(),

    };
    if (!data.employee || !data.posting_date || !data.department || !data.employee_name || !data.leave_type || !data.status || !data.from_datetime || !data.to_datetime || !data.description) {
      frappe.msgprint({
        title: 'Error',
        message: 'Por favor, completa los campos obligatorios',
        indicator: 'red',
      });
      return;
    }
    frappe.call({
      method: 'employee_portal.api.leave_application.create_leave_application',
      args: {
        data: data,
        mentum_hours: mentum_hours,
      },
      callback: function (r) {
        $("#loader-overlay").fadeOut(200);

        if (r.message?.success) {
          frappe.msgprint({
            title: __('Éxito'),
            message: r.message.message,
            indicator: 'green',
          });

        } else {
          frappe.msgprint({
            title: __('Error'),
            message: r.message?.message || __('Error al enviar la solicitud de permiso'),
            indicator: 'red',
          });
        }
      }
    });
  }
  setTimeout(function() {
    var calendarEl = document.getElementById('calendar');
    if (calendarEl) {
        var eventsData = document.getElementById('events_data');
        var events = eventsData ? JSON.parse(eventsData.value) : [];
        
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: events,
            editable: false,
            eventClick: function(info) {
                // Prevenir navegación si el evento tiene URL
                info.jsEvent.preventDefault();
                
                // Mostrar información del evento
                var eventDetails = 'Título: ' + info.event.title + '\n' +
                    'Inicio: ' + info.event.start.toLocaleString() + '\n' +
                    (info.event.end ? 'Fin: ' + info.event.end.toLocaleString() + '\n' : '') +
                    (info.event.extendedProps.location ? 'Ubicación: ' + info.event.extendedProps.location + '\n' : '') +
                    (info.event.extendedProps.trainer_name ? 'Entrenador: ' + info.event.extendedProps.trainer_name + '\n' : '') +
                    (info.event.extendedProps.introduction ? 'Descripción: ' + info.event.extendedProps.introduction + '\n' : '') 
                    ;
                
                
                event_details_html_formated = eventDetails.replace(/\n/g, "<br>");
                frappe.msgprint({
                    title: 'Detalles del Evento',
                    message: event_details_html_formated,
                    indicator: 'blue',
                });
            }
        });
        calendar.render();
    }
  }, 0);
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
web_include_js = "/assets/employee_portal/js/employee_portal.js"
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

  // Inicializar DataTables solo si existen los elementos y la librería está disponible
  if ($.fn.DataTable) {
    if ($('#table-applications').length) {
      $('#table-applications').DataTable();
    }
    if ($('#table-leaves').length) {
      $('#table-leaves').DataTable();
    }
    if ($('#table-my-employees-leaves').length) {
      $('#table-my-employees-leaves').DataTable();
    }
    if ($('#table-documents').length) {
      $('#table-documents').DataTable();
    }
    if ($('#activeEvaluationsTable').length) {
      $('#activeEvaluationsTable').DataTable();
    }
    if ($('#activeEvaluationsSupervisorTable').length) {
      $('#activeEvaluationsSupervisorTable').DataTable();
    }
    if ($('#completedEvaluationsTable').length) {
      $('#completedEvaluationsTable').DataTable();
    }
  }

  $('#approve-leave-application').off('click').on('click', function() {
      const leave_application_name = $('#leave-name').val();
      approve_leave_application(leave_application_name);
  });
  $('#profile-save').off('click').on('click', updateEmployeeProfile);
  $('#send-application').off('click').on('click', saveLeaveApplication);
  $('#appraisal-save').off('click').on('click', updateAppraisal);
  $('#send-vacation').off('click').on('click', function () {
    sendVacationRequest();
  });

}


$(document).ready(function () {
  initEmployeePortalEvents();
});


$(document).on('router:page_loaded', function (e, url) {
  initEmployeePortalEvents();
});
