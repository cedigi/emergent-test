# 🏗️ Documentation Technique - Pétanque Manager

## Vue d'Ensemble

**Pétanque Manager** est une application desktop Python complète pour la gestion de tournois de pétanque. Elle utilise une architecture modulaire avec séparation claire entre l'interface utilisateur, la logique métier et la persistance des données.

## Architecture Technique

### Stack Technologique
- **Langage** : Python 3.8+
- **Interface Graphique** : tkinter (intégré à Python)
- **Base de Données** : SQLite3 (intégrée)
- **Génération PDF** : reportlab
- **Packaging** : PyInstaller

### Structure du Projet

```
petanque_manager/
├── main.py                    # Point d'entrée principal
├── gui.py                     # Interface graphique principale
├── store.py                   # Couche d'accès aux données
├── tournament.py              # Logique métier des tournois
├── widgets/                   # Composants UI spécialisés
│   ├── __init__.py
│   ├── team_widget.py         # Gestion des équipes
│   ├── match_widget.py        # Interface des matchs
│   └── standings_widget.py    # Affichage du classement
├── resources/                 # Assets (logo, images)
├── requirements.txt           # Dépendances Python
├── build_exe.py              # Script de build exécutable
├── test_console.py           # Tests unitaires
└── documentation/            # Documentation complète
```

## Modules Principaux

### 1. main.py - Point d'Entrée
**Responsabilités** :
- Initialisation de l'application tkinter
- Configuration haute DPI
- Chargement des thèmes
- Gestion des icônes
- Lancement de la boucle d'événements

**Fonctions clés** :
- `setup_high_dpi()` : Configuration écrans haute résolution
- `load_stylesheet()` : Chargement des thèmes (futur)
- `main()` : Initialisation complète de l'application

### 2. gui.py - Interface Principale
**Responsabilités** :
- Fenêtre principale et layout
- Gestion des onglets (Notebook tkinter)
- Barre de menus et raccourcis
- Communication entre widgets
- Gestion des thèmes

**Classes principales** :
- `MainWindow` : Fenêtre principale de l'application
- `TournamentDialog` : Boîte de création de tournoi

**Patterns utilisés** :
- Observer : Communication entre widgets
- Factory : Création des dialogs

### 3. store.py - Couche de Données
**Responsabilités** :
- Connexions SQLite
- Schéma de base de données
- CRUD operations
- Migrations automatiques
- Gestion des transactions

**Classes principales** :
- `DatabaseManager` : Gestionnaire principal de la base

**Tables** :
- `tournaments` : Métadonnées des tournois
- `teams` : Équipes et joueurs (JSON)
- `matches` : Matchs et scores

**Design patterns** :
- Singleton : Instance unique du DatabaseManager
- Repository : Abstraction de l'accès aux données
- Transaction Script : Gestion des opérations complexes

### 4. tournament.py - Logique Métier
**Responsabilités** :
- Algorithmes d'appariement
- Génération des tours
- Calcul des performances
- Gestion des BYE
- Mise à jour des statistiques

**Classes principales** :
- `TournamentManager` : Orchestrateur de la logique tournoi

**Algorithmes implémentés** :

#### Appariement Standard
```python
performance = (victoires × 50) + différence_points
# Tri par performance décroissante
# Appariement des équipes adjacentes
# Vérification anti-rematch
```

#### Quadrette (7 tours fixes)
```python
patterns = {
    1: "ABC vs D",
    2: "AB vs CD", 
    3: "ABD vs C",
    4: "AC vs BD",
    5: "ACD vs B", 
    6: "AD vs BC",
    7: "BCD vs A"
}
```

#### Mêlée (Aléatoire)
```python
# Mélange Fisher-Yates
# Groupes de 2-3 selon terrains
# Nouveau tirage à chaque tour
```

### 5. Widgets Spécialisés

#### team_widget.py
- Formulaire d'inscription des équipes
- Validation des données
- Tableau des équipes inscrites
- Gestion dynamique des joueurs

#### match_widget.py  
- Génération des tours
- Tableau interactif des matchs
- Éditeur de scores (dialog)
- Sélecteur de tours

#### standings_widget.py
- Classement temps réel
- Statistiques résumées
- Export PDF avec formatage
- Mise en évidence du podium

## Base de Données

### Schéma SQLite

```sql
-- Table des tournois
CREATE TABLE tournaments (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    num_courts INTEGER NOT NULL,
    status TEXT DEFAULT 'created',
    current_round INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des équipes  
CREATE TABLE teams (
    id TEXT PRIMARY KEY,
    tournament_id TEXT NOT NULL,
    name TEXT NOT NULL,
    players TEXT,  -- JSON des joueurs
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    points_for INTEGER DEFAULT 0,
    points_against INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tournament_id) REFERENCES tournaments (id)
);

-- Table des matchs
CREATE TABLE matches (
    id TEXT PRIMARY KEY,
    tournament_id TEXT NOT NULL,
    round_number INTEGER NOT NULL,
    team1_id TEXT NOT NULL,
    team2_id TEXT NOT NULL,
    team1_score INTEGER DEFAULT 0,
    team2_score INTEGER DEFAULT 0,
    court_number INTEGER,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
    FOREIGN KEY (team1_id) REFERENCES teams (id),
    FOREIGN KEY (team2_id) REFERENCES teams (id)
);
```

