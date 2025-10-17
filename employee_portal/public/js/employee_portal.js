function initEmployeePortalEvents(){
    $('#profile-save').off('click').on('click', function() {
    $("#loader-overlay").fadeIn(200);
    var employee_id = $('#employee-name').val();
    var data = {
      'first_name': $('#first_name').val(),
      'middle_name': $('#middle_name').val(),
      'last_name': $('#last_name').val(),
      'dob': $('#dob').val(),
      'gender': $('#gender').val(),
      'employee_number': $('#employee-number').val(),
      'emergency_phone': $('#emergency-phone').val(),
      'emergency_contact': $('#emergency-contact').val(),
      'relation': $('#relation').val(),
      'current_accommodation_type': $('#current_accommodation_type').val(),
      'current_address': $('#current_address').val(),
      'health_details': $('#health_details').val(),
      'family_background': $('#family_background').val()
    };
    if (!data.first_name || !data.last_name || !data.dob || !data.gender) {
      $("#loader-overlay").fadeOut(200);
      frappe.msgprint({
        title: 'Error',
        message: 'Por favor, completa los campos obligatorios',
        indicator: 'red',
      });
      return;
    }
    frappe.call({
      method: 'employee_portal.employee_portal.uses_cases.employee.employee.save_profile',
      freeze: true,
      args: {
        employee_id: employee_id,
        data: data
      },
      callback: function(r) {
        $("#loader-overlay").fadeOut(200);
        response = r.message;
        console.log(response);
        if (response.status == 'success') {
          frappe.msgprint(
            {
              title: 'Notificación',
              message: 'Tu información ha sido actualizada',
              indicator: 'green',
            }
          );
        } else {
          frappe.msgprint({
            title: 'Error',
            message: response.error,
            indicator: 'red',
          }
          );
          console.error(response.error);
        }
      }
    });
  });

  $('#send-vacation').off('click').on('click', function() {
    var employee_id = $('#employee-name').val();

    // Validación días mínimos de vacaciones
    var fromDate = new Date($('#from-datetime').val());
    var toDate = new Date($('#to-datetime').val());

    var diffMs = toDate - fromDate;
    var diffDays = diffMs / (1000 * 60 * 60 * 24);

    if (diffDays < 6) {
      frappe.msgprint({
        title: 'Error',
        message: 'El período de vacaciones debe ser de al menos 6 días.',
        indicator: 'red',
      });
      return;
    }

    // Validación días disponibles de vacaciones
    var remainigVacationDays = parseInt($('#remaining-vacation-days').val());
    if (diffDays > remainigVacationDays) {
      frappe.msgprint({
        title: 'Error',
        message: 'Solo tienes ' + remainigVacationDays + ' días de vacaciones disponibles.',
        indicator: 'red',
      });
      return;
    }

    // Validación solicitud realizada con al menos dos meses de anticipación
    var today = new Date();
    var requestedDate = new Date($('#from-datetime').val());
    var minRequestDate = new Date();
    minRequestDate.setDate(today.getDate() + 60);
    if (requestedDate < minRequestDate) {
      frappe.msgprint({
        title: 'Error',
        message: 'La solicitud debe ser realizada con al menos 2 meses de anticipación.',
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
      'period_from': $('#period-from').val(),
      'period_to': $('#period-to').val(),
      'description': $('#description').val(),
      'status': $('#leave-status').val(),
      'replacement': $('#replacement').val(),
      'follow_via_email': true,
    };

    if (!data.employee || !data.posting_date || !data.department || !data.employee_name || !data.status || !data.from_date || !data.to_date || !data.description) {
      frappe.msgprint({
        title: 'Error',
        message: 'Por favor, completa los campos obligatorios',
        indicator: 'red',
      });
      return;
    }

    frappe.call({
      method: 'employee_portal.employee_portal.uses_cases.employee.employee.create_leave_application_vacation_type',
      args: {
        employee_id: employee_id,
        data: data
      },
      callback: function(r) {
        var response = r.message;
        if (response.status == 'success') {
          frappe.msgprint({
            title: 'Notificación',
            message: 'Tu solicitud de vacaciones ha sido enviada',
            indicator: 'green',
          });
          loadModule('/employee_portal/vacations');
        } else {
          frappe.msgprint({
            title: 'Error',
            message: response.message,
            indicator: 'red',
          });
        }
      }
    });
  });

  $('#send-application').off('click').on('click', function() {
    var employee_id = $('#employee-name').val();
    var fromDatetime = new Date($('#from-datetime').val());
    var toDatetime = new Date($('#to-datetime').val());
    var fromDate = fromDatetime.toISOString().split('T')[0];
    var toDate = toDatetime.toISOString().split('T')[0];

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

    if (diffHours > 24) {
      frappe.msgprint({
        title: 'Error',
        message: 'El permiso no puede exceder 1 día.',
        indicator: 'red',
      });
      return;
    }
    

    var data = {
      'employee' : $('#employee-name').val(),
      'employee_name' : $('#employee-full-name').val(),
      'company' : $('#company').val(),
      'department' : $('#department').val(),
      'leave_approver' : $('#leave-approver').val(),
      'leave_type' : $('#leave-type').val(),
      'posting_date' : $('#posting-date').val(),
      'from_date' : fromDate,
      'to_date' : toDate,
      'from_datetime' : $('#from-datetime').val(),
      'to_datetime' : $('#to-datetime').val(),
      'description' : $('#description').val(),
      'status' : $('#leave-status').val(),
      
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
      method: 'employee_portal.employee_portal.uses_cases.employee.employee.create_leave_application',
      args: {
        data: data
      },
      callback: function(r) {
        response = r.message;
        if (response.status == 'success') {
          frappe.msgprint(
            {
              title: 'Notificación',
              message: 'Tu solicitud de permiso ha sido enviada',
              indicator: 'green',
            }
          );
        loadModule('/employee_portal/leave_application');
        } else {
          frappe.msgprint({
            title: 'Error',
            message: response.message,
            indicator: 'red',
          }
          );
        }
      }
    });
  });

}


$(document).ready(function() {
  initEmployeePortalEvents();
});


$(document).on('router:page_loaded', function(e, url) {
  initEmployeePortalEvents();
});
