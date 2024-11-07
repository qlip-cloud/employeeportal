frappe.ready(() => {
  console.log('New Endowment JS loaded');
  document.getElementById('endowment-form').addEventListener('submit', async function(event) {
      event.preventDefault();
      const formData = new FormData(this);

      // Validación de campos obligatorios
      if (!formData.get('title') || !formData.get('value') || !formData.get('date') || !formData.get('employee')) {
          alert('Por favor, completa todos los campos obligatorios.');
          return;
      }

      // Subir archivo
      const fileInput = document.getElementById('invoice');
      const file = fileInput.files[0];
      if (file) {
          const uploadData = new FormData();
          uploadData.append('file', file);
          uploadData.append('is_private', 0); // Opcional: define si el archivo es privado

          try {
              const fileResponse = await fetch('/api/method/upload_file', {
                  method: 'POST',
                  headers: {
                      'X-Frappe-CSRF-Token': frappe.csrf_token
                  },
                  body: uploadData
              });

              if (!fileResponse.ok) {
                  const errorResponse = await fileResponse.json();
                  alert('Error al subir el archivo: ' + (errorResponse.message || 'Error desconocido'));
                  return; // Detener el proceso si hay un error al subir el archivo
              }

              const fileData = await fileResponse.json();
              const fileUrl = fileData.message.file_url;

              // Agregar URL del archivo a formData
              formData.append('invoice', fileUrl);
          } catch (error) {
              alert(error.message);
              console.error('Error en la subida del archivo:', error);
              return; // Detener el proceso si hay un error al subir el archivo
          }
      }

      // Agregar el doctype al formData
      formData.append('doctype', 'Endowment'); // Asegúrate de agregar el doctype

      // Depurar el contenido del formData
      for (const [key, value] of formData.entries()) {
          console.log(`${key}: ${value}`);
      }

      try {
          const response = await fetch('/api/resource/Endowment', {
              method: 'POST',
              headers: {
                  'X-Frappe-CSRF-Token': frappe.csrf_token,
              },
              body: formData // Enviar el FormData directamente
          });

          if (response.ok) {
              const responseData = await response.json();
              alert('Comprobante de Dotación agregado con éxito.');
              window.location.href = '/employee_portal/endowment';
          } else {
              const error = await response.json();
              console.error('Error en la respuesta del servidor:', error); // Log del error
              alert('Error al agregar el comprobante: ' + (error.message || 'Error desconocido'));
          }
      } catch (err) {
          alert('Ocurrió un error al enviar el formulario.');
          console.error('Error en el envío del formulario:', err);
      }
  });
});