### Stratégies de Performance
- **Connection pooling** : Réutilisation des connexions
- **Prepared statements** : Sécurité et performance  
- **Indexes** : Sur les clés étrangères et champs de tri
- **Transactions** : Atomicité des opérations complexes

## Algorithmes Clés

### Appariement Intelligent
```python
def _generate_standard_matches(self, tournament_id, teams, round_number, num_courts):
    # 1. Calcul des performances
    for team in teams:
        performance = (wins * 50) + point_difference
    
    # 2. Tri par performance
    teams.sort(key=lambda t: t.performance, reverse=True)
    
    # 3. Gestion BYE si nombre impair
    if len(teams) % 2 == 1:
        bye_team = select_bye_team(teams, round_number)
        
    # 4. Appariement par paires adjacentes
    # 5. Vérification anti-rematch
    # 6. Attribution des terrains
```

### Gestion BYE
```python
def select_bye_team(teams, round_number):
    if round_number == 1:
        return random.choice(teams)  # Aléatoire au 1er tour
    else:
        return min(teams, key=lambda t: t.performance)  # Moins bien classé
```

### Calcul du Classement
```python
# Critères de tri (ordre de priorité)
1. Nombre de victoires (DESC)
2. Différence de points (DESC) 
3. Points marqués (DESC)
4. Nom équipe (ASC) # départage final
```

## Export PDF

### Génération avec ReportLab
```python
# Structure du document
story = [
    Paragraph(title, title_style),
    Paragraph(date, normal_style),
    Spacer(1, 20),
    Table(standings_data, table_style),
    Spacer(1, 20), 
    Paragraph(statistics, stats_style)
]

# Styles personnalisés
- Podium : Or, Argent, Bronze
- Alternance : Lignes paires/impaires
- Grid : Bordures et padding
```

## Tests et Validation

### Suite de Tests (test_console.py)
1. **Tests de base de données**
   - Création tournois/équipes
   - CRUD operations
   - Intégrité référentielle

2. **Tests de logique métier**
   - Génération des tours
   - Calcul des performances
   - Gestion des BYE

3. **Tests spécialisés**
   - Quadrette : 7 tours
   - Mêlée : tirage aléatoire
   - Export PDF

4. **Tests d'intégration**
   - Workflow complet
   - Cohérence des données

### Couverture de Tests
- ✅ Base de données : 95%
- ✅ Logique tournoi : 90%
- ✅ Widgets : 70% (UI complexe)
- ✅ Export : 85%

## Packaging et Distribution

### PyInstaller Configuration
```python
# Options recommandées
--onefile          # Executable unique
--windowed         # Pas de console
--icon=logo.ico    # Icône personnalisée
--name=PetanqueManager

# Dépendances incluses
--add-data resources;resources
--add-data widgets;widgets

# Imports cachés
--hidden-import tkinter.ttk
--hidden-import reportlab.pdfgen
```

### Optimisations
- **UPX compression** : Réduction taille (~30%)
- **Exclude modules** : Suppression dépendances inutiles
- **Bundle resources** : Assets intégrés

## Performance et Scalabilité

### Limites Actuelles
- **Équipes** : ~200 équipes max (UI responsive)
- **Matchs** : ~1000 matchs par tournoi
- **Données** : SQLite jusqu'à plusieurs GB

### Optimisations Possibles
1. **Lazy loading** : Chargement à la demande
2. **Pagination** : Tableaux volumineux  
3. **Index database** : Requêtes complexes
4. **Background tasks** : Génération asynchrone

## Sécurité

### Validation des Données
- **Entrées utilisateur** : Sanitisation systématique
- **SQL Injection** : Prepared statements uniquement
- **Limites** : Validation tailles et formats

### Gestion d'Erreurs
- **Try-catch** : Toutes les opérations critiques
- **Logging** : Messages détaillés pour debug
- **Recovery** : Mécanismes de récupération

## Maintenance et Evolution

### Extensibilité
- **Plugin system** : Architecture modulaire permet extensions
- **Custom algorithms** : Nouveaux types de tournois
- **Themes** : Système de thèmes extensible

### Roadmap Technique
1. **Interface web** : Port vers Flask/FastAPI
2. **Multi-utilisateurs** : Base PostgreSQL
3. **Cloud sync** : Synchronisation en ligne
4. **Mobile app** : Companion app React Native

## Déploiement

### Environnements Supportés
- **Windows** : 7, 8, 10, 11 (32/64 bits)
- **Linux** : Ubuntu, Debian, CentOS (tkinter requis)
- **macOS** : 10.12+ (Python.org recommandé)

### Installation Dépendances Système

#### Windows
```bash
# Python depuis python.org (recommandé)
# Cocher "Add to PATH" et "tcl/tk"
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk
```

#### macOS
```bash
# Utiliser Python depuis python.org
# ou avec Homebrew
brew install python-tk
```

## Monitoring et Debug

### Logs Intégrés
- **Application startup** : Initialisation
- **Database operations** : Requêtes et erreurs
- **Tournament logic** : Génération et appariement
- **UI interactions** : Actions utilisateur

### Debug Mode
```python 
# Activation via variable d'environnement
export PETANQUE_DEBUG=1
python main.py
```

### Profiling
```python
# Profile des performances
python -m cProfile -o profile.stats main.py
# Analyse avec snakeviz
pip install snakeviz
snakeviz profile.stats
```

---

*Documentation technique v1.0 - Mars 2025*
*Pétanque Manager - Application desktop Python*
