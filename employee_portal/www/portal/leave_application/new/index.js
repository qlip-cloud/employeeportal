
(function () {

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
    $('#send-application').off('click').on('click', saveLeaveApplication);
  }, 0);
})();