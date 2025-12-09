from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class VisiteClient(models.Model):
    _name = 'visite.client'
    _description = 'Client du Visite'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'

    name = fields.Char(string='Nom', required=True, index=True, tracking=True)
    prenom = fields.Char(string='Prénom', required=True, tracking=True)
    display_name = fields.Char(string='Nom Complet', compute='_compute_display_name', store=True)
    ville = fields.Char(string='Ville', tracking=True)
    adresse = fields.Text(string='Adresse')
    pays = fields.Char(string='Pays', tracking=True)
    mobile = fields.Char(string='Mobile', required=True, tracking=True)
    email = fields.Char(string='Email', required=True, tracking=True)
    visite_ids = fields.One2many('visite.management', 'client_id', string='Visites')
    result_ids = fields.One2many('visite.result', 'client_id', string='Résultats')
    
    # 🔥 NOUVELLES FONCTIONNALITÉS PRO
    # Statistiques
    total_visits = fields.Integer(string='Total Visites', compute='_compute_statistics')
    total_revenue = fields.Float(string='Chiffre d\'Affaires Total', compute='_compute_statistics')
    avg_purchase = fields.Float(string='Panier Moyen', compute='_compute_statistics')
    success_rate = fields.Float(string='Taux de Conversion (%)', compute='_compute_statistics')
    last_visit_date = fields.Date(string='Dernière Visite', compute='_compute_statistics')
    
    # Segmentation client
    category = fields.Selection([
        ('prospect', '🆕 Prospect'),
        ('regular', '👤 Régulier'),
        ('vip', '⭐ VIP'),
        ('inactive', '💤 Inactif')
    ], string='Catégorie', compute='_compute_category', store=True)
    
    # Badge de fidélité
    loyalty_badge = fields.Selection([
        ('bronze', '🥉 Bronze'),
        ('silver', '🥈 Argent'),
        ('gold', '🥇 Or'),
        ('diamond', '💎 Diamant')
    ], string='Badge Fidélité', compute='_compute_loyalty_badge', store=True)
    
    # Score client
    client_score = fields.Integer(string='Score Client', compute='_compute_client_score', store=True)
    
    color = fields.Integer(string='Couleur', compute='_compute_color')

    @api.depends('name', 'prenom')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} {record.prenom}"

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, record.email):
                    raise ValidationError("Format d'email invalide")

    @api.constrains('mobile')
    def _check_mobile(self):
        for record in self:
            if record.mobile:
                mobile_clean = re.sub(r'[\s\-\(\)\+]', '', record.mobile)
                if not mobile_clean.isdigit() or len(mobile_clean) < 10:
                    raise ValidationError("Numéro de téléphone invalide (minimum 10 chiffres)")
    
    @api.depends('visite_ids', 'result_ids')
    def _compute_statistics(self):
        """Calcule toutes les statistiques du client"""
        for record in self:
            # Total visites
            record.total_visits = len(record.visite_ids)
            
            # Chiffre d'affaires total
            won_results = record.result_ids.filtered(lambda r: r.note == 'won')
            record.total_revenue = sum(won_results.mapped('total_price'))
            
            # Panier moyen
            record.avg_purchase = record.total_revenue / len(won_results) if won_results else 0
            
            # Taux de conversion
            total_results = len(record.result_ids)
            record.success_rate = (len(won_results) / total_results * 100) if total_results > 0 else 0
            
            # Dernière visite
            if record.visite_ids:
                record.last_visit_date = max(record.visite_ids.mapped('date'))
            else:
                record.last_visit_date = False
    
    @api.depends('total_revenue', 'total_visits', 'last_visit_date')
    def _compute_category(self):
        """Segmentation automatique du client"""
        from datetime import timedelta
        today = fields.Date.today()
        for record in self:
            if not record.total_visits:
                record.category = 'prospect'
            elif record.total_revenue >= 10000:
                record.category = 'vip'
            elif record.last_visit_date and (today - record.last_visit_date).days > 90:
                record.category = 'inactive'
            else:
                record.category = 'regular'
    
    @api.depends('total_revenue')
    def _compute_loyalty_badge(self):
        """Attribution du badge de fidélité selon le CA"""
        for record in self:
            if record.total_revenue >= 20000:
                record.loyalty_badge = 'diamond'
            elif record.total_revenue >= 10000:
                record.loyalty_badge = 'gold'
            elif record.total_revenue >= 5000:
                record.loyalty_badge = 'silver'
            else:
                record.loyalty_badge = 'bronze'
    
    @api.depends('total_visits', 'total_revenue', 'success_rate')
    def _compute_client_score(self):
        """Calcule un score global du client"""
        for record in self:
            score = 0
            score += min(record.total_visits * 10, 50)  # Max 50 points
            score += min(record.total_revenue / 100, 30)  # Max 30 points
            score += min(record.success_rate / 5, 20)  # Max 20 points
            record.client_score = int(min(score, 100))
    
    def _compute_color(self):
        """Couleur selon la catégorie"""
        for record in self:
            if record.category == 'vip':
                record.color = 10  # Vert
            elif record.category == 'inactive':
                record.color = 1   # Rouge
            elif record.category == 'regular':
                record.color = 3   # Bleu
            else:
                record.color = 7   # Jaune
    
    # Actions pour les boutons statistiques
    def action_view_visits(self):
        """Affiche toutes les visites du client"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visites',
            'res_model': 'visite.management',
            'view_mode': 'tree,form,kanban',
            'domain': [('client_id', '=', self.id)],
            'context': {'default_client_id': self.id}
        }
    
    def action_view_results(self):
        """Affiche tous les résultats du client"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Résultats',
            'res_model': 'visite.result',
            'view_mode': 'tree,form',
            'domain': [('client_id', '=', self.id)],
            'context': {'default_client_id': self.id}
        }