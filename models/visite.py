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

    def action_start(self):
        """Démarrer une visite planifiée"""
        for record in self:
            if record.etat == 'planned':
                record.etat = 'in_progress'

    def action_complete(self):
        """Terminer une visite en cours"""
        for record in self:
            if record.etat == 'in_progress':
                record.etat = 'done'

    def action_cancel(self):
        """Annuler une visite"""
        for record in self:
            if record.etat not in ['done', 'cancelled']:
                record.etat = 'cancelled'

    def action_create_result(self):
        """Créer un résultat pour cette visite"""
        self.ensure_one()
        if self.etat == 'done' and not self.result_id:
            result = self.env['visite.result'].create({
                'visite_id': self.id,
                'client_id': self.client_id.id,
                'date_visite': self.date,
            })
            self.result_id = result.id
            return {
                'type': 'ir.actions.act_window',
                'name': 'Résultat de visite',
                'res_model': 'visite.result',
                'res_id': result.id,
                'view_mode': 'form',
                'target': 'current',
            }
        
