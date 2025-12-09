# 🚀 Guide Rapide - Installation et Configuration

## ⚡ Installation Rapide

### 1️⃣ Installer le Module
```bash
# Redémarrer Odoo
sudo service odoo restart

# Ou via docker
docker restart odoo
```

Puis dans Odoo :
1. **Settings** → **Activate Developer Mode**
2. **Apps** → Chercher "**Visites**"
3. Cliquer sur **Install**

### 2️⃣ Configurer les Utilisateurs

**Administrateur (accès complet):**
```
Settings → Users → [Votre utilisateur]
→ Access Rights → Gestion des Visites → Administrateur
```

**Commercial (gestion complète):**
```
Settings → Users → [Utilisateur]
→ Access Rights → Gestion des Visites → Commercial
```

**Utilisateur (accès basique):**
```
Settings → Users → [Utilisateur]
→ Access Rights → Gestion des Visites → Utilisateur
```

### 3️⃣ Configuration Initiale

**A. Créer des Produits (Admin seulement)**
```
Menu: Visites → Configuration → Produits
→ Nouveau → Remplir: Nom, Prix
```

**B. Créer des Clients**
```
Menu: Visites → Clients
→ Nouveau → Remplir: Nom, Prénom, Email, Téléphone
```

## 📋 Utilisation Quotidienne

### Créer une Visite
```
Visites → Visites → Nouveau
1. Sélectionner un Client
2. Choisir la Date
3. Indiquer l'Objet
4. Sauvegarder
→ Référence auto: VISITE/0001
```

### Gérer une Visite
```
Ouvrir la visite:
- Bouton "Démarrer" → Passe à "En cours"
- Bouton "Terminer" → Passe à "Terminée"
- Bouton "Créer Résultat" → Apparaît quand terminée
```

### Enregistrer un Résultat
```
Après "Créer Résultat":
1. Ajouter des produits (lignes)
2. Les totaux se calculent automatiquement
3. Changer l'état: Gagné/Échoué/En attente
4. Ajouter des remarques
5. Sauvegarder
```

## 🔐 Permissions Rapides

| Fonctionnalité | Utilisateur | Commercial | Admin |
|----------------|:-----------:|:----------:|:-----:|
| Voir visites | ✅ | ✅ | ✅ |
| Créer visites | ✅ | ✅ | ✅ |
| Modifier visites | ✅ (ses visites) | ✅ (toutes) | ✅ |
| Supprimer visites | ❌ | ✅ | ✅ |
| Voir clients | ✅ | ✅ | ✅ |
| Créer clients | ✅ | ✅ | ✅ |
| Modifier clients | ✅ (ses clients) | ✅ (tous) | ✅ |
| Supprimer clients | ❌ | ✅ | ✅ |
| Créer résultats | ✅ | ✅ | ✅ |
| Voir produits | ✅ (lecture) | ✅ | ✅ |
| Créer produits | ❌ | ✅ | ✅ |
| Configuration | ❌ | ❌ | ✅ |

## 🆘 Problèmes Fréquents

### ❌ Impossible de créer une visite
**Cause**: Pas de droits  
**Solution**: Vérifier les droits utilisateur (minimum: Utilisateur)

### ❌ Menu Configuration invisible
**Cause**: Rôle insuffisant  
**Solution**: Seuls les Admins voient ce menu

### ❌ Erreur email invalide
**Cause**: Format email incorrect  
**Solution**: Format requis: `nom@domaine.com`

### ❌ Erreur téléphone invalide
**Cause**: Moins de 10 chiffres  
**Solution**: Minimum 10 chiffres requis

### ❌ Impossible de créer résultat
**Cause**: Visite pas terminée  
**Solution**: Terminer la visite d'abord

### ❌ Erreur: Résultat gagné sans produits
**Cause**: Aucun produit ajouté  
**Solution**: Ajouter au moins 1 produit

## 💡 Astuces

1. **Vue Kanban** = Meilleure vue pour organisation
2. **Calendrier** = Idéal pour planification
3. **Filtres** = Utiliser les filtres prédéfinis
4. **Recherche** = Recherche rapide par client/date
5. **Groupement** = Grouper par client/état/date

## 📊 Workflow Complet

```
Client → Visite (Planifiée) → Démarrer → En cours
         ↓                                  ↓
    Calendrier                         Terminer
                                           ↓
                                      Terminée
                                           ↓
                                   Créer Résultat
                                           ↓
                                  Ajouter Produits
                                           ↓
                                  Marquer: Gagné/Échoué
```

## 🔄 Mise à Jour du Module

```bash
# 1. Mettre à jour le code
git pull origin master

# 2. Redémarrer Odoo
sudo service odoo restart

# 3. Dans Odoo (mode développeur activé)
Apps → Gestion des Visites → Upgrade
```

---

📧 **Support**: support@ensah.ma  
🌐 **Site**: https://www.ensah.ma
