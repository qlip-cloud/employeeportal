$(document).ready(function() {
  $('#send-application').off('click').on('click', function() {
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
    var requestDate = new Date($('#posting-date').val());
    var minRequestDate = new Date();
    minRequestDate.setDate(today.getDate() + 60);

    if (requestDate < minRequestDate) {
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
      'replacement': $('#replacement').val()  
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
      method: 'employee_portal.www.employee_portal.leave_application.new.index.send_application',
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

  function loadModule(url) {
    $('#dynamic-content').fadeOut(200, function() {
      $(this).load(url + ' #dynamic-content > *', function(response, status, xhr) {
        if (status !== "error") {
          $(this).fadeIn(200);
        }
      });
    });
  }
});
