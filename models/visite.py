from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class VisiteManagement(models.Model):
    _name = 'visite.management'
    _description = 'Gestion des Visites'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, date desc, id desc'

    # Champs de base
    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, default='New', tracking=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today, tracking=True)
    client_id = fields.Many2one('visite.client', string='Client', required=True, ondelete='restrict', tracking=True)
    nom = fields.Char(string='Objet de la visite', required=True, tracking=True)
    etat = fields.Selection([
        ('planned', 'Planifiée'),
        ('in_progress', 'En cours'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée')
    ], string='État', default='planned', required=True, tracking=True)
    notes = fields.Text(string='Notes')
    result_id = fields.Many2one('visite.result', string='Résultat', readonly=True)
    
    # 🔥 NOUVELLES FONCTIONNALITÉS PRO
    priority = fields.Selection([
        ('0', 'Faible'),
        ('1', 'Normal'),
        ('2', 'Élevée'),
        ('3', 'Urgente')
    ], string='Priorité', default='1', tracking=True)
    
    tag_ids = fields.Many2many('visite.tag', string='Tags')
    
    duration = fields.Float(string='Durée estimée (heures)', default=1.0)
    actual_duration = fields.Float(string='Durée réelle (heures)')
    
    user_id = fields.Many2one('res.users', string='Responsable', default=lambda self: self.env.user, tracking=True)
    
    color = fields.Integer(string='Couleur', compute='_compute_color', store=True)
    
    # Champs calculés avancés
    is_late = fields.Boolean(string='En retard', compute='_compute_is_late')
    days_until = fields.Integer(string='Jours restants', compute='_compute_days_until')
    
    kanban_state = fields.Selection([
        ('normal', 'En cours'),
        ('done', 'Prêt'),
        ('blocked', 'Bloqué')
    ], string='État Kanban', default='normal', tracking=True)
    
    # Scoring de la visite
    success_rate = fields.Float(string='Taux de succès (%)', compute='_compute_success_rate')

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
            self.message_post(body="✅ Résultat de visite créé avec succès")
            return {
                'type': 'ir.actions.act_window',
                'name': 'Résultat de visite',
                'res_model': 'visite.result',
                'res_id': result.id,
                'view_mode': 'form',
                'target': 'current',
            }
    
    @api.depends('priority', 'etat')
    def _compute_color(self):
        """Calcul de la couleur pour le kanban"""
        for record in self:
            if record.etat == 'cancelled':
                record.color = 1  # Rouge
            elif record.etat == 'done':
                record.color = 10  # Vert
            elif record.priority == '3':
                record.color = 2  # Orange (urgente)
            elif record.priority == '2':
                record.color = 7  # Jaune (élevée)
            else:
                record.color = 0  # Normal
    
    @api.depends('date', 'etat')
    def _compute_is_late(self):
        """Vérifie si la visite est en retard"""
        today = fields.Date.context_today(self)
        for record in self:
            record.is_late = (record.date < today and record.etat in ['planned', 'in_progress'])
    
    @api.depends('date')
    def _compute_days_until(self):
        """Calcule le nombre de jours avant la visite"""
        today = fields.Date.context_today(self)
        for record in self:
            if record.date:
                delta = (record.date - today).days
                record.days_until = delta
            else:
                record.days_until = 0
    
    def _compute_success_rate(self):
        """Calcule le taux de succès basé sur l'historique client"""
        for record in self:
            if record.client_id:
                results = self.env['visite.result'].search([
                    ('client_id', '=', record.client_id.id)
                ])
                total = len(results)
                won = len(results.filtered(lambda r: r.note == 'won'))
                record.success_rate = (won / total * 100) if total > 0 else 0
            else:
                record.success_rate = 0
        
