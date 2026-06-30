{
    "name": "Field Service Mail",
    "description": "Used to send emails of field service orders",
    "version": "16.0.5.6.0",
    "depends": ["fieldservice"],
    "data": [
        "wizard/fsm_order_sign_wizard.xml",
        "wizard/mail_wizard.xml",
        "views/buttons.xml",
        "views/fsm_order_form_sign_page.xml",
        "report/field_service_order_template.xml",
        "security/ir.model.access.csv",
    ]
}
