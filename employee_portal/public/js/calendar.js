function initializeCalendar() {
  var calendarEl = document.getElementById('calendar');
  if (calendarEl) {
      var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          headerToolbar: {
              left: 'prev,next today',
              center: 'title',
              right: 'dayGridMonth,timeGridWeek,timeGridDay'
          },
          events: function(fetchInfo, successCallback, failureCallback) {
              frappe.call({
                  method: "employee_portal.api.get_events",
                  args: {},
                  callback: function(response) {
                      var events = response.message || [];
                      successCallback(events);
                  }
              });
          },
          editable: false
      });
      calendar.render();
  }
}
initializeCalendar();