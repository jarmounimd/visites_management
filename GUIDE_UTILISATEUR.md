# 📋 Gestion des Visites - Module Odoo 17.0

## 📝 Description

Module complet pour la gestion des visites clients, permettant de planifier, suivre et enregistrer les résultats des visites commerciales.

## ✨ Fonctionnalités Principales

### 🎯 Gestion des Visites
- ✅ Planification de visites avec dates et clients
- ✅ Suivi de l'état : Planifiée → En cours → Terminée
- ✅ Annulation possible des visites
- ✅ Vue Kanban pour organisation visuelle
- ✅ Vue Calendrier pour planification
- ✅ Génération automatique de références (VISITE/XXXX)

### 👥 Gestion des Clients
- ✅ Fiche client complète (nom, prénom, coordonnées)
- ✅ Historique des visites par client
- ✅ Historique des résultats par client
- ✅ Validation email et téléphone
- ✅ Vue Kanban et Liste

### 📊 Résultats de Visites
- ✅ Enregistrement des ventes réalisées
- ✅ Lignes de produits avec calcul automatique
- ✅ États : En attente, Gagné, Échoué
- ✅ Vue Kanban pour suivi rapide
- ✅ Graphiques et statistiques
- ✅ Calcul automatique du total

### 🛍️ Produits
- ✅ Intégration avec le module produit d'Odoo
- ✅ Prix unitaires automatiques
- ✅ Suivi des quantités vendues

## 🔐 Groupes de Sécurité

Le module définit 3 niveaux d'accès :

### 1️⃣ **Utilisateur** (`group_visite_user`)
- ✅ Créer et modifier ses propres visites
- ✅ Créer et modifier ses propres clients
- ✅ Créer et modifier ses propres résultats
- ✅ Voir les produits (lecture seule)
- ❌ Pas de suppression

### 2️⃣ **Commercial** (`group_commercial`)
- ✅ Tous les droits de l'utilisateur
- ✅ Voir et modifier TOUTES les visites/clients/résultats
- ✅ Supprimer des enregistrements
- ✅ Créer des produits
- ❌ Pas de configuration avancée

### 3️⃣ **Administrateur** (`group_admin_visite`)
- ✅ Tous les droits du commercial
- ✅ Accès au menu Configuration
- ✅ Gestion complète des produits
- ✅ Tous les droits de suppression

## 🚀 Installation et Configuration

### Étape 1 : Installation du Module
1. Redémarrer le serveur Odoo
2. Activer le mode développeur (Settings → Developer Tools → Activate developer mode)
3. Aller dans **Apps**
4. Retirer le filtre "Apps" et chercher "**Gestion des Visites**"
5. Cliquer sur **Installer**

### Étape 2 : Attribution des Droits

#### Pour un Administrateur :
1. Aller dans **Settings → Users & Companies → Users**
2. Sélectionner l'utilisateur
3. Dans l'onglet **Access Rights**
4. Section **Gestion des Visites** : sélectionner **Administrateur**
5. Sauvegarder

#### Pour un Commercial :
- Même procédure, sélectionner **Commercial**

#### Pour un Utilisateur simple :
- Même procédure, sélectionner **Utilisateur**

### Étape 3 : Première Utilisation

1. **Créer des Produits** (Admin/Commercial)
   - Menu : **Visites → Configuration → Produits**
   - Cliquer sur **Nouveau**
   - Remplir : Nom, Prix de vente, etc.
   - Sauvegarder

2. **Créer des Clients**
   - Menu : **Visites → Clients**
   - Cliquer sur **Nouveau**
   - Remplir les informations (nom, prénom, email, téléphone obligatoires)
   - Sauvegarder

3. **Planifier une Visite**
   - Menu : **Visites → Visites**
   - Cliquer sur **Nouveau**
   - Sélectionner un client
   - Choisir la date
   - Indiquer l'objet de la visite
   - Sauvegarder
   - La référence sera générée automatiquement (ex: VISITE/0001)

4. **Gérer l'État de la Visite**
   - Ouvrir la visite
   - Cliquer sur **Démarrer** pour passer à "En cours"
   - Cliquer sur **Terminer** quand la visite est finie
   - Le bouton **Créer Résultat** apparaît

5. **Enregistrer le Résultat**
   - Cliquer sur **Créer Résultat**
   - Ajouter les produits vendus (ligne par ligne)
   - Le total se calcule automatiquement
   - Changer l'état : Gagné/Échoué/En attente
   - Ajouter des remarques si nécessaire
   - Sauvegarder

## 📱 Utilisation Quotidienne

### Vue Kanban (Recommandée)
- **Visites** : Organisées par état (Planifiée, En cours, Terminée)
- **Clients** : Cartes visuelles avec infos principales
- **Résultats** : Glisser-déposer entre états

### Filtres et Recherches
- **Visites** : Par état, date, client
- **Résultats** : Par état, client, période

### Rapports
- Menu : **Visites → Résultats de visite**
- Voir les graphiques et statistiques
- Filtrer par période, client, etc.

## 🔧 Dépannage

### ❌ "Je ne peux pas créer de visite"
**Solution** : Vérifier que vous avez au moins le rôle **Utilisateur** dans les droits d'accès

### ❌ "Je ne vois pas le menu Configuration"
**Solution** : Le menu Configuration est réservé aux **Administrateurs**

### ❌ "Erreur lors de la création d'un client"
**Solution** : Vérifier que :
- L'email est valide (format: xxx@xxx.xx)
- Le téléphone contient au moins 10 chiffres

### ❌ "Je ne peux pas créer de résultat"
**Solution** : La visite doit être à l'état "Terminée" d'abord

### ❌ "Erreur : Un résultat gagné doit avoir des produits"
**Solution** : Ajouter au moins un produit avant de marquer le résultat comme "Gagné"

## 📊 Workflows

### Workflow Visite Complète
```
1. Créer Client
   ↓
2. Planifier Visite (État: Planifiée)
   ↓
3. Démarrer Visite (État: En cours)
   ↓
4. Terminer Visite (État: Terminée)
   ↓
5. Créer Résultat
   ↓
6. Ajouter Produits
   ↓
7. Marquer Gagné/Échoué
```

## 🎓 Conseils d'Utilisation

### Pour les Commerciaux
1. ✅ Planifiez vos visites à l'avance via le calendrier
2. ✅ Utilisez la vue Kanban pour voir rapidement vos visites du jour
3. ✅ Créez les résultats immédiatement après la visite
4. ✅ Consultez les statistiques pour suivre vos performances

### Pour les Administrateurs
1. ✅ Configurez d'abord tous les produits
2. ✅ Assignez les bons rôles aux utilisateurs
3. ✅ Surveillez les rapports pour identifier les tendances
4. ✅ Nettoyez régulièrement les visites annulées

## 📞 Support

Pour toute question ou problème :
- 📧 Email : support@ensah.ma
- 🌐 Site : https://www.ensah.ma

## 👨‍💻 Développé par

**ENSAH GI3-GL**
- Version : 1.0.0
- Licence : LGPL-3
- Odoo Version : 17.0

---

**Note** : Après toute mise à jour du module, pensez à :
1. Redémarrer Odoo
2. Mettre à jour le module (Mode développeur → Apps → Gestion des Visites → Upgrade)
