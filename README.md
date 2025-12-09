# 🎯 Module Gestion des Visites - VERSION 2.0 PRO MAX

## 📌 Description
Module Odoo professionnel pour la gestion avancée des visites commerciales avec système de priorisation, tags, statistiques clients automatiques, et suivi de performance.

## ✨ Fonctionnalités PRO

### 🚀 Gestion des Visites Avancée
- **Système de priorités** : 4 niveaux (Faible, Normal, Élevée, Urgente) avec étoiles ⭐
- **Tags personnalisables** : 6 tags prédéfinis (Important, Suivi, Urgente, Démonstration, Négociation, Signature)
- **Suivi du temps** : Durée estimée vs durée réelle
- **Alertes intelligentes** : Rubans "EN RETARD", "URGENT", badges "AUJOURD'HUI", "DEMAIN"
- **Responsables** : Assignation automatique à l'utilisateur courant
- **Couleurs dynamiques** : Code couleur selon état et priorité
- **États Kanban** : Progress bar avec états avancés
- **Calcul automatique** : Taux de succès basé sur l'historique client
- **Chatter intégré** : Suivi des modifications et activités
- **Génération automatique de références** (VIS00001, VIS00002, etc.)
- **Validation de dates** : Empêche les dates dans le passé pour visites planifiées

### 👥 Gestion des Clients Intelligente
- **Statistiques automatiques** : 7 KPIs calculés en temps réel
  - Total visites
  - Chiffre d'affaires total (CA)
  - Panier moyen
  - Taux de conversion (%)
  - Date dernière visite
  - Score client (0-100)
  - Nombre de jours depuis dernière visite
- **Segmentation automatique** : 4 catégories
  - 🆕 Prospect (nouveau client)
  - 👤 Régulier (client habituel)
  - ⭐ VIP (CA > 10,000 DH)
  - 💤 Inactif (pas de visite depuis 90 jours)
- **Badges de fidélité** : Attribution automatique selon CA
  - 🥉 Bronze (< 5,000 DH)
  - 🥈 Argent (5,000-10,000 DH)
  - 🥇 Or (10,000-20,000 DH)
  - 💎 Diamant (> 20,000 DH)
- **Boutons statistiques** : Accès rapide aux visites et résultats
- **Validation stricte** : Email et mobile (min 10 chiffres)
- **Chatter intégré** : Suivi et activités

### 💰 Résultats de Visite Enrichis
- **Score de satisfaction** : Notation de 1 à 5 étoiles ⭐⭐⭐⭐⭐
- **Badges de performance** : Attribution automatique selon CA
  - 🥉 Bronze (< 500 DH)
  - 🥈 Argent (500-2,000 DH)
  - 🥇 Or (2,000-5,000 DH)
  - 💎 Platine (> 5,000 DH)
- **Calculs automatiques** :
  - Marge bénéficiaire (%)
  - Nombre de produits vendus
  - Suggestion date prochaine visite (+30 jours)
- **Planification automatique** : Bouton "📅 Planifier Visite de Suivi"
- **Rubans visuels** : "GAGNÉ 🎉" (vert), "ÉCHOUÉ" (rouge)
- **Vue Kanban colorée** : Code couleur selon état
- **Graphiques de performance**
- **Chatter intégré**

### 📦 Gestion des Produits
- **Intégration native** : Utilise `product.template` (modèle Odoo standard)
- **Accessible depuis 2 menus** :
  - Visites → Configuration → Produits
  - Inventaire/Ventes → Produits (Odoo standard)
- **Lignes de produits** : Ajout direct dans chaque résultat
- **Calcul automatique** : Prix total, marge, nombre de produits
- **Import facilité** : CSV/XLSX supporté

## 📊 Structure des Modèles

### visite.management (Visites)
**Champs de base :**
- **name**: Référence auto-générée (VIS00001, VIS00002...)
- **date**: Date de la visite (validation : pas dans le passé si planned)
- **client_id**: Client concerné (Many2one)
- **nom**: Objet de la visite
- **etat**: État (planned/in_progress/done/cancelled)
- **notes**: Notes libres

