$(document).ready(function() {
  $('#profile-save').off('click').on('click', function() {
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
    };
    if (!data.first_name || !data.last_name || !data.dob || !data.gender) {
      frappe.msgprint({
        title: 'Error',
        message: 'Por favor, completa los campos obligatorios',
        indicator: 'red',
      });
      return;
    }
    frappe.call({
      method: 'employee_portal.www.employee_portal.profile.index.save_profile',
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
              message: 'Tu perfil ha sido actualizado',
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
  } );
});