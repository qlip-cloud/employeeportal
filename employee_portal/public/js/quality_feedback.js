function removeColumns(frm, fields, table) {
    let grid = frm.get_field(table).grid;

    for (let field of fields) {
        grid.fields_map[field].hidden = 1;
    }

    grid.visible_columns = undefined;
    grid.setup_visible_columns();

    if (grid.header_row) {
        grid.header_row.wrapper.remove();
        delete grid.header_row;
    }
    grid.make_head();

    for (let row of grid.grid_rows) {
        if (row.open_form_button) {
            row.open_form_button.parent().remove();
            delete row.open_form_button;
        }

        for (let field in row.columns) {
            if (row.columns[field] !== undefined) {
                row.columns[field].remove();
            }
        }
        delete row.columns;
        row.columns = [];
        row.render_row();
    }
}
frappe.ui.form.on('Quality Feedback', {
    template: function(frm) {
        frm.trigger("toggle_fields_based_on_template");
    },

    toggle_fields_based_on_template: function(frm) {
        const esEvaluacion = frm.doc.template && frm.doc.template.startsWith("Evaluación de Desempeño");
        frm.set_df_property("pr_fecha_feedback", "hidden", !esEvaluacion);
        frm.set_df_property("pr_periodo_evaluado", "hidden", !esEvaluacion);
        frm.set_df_property("pr_jefe_inmediato", "hidden", !esEvaluacion);
        frm.set_df_property("sb_fortalezas", "hidden", !esEvaluacion);
        frm.set_df_property("pr_fortalezas", "hidden", !esEvaluacion);
        frm.set_df_property("sb_plan", "hidden", !esEvaluacion);
        frm.set_df_property("pr_acciones_mejora", "hidden", !esEvaluacion);
        frm.set_df_property("pr_lecciones", "hidden", !esEvaluacion);
        frm.set_df_property("pr_buenas_practicas", "hidden", !esEvaluacion);
        //frm.set_df_property("sb_eva_jefe", "hidden", !esEvaluacion);
        //frm.set_df_property("pr_supervisor_feedback", "hidden", !esEvaluacion);
        frm.set_df_property("asunto", "hidden", esEvaluacion);
        frm.set_df_property("cl_consultor", "hidden", esEvaluacion);
        frm.set_df_property("incidencia", "hidden", esEvaluacion);
        

        const grid = frm.fields_dict["parameters"]?.grid;
        if (grid) {
            grid.update_docfield_property("autoevaluacion", "read_only", !esEvaluacion);

            if (!esEvaluacion) {
                (frm.doc.parameters || []).forEach(row => {
                    row.autoevaluacion = null;
                });
                removeColumns(frm, ["autoevaluacion"], "parameters");
            }else{
                grid.fields_map["autoevaluacion"].hidden = 0;
                grid.visible_columns = undefined;
                grid.setup_visible_columns();
                grid.refresh();
            }
            frm.refresh_field("parameters");
        }

    }
});

frappe.ui.form.on('Quality Feedback Parameter', {
    form_render: function(frm, cdt, cdn) {
        const child = locals[cdt][cdn];
        const parent = locals[child.parenttype][child.parent];
        const mostrar = parent?.template && parent.template.startsWith("Evaluación de Desempeño");
        frm.toggle_display('autoevaluacion', mostrar);
    }
});
