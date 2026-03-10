frappe.listview_settings['Appraisal'] = {
	onload: function(listview) {
		listview.page.add_inner_button(__('Crear Evaluaciones Masivas'), function() {
			// Crear diálogo para creación masiva de evaluaciones
			let dialog = new frappe.ui.Dialog({
				title: __('Crear Evaluaciones Masivas'),
				fields: [
					{
						fieldname: 'company',
						label: __('Compañía'),
						fieldtype: 'Link',
						options: 'Company',
						reqd: 1
					},
					{
						fieldname: 'kra_template',
						label: __('Plantilla de Evaluación'),
						fieldtype: 'Link',
						options: 'Appraisal Template',
						reqd: 1,
						description: __('Seleccione la plantilla de evaluación a utilizar')
					},
					{
						fieldname: 'is_performance_review',
						label: __('¿Es Evaluación de Desempeño?'),
						fieldtype: 'Check',
						default: 0
					},
					{
						fieldname: 'second_kra_template',
						label: __('Segunda Plantilla de Evaluación (Supervisor)'),
						fieldtype: 'Link',
						options: 'Appraisal Template',
						depends_on: 'eval:doc.is_performance_review==1',
						description: __('Seleccione la plantilla para la evaluación del supervisor')
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
		
					
					// Validar fechas
					if (values.start_date && values.end_date) {
						if (frappe.datetime.get_diff(values.end_date, values.start_date) < 0) {
							frappe.msgprint(__('La fecha final debe ser mayor que la fecha de inicio'));
							return;
						}
					}
					
					dialog.hide();
					
					frappe.call({
						method: 'employee_portal.api.evaluation.bulk_create_appraisals',
						args: {
							company: values.company,
							kra_template: values.kra_template,
							second_kra_template: values.second_kra_template,
							start_date: values.start_date,
							end_date: values.end_date,
							is_performance_review: values.is_performance_review
						},
						freeze: true,
						freeze_message: __('Creando evaluaciones...'),
						callback: function(r) {
							if (r.message && r.message.success) {
								frappe.show_alert({
									message: __('Evaluaciones creadas exitosamente'),
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
									message: __('Error al crear las evaluaciones'),
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