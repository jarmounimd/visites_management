from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Result(models.Model):
    _name = 'visite.result'
    _description = 'Résultat de chaque visite'
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Référence', compute='_compute_name', store=True)
    visite_id = fields.Many2one('visite.management', string='Visite', ondelete='restrict')
    client_id = fields.Many2one('visite.client', string='Client', required=True, ondelete='restrict')
    date_visite = fields.Date(string='Date de visite', default=fields.Date.context_today, required=True)
    product_line_ids = fields.One2many('visite.product.line', 'visite_id', string='Produits Vendus')
    total_price = fields.Float(string='Prix Total', compute='_compute_total_price', store=True)
    result_remark = fields.Text(string='Remarque sur le résultat')
    note = fields.Selection([
        ('pending', 'En attente'),
        ('won', 'Gagné'),
        ('failed', 'Échoué')
    ], string='État', group_expand='_group_expand_notes', default='pending', required=True)

    @api.depends('client_id', 'date_visite')
    def _compute_name(self):
        for record in self:
            if record.client_id and record.date_visite:
                record.name = f"Résultat - {record.client_id.display_name} - {record.date_visite}"
            else:
                record.name = 'Nouveau résultat'

    @api.depends('product_line_ids.subtotal')
    def _compute_total_price(self):
        for record in self:
            record.total_price = sum(line.subtotal for line in record.product_line_ids)

    def _group_expand_notes(self, notes, domain, order):
        return [key for key, val in type(self).note.selection]

    @api.constrains('product_line_ids')
    def _check_product_lines(self):
        for record in self:
            if record.note == 'won' and not record.product_line_ids:
                raise ValidationError("Un résultat gagné doit avoir au moins un produit vendu")
    
    
    