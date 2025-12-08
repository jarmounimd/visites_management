# Module Gestion des Visites - Odoo

## Description
Module Odoo pour la gestion des visites commerciales et le suivi des résultats de vente.

## Fonctionnalités

### 📅 Gestion des Visites
- Planification des visites clients
- Suivi de l'état des visites (Planifiée, En cours, Terminée, Annulée)
- Vue calendrier pour visualiser les visites
- Génération automatique de références (VIS00001, VIS00002, etc.)
- Lien avec les résultats de visite

### 👥 Gestion des Clients
- Registre personnalisé des clients
- Informations complètes (nom, prénom, adresse, contact)
- Validation automatique des emails et numéros de téléphone
- Historique des visites et résultats par client

### 💰 Résultats de Visite
- Enregistrement des produits vendus
- Calcul automatique des prix totaux
- Suivi du statut (En attente, Gagné, Échoué)
- Vue Kanban pour le suivi visuel
- Graphiques de performance
- Génération de rapports PDF

### 📦 Produits
- Intégration avec le module produit Odoo
- Gestion des lignes de produits vendus
- Calcul automatique des sous-totaux
- Validation des quantités et prix

## Structure des Modèles

### visite.management
- **name**: Référence de la visite (auto-générée)
- **date**: Date de la visite
- **client_id**: Client concerné
- **nom**: Objet de la visite
- **etat**: État (planned, in_progress, done, cancelled)
- **notes**: Notes sur la visite
- **result_id**: Lien vers le résultat

### visite.client
- **name**: Nom
- **prenom**: Prénom
- **display_name**: Nom complet (calculé)
- **email**: Email (validé)
- **mobile**: Téléphone (validé)
- **adresse**: Adresse postale
- **ville**: Ville
- **pays**: Pays
- **visite_ids**: Visites liées
- **result_ids**: Résultats liés

### visite.result
- **name**: Référence (calculée)
- **visite_id**: Visite source (optionnel)
- **client_id**: Client
- **date_visite**: Date de la visite
- **product_line_ids**: Produits vendus
- **total_price**: Prix total (calculé)
- **note**: État (pending, won, failed)
- **result_remark**: Remarques

### visite.product.line
- **visite_id**: Résultat de visite
- **product_id**: Produit
- **quantity**: Quantité
- **unit_price**: Prix unitaire (depuis le produit)
- **subtotal**: Sous-total (calculé)

## Sécurité

### Groupes d'utilisateurs
- **Admin Visite**: Accès complet à tous les modèles
- **Commercial**: Création/modification des résultats et lignes de produits, lecture seule sur les produits

### Validations
- Email: Format valide requis
- Téléphone: Minimum 10 chiffres
- Quantité: Doit être > 0
- Prix: Ne peut pas être négatif
- Date de visite planifiée: Ne peut pas être dans le passé

## Installation

1. Copier le module dans le dossier addons d'Odoo
2. Redémarrer le serveur Odoo
3. Activer le mode développeur
4. Mettre à jour la liste des applications
5. Installer "Gestion des Visites"

## Configuration

### Permissions utilisateurs
1. Aller dans Paramètres > Utilisateurs & Entreprises > Utilisateurs
2. Sélectionner un utilisateur
3. Ajouter le groupe "Admin Visite" ou "Commercial"

### Séquences
Les références de visites sont générées automatiquement avec le préfixe "VIS"

## Vues disponibles

### Visites
- Vue liste (avec filtres et recherche)
- Vue formulaire (avec statusbar)
- Vue calendrier

### Résultats
- Vue Kanban (groupée par statut)
- Vue liste (avec totaux)
- Vue formulaire (avec onglets)
- Vue graphique (bar chart)

### Clients
- Vue liste
- Vue formulaire (avec historique)
- Recherche avancée

## Rapports
- Rapport PDF de résultat de visite
- Inclut: client, date, produits, quantités, prix, remarques

## Dépendances
- base
- product
- web

## Version
1.0.0

## Auteur
ENSAH GI3-GL

## Licence
LGPL-3

## Améliorations futures possibles
- Dashboard avec statistiques
- Notifications automatiques
- Workflow d'approbation
- Export Excel
- Intégration avec Google Maps pour géolocalisation
- Application mobile pour les commerciaux
