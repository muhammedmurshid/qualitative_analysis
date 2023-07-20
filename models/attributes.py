from odoo import models, fields, api, _


class QualitativeAttributes(models.Model):
    _name = 'quality.attributes'
    _description = 'Qualitative Attributes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'attribute_type'

    attribute_type = fields.Text(string='Attribute')

