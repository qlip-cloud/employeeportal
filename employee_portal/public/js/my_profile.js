function initializeEmployeeForm() {
    $('#employee-form').on('submit', function (e) {
        e.preventDefault(); 
    
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
            "employee-number": employeeNumber,
            "emergency-phone": emergencyPhone,
            "emergency-contact": emergencyContact
        };
    
        // Call the server-side function
        frappe.call({
            method: 'employee_portal.employee_portal.services.employee.update_employee_info',
            args: formData,
            callback: function (response) {
                if (response && !response.exc) {
                    frappe.msgprint({
                        title: __('Success'),
                        indicator: 'green',
                        message: __('Los datos se han actualizado correctamente.')
                    });
                }
            },
            error: function () {
                frappe.msgprint({
                    title: __('Error'),
                    indicator: 'red',
                    message: __('No se pudieron guardar los datos. Intente de nuevo.')
                });
            }
        });
    });

}    