**Champs PRO :**
- **priority**: Priorité (0=Faible, 1=Normal, 2=Élevée, 3=Urgente)
- **tag_ids**: Tags (Many2many vers visite.tag)
- **duration**: Durée estimée (heures)
- **actual_duration**: Durée réelle (heures)
- **user_id**: Responsable (Many2one vers res.users)
- **color**: Couleur (calculée selon état/priorité)
- **is_late**: Indicateur retard (calculé)
- **days_until**: Jours avant visite (calculé)
- **kanban_state**: État Kanban (normal/done/blocked)
- **success_rate**: Taux succès client (calculé)
- **result_id**: Lien résultat

**Héritage :** mail.thread, mail.activity.mixin

### visite.client (Clients)
**Champs de base :**
- **name**: Nom (requis)
- **prenom**: Prénom (requis)
- **display_name**: Nom complet (calculé : "Nom Prénom")
- **email**: Email (requis, validé format)
- **mobile**: Téléphone (requis, min 10 chiffres)
- **adresse**: Adresse postale
- **ville**: Ville
- **pays**: Pays
- **visite_ids**: Visites liées (One2many)
- **result_ids**: Résultats liés (One2many)

**Statistiques calculées :**
- **total_visits**: Nombre total de visites
- **total_revenue**: CA total (somme résultats gagnés)
- **avg_purchase**: Panier moyen (CA / nombre résultats)
- **success_rate**: Taux conversion % (gagnés / total)
- **last_visit_date**: Date dernière visite

**Segmentation automatique :**
- **category**: Catégorie (prospect/regular/vip/inactive)
- **loyalty_badge**: Badge fidélité (bronze/silver/gold/diamond)
- **client_score**: Score 0-100 (basé sur visites + CA + taux)
- **color**: Couleur (selon catégorie)

**Héritage :** mail.thread, mail.activity.mixin

**Actions :**
- `action_view_visits()`: Ouvre toutes les visites du client
- `action_view_results()`: Ouvre tous les résultats du client

### visite.result (Résultats)
**Champs de base :**
- **name**: Référence (calculée depuis visite)
- **visite_id**: Visite source (optionnel)
- **client_id**: Client (requis)
- **date_visite**: Date de visite (requis)
- **product_line_ids**: Produits vendus (One2many)
- **total_price**: Prix total (calculé auto)
- **note**: État (pending/won/failed)
- **result_remark**: Remarques

**Champs PRO :**
- **user_id**: Commercial responsable
- **satisfaction_score**: Score 1-5 étoiles
- **profit_margin**: Marge % (calculée)
- **product_count**: Nombre produits (calculé)
- **next_visit_date**: Suggestion prochaine visite (+30j)
- **performance_badge**: Badge (bronze/silver/gold/platinum)
- **color**: Couleur (selon état)

**Héritage :** mail.thread, mail.activity.mixin

**Actions :**
- `action_create_followup_visit()`: Crée auto visite de suivi

### visite.product.line (Lignes de produits)
- **visite_id**: Résultat de visite (Many2one vers visite.result)
- **product_id**: Produit (Many2one vers product.template)
- **quantity**: Quantité (validation > 0)
- **unit_price**: Prix unitaire (depuis produit)
- **subtotal**: Sous-total (calculé : quantity × unit_price)

### visite.tag (Tags)
- **name**: Nom du tag (unique)
- **color**: Couleur (0-11)

**Tags prédéfinis :**
- Important (rouge)
- Suivi (bleu)
- Urgente (orange)
- Démonstration (vert)
- Négociation (violet)
- Signature (jaune)

## 🔐 Sécurité

### Groupes d'utilisateurs hiérarchiques
**3 niveaux d'accès :**

1. **👤 Utilisateur** (group_visite_user)
   - Lecture : visites, clients, résultats, produits, tags
   - Création/Modification : visites uniquement
   - Accès : Menu Visites de base

