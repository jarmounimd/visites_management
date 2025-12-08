from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    product_line_ids = fields.One2many('visite.product.line', 'product_id', string="product_lines")

    