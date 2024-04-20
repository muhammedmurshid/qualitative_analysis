from odoo import models, fields, api


class QuantitativeAnalysis(models.Model):
    _name = 'quantitative.analysis'
    _description = 'Quantitative Analysis'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'

    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  domain=lambda self: [('parent_id.user_id', '=', self.env.user.id)], required=True)
    added_date = fields.Date(string='Date', default=fields.Date.today)
    attribute_ids = fields.One2many('quantitative.attribute.tree', 'attr_id', string='Attribute',
                                    copy=False, unique=True)
    quality_type = fields.Selection([('monthly', 'Monthly')], string='Type', default='monthly')

    def _compute_display_name(self):
        for order in self:
            order.display_name = order.employee_id.name + ' - ' + 'Rating'

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


class QuantitativeAttributesTree(models.Model):
    _name = 'quantitative.attribute.tree'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    attr_id = fields.Many2one('quantitative.analysis', string='Attribute')

    performance = fields.Selection([
        ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
    ], string='Performance')
    stars_count = fields.Integer(string='Stars Count', default=5)
    remarks = fields.Char(string='Remarks')
    performance_no = fields.Float(string='Performance No', compute='_compute_performance_no', store=True)

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

    @api.onchange('performance', 'attr_id')
    def _onchange_attributes(self):
        print('performance', self.attr_id.employee_id.department_id.name)
        print('dep', self.attribute.department_id.name)
        batch = self.env['quantitative.attributes'].sudo().search([])
        attrs = []
        for i in batch:
            print(i.department_id, 'nmae')
            if self.attr_id.employee_id.department_id.id == i.department_id.id:
                print(i.department_id.name, 'rrr')
                attrs.append(i.id)
        print(attrs, 'attrs')
        domain = [('id', 'in', attrs)]
        return {'domain': {'attribute': domain}}

    attribute = fields.Many2one('quantitative.attributes', string='Attribute', unique=True, domain=_onchange_attributes)
