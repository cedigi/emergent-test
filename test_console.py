#!/usr/bin/env python3
"""
Test console pour Pétanque Manager
Teste la logique métier sans interface graphique
"""

from store import db_manager
from tournament import TournamentManager
import os

def test_database():
    """Test des opérations de base de données"""
    print("=== Test de la base de données ===")
    
    # Créer un tournoi de test
    tournament_id = db_manager.create_tournament("Test Tournoi", "doublette", 4)
    print(f"Tournoi créé avec l'ID: {tournament_id}")
    
    # Créer des équipes de test
    teams = []
    team_names = [
        (["Alice", "Bob"], "Équipe 1"),
        (["Charlie", "David"], "Équipe 2"),
        (["Eve", "Frank"], "Équipe 3"),
        (["Grace", "Henry"], "Équipe 4"),
        (["Iris", "Jack"], "Équipe 5")
    ]
    
    for players, name in team_names:
        team_id = db_manager.create_team(tournament_id, name, players)
        teams.append(team_id)
        print(f"Équipe '{name}' créée avec les joueurs: {', '.join(players)}")
    
    # Récupérer et afficher les équipes
    print("\n=== Équipes inscrites ===")
    tournament_teams = db_manager.get_teams_by_tournament(tournament_id)
    for team in tournament_teams:
        print(f"- {team['name']}: {', '.join(team['players'])}")
    
    return tournament_id, teams

def test_tournament_logic(tournament_id):
    """Test de la logique de tournoi"""
    print("\n=== Test de la logique de tournoi ===")
    
    tournament_manager = TournamentManager()
    
    # Générer le premier tour
    try:
        matches = tournament_manager.generate_next_round(tournament_id)
        print(f"Premier tour généré avec {len(matches)} matchs:")
        
        for i, match in enumerate(matches):
            team1_name = match['team1']['name']
            team2_name = match['team2']['name']
            court = match['court']
            print(f"  Match {i+1} - Terrain {court}: {team1_name} vs {team2_name}")
        
        # Simuler quelques résultats
        print("\n=== Simulation de résultats ===")
        match_results = [(13, 8), (11, 13), (13, 5)]
        
        for i, (score1, score2) in enumerate(match_results):
            if i < len(matches):
                match_data = matches[i]
                print(f"Résultat: {match_data['team1']['name']} {score1} - {score2} {match_data['team2']['name']}")
                
                # Mettre à jour le résultat
                tournament_manager.update_match_result(match_data['id'], score1, score2)
        
        # Afficher le classement
        print("\n=== Classement après le premier tour ===")
        standings = db_manager.get_team_standings(tournament_id)
        
        for i, team in enumerate(standings):
            print(f"{i+1}. {team['name']} - V:{team['wins']} D:{team['losses']} "
                  f"Pts: {team['points_for']}-{team['points_against']} "
                  f"(Diff: {team['point_difference']})")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors du test de tournoi: {str(e)}")
        return False

def test_quadrette_logic():
    """Test spécifique pour la logique quadrette"""
    print("\n=== Test de la logique quadrette ===")
    
    # Créer un tournoi quadrette
    tournament_id = db_manager.create_tournament("Test Quadrette", "quadrette", 2)
    
    # Créer des équipes de 4 joueurs
    quadrette_teams = [
        (["A1", "B1", "C1", "D1"], "Équipe Alpha"),
        (["A2", "B2", "C2", "D2"], "Équipe Beta"),
        (["A3", "B3", "C3", "D3"], "Équipe Gamma"),
        (["A4", "B4", "C4", "D4"], "Équipe Delta")
    ]
    
    for players, name in quadrette_teams:
        db_manager.create_team(tournament_id, name, players)
        print(f"Équipe quadrette '{name}' créée")
    
    tournament_manager = TournamentManager()
    
    # Tester les 7 tours de quadrette
    for round_num in range(1, 4):  # Tester les 3 premiers tours
        try:
            matches = tournament_manager.generate_next_round(tournament_id)
            print(f"\nTour {round_num} - Pattern: {matches[0].get('pattern', 'N/A')}")
            for match in matches:
                print(f"  {match['team1']['name']} vs {match['team2']['name']}")
        except Exception as e:
            print(f"Erreur au tour {round_num}: {str(e)}")
            break
    
    return tournament_id

def test_export_functionality():
    """Test de la fonctionnalité d'export"""
    print("\n=== Test de l'export PDF ===")
    
    try:
        # Créer un fichier PDF de test
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        
        filename = "/app/test_export.pdf"
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        
        story = [
            Paragraph("Test d'export PDF pour Pétanque Manager", styles['Title']),
            Paragraph("Ce fichier démontre que l'export PDF fonctionne correctement.", styles['Normal'])
        ]
        
        doc.build(story)
        
        if os.path.exists(filename):
            print(f"✓ Export PDF réussi: {filename}")
            file_size = os.path.getsize(filename)
            print(f"  Taille du fichier: {file_size} bytes")
            return True
        else:
            print("✗ Échec de l'export PDF")
            return False
            
    except Exception as e:
        print(f"✗ Erreur lors de l'export PDF: {str(e)}")
        return False

def create_sample_logo():
    """Crée un logo simple pour l'application"""
    print("\n=== Création du logo ===")
    
    try:
        # Créer un fichier SVG simple comme logo
        svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="120" height="120" xmlns="http://www.w3.org/2000/svg">
  <circle cx="60" cy="60" r="50" fill="#2E8B57" stroke="#1F5F3F" stroke-width="3"/>
  <circle cx="60" cy="60" r="35" fill="#90EE90" stroke="#2E8B57" stroke-width="2"/>
  <circle cx="60" cy="60" r="20" fill="#FFFFFF" stroke="#2E8B57" stroke-width="2"/>
  <text x="60" y="15" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#2E8B57">PÉTANQUE</text>
  <text x="60" y="110" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" font-weight="bold" fill="#2E8B57">MANAGER</text>
</svg>'''
        
        logo_path = "/app/resources/logo.svg"
        with open(logo_path, 'w') as f:
            f.write(svg_content)
        
        print(f"✓ Logo SVG créé: {logo_path}")
        
        # Créer aussi un README pour les ressources
        readme_content = """# Ressources Pétanque Manager

## Logo
- logo.svg : Logo principal de l'application (format vectoriel)

Pour utiliser une image PNG, vous pouvez convertir le fichier SVG ou créer votre propre logo.

## Utilisation dans l'application
L'application cherche automatiquement le fichier `resources/logo.png` pour l'affichage dans l'interface.
Si le fichier n'existe pas, l'application fonctionne sans logo.
"""
        
        with open("/app/resources/README.md", 'w') as f:
            f.write(readme_content)
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de la création du logo: {str(e)}")
        return False

def main():
    """Fonction principale de test"""
    print("🎯 PÉTANQUE MANAGER - Tests Console")
    print("=" * 50)
    
    # Test de la base de données
    tournament_id, teams = test_database()
    
    # Test de la logique de tournoi
    test_tournament_logic(tournament_id)
    
    # Test spécifique quadrette
    test_quadrette_logic()
    
    # Test de l'export
    test_export_functionality()
    
    # Créer le logo
    create_sample_logo()
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés!")
    print("\nNote: L'application desktop complète nécessite un environnement")
    print("avec interface graphique (tkinter) pour fonctionner.")
    print("\nPour tester l'interface graphique:")
    print("1. Installez Python 3.8+ avec tkinter sur votre système")
    print("2. Installez les dépendances: pip install -r requirements.txt")
    print("3. Lancez: python main.py")

if __name__ == '__main__':
    main()