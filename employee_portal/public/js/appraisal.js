frappe.ui.form.on('Appraisal', {
	refresh(frm) {
		frm.add_custom_button("Generar Empleado", function () {
			let d = new frappe.ui.Dialog({
				title: "Generar nuevo Empleado",
				fields: [
					{
						label: "Usuario del empleado",
						fieldname: "user_id",
						fieldtype: "Link",
						options: "User",
						reqd: 1
					},
					{
						label: "Jefe inmediato",
						fieldname: "supervisor_user_id",
						fieldtype: "Link",
						options: "Employee"
					},
					{
						label: "Fecha de ingreso",
						fieldname: "date_of_joining",
						fieldtype: "Date"
					},
					{
						label: "Puesto",
						fieldname: "designation",
						fieldtype: "Link",
						options: "Designation"
					},
					{
						label: "Departamento",
						fieldname: "department",
						fieldtype: "Link",
						options: "Department"
					}
				],
				primary_action_label: "Crear",
				primary_action(values) {
					if (!values.user_id || !values.supervisor_user_id) {
						frappe.msgprint("Debes ingresar el usuario del empleado y el del jefe.");
						return;
					}

					frappe.db.get_value("Employee", { user_id: values.user_id }, "name")
						.then(r => {
							if (r.message && r.message.name) {
								frm.set_value("employee", r.message.name);
								frappe.msgprint("Empleado existente asignado al Appraisal.");
								d.hide();
							} else {
								frappe.db.get_value("User", values.user_id, ["first_name", "last_name"])
									.then(user_res => {
										let user_data = user_res.message || {};

										frappe.call({
											method: "frappe.client.insert",
											args: {
												doc: {
													doctype: "Employee",
													user_id: values.user_id,
													reports_to: values.supervisor_user_id,
													date_of_joining: values.date_of_joining || undefined,
													designation: values.designation || undefined,
													department: values.department || undefined,
													first_name: user_data.first_name || "",
													last_name: user_data.last_name || ""
												}
											},
											callback: function (res) {
												if (!res.exc) {
													frm.set_value("employee", res.message.name);
													frappe.msgprint("Empleado creado y asignado al Appraisal.");
													d.hide();
												}
											}
										});
									});
							}
						});
				}
			});

			d.show();
		});
	},
	supervisor_template: function (frm) {
		frm.doc.supervisor_feedback = [];
		erpnext.utils.map_current_doc({
			method: "employee_portal.employee_portal.override.appraisal.fetch_supervisor_template",
			source_name: frm.doc.supervisor_template,
			frm: frm
		});
	},

	calculate_supervisor_total: function (frm) {
		let goals = frm.doc.supervisor_feedback || [];
		let total = 0;

		if (goals == []) {
			frm.set_value('total_supervisor_score', 0);
			return;
		}
		for (let i = 0; i < goals.length; i++) {
			total = flt(total) + flt(goals[i].score_earned)
		}
		if (!isNaN(total)) {
			frm.set_value('total_supervisor_score', total);
			frm.refresh_field('calculate_supervisor_total');
		}
	},

	set_supervisor_score_earned: function (frm) {
		let supervisor_feedback = frm.doc.supervisor_feedback || [];
		for (let i = 0; i < supervisor_feedback.length; i++) {
			var d = locals[supervisor_feedback[i].doctype][supervisor_feedback[i].name];
			if (d.score && d.per_weightage) {
				d.score_earned = flt(d.per_weightage * d.score, precision("score_earned", d)) / 100;
			}
			else {
				d.score_earned = 0;
			}
			refresh_field('score_earned', d.name, 'supervisor_feedback');
		}
		frm.trigger('calculate_supervisor_total');
	},

	set_score_earned: function (frm) {
		let goals = frm.doc.goals || [];
		for (let i = 0; i < goals.length; i++) {
			var d = locals[goals[i].doctype][goals[i].name];
			let score = flt(d.score);
			let self_score = flt(d.self_assessment);
			let avg_score = 0;
			if (score || self_score) {
				avg_score = (score && self_score) ? (score + self_score) / 2 : (score || self_score);
			}
			if (avg_score && d.per_weightage) {
				d.score_earned = flt(d.per_weightage * avg_score, precision("score_earned", d)) / 100;
				console.log(d.score_earned);
			} else {
				d.score_earned = 0;
			}

			refresh_field('score_earned', d.name, 'goals');
		}
		frm.trigger('calculate_total');
	}

});

frappe.ui.form.on('Appraisal Goal', {
	score: function (frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (flt(d.score) > 5) {
			frappe.msgprint(__("Score must be less than or equal to 5"));
			d.score = 0;
			refresh_field('score', d.name, 'goals');
		}
		else {
			frm.trigger('set_score_earned');
		}
	},
	self_assessment: function (frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (flt(d.self_assessment) > 5) {
			frappe.msgprint(__("Self Assessment must be less than or equal to 5"));
			d.self_assessment = 0;
			refresh_field('self_assessment', d.name, 'goals');
		}
		frm.trigger('set_score_earned');
	},
	per_weightage: function (frm) {
		frm.trigger('set_score_earned');
	},
	goals_remove: function (frm) {
		frm.trigger('set_score_earned');
	}
});


frappe.ui.form.on('Appraisal Supervisor Goal', {
	score: function (frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (flt(d.score) > 5) {
			frappe.msgprint(__("Score must be less than or equal to 5"));
			d.score = 0;
			refresh_field('score', d.name, 'supervisor_feedback');
		}
		else {
			frm.trigger('set_supervisor_score_earned');
		}
	},
	per_weightage: function (frm) {
		frm.trigger('set_supervisor_score_earned');
	},
	goals_remove: function (frm) {
		frm.trigger('set_supervisor_score_earned');
	}
});