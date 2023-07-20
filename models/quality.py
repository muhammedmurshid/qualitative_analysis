from odoo import models, fields, api, _


class QualitativeAnalysis(models.Model):
    _name = 'base.qualitative.analysis'
    _description = 'Qualitative Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one('hr.employee', string='Employee Name',
                           domain=lambda self: [('parent_id.user_id', '=', self.env.user.id)], required=True)

    current_user_id = fields.Many2one('res.users', string='Current User',
                                      default=lambda self: self.env.user)
    added_date = fields.Date(string='Date')
    attribute_ids = fields.One2many('attribute.tree', 'attr_id', string='Attribute',
                                    copy=False, unique=True)
    quality_type = fields.Selection([('weekly', 'Weekly'), ('monthly', 'Monthly')], string='Type')

    # total_performance_percent = fields.Float(string='Total Performance')

    # incase the total performance calculation is using
    @api.depends('attribute_ids.performance_no')
    def _compute_performance(self):
        total = 0
        for order in self.attribute_ids:
            total += order.performance_no
        self.update({
            'total_performance': total,
        })

    total_performance = fields.Integer(string='Total Performance', compute='_compute_performance', store=True)

    # this is the total rating counts
    @api.depends('attribute_ids.stars_count')
    def _compute_counts(self):
        total = 0
        for order in self.attribute_ids:
            total += order.stars_count
        self.update({
            'total_stars_count': total,
        })

    total_stars_count = fields.Integer(string='Total Rating', compute='_compute_counts', store=True)

    # compute total performance percentage
    @api.depends('total_performance', 'total_stars_count')
    def _compute_percentage(self):
        if self.total_performance != 0:
            if self.total_stars_count != 0:
                self.update({
                    'work_performance': self.total_performance / self.total_stars_count * 100,
                })

    work_performance = fields.Float(string='Performance (%)', compute='_compute_percentage', store=True)

    _sql_constraints = [
        ('attribute_uniq', 'unique (attribute)', 'Duplicate Attribute is not allowed !')
    ]


class QualitativeAttributesTree(models.Model):
    _name = 'attribute.tree'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    attr_id = fields.Many2one('base.qualitative.analysis', string='Attribute')
    attribute = fields.Many2one('quality.attributes', string='Attribute', unique=True)

    performance = fields.Selection([
        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
    ], string='Performance')
    stars_count = fields.Integer(string='Stars Count', default=5)
    performance_no = fields.Float(string='Performance No', compute='_compute_performance_no', store=True)
    int_field = fields.Integer(string='Int Field')

    # this is the performance number added another field
    @api.depends('performance')
    def _compute_performance_no(self):
        for rec in self:
            if rec.performance == '0':
                rec.performance_no = 0
            elif rec.performance == '1':
                rec.performance_no = 1
            elif rec.performance == '2':
                rec.performance_no = 2
            elif rec.performance == '3':
                rec.performance_no = 3
            elif rec.performance == '4':
                rec.performance_no = 4
            elif rec.performance == '5':
                rec.performance_no = 5
