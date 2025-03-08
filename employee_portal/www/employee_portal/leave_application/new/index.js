$(document).ready(function() {
  $('#send-application').off('click').on('click', function() {
    var employee_id = $('#employee-name').val();
    var data = {
      'employee' : $('#employee').val(),
      'posting_date' : $('#posting-date').val(),
      'department' : $('#department').val(),
      'employee_name' : $('#employee-full-name').val(),
      'leave_type' : $('#leave-type').val(),
      'status' : $('#leave-status').val(),
      'from_date' : $('#from-datetime').val(),
      'to_date' : $('#to-datetime').val(),
      'reason' : $('#reason').val(),
      
    };
    if (!data.employee || !data.posting_date || !data.department || !data.employee_name || !data.leave_type || !data.status || !data.from_date || !data.to_date || !data.reason) {
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
        response = r.message;
        console.log(response);
        if (response.status == 'success') {
          frappe.msgprint(
            {
              title: 'Notificación',
              message: 'Tu solicitud de permiso ha sido enviada',
              indicator: 'green',
            }
          );
        } else {
          frappe.msgprint({
            title: 'Error',
            message: response.message,
            indicator: 'red',
          }
          );
          console.error(response.error);
        }
      }
    });
  } );

} );