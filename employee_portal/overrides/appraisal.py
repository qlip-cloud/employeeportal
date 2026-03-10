# Copyright (c) 2024, Ashley Mercado Defort and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt, getdate
from frappe import _
from erpnext.hr.doctype.appraisal.appraisal import Appraisal

class CustomAppraisal(Appraisal):
	"""
	Clase personalizada que extiende Appraisal para permitir
	la creación de evaluaciones sin puntajes (para creación masiva)
	"""
	
	def calculate_total(self):
		"""
		Sobreescribe el método calculate_total para permitir
		evaluaciones con total 0 cuando se están creando masivamente
		"""
		total, total_w = 0, 0
		for d in self.get('goals'):
			if d.score:
				d.score_earned = flt(d.score) * flt(d.per_weightage) / 100
				total = total + d.score_earned
			total_w += flt(d.per_weightage)

		if int(total_w) != 100:
			frappe.throw(_("Total weightage assigned should be 100%.<br>It is {0}").format(str(total_w) + "%"))

		# Modificación: Solo validar total != 0 si el documento ya está siendo enviado/submitted
		# Esto permite crear evaluaciones en borrador con total 0 para responder después
		if self.docstatus == 1:  # 1 = Submitted
			if frappe.db.get_value("Employee", self.employee, "user_id") != \
					frappe.session.user and total == 0:
				frappe.throw(_("Total cannot be zero"))

		self.total_score = total
