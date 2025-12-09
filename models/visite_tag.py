from odoo import models, fields, api

class VisiteTag(models.Model):
    _name = 'visite.tag'
    _description = 'Tags de Visite'
    _order = 'name'

    name = fields.Char(string='Nom', required=True, translate=True)
    color = fields.Integer(string='Couleur', default=0)
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Le nom du tag doit être unique !')
    ]
