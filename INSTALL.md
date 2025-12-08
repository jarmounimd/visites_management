# Guide d'Installation - Module Gestion des Visites

## Prérequis
- Odoo 15.0 ou supérieur installé et fonctionnel
- Accès administrateur à l'instance Odoo
- Module `product` installé (dépendance)

## Installation

### Étape 1: Copier le module
```bash
# Copier le dossier visites_management dans le répertoire addons d'Odoo
cp -r visites_management /path/to/odoo/addons/
```

### Étape 2: Donner les permissions appropriées
```bash
# Sur Linux/Mac
chmod -R 755 /path/to/odoo/addons/visites_management

# Assurer que l'utilisateur Odoo peut lire les fichiers
chown -R odoo:odoo /path/to/odoo/addons/visites_management
```

### Étape 3: Redémarrer le serveur Odoo
```bash
# Arrêter le serveur
sudo systemctl stop odoo

# Ou si vous utilisez la commande directement:
# killall odoo-bin

# Redémarrer avec le chemin des addons
./odoo-bin -c /etc/odoo/odoo.conf --addons-path=/path/to/addons

# Ou avec systemctl
sudo systemctl start odoo
```

### Étape 4: Activer le mode développeur
1. Connectez-vous à Odoo en tant qu'administrateur
2. Allez dans **Paramètres**
3. Faites défiler jusqu'à **Outils de développement**
4. Cliquez sur **Activer le mode développeur**

### Étape 5: Mettre à jour la liste des applications
1. Allez dans **Applications**
2. Cliquez sur le menu hamburger (☰) en haut à gauche
3. Cliquez sur **Mettre à jour la liste des Apps**
4. Cliquez sur **Mettre à jour** dans la boîte de dialogue

### Étape 6: Installer le module
1. Dans **Applications**, retirez le filtre "Apps"
2. Recherchez "Gestion des Visites"
3. Cliquez sur **Installer**

## Configuration Post-Installation

### 1. Créer les groupes d'utilisateurs
Le module crée automatiquement deux groupes:
- **Admin Visite**: Accès complet
- **Commercial**: Accès limité aux résultats

### 2. Assigner les utilisateurs aux groupes
1. Allez dans **Paramètres** > **Utilisateurs & Entreprises** > **Utilisateurs**
2. Sélectionnez un utilisateur
3. Onglet **Droits d'accès**
4. Cochez **Admin Visite** ou **Commercial**

### 3. Configurer les produits (optionnel)
1. Allez dans **Visites** > **Configuration** > **Produits**
2. Créez ou importez vos produits
3. Définissez les prix de vente

### 4. Créer les premiers clients
1. Allez dans **Visites** > **Clients**
2. Cliquez sur **Créer**
3. Remplissez les informations client

## Vérification de l'installation

### Test 1: Créer une visite
1. **Visites** > **Visites** > **Créer**
2. Sélectionnez un client
3. Définissez une date
4. Ajoutez un objet
5. Enregistrez

✅ La visite doit avoir une référence auto-générée (VIS00001)

### Test 2: Créer un résultat
1. **Visites** > **Résultats** > **Résultats de visite** > **Créer**
2. Sélectionnez un client
3. Ajoutez des produits vendus
4. Le prix total doit se calculer automatiquement

✅ Le résultat doit apparaître dans le Kanban

### Test 3: Générer un rapport
1. Ouvrez un résultat de visite
2. Cliquez sur **Imprimer** > **Print Rapport**
3. Un PDF doit se télécharger

✅ Le PDF doit contenir toutes les informations

## Résolution des problèmes courants

### Le module n'apparaît pas dans la liste
- Vérifiez que le dossier est bien dans `addons/`
- Vérifiez les permissions des fichiers
- Redémarrez le serveur Odoo
- Mettez à jour la liste des applications

### Erreur "Module not found"
```bash
# Vérifiez le chemin des addons dans la configuration
grep addons_path /etc/odoo/odoo.conf

# Ajoutez le chemin si nécessaire
addons_path = /path/to/odoo/addons,/path/to/custom/addons
```

### Erreur de dépendance
```
Module visite_management depends on product
```
**Solution**: Installez d'abord le module `product` (Sale ou Inventory)

### Erreur de permissions
```
PermissionError: [Errno 13] Permission denied
```
**Solution**:
```bash
sudo chown -R odoo:odoo /path/to/addons/visites_management
sudo chmod -R 755 /path/to/addons/visites_management
```

### Erreur de séquence
Si les références ne se génèrent pas:
1. Allez dans **Paramètres** > **Technique** > **Séquences & Identifiants** > **Séquences**
2. Recherchez "Visite Management"
3. Vérifiez que la séquence existe
4. Si non, réinstallez le module

## Désinstallation

### Sauvegarder les données
```bash
# Exporter les données avant désinstallation
# Via l'interface: Paramètres > Technique > Base de données > Sauvegarder
```

### Désinstaller le module
1. Allez dans **Applications**
2. Recherchez "Gestion des Visites"
3. Cliquez sur **Désinstaller**
4. Confirmez la désinstallation

⚠️ **Attention**: Toutes les données (visites, résultats, clients) seront supprimées!

## Migration depuis une version antérieure

Si vous mettez à jour depuis une version précédente:

### Étape 1: Sauvegarder
```bash
# Sauvegarde complète de la base de données
pg_dump -U odoo -h localhost odoo_db > backup_avant_migration.sql
```

### Étape 2: Mettre à jour le code
```bash
cd /path/to/addons/visites_management
git pull  # Si vous utilisez git
# Ou copiez la nouvelle version
```

### Étape 3: Mettre à jour le module
1. Mode développeur activé
2. **Applications** > **Gestion des Visites**
3. Cliquez sur **Mettre à jour**

### Étape 4: Vérifier les données
- Vérifiez que toutes les visites ont des références
- Vérifiez les liaisons client-visite-résultat
- Testez la génération de rapports

## Support

Pour toute question ou problème:
1. Consultez le fichier `README.md`
2. Vérifiez le `CHANGELOG.md` pour les modifications récentes
3. Contactez l'équipe ENSAH GI3-GL

## Ressources

- Documentation Odoo: https://www.odoo.com/documentation
- Forum Odoo: https://www.odoo.com/forum
- GitHub Odoo: https://github.com/odoo/odoo

---

**Version**: 1.0.0  
**Date**: Décembre 2025  
**Auteur**: ENSAH GI3-GL
