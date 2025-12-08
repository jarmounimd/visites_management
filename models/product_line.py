from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VisiteProductLine(models.Model):
    _name = 'visite.product.line'
    _description = 'Ligne de Produit Vendue'
    _order = 'id'

    visite_id = fields.Many2one('visite.result', string='Visite', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.template', string='Produit', required=True, ondelete='restrict')
    quantity = fields.Integer(string='Quantité', required=True, default=1)
    unit_price = fields.Float(string='Prix Unitaire', related='product_id.list_price', readonly=True)
    subtotal = fields.Float(string='Sous-total', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError("La quantité doit être supérieure à zéro")

    @api.constrains('unit_price')
    def _check_price(self):
        for record in self:
            if record.unit_price < 0:
                raise ValidationError("Le prix unitaire ne peut pas être négatif")
