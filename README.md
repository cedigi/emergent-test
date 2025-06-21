# Pétanque Manager v1.0

Application desktop de gestion de tournois de pétanque développée en Python avec tkinter.

## 🎯 Fonctionnalités

### Types de Tournois Supportés
- **Tête-à-tête** : 1 joueur par équipe
- **Doublette** : 2 joueurs par équipe  
- **Triplette** : 3 joueurs par équipe
- **Quadrette** : 4 joueurs par équipe (planning fixe sur 7 tours)
- **Mêlée** : Tirage aléatoire des participants individuels

### Gestion des Équipes
- Inscription automatique des équipes (numérotées Équipe 1, 2, 3...)
- Support de 1 à 4 joueurs par équipe selon le format
- Gestion automatique des équipes BYE (nombre impair d'équipes)

### Système de Matchs
- Génération automatique des tours avec appariement intelligent
- Algorithme d'appariement par performance pour éviter les re-rencontres
- Gestion des terrains avec assignation automatique
- Saisie et modification des scores via interface intuitive
- Système BYE automatique (victoire 13-7)

### Classement et Statistiques
- Classement temps réel basé sur victoires/défaites et différence de points
- Calcul automatique des statistiques d'équipe
- Affichage détaillé : victoires, défaites, points pour/contre, différence
- Export PDF du classement avec mise en forme professionnelle

### Interface Utilisateur
- Interface moderne avec onglets (Équipes, Matchs, Classement)
- Thèmes clair et sombre
- Tableaux interactifs avec tri et édition
- Barre de menus complète avec raccourcis
- Logo personnalisé et branding

## 🚀 Installation et Exécution

### Prérequis
- Python 3.8 ou supérieur
- tkinter (généralement inclus avec Python)
- Système avec interface graphique

### Installation des Dépendances
```bash
pip install -r requirements.txt
```

Copiez le fichier d'exemple d'environnement puis personnalisez-le :
```bash
cp backend/.env.example backend/.env
```

### Lancement de l'Application
```bash
python main.py
```

## 🏗️ Architecture

### Structure des Fichiers
```
petanque_manager/
├── main.py                    # Point d'entrée principal
├── gui.py                     # Interface graphique principale
├── store.py                   # Gestion base de données SQLite
├── tournament.py              # Logique de tournoi et appariement
├── widgets/                   # Composants d'interface spécialisés
│   ├── team_widget.py         # Gestion des équipes
│   ├── match_widget.py        # Tableau des matchs
│   └── standings_widget.py    # Affichage du classement
├── resources/                 # Ressources (logo, images)
├── styles/                    # Feuilles de style (future fonctionnalité)
├── requirements.txt           # Dépendances Python
└── README.md                  # Cette documentation
```

### Base de Données
- **SQLite** pour la persistance locale
- Tables : `tournaments`, `teams`, `matches`
- Gestion automatique des migrations et de l'initialisation

### Algorithmes de Tournoi

#### Formats Standard (Tête-à-tête, Doublette, Triplette)
- Calcul de performance basé sur la différence de points et le ratio victoires/défaites
- Appariement des équipes de performance similaire
- Vérification pour éviter les re-rencontres
- Gestion automatique des équipes BYE

#### Quadrette (Planning Fixe)
7 tours prédéfinis :
1. ABC vs D
2. AB vs CD  
3. ABD vs C
4. AC vs BD
5. ACD vs B
6. AD vs BC
7. BCD vs A

#### Mêlée
- Tirage aléatoire complet à chaque tour
- Constitution de groupes selon le nombre de terrains
- Évitement des répétitions de duos quand possible

## 🧪 Tests

### Test Console
Pour tester la logique sans interface graphique :
```bash
python test_console.py
```

Ce script teste :
- Création de tournois et équipes
- Génération de tours et appariement
- Mise à jour des scores et classements
- Export PDF
- Logique spécifique quadrette

## 📤 Export et Packaging

### Export PDF
- Classement complet avec statistiques
- Mise en forme professionnelle avec couleurs
- Podium mis en évidence (or, argent, bronze)
- Statistiques détaillées du tournoi

### Création d'un Exécutable
```bash
pyinstaller --onefile --windowed main.py
```

Options recommandées :
```bash
pyinstaller --onefile --windowed --icon=resources/logo.ico --name="PetanqueManager" main.py
```

## 🎨 Personnalisation

### Thèmes
- Thème clair (par défaut)
- Thème sombre
- Basculement via menu Affichage

### Logo et Branding
- Placez votre logo dans `resources/logo.png`
- Format recommandé : PNG, 120x120 pixels
- L'application fonctionne sans logo si le fichier n'existe pas

## 🤝 Utilisation

### Workflow Typique
1. **Créer un tournoi** : Menu Fichier > Nouveau Tournoi
2. **Inscrire les équipes** : Onglet Équipes, ajouter joueurs et créer équipes
3. **Générer les tours** : Onglet Matchs > Générer tour suivant
4. **Saisir les scores** : Double-clic sur un match pour éditer le score
5. **Consulter le classement** : Onglet Classement (mise à jour automatique)
6. **Exporter** : Menu Fichier > Exporter PDF

### Conseils d'Usage
- **Équipes BYE** : Gérées automatiquement, victoire 13-7 attribuée
- **Re-rencontres** : L'algorithme évite autant que possible les matchs répétés
- **Quadrette** : Respectez le planning des 7 tours pour une compétition équitable
- **Mêlée** : Idéal pour les événements conviviaux avec tirage aléatoire

## 🐛 Dépannage

### Problèmes Courants
- **tkinter non disponible** : Réinstallez Python avec support GUI ou installez python3-tk
- **Export PDF échoue** : Vérifiez l'installation de reportlab
- **Base de données corrompue** : Supprimez `petanque_manager.db`, l'application la recréera

### Logs et Débogage
L'application affiche les erreurs dans la barre de statut et via des boîtes de dialogue.

## 📝 Licence

Application développée pour la gestion de tournois de pétanque.

## 🏆 Crédits

Développé avec Python, tkinter, SQLite et reportlab.
Interface optimisée pour la gestion intuitive de tournois de pétanque.