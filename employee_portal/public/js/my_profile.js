$(document).ready(function() {
  $('#employee-form').on('submit', function(e) {
      e.preventDefault(); 
      
      var formData = $(this).serialize(); 

      $.ajax({
          method: "POST",
          url: "/api/method/employee_portal.api.update_employee_info?employee_id={{employee.name}}", 
          data: formData,
          success: function(response) {
              var messageDiv = $('#message');
              console.log(response);
              if (response.status === "success") {
                  messageDiv.html('<div class="alert alert-success">' + response.message + '</div>');
              } else {
                  messageDiv.html('<div class="alert alert-danger">' + response.message + '</div>');
              }
          },
          error: function(xhr, status, error) {
              $('#message').html('<div class="alert alert-danger">Error en la actualización: ' + error + '</div>');
          }
      });
  });
});
