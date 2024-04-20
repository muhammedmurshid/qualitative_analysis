from odoo import models, fields, api, _


class QuantitativeAttributes(models.Model):
    _name = 'quantitative.attributes'
    _description = 'Quantitative Attributes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'attribute_type'

    attribute_type = fields.Text(string='Attribute', required=1)
    department_head = fields.Many2one('res.users', string='Department Head', related='department_id.manager_id.user_id')
    department_id = fields.Many2one('hr.department', string='Department', required=1)

