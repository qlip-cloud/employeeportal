frappe.listview_settings['Appraisal'] = {
	onload: function(listview) {
		listview.page.add_inner_button(__('Bulk Appraise Employees'), function() {
			// Crear diálogo para creación masiva de evaluaciones
			let dialog = new frappe.ui.Dialog({
				title: __('Crear Evaluaciones Masivas'),
				fields: [
					{
						fieldname: 'employees',
						label: __('Empleados'),
						fieldtype: 'MultiSelectList',
						reqd: 1,
						get_data: function(txt) {
							return frappe.db.get_link_options('Employee', txt);
						}
					},
					{
						fieldname: 'appraisal_template',
						label: __('Plantilla de Evaluación'),
						fieldtype: 'Link',
						options: 'Appraisal Template',
						reqd: 1,
						description: __('Seleccione la plantilla de evaluación a utilizar')
					},
					{
						fieldname: 'col_break',
						fieldtype: 'Column Break'
					},
					{
						fieldname: 'start_date',
						label: __('Fecha de Inicio'),
						fieldtype: 'Date',
						reqd: 1,
						default: frappe.datetime.get_today()
					},
					{
						fieldname: 'end_date',
						label: __('Fecha Final'),
						fieldtype: 'Date',
						reqd: 1
					}
				],
				primary_action_label: __('Crear Evaluaciones'),
				primary_action: function(values) {
					// Validar que se hayan seleccionado empleados
					if (!values.employees || values.employees.length === 0) {
						frappe.msgprint(__('Por favor seleccione al menos un empleado'));
						return;
					}
					
					// Validar fechas
					if (values.start_date && values.end_date) {
						if (frappe.datetime.get_diff(values.end_date, values.start_date) < 0) {
							frappe.msgprint(__('La fecha final debe ser mayor que la fecha de inicio'));
							return;
						}
					}
					
					dialog.hide();
					
					frappe.call({
						method: 'employee_portal.employee_portal.api.bulk_create_appraisals',
						args: {
							employees: values.employees,
							appraisal_template: values.appraisal_template,
							start_date: values.start_date,
							end_date: values.end_date
						},
						freeze: true,
						freeze_message: __('Creando evaluaciones...'),
						callback: function(r) {
							if (r.message && r.message.status === 'success') {
								frappe.show_alert({
									message: r.message.message,
									indicator: 'green'
								}, 5);
								
								// Mostrar errores si los hay
								if (r.message.errors && r.message.errors.length > 0) {
									frappe.msgprint({
										title: __('Algunas evaluaciones no se pudieron crear'),
										message: r.message.errors.join('<br>'),
										indicator: 'orange'
									});
								}
								
								// Refrescar la lista
								listview.refresh();
							} else {
								frappe.msgprint({
									title: __('Error'),
									message: r.message.message || __('Error al crear las evaluaciones'),
									indicator: 'red'
								});
							}
						}
					});
				}
			});
			
			dialog.show();
		});
	}
};