# 🎯 Guide Utilisateur - Pétanque Manager

## Table des Matières
1. [Installation](#installation)
2. [Premier Lancement](#premier-lancement)
3. [Créer un Tournoi](#créer-un-tournoi)
4. [Gérer les Équipes](#gérer-les-équipes)
5. [Organiser les Matchs](#organiser-les-matchs)
6. [Consulter le Classement](#consulter-le-classement)
7. [Export et Impression](#export-et-impression)
8. [Types de Tournois](#types-de-tournois)
9. [Conseils et Astuces](#conseils-et-astuces)
10. [Résolution de Problèmes](#résolution-de-problèmes)

---

## Installation

### Installation Automatique (Recommandée)
1. **Téléchargez** le dossier Pétanque Manager
2. **Double-cliquez** sur `install.bat`
3. **Suivez** les instructions à l'écran
4. **Lancez** l'application avec `launch.bat` ou `python main.py`

### Installation Manuelle
1. **Installez Python 3.8+** depuis [python.org](https://python.org)
   - ⚠️ Cochez "Add Python to PATH" pendant l'installation
2. **Ouvrez** un terminal dans le dossier de l'application
3. **Exécutez** : `pip install -r requirements.txt`
4. **Lancez** : `python main.py`

### Création d'un Exécutable (.exe)
1. **Exécutez** : `python build_exe.py`
2. **Choisissez** l'option 1 pour créer l'exécutable
3. **Trouvez** l'exécutable dans le dossier `dist/`

---

## Premier Lancement

### Interface Principale
Au lancement, vous découvrirez :
- **Bandeau supérieur** : Logo, sélecteur de tournoi, boutons de gestion
- **Onglets** : Équipes/Joueurs, Matchs, Classement
- **Barre de statut** : Messages d'information

### Première Configuration
1. **Menu Affichage** → Choisir le thème (Clair/Sombre)
2. **Créer votre premier tournoi** (voir section suivante)

---

## Créer un Tournoi

### Étapes de Création
1. **Cliquez** sur "Nouveau Tournoi" ou Menu Fichier → Nouveau Tournoi
2. **Remplissez** les informations :
   - **Nom** : Nom du tournoi (ex: "Championnat Club 2025")
   - **Type** : Format du tournoi (voir [Types de Tournois](#types-de-tournois))
   - **Terrains** : Nombre de terrains disponibles (1-20)
3. **Cliquez** "Créer"

### Types Disponibles
- **tete_a_tete** : 1 joueur par équipe
- **doublette** : 2 joueurs par équipe
- **triplette** : 3 joueurs par équipe
- **quadrette** : 4 joueurs par équipe
- **melee** : Participants individuels, groupes aléatoires

---

## Gérer les Équipes

### Onglet Équipes/Joueurs

#### Inscription d'une Équipe
1. **Saisissez** les noms des joueurs :
   - Joueur 1 (obligatoire)
   - Joueurs 2, 3, 4 (selon le format)
2. **Cliquez** "+ Ajouter un joueur" si nécessaire
3. **Cliquez** "Créer l'équipe"

> 💡 **Astuce** : Les équipes sont automatiquement nommées "Équipe 1", "Équipe 2", etc.

#### Gestion des Équipes
- **Liste à droite** : Toutes les équipes inscrites
- **Colonnes** : Nom, Joueurs, Victoires, Défaites, Points +/-
- **Boutons** : Supprimer, Modifier (à venir)

### Formats Spéciaux

#### Quadrette
- **4 joueurs exactement** par équipe
- Joueurs étiquetés A, B, C, D automatiquement
- Planning fixe sur 7 tours

#### Mêlée
- **Joueurs individuels** uniquement
- Tirage aléatoire à chaque tour
- Groupes de 2-3 selon les terrains

---

## Organiser les Matchs

### Onglet Matchs

#### Génération d'un Tour
1. **Vérifiez** que les équipes sont inscrites
2. **Cliquez** "Générer tour suivant"
3. **Consultez** les matchs générés

#### Tableau des Matchs
- **Terrain** : Numéro du terrain
- **Équipes** : Adversaires du match
- **Scores** : Résultats (modifiables)
- **Statut** : En attente / En cours / Terminé

#### Saisie des Scores
1. **Double-cliquez** sur un match OU sélectionnez + "Modifier le score"
2. **Ajustez** les scores avec les boutons +/-
3. **Cliquez** "Sauvegarder"

> ⚠️ **Important** : Les statistiques se mettent à jour automatiquement

### Gestion des BYE
- **Nombre impair d'équipes** : Une équipe est automatiquement "BYE"
- **Tour 1** : BYE aléatoire
- **Tours suivants** : BYE pour l'équipe la moins bien classée
- **Score BYE** : Victoire automatique 13-7

---

## Consulter le Classement

### Onglet Classement

#### Tableau de Classement
- **Position** : Rang dans le tournoi
- **Équipe** : Nom de l'équipe
- **V/D** : Victoires et défaites
- **Points +/-** : Points marqués et encaissés
- **Différence** : Écart de points
- **Ratio** : Victoires/Total matchs

#### Critères de Classement
1. **Nombre de victoires** (principal)
2. **Différence de points** (départage)
3. **Points marqués** (départage final)

#### Statistiques Résumées
- Équipes inscrites
- Matchs joués
- Score moyen
- Score le plus élevé

---

## Export et Impression

### Export PDF
1. **Menu Fichier** → Exporter PDF
2. **Choisissez** l'emplacement
3. **Cliquez** "Enregistrer"

### Contenu du PDF
- **Titre** du tournoi et date
- **Classement complet** avec mise en forme
- **Podium** mis en évidence (or, argent, bronze)
- **Statistiques** détaillées

---

## Types de Tournois

### Tournois Standard (Tête-à-tête, Doublette, Triplette)

#### Fonctionnement
- **Appariement intelligent** : Équipes de niveau similaire
- **Évitement des re-rencontres** : Algorithme de vérification
- **Performance** : Basée sur victoires + différence de points

#### Stratégie d'Appariement
1. Calcul performance = (Victoires × 50) + différence de points
2. Tri des équipes par performance
3. Appariement des équipes adjacentes
4. Vérification des rencontres précédentes

### Quadrette - Planning Fixe

#### 7 Tours Prédéfinis
1. **Tour 1** : ABC vs D
2. **Tour 2** : AB vs CD
3. **Tour 3** : ABD vs C
4. **Tour 4** : AC vs BD
5. **Tour 5** : ACD vs B
6. **Tour 6** : AD vs BC
7. **Tour 7** : BCD vs A

> 📚 **Note** : Chaque joueur joue avec et contre tous les autres dans des configurations différentes

### Mêlée - Tirage Aléatoire

#### Caractéristiques
- **Participants individuels**
- **Groupes aléatoires** à chaque tour
- **2-3 joueurs par groupe** selon les terrains
- **Convivialité** : Idéal pour les événements sociaux

---

## Conseils et Astuces

### Préparation du Tournoi
- 📋 **Listez les participants** à l'avance
- 🏟️ **Comptez vos terrains** disponibles
- ⏰ **Prévoyez le temps** : ~30min par tour
- 📱 **Ayez une sauvegarde** de la base de données

### Pendant le Tournoi
- 🔄 **Saisissez les scores** au fur et à mesure
- 👥 **Vérifiez les équipes** avant chaque tour
- 📊 **Consultez le classement** régulièrement
- 🎯 **Adaptez le nombre de tours** selon le temps

### Gestion des Équipes
- 👤 **Équipes incomplètes** : Utilisez des "joueurs fantômes"
- 🔄 **Remplacements** : Modifiez les équipes entre les tours
- ⚖️ **Équilibrage** : Mélangez les niveaux si nécessaire

### Optimisation
- 🚀 **Performance** : Fermez les autres applications
- 💾 **Sauvegarde** : La base SQLite se sauvegarde automatiquement
- 🎨 **Thème** : Utilisez le thème sombre en soirée

---

## Résolution de Problèmes

### Problèmes Courants

#### "Aucun module nommé tkinter"
**Cause** : tkinter non installé
**Solution** :
- Windows : Réinstallez Python avec "tcl/tk and IDLE"
- Linux : `sudo apt-get install python3-tk`
- macOS : Utilisez Python depuis python.org

#### "Erreur lors de l'export PDF"
**Cause** : reportlab non installé
**Solution** : `pip install reportlab`

#### Application ne se lance pas
**Solutions** :
1. Vérifiez Python 3.8+ : `python --version`
2. Installez les dépendances : `pip install -r requirements.txt`
3. Testez en console : `python test_console.py`

#### Performance lente
**Causes possibles** :
- Trop d'équipes (>50)
- Base de données corrompue
- Mémoire insuffisante

**Solutions** :
1. Redémarrez l'application
2. Supprimez `petanque_manager.db` (reset)
3. Réduisez le nombre d'équipes par tournoi

### Messages d'Erreur Spécifiques

#### "Au moins 2 équipes sont nécessaires"
- Inscrivez plus d'équipes avant de générer un tour

#### "Type de tournoi non supporté"
- Vérifiez la configuration du tournoi
- Recréez le tournoi si nécessaire

#### "Match introuvable"
- Erreur de base de données
- Redémarrez l'application

### Récupération de Données
La base de données SQLite (`petanque_manager.db`) contient toutes vos données. Pour récupérer :
1. **Sauvegardez** ce fichier régulièrement
2. **Copiez-le** pour le transférer sur un autre PC
3. **Supprimez-le** pour reset complet l'application

---

## Support et Contact

### Auto-Support
1. **Lisez** ce guide complet
2. **Testez** avec `python test_console.py`
3. **Vérifiez** les dépendances avec `pip list`

### Fonctionnalités à Venir
- Modification d'équipes après création
- Import/Export de tournois
- Statistiques avancées
- Interface web (optionnel)

---

*Guide rédigé pour Pétanque Manager v1.0 - Mars 2025*