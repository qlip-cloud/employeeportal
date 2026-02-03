(function(){
  $('#send-vacation').off('click').on('click', function () {
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
  });
})();