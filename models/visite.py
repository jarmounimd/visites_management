from odoo import models, fields, api
from odoo.exceptions import ValidationError

class VisiteManagement(models.Model):
    _name = 'visite.management'
    _description = 'Gestion des Visites'
    _order = 'date desc, id desc'

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, default='New')
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    client_id = fields.Many2one('visite.client', string='Client', required=True, ondelete='restrict')
    nom = fields.Char(string='Objet de la visite', required=True)
    etat = fields.Selection([
        ('planned', 'Planifiée'),
        ('in_progress', 'En cours'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée')
    ], string='État', default='planned', required=True)
    notes = fields.Text(string='Notes')
    result_id = fields.Many2one('visite.result', string='Résultat', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('visite.management') or 'New'
        return super(VisiteManagement, self).create(vals)

    @api.constrains('date')
    def _check_date(self):
        for record in self:
            if record.date and record.date < fields.Date.context_today(self):
                if record.etat == 'planned':
                    raise ValidationError("La date de visite planifiée ne peut pas être dans le passé")

    
        
