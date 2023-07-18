from odoo import models, fields, api, _


class QualitativeAnalysis(models.Model):
    _name = 'base.qualitative.analysis'
    _description = 'Qualitative Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one('hr.employee', string='Employee Name',
                           domain=lambda self: [('parent_id.user_id', '=', self.env.user.id)])
    performance = fields.Selection([
        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
    ], string='Performance')
    current_user_id = fields.Many2one('res.users', string='Current User',
                                      default=lambda self: self.env.user)
    added_date = fields.Date(string='Date')
    attribute = fields.Many2one('quality.attributes', string='Attribute')