2. **💼 Commercial** (group_commercial - hérite de Utilisateur)
   - + Création/Modification : résultats, lignes de produits
   - + Gestion complète des ventes
   - Accès : Tout sauf Configuration

3. **⚙️ Administrateur** (group_admin_visite - hérite de Commercial)
   - + Accès total : tous les modèles
   - + Configuration : produits, tags
   - + Paramètres système
   - Accès : Menu Configuration visible

**Fichiers de sécurité :**
- `security/groups.xml` : Définition des groupes
- `security/ir.model.access.csv` : Permissions par modèle (18 règles)

### Validations et contraintes
**Client :**
- Email : Format valide requis (`@`, `.`, domaine)
- Mobile : Minimum 10 chiffres (validation regex)

**Visite :**
- Date : Ne peut pas être dans le passé si état = 'planned'

**Ligne de produit :**
- Quantité : Doit être > 0
- Prix : Ne peut pas être négatif

## 🚀 Installation

### Prérequis
- Odoo 17.0
- Modules dépendances : `base`, `product`, `web`, `mail`

### Étapes d'installation
1. **Copier** le module dans le dossier addons d'Odoo
2. **Redémarrer** le serveur Odoo
3. **Activer** le mode développeur
4. **Mettre à jour** la liste des applications
5. **Installer** "Gestion des Visites"

### Configuration post-installation

#### 1. Permissions utilisateurs
1. Aller dans **Paramètres → Utilisateurs & Entreprises → Utilisateurs**
2. Sélectionner un utilisateur
3. Section **Gestion des Visites** :
   - Choisir : **Utilisateur** / **Commercial** / **Administrateur**

#### 2. Tags prédéfinis
Après installation, 6 tags sont créés automatiquement :
- Important, Suivi, Urgente, Démonstration, Négociation, Signature

#### 3. Séquences
Les références sont générées automatiquement :
- Visites : `VIS00001`, `VIS00002`...
- Préfixe : "VIS"

## 📱 Vues disponibles

### Visites
- **Kanban PRO** : Couleurs dynamiques, priorités étoiles, tags colorés, alertes, progress bar
- **Liste** : Filtres avancés, recherche, groupement
- **Formulaire** : Statusbar, rubans alertes, statistiques client, chatter
- **Calendrier** : Vue mensuelle des visites

### Clients
- **Kanban PRO** : Badges catégorie et fidélité, CA total, score client, couleurs
- **Liste** : Tri par CA, taux conversion, dernière visite
- **Formulaire** : 4 boutons statistiques, historique complet, chatter

### Résultats
- **Kanban** : Groupée par statut avec code couleur
- **Liste** : Avec totaux, badges performance
- **Formulaire** : Rubans succès/échec, satisfaction étoiles, bouton suivi, chatter
- **Graphique** : Bar chart performance

### Tags
- **Liste** : Gestion des tags personnalisés
- **Formulaire** : Nom + choix couleur

## 📄 Rapports
- **Rapport PDF** de résultat de visite
- Contenu : Client, date, produits, quantités, prix, remarques, totaux

## 📥 Import de données

### Fichiers disponibles (dossier `data/`)
1. **import_clients.csv** - 10 clients exemple
2. **import_products_simple.csv** - 20 produits (sans accents)
3. **import_visites.csv** - 15 visites (dates futures)
4. **import_results.csv** - 5 résultats

### Ordre d'import
```
Clients → Produits → Visites → Résultats
```

### Guides disponibles
- `GUIDE_IMPORT_SIMPLE.md` : Procédure complète
- `GUIDE_CHAMPS_EXACTS.md` : Mapping des colonnes
- `SOLUTION_IMPORT_CSV.md` : Résolution erreurs

## 📦 Dépendances
- `base` - Odoo Core
- `product` - Gestion produits
- `web` - Interface web
- `mail` - Chatter et activités

