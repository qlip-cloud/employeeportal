document.getElementById("employee-form").addEventListener("submit", function (event) {
    event.preventDefault();
    // Get form data
    const employeeName = $('#employee-name').val().trim();
    const firstName = $('#first_name').val().trim();
    const middleName = $('#middle_name').val().trim();
    const lastName = $('#last_name').val().trim();
    const dob = $('#dob').val();
    const gender = $('#gender').val();
    const employeeNumber = $('#employee-number').val().trim();
    const emergencyPhone = $('#emergency-phone').val().trim();
    const emergencyContact = $('#emergency-contact').val().trim();
    const csrf_token = $('#csrf_token').val();
    console.log('csfr_token', csrf_token);

    if (!firstName || !lastName || !dob || !gender) {
        frappe.msgprint({
            title: __('Validation Error'),
            indicator: 'red',
            message: __('Por favor complete todos los campos obligatorios.')
        });
        return;
    }

    // Collect form data
    const formData = {
        name: employeeName, 
        first_name: firstName,
        middle_name: middleName,
        last_name: lastName,
        dob: dob,
        gender: gender,
        employee_number: employeeNumber,
        emergency_phone: emergencyPhone,
        emergency_contact: emergencyContact
    };

    fetch('/api/method/employee_portal.services.employee.update_employee_info', {
        method: 'POST',
        headers: {
            'X-Frappe-CSRF-Token': csrf_token
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al actualizar los datos');
        }
        return response.json();
    })
    .then(data => {
        frappe.msgprint({
            title: __('Éxito'),
            indicator: 'green',
            message: __('Datos actualizados correctamente.')
        });
    })
    .catch(error => {
        frappe.msgprint({
            title: __('Error'),
            indicator: 'red',
            message: error.message
        });
    });
});
