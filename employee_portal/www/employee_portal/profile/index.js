$(document).ready(function() {

  console.log('Frappe ready');
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
    frappe.call({
      method: 'employee_portal.www.employee_portal.profile.index.save_profile',
      args: {
        employee_id: employee_id,
        data: data
      },
      callback: function(r) {
        response = r.message;
        if (response.success) {
          frappe.msgprint('Profile saved successfully');
        } else {
          frappe.msgprint('Error saving profile');
          console.error(response.error);
        }
      }
    });
  } );
});