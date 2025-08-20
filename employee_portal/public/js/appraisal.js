frappe.ui.form.on('Appraisal', {
	kra_template: function (frm) {
		if (frm.doc.kra_template) {
			frappe.db.get_value('Appraisal Template', frm.doc.kra_template, 'is_180_evaluation')
				.then(r => {
					if (r.message) {
						frm.set_value('is_180_evaluation', r.message.is_180_evaluation);
						frm.trigger('toggle_180_fields');
					}
				});
		}
	},

	refresh: function (frm) {
		frm.trigger('toggle_180_fields');
	},

	toggle_180_fields: function (frm) {
		let show = frm.doc.is_180_evaluation;

		const fields = [
			'start_action',
			'stop_action',
			'cb_actions',
			'continue_action',
			'sb_action_plan',
			'sb_supervisor',
			'total_supervisor_score',
			'supervisor_feedback',
			'supervisor_template',
			'remarks'
		];

		fields.forEach(f => {
			frm.toggle_display(f, show);
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