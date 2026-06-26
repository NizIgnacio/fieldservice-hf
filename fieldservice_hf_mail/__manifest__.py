{
    "name": "Field Service Mail",
    "description": "Used to send emails of field service orders",
    "version": "18.0.5.6.0",
    "depends": ["fieldservice"],
    "data": [
        "wizard/mail_wizard.xml",
        "views/mail_button.xml",
        "views/wizard_dni_field.xml",
        "views/form_dni_field.xml",
        "report/field_service_order_template.xml",
        "security/ir.model.access.csv"
    ]
}