## 🏗️ Structure du module
```
visites_management/
├── models/
│   ├── client.py          # Modèle clients + stats
│   ├── visite.py          # Modèle visites + priorités
│   ├── result.py          # Modèle résultats + badges
│   ├── product_line.py    # Lignes de produits
│   ├── product.py         # Extension produits
│   └── visite_tag.py      # Modèle tags
├── views/
│   ├── client_view.xml    # Vues clients enrichies
│   ├── visite_views.xml   # Vues visites PRO
│   ├── result_view.xml    # Vues résultats
│   ├── visite_tag_views.xml
│   ├── product_view.xml
│   ├── product_line.xml
│   └── menu.xml           # Structure menus
├── security/
│   ├── groups.xml         # Groupes hiérarchiques
│   └── ir.model.access.csv # 18 règles permissions
├── data/
│   ├── sequence.xml       # Séquences auto
│   ├── visite_tag_data.xml # Tags prédéfinis
│   └── import_*.csv       # Fichiers import
├── report/
│   ├── visite_report.xml
│   └── visite_report_template.xml
├── static/description/
│   └── icon.png
├── __manifest__.py
├── __init__.py
└── README.md (ce fichier)
```

## 📊 Statistiques du module

### Version 2.0 PRO MAX
- **6 modèles** (dont 1 nouveau : visite.tag)
- **26+ nouveaux champs** calculés automatiquement
- **14+ méthodes** de calcul
- **10+ widgets visuels** (badges, rubans, étoiles)
- **3 groupes** de sécurité hiérarchiques
- **18 règles** de permissions
- **6 tags** prédéfinis
- **7 KPIs** clients automatiques
- **3 systèmes** de badges (fidélité, performance, catégorie)

## 📖 Documentation complète

### Guides utilisateur (dossier racine)
- `QUICK_START.md` - Démarrage rapide
- `GUIDE_UTILISATEUR.md` - Manuel complet
- `NOUVELLES_FONCTIONNALITÉS.md` - Détails version 2.0
- `RECAP_V2.md` - Récapitulatif complet

### Guides import (dossier `data/`)
- `GUIDE_IMPORT_SIMPLE.md`
- `GUIDE_IMPORT_COMPLET.md`
- `GUIDE_CHAMPS_EXACTS.md`
- `SOLUTION_IMPORT_CSV.md`

## 👨‍💻 Développement

### Technologies
- Python 3.10+
- PostgreSQL 12+
- Odoo Framework 17.0
- XML (vues)
- CSV (données)

### Patterns utilisés
- MVC (Model-View-Controller)
- Computed fields avec `@api.depends`
- Héritage de modèles (`_inherit`)
- Contraintes avec `@api.constrains`
- Actions serveur pour workflows
- Chatter integration (mail.thread)

## 📝 Version
**2.0.0 PRO MAX** - 9 Décembre 2025

### Changelog v2.0
- ✅ Système de priorités (4 niveaux)
- ✅ Tags personnalisables (6 prédéfinis)
- ✅ Statistiques clients (7 KPIs auto)
- ✅ Segmentation automatique (4 catégories)
- ✅ Badges (fidélité + performance)
- ✅ Satisfaction scoring (1-5 étoiles)
- ✅ Couleurs dynamiques partout
- ✅ Alertes intelligentes
- ✅ Chatter & activités
- ✅ Planification automatique suivis
- ✅ Import CSV facilité
- ✅ Documentation complète (5 guides)

## 👥 Auteur
**ENSAH GI3-GL** - École Nationale des Sciences Appliquées Al Hoceima

## 📄 Licence
LGPL-3

## 🔮 Roadmap futures versions
- [ ] Dashboard avec graphiques interactifs
- [ ] Notifications email automatiques
- [ ] Workflow d'approbation visites
- [ ] Export Excel avancé
- [ ] API REST pour intégrations externes
- [ ] Intégration Google Maps (géolocalisation)
- [ ] Application mobile commerciaux
- [ ] IA : Prédiction succès visite
- [ ] Synchronisation calendrier Google/Outlook
- [ ] Rapports personnalisables
