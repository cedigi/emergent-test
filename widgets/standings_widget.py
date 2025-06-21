"""
Widget d'affichage du classement
Affiche les statistiques et permet l'export PDF
"""

import tkinter as tk
from tkinter import ttk, messagebox
from store import db_manager
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

class StandingsWidget:
    """Widget pour l'affichage du classement"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du widget"""
        # Configuration de la grille
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        
        # Entête avec boutons d'export
        header_frame = ttk.Frame(self.parent)
        header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        
        # Titre
        self.title_label = ttk.Label(header_frame, text="Classement du tournoi", 
                                    font=('Arial', 14, 'bold'))
        self.title_label.grid(row=0, column=0, sticky='w')
        
        # Boutons d'export
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.grid(row=0, column=1, sticky='e')
        
        ttk.Button(buttons_frame, text="Exporter PDF", 
                  command=self.export_to_pdf).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Rafraîchir", 
                  command=self.refresh).grid(row=0, column=1, padx=5)
        
        # Configuration de la grille de l'entête
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Tableau du classement
        standings_frame = ttk.LabelFrame(self.parent, text="Classement", padding="10")
        standings_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        
        # Configuration du tableau
        columns = ('Position', 'Équipe', 'Victoires', 'Défaites', 'Points +', 'Points -', 'Différence', 'Ratio')
        self.standings_tree = ttk.Treeview(standings_frame, columns=columns, show='headings', height=15)
        
        # Configuration des colonnes
        col_widths = [80, 150, 80, 80, 80, 80, 80, 80]
        for i, col in enumerate(columns):
            self.standings_tree.heading(col, text=col)
            self.standings_tree.column(col, width=col_widths[i], anchor='center' if i > 1 else 'w')
        
        # Scrollbar pour le tableau
        scrollbar = ttk.Scrollbar(standings_frame, orient='vertical', command=self.standings_tree.yview)
        self.standings_tree.configure(yscrollcommand=scrollbar.set)
        
        self.standings_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Style pour les lignes du tableau
        self.standings_tree.tag_configure('first', background='#FFD700')  # Or pour le premier
        self.standings_tree.tag_configure('podium', background='#E6E6FA')  # Lavande pour le podium
        self.standings_tree.tag_configure('even', background='#F5F5F5')   # Gris clair pour les lignes paires
        
        # Statistiques résumées
        stats_frame = ttk.LabelFrame(self.parent, text="Statistiques", padding="10")
        stats_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=5)
        
        # Grille pour les statistiques
        self.stats_labels = {}
        stats_info = [
            ('total_teams', 'Équipes inscrites:'),
            ('total_matches', 'Matchs joués:'),
            ('avg_score', 'Score moyen:'),
            ('highest_score', 'Score le plus élevé:')
        ]
        
        for i, (key, label) in enumerate(stats_info):
            ttk.Label(stats_frame, text=label).grid(row=i//2, column=(i%2)*2, sticky='w', padx=5, pady=2)
            self.stats_labels[key] = ttk.Label(stats_frame, text="0", font=('Arial', 10, 'bold'))
            self.stats_labels[key].grid(row=i//2, column=(i%2)*2+1, sticky='w', padx=5, pady=2)
        
        # Configuration de la grille
        standings_frame.grid_rowconfigure(0, weight=1)
        standings_frame.grid_columnconfigure(0, weight=1)
    
    def refresh(self):
        """Rafraîchit l'affichage du classement"""
        if not self.main_window.current_tournament_id:
            self.title_label.config(text="Aucun tournoi sélectionné")
            return
        
        # Récupérer les informations du tournoi
        tournament = db_manager.get_tournament(self.main_window.current_tournament_id)
        if not tournament:
            return
        
        self.title_label.config(text=f"Classement - {tournament['name']}")
        
        # Vider le tableau
        for item in self.standings_tree.get_children():
            self.standings_tree.delete(item)
        
        # Charger le classement
        standings = db_manager.get_team_standings(self.main_window.current_tournament_id)
        
        for i, team in enumerate(standings):
            position = i + 1
            name = team['name']
            wins = team.get('wins', 0)
            losses = team.get('losses', 0)
            points_for = team.get('points_for', 0)
            points_against = team.get('points_against', 0)
            difference = team.get('point_difference', 0)
            
            # Calculer le ratio victoires/défaites
            total_games = wins + losses
            ratio = f"{wins}/{total_games}" if total_games > 0 else "0/0"
            
            # Déterminer le tag pour le style
            tag = ''
            if position == 1:
                tag = 'first'
            elif position <= 3:
                tag = 'podium'
            elif position % 2 == 0:
                tag = 'even'
            
            self.standings_tree.insert('', 'end', values=(
                position, name, wins, losses, points_for, points_against, 
                f"+{difference}" if difference >= 0 else str(difference), ratio
            ), tags=(tag,))
        
        # Mettre à jour les statistiques
        self.update_statistics(standings)
    
    def update_statistics(self, standings):
        """Met à jour les statistiques résumées"""
        if not standings:
            for key in self.stats_labels:
                self.stats_labels[key].config(text="0")
            return
        
        total_teams = len(standings)
        total_matches = sum(team.get('wins', 0) + team.get('losses', 0) for team in standings) // 2
        
        all_scores = []
        for team in standings:
            points_for = team.get('points_for', 0)
            points_against = team.get('points_against', 0)
            if points_for > 0:
                all_scores.append(points_for)
            if points_against > 0:
                all_scores.append(points_against)
        
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
        highest_score = max(all_scores) if all_scores else 0
        
        self.stats_labels['total_teams'].config(text=str(total_teams))
        self.stats_labels['total_matches'].config(text=str(total_matches))
        self.stats_labels['avg_score'].config(text=f"{avg_score:.1f}")
        self.stats_labels['highest_score'].config(text=str(highest_score))
    
    def export_to_pdf(self, filename=None):
        """Exporte le classement en PDF"""
        if not self.main_window.current_tournament_id:
            messagebox.showwarning("Attention", "Aucun tournoi sélectionné")
            return
        
        if not filename:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Exporter le classement"
            )
        
        if not filename:
            return
        
        try:
            # Récupérer les données
            tournament = db_manager.get_tournament(self.main_window.current_tournament_id)
            standings = db_manager.get_team_standings(self.main_window.current_tournament_id)
            
            # Créer le document PDF
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1  # Centré
            )
            
            # Titre
            title = Paragraph(f"Classement du Tournoi: {tournament['name']}", title_style)
            story.append(title)
            
            # Date et heure
            date_str = datetime.now().strftime("%d/%m/%Y à %H:%M")
            date_para = Paragraph(f"Généré le {date_str}", styles['Normal'])
            story.append(date_para)
            story.append(Spacer(1, 20))
            
            # Tableau du classement
            table_data = [
                ['Position', 'Équipe', 'V', 'D', 'Pts +', 'Pts -', 'Diff', 'Ratio']
            ]
            
            for i, team in enumerate(standings):
                position = i + 1
                name = team['name']
                wins = team.get('wins', 0)
                losses = team.get('losses', 0)
                points_for = team.get('points_for', 0)
                points_against = team.get('points_against', 0)
                difference = team.get('point_difference', 0)
                
                total_games = wins + losses
                ratio = f"{wins}/{total_games}" if total_games > 0 else "0/0"
                
                table_data.append([
                    str(position), name, str(wins), str(losses), 
                    str(points_for), str(points_against),
                    f"+{difference}" if difference >= 0 else str(difference), 
                    ratio
                ])
            
            # Créer et styliser le tableau
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            # Mettre en évidence le podium
            if len(standings) >= 1:
                table.setStyle(TableStyle([('BACKGROUND', (0, 1), (-1, 1), colors.gold)]))
            if len(standings) >= 2:
                table.setStyle(TableStyle([('BACKGROUND', (0, 2), (-1, 2), colors.silver)]))
            if len(standings) >= 3:
                table.setStyle(TableStyle([('BACKGROUND', (0, 3), (-1, 3), colors.Color(0.8, 0.5, 0.2))]))
            
            story.append(table)
            
            # Statistiques
            story.append(Spacer(1, 20))
            stats_title = Paragraph("Statistiques du Tournoi", styles['Heading2'])
            story.append(stats_title)
            
            total_teams = len(standings)
            total_matches = sum(team.get('wins', 0) + team.get('losses', 0) for team in standings) // 2
            
            stats_text = f"""
            • Nombre d'équipes: {total_teams}<br/>
            • Nombre de matchs joués: {total_matches}<br/>
            • Type de tournoi: {tournament['type']}<br/>
            • Nombre de terrains: {tournament['num_courts']}<br/>
            • Tour actuel: {tournament.get('current_round', 0)}
            """
            
            stats_para = Paragraph(stats_text, styles['Normal'])
            story.append(stats_para)
            
            # Générer le PDF
            doc.build(story)
            
            return True
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export PDF: {str(e)}")
            return False