$(document).ready(function() {
  $('#profile-save').off('click').on('click', function() {
    console.log("Profile save button clicked");
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
  } );
});