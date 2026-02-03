function initEmployeePortalEvents() {

  $('#table-applications').DataTable();
  $('#table-leaves').DataTable();
  $('#table-my-employees-leaves').DataTable();
  $('#table-documents').DataTable();
  $('#activeEvaluationsTable').DataTable();
  $('#activeEvaluationsSupervisorTable').DataTable();
  $('#completedEvaluationsTable').DataTable();
}


$(document).ready(function () {
  initEmployeePortalEvents();
});


$(document).on('router:page_loaded', function (e, url) {
  initEmployeePortalEvents();
});
