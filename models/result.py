from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Result(models.Model):
    _name = 'visite.result'
    _description = 'Résultat de chaque visite'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Référence', compute='_compute_name', store=True)
    visite_id = fields.Many2one('visite.management', string='Visite', ondelete='restrict')
    client_id = fields.Many2one('visite.client', string='Client', required=True, ondelete='restrict', tracking=True)
    date_visite = fields.Date(string='Date de visite', default=fields.Date.context_today, required=True, tracking=True)
    product_line_ids = fields.One2many('visite.product.line', 'visite_id', string='Produits Vendus')
    total_price = fields.Float(string='Prix Total', compute='_compute_total_price', store=True)
    result_remark = fields.Text(string='Remarque sur le résultat')
    note = fields.Selection([
        ('pending', 'En attente'),
        ('won', 'Gagné'),
        ('failed', 'Échoué')
    ], string='État', group_expand='_group_expand_notes', default='pending', required=True, tracking=True)
    
    # 🔥 NOUVELLES FONCTIONNALITÉS PRO
    user_id = fields.Many2one('res.users', string='Commercial', default=lambda self: self.env.user, tracking=True)
    
    # Scoring et performance
    satisfaction_score = fields.Selection([
        ('1', '⭐ Très insatisfait'),
        ('2', '⭐⭐ Insatisfait'),
        ('3', '⭐⭐⭐ Neutre'),
        ('4', '⭐⭐⭐⭐ Satisfait'),
        ('5', '⭐⭐⭐⭐⭐ Très satisfait')
    ], string='Satisfaction Client', tracking=True)
    
    profit_margin = fields.Float(string='Marge (%)', compute='_compute_profit_margin', store=True)
    
    # Statistiques
    product_count = fields.Integer(string='Nombre de produits', compute='_compute_product_count')
    
    color = fields.Integer(string='Couleur', compute='_compute_color', store=True)
    
    # Recommandations automatiques
    next_visit_date = fields.Date(string='Prochaine visite suggérée', compute='_compute_next_visit_date')
    
    # Badge de performance
    performance_badge = fields.Selection([
        ('bronze', '🥉 Bronze'),
        ('silver', '🥈 Argent'),
        ('gold', '🥇 Or'),
        ('platinum', '💎 Platine')
    ], string='Badge', compute='_compute_performance_badge', store=True)

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
    
    @api.depends('total_price')
    def _compute_profit_margin(self):
        """Calcule la marge bénéficiaire (exemple simple: 30%)"""
        for record in self:
            record.profit_margin = 30.0 if record.total_price > 0 else 0.0
    
    @api.depends('product_line_ids')
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.product_line_ids)
    
    @api.depends('note', 'total_price')
    def _compute_color(self):
        """Calcul de la couleur pour le kanban"""
        for record in self:
            if record.note == 'won':
                record.color = 10  # Vert
            elif record.note == 'failed':
                record.color = 1   # Rouge
            else:
                record.color = 7   # Jaune
    
    @api.depends('date_visite', 'client_id')
    def _compute_next_visit_date(self):
        """Suggère une date pour la prochaine visite (30 jours après)"""
        from datetime import timedelta
        for record in self:
            if record.date_visite:
                record.next_visit_date = record.date_visite + timedelta(days=30)
            else:
                record.next_visit_date = False
    
    @api.depends('total_price', 'satisfaction_score')
    def _compute_performance_badge(self):
        """Attribue un badge selon la performance"""
        for record in self:
            if record.total_price >= 5000:
                record.performance_badge = 'platinum'
            elif record.total_price >= 2000:
                record.performance_badge = 'gold'
            elif record.total_price >= 500:
                record.performance_badge = 'silver'
            else:
                record.performance_badge = 'bronze'
    
    def action_create_followup_visit(self):
        """Crée automatiquement une visite de suivi"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nouvelle Visite de Suivi',
            'res_model': 'visite.management',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_client_id': self.client_id.id,
                'default_date': self.next_visit_date,
                'default_nom': f'Suivi - {self.client_id.display_name}',
            }
        }
    