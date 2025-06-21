# 🚀 Guide d'Installation Locale - Pétanque Manager

## 📋 Prérequis Système

### Windows (Recommandé)
- Windows 7, 8, 10, ou 11
- Au moins 100 MB d'espace libre
- Connexion internet pour l'installation

### Linux (Ubuntu/Debian)
- Ubuntu 18.04+ ou Debian 9+
- Interface graphique (GNOME, KDE, etc.)

### macOS
- macOS 10.12 (Sierra) ou plus récent
- Xcode Command Line Tools

---

## 🔽 Étape 1: Télécharger les Fichiers

### Option A: Téléchargement Direct
1. **Créez un dossier** sur votre Bureau : `PetanqueManager`
2. **Téléchargez tous les fichiers** du projet dans ce dossier

### Option B: Via Git (si installé)
```bash
git clone <url-du-projet> PetanqueManager
cd PetanqueManager
```

---

## 🐍 Étape 2: Installation de Python

### Windows
1. **Allez sur** https://python.org/downloads/
2. **Téléchargez** Python 3.8 ou plus récent
3. **Lancez l'installateur**
4. **⚠️ IMPORTANT** : Cochez "Add Python to PATH" et "Install tcl/tk and IDLE"
5. **Cliquez** "Install Now"
6. **Vérifiez** l'installation :
   ```cmd
   python --version
   ```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

### macOS
1. **Téléchargez** Python depuis python.org (recommandé)
2. **Ou via Homebrew** :
   ```bash
   brew install python-tk
   ```

---

## 📦 Étape 3: Installation Automatique

### Windows - Méthode Simple
1. **Ouvrez** le dossier PetanqueManager
2. **Double-cliquez** sur `install.bat`
3. **Suivez** les instructions à l'écran
4. **Attendez** la fin de l'installation

### Installation Manuelle (tous systèmes)
1. **Ouvrez** un terminal/invite de commandes
2. **Naviguez** vers le dossier :
   ```bash
   cd chemin/vers/PetanqueManager
   ```
3. **Installez** les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎯 Étape 4: Premier Lancement

### Windows - Lancement Simple
**Double-cliquez** sur `launch.bat`

### Lancement Manuel
```bash
python main.py
```

### ✅ Vérification du Lancement
Si tout fonctionne, vous devriez voir :
- Fenêtre "Pétanque Manager v1.0"
- 3 onglets : Équipes/Joueurs, Matchs, Classement
- Bandeau avec logo et sélecteur de tournoi

---

## 🧪 Étape 5: Test Rapide

### Test des Fonctionnalités de Base
1. **Créez un tournoi** :
   - Cliquez "Nouveau Tournoi"
   - Nom : "Test Tournoi"
   - Type : "doublette"
   - Terrains : 2
   - Cliquez "Créer"

2. **Ajoutez des équipes** (onglet Équipes) :
   - Joueur 1 : "Alice", Joueur 2 : "Bob"
   - Cliquez "Créer l'équipe"
   - Répétez pour 4-6 équipes

3. **Générez un tour** (onglet Matchs) :
   - Cliquez "Générer tour suivant"
   - Vérifiez que les matchs apparaissent

4. **Saisissez des scores** :
   - Double-cliquez sur un match
   - Modifiez les scores
   - Cliquez "Sauvegarder"

5. **Consultez le classement** (onglet Classement) :
   - Vérifiez que les statistiques se mettent à jour

---

## 🔧 Résolution de Problèmes

### Erreur "tkinter not found"
**Windows** :
- Réinstallez Python en cochant "tcl/tk and IDLE"

**Linux** :
```bash
sudo apt install python3-tk
```

**macOS** :
- Utilisez Python depuis python.org (pas celui du système)

### Erreur "No module named 'reportlab'"
```bash
pip install reportlab
```

### Application ne se lance pas
1. **Vérifiez Python** :
   ```bash
   python --version  # Doit être 3.8+
   ```

2. **Testez la logique** sans interface :
   ```bash
   python test_console.py
   ```

3. **Réinstallez les dépendances** :
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

### Erreur de permissions (Linux/macOS)
```bash
chmod +x main.py
sudo pip install -r requirements.txt
```

---

## 🎨 Personnalisation

### Ajouter votre Logo
1. **Remplacez** `resources/logo.png` par votre logo (120x120 pixels)
2. **Redémarrez** l'application

### Changer le Thème
- **Menu Affichage** → Thème Clair/Sombre

---

## 🔄 Test Complet - Workflow

### Scenario de Test Complet
1. **Créer un tournoi** "Championnat Club 2025" (doublette, 3 terrains)

2. **Inscrire 8 équipes** :
   - Équipe 1 : Alice, Bob
   - Équipe 2 : Charlie, David
   - Équipe 3 : Eve, Frank
   - Équipe 4 : Grace, Henry
   - Équipe 5 : Iris, Jack
   - Équipe 6 : Kate, Liam
   - Équipe 7 : Mary, Nick
   - Équipe 8 : Olivia, Peter

3. **Générer 3 tours** avec scores variés

4. **Exporter le classement** en PDF

5. **Vérifier la cohérence** des statistiques

---

## 📊 Fonctionnalités à Tester

### ✅ Checklist de Validation
- [ ] Création de tournoi
- [ ] Inscription d'équipes (1-4 joueurs)
- [ ] Génération de tours
- [ ] Édition de scores
- [ ] Calcul automatique du classement
- [ ] Gestion des BYE (nombre impair d'équipes)
- [ ] Export PDF
- [ ] Basculement de thèmes
- [ ] Navigation entre les onglets

### 🎯 Tests Avancés
- [ ] Tournoi quadrette (4 joueurs/équipe, 7 tours)
- [ ] Tournoi mêlée (participants individuels)
- [ ] Gros tournoi (20+ équipes)
- [ ] Sauvegarde/rechargement des données

---

## 📞 Support

### Si l'Application Fonctionne
**Félicitations !** Vous pouvez maintenant :
- Gérer vos tournois de pétanque
- Créer des exécutables avec `python build_exe.py`
- Consulter le guide utilisateur complet

### Si Vous Rencontrez des Problèmes
1. **Vérifiez** que vous avez suivi toutes les étapes
2. **Testez** avec `python test_console.py`
3. **Consultez** la section résolution de problèmes
4. **Vérifiez** votre version de Python (3.8+ requis)

### Informations de Debug
Si vous avez besoin d'aide, collectez ces informations :
```bash
python --version
pip list | grep -E "(tkinter|reportlab)"
python test_console.py
```

---

## 🎉 Prochaines Étapes

Une fois l'application testée :
1. **Lisez** le Guide Utilisateur complet (`GUIDE_UTILISATEUR.md`)
2. **Créez** un exécutable Windows (`python build_exe.py`)
3. **Partagez** l'application avec votre club de pétanque
4. **Personnalisez** avec votre logo et vos couleurs

---

**Bon test avec Pétanque Manager ! 🎯**

*N'hésitez pas à signaler tout problème ou suggestion d'amélioration.*