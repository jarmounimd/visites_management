from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class VisiteClient(models.Model):
    _name = 'visite.client'
    _description = 'Client du Visite'
    _rec_name = 'display_name'

    name = fields.Char(string='Nom', required=True, index=True)
    prenom = fields.Char(string='Prénom', required=True)
    display_name = fields.Char(string='Nom Complet', compute='_compute_display_name', store=True)
    ville = fields.Char(string='Ville')
    adresse = fields.Text(string='Adresse')
    pays = fields.Char(string='Pays')
    mobile = fields.Char(string='Mobile', required=True)
    email = fields.Char(string='Email', required=True)
    visite_ids = fields.One2many('visite.management', 'client_id', string='Visites')
    result_ids = fields.One2many('visite.result', 'client_id', string='Résultats')

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