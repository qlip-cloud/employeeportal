$(document).ready(function() {
  $('#send-endowment').off('click').on('click', function() {

    var data = {
      'employee': $('#employee_id').val(),
      'company': $('#company').val(),
      'department': $('#department').val(),
      'date': $('#date').val(),
      'period': $('#period').val(),
      'amount': $('#amount').val(),
      'items': [
        {
          'article': 'Camisa',
          'quantity': $('#quantity_camisa').val(),
          'description': $('#description_camisa').val(),
          'size': $('#size_camisa').val(),
        },
        {
          'article': 'Pantalón',
          'quantity': $('#quantity_pantalon').val(),
          'description': $('#description_pantalon').val(),
          'size': $('#size_pantalon').val(),
        },
        {
          'article': 'Zapatos',
          'quantity': $('#quantity_zapatos').val(),
          'description': $('#description_zapatos').val(),
          'size': $('#size_zapatos').val(),
        }
      ]
    };
    if (!data.employee || !data.date || !data.department || 
        !data.company || !data.amount || !data.period) {
      frappe.msgprint({
        title: 'Error',
        message: 'Por favor, completa los campos obligatorios',
        indicator: 'red',
      });
      return;
    }


    frappe.call({
      method: 'employee_portal.www.employee_portal.endowment.new.index.send_endowment',
      type: 'POST',
      args: {
        data: data
      },
      callback: function(r) {
        var response = r.message;
        if (response.status == 'success') {
          frappe.msgprint({
            title: 'Notificación',
            message: 'Tu comprobante de dotación ha sido enviado',
            indicator: 'green',
          });
          loadModule('/employee_portal/endowment');
        } else {
          frappe.msgprint({
            title: 'Error',
            message: response.message,
            indicator: 'red',
          });
        }
      },
      error: function(xhr, status, error) {
        console.error(error);
      }
    });
  })
  function loadModule(url) {
    $('#dynamic-content').fadeOut(200, function() {
      $(this).load(url + ' #dynamic-content > *', function(response, status, xhr) {
        if (status == "error") {
        } else {
          $(this).fadeIn(200);
        }
      });
    });
  }
});
