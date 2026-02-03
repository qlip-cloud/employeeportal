(function() {
  setTimeout(function() {
    var calendarEl = document.getElementById('calendar');
    if (calendarEl) {
        var eventsData = document.getElementById('events_data');
        var events = eventsData ? JSON.parse(eventsData.value) : [];
        
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: events,
            editable: false,
            eventClick: function(info) {
                // Prevenir navegación si el evento tiene URL
                info.jsEvent.preventDefault();
                
                // Mostrar información del evento
                var eventDetails = 'Título: ' + info.event.title + '\n' +
                    'Inicio: ' + info.event.start.toLocaleString() + '\n' +
                    (info.event.end ? 'Fin: ' + info.event.end.toLocaleString() + '\n' : '') +
                    (info.event.extendedProps.location ? 'Ubicación: ' + info.event.extendedProps.location + '\n' : '') +
                    (info.event.extendedProps.trainer_name ? 'Entrenador: ' + info.event.extendedProps.trainer_name + '\n' : '') +
                    (info.event.extendedProps.introduction ? 'Descripción: ' + info.event.extendedProps.introduction + '\n' : '') 
                    ;
                
                
                event_details_html_formated = eventDetails.replace(/\n/g, "<br>");
                frappe.msgprint({
                    title: 'Detalles del Evento',
                    message: event_details_html_formated,
                    indicator: 'blue',
                });
            }
        });
        calendar.render();
    }
  }, 0);
})();