
(function () {

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

  setTimeout(function() {
    $('#profile-save').off('click').on('click', updateEmployeeProfile);
  }, 0);
})();