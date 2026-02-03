
(function () {
  function approve_leave_application(leave_application_name) {
    // Mostrar loader
    $("#loader-overlay").fadeIn(200);
    
    frappe.call({
      method: 'employee_portal.api.leave_application.approve_leave_application',
      freeze: true,
      args: {
        'leave_application_name': leave_application_name,
        'approver_user': frappe.session.user
      },
      callback: function (r) {
        $("#loader-overlay").fadeOut(200);
        
        if (r.message?.success) {
          frappe.msgprint({
            title: __('Éxito'),
            message: r.message.message,
            indicator: 'green',
          });
          // Recargar la página para reflejar los cambios
          location.reload();
          
        } else {
          frappe.msgprint({
            title: __('Error'),
            message: r.message?.message || __('Error al aprobar la solicitud de permiso'),
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
    $('#approve-leave-application').off('click').on('click', function() {
      const leave_application_name = $('#leave-name').val();
      approve_leave_application(leave_application_name);
    });
  
    
  }, 0);
})();