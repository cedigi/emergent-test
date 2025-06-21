"""
Widget de gestion des matchs
Affiche les matchs et permet la saisie des scores
"""

import tkinter as tk
from tkinter import ttk, messagebox
from store import db_manager
from tournament import TournamentManager

class MatchWidget:
    """Widget pour la gestion des matchs"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.tournament_manager = TournamentManager()
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du widget"""
        # Configuration de la grille
        self.parent.grid_rowconfigure(2, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        
        # Entête avec les boutons de contrôle
        header_frame = ttk.Frame(self.parent)
        header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        
        # Informations du tour actuel
        self.round_info = ttk.Label(header_frame, text="Aucun tournoi sélectionné", 
                                   font=('Arial', 12, 'bold'))
        self.round_info.grid(row=0, column=0, sticky='w')
        
        # Boutons de génération
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.grid(row=0, column=1, sticky='e')
        
        ttk.Button(buttons_frame, text="Générer tour suivant", 
                  command=self.generate_next_round).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Valider tous les scores", 
                  command=self.validate_all_scores).grid(row=0, column=1, padx=5)
        
        # Configuration de la grille de l'entête
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Sélecteur de tour
        tour_frame = ttk.Frame(self.parent)
        tour_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        
        ttk.Label(tour_frame, text="Tour:").grid(row=0, column=0, padx=5)
        self.round_var = tk.StringVar()
        self.round_combo = ttk.Combobox(tour_frame, textvariable=self.round_var, 
                                       state='readonly', width=10)
        self.round_combo.grid(row=0, column=1, padx=5)
        self.round_combo.bind('<<ComboboxSelected>>', self.on_round_change)
        
        # Tableau des matchs
        matches_frame = ttk.LabelFrame(self.parent, text="Matchs du tour", padding="10")
        matches_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
        
        # Configuration du tableau
        columns = ('Terrain', 'Équipe 1', 'Score 1', 'Score 2', 'Équipe 2', 'Statut')
        self.matches_tree = ttk.Treeview(matches_frame, columns=columns, show='headings', height=15)
        
        # Configuration des colonnes
        self.matches_tree.heading('Terrain', text='Terrain')
        self.matches_tree.column('Terrain', width=70, anchor='center')
        
        self.matches_tree.heading('Équipe 1', text='Équipe 1')
        self.matches_tree.column('Équipe 1', width=150)
        
        self.matches_tree.heading('Score 1', text='Score 1')
        self.matches_tree.column('Score 1', width=70, anchor='center')
        
        self.matches_tree.heading('Score 2', text='Score 2')
        self.matches_tree.column('Score 2', width=70, anchor='center')
        
        self.matches_tree.heading('Équipe 2', text='Équipe 2')
        self.matches_tree.column('Équipe 2', width=150)
        
        self.matches_tree.heading('Statut', text='Statut')
        self.matches_tree.column('Statut', width=100, anchor='center')
        
        # Scrollbar pour le tableau
        scrollbar = ttk.Scrollbar(matches_frame, orient='vertical', command=self.matches_tree.yview)
        self.matches_tree.configure(yscrollcommand=scrollbar.set)
        
        self.matches_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Double-clic pour éditer un match
        self.matches_tree.bind('<Double-1>', self.edit_match)
        
        # Boutons de gestion des matchs
        match_buttons_frame = ttk.Frame(matches_frame)
        match_buttons_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(match_buttons_frame, text="Modifier le score", 
                  command=self.edit_match).grid(row=0, column=0, padx=5)
        ttk.Button(match_buttons_frame, text="Changer le terrain", 
                  command=self.change_court).grid(row=0, column=1, padx=5)
        
        # Configuration de la grille
        matches_frame.grid_rowconfigure(0, weight=1)
        matches_frame.grid_columnconfigure(0, weight=1)
    
    def generate_next_round(self):
        """Génère le tour suivant"""
        if not self.main_window.current_tournament_id:
            messagebox.showwarning("Attention", "Aucun tournoi sélectionné")
            return
        
        try:
            # Vérifier qu'il y a des équipes
            teams = db_manager.get_teams_by_tournament(self.main_window.current_tournament_id)
            if len(teams) < 2:
                messagebox.showwarning("Attention", "Au moins 2 équipes sont nécessaires pour générer un tour")
                return
            
            # Générer le tour
            matches = self.tournament_manager.generate_next_round(self.main_window.current_tournament_id)
            
            # Rafraîchir l'affichage
            self.refresh()
            
            self.main_window.update_status(f"Tour généré avec {len(matches)} matchs")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération du tour: {str(e)}")
    
    def validate_all_scores(self):
        """Valide tous les scores du tour actuel"""
        if not self.main_window.current_tournament_id:
            messagebox.showwarning("Attention", "Aucun tournoi sélectionné")
            return
        
        # TODO: Implémenter la validation de tous les scores
        messagebox.showinfo("Info", "Fonctionnalité de validation à implémenter")
    
    def on_round_change(self, event=None):
        """Appelé quand le tour sélectionné change"""
        selection = self.round_combo.current()
        if selection >= 0:
            self.load_matches_for_round(selection + 1)
    
    def load_matches_for_round(self, round_number):
        """Charge les matchs pour un tour donné"""
        if not self.main_window.current_tournament_id:
            return
        
        # Vider le tableau
        for item in self.matches_tree.get_children():
            self.matches_tree.delete(item)
        
        # Charger les matchs
        matches = db_manager.get_matches_by_tournament_round(
            self.main_window.current_tournament_id, round_number)
        
        for match in matches:
            court = match.get('court_number', '-')
            team1_name = match.get('team1_name', 'Équipe 1')
            team2_name = match.get('team2_name', 'Équipe 2')
            score1 = match.get('team1_score', '-')
            score2 = match.get('team2_score', '-')
            status = self.get_status_text(match.get('status', 'pending'))
            
            self.matches_tree.insert('', 'end', iid=match['id'], values=(
                court, team1_name, score1, score2, team2_name, status
            ))
    
    def get_status_text(self, status):
        """Convertit le statut en texte français"""
        status_map = {
            'pending': 'En attente',
            'playing': 'En cours',
            'finished': 'Terminé'
        }
        return status_map.get(status, status)
    
    def edit_match(self, event=None):
        """Ouvre la boîte de dialogue pour modifier un match"""
        selection = self.matches_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Aucun match sélectionné")
            return
        
        match_id = selection[0]
        
        # Récupérer les informations du match
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.*, t1.name as team1_name, t2.name as team2_name
                FROM matches m
                JOIN teams t1 ON m.team1_id = t1.id
                JOIN teams t2 ON m.team2_id = t2.id
                WHERE m.id = ?
            ''', (match_id,))
            row = cursor.fetchone()
            
            if not row:
                messagebox.showerror("Erreur", "Match introuvable")
                return
            
            match_data = dict(row)
        
        # Ouvrir la boîte de dialogue d'édition
        dialog = MatchEditDialog(self.parent, match_data, self.tournament_manager)
        if dialog.result:
            self.refresh()
    
    def change_court(self):
        """Change le terrain d'un match"""
        selection = self.matches_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Aucun match sélectionné")
            return
        
        match_id = selection[0]
        # TODO: Implémenter le changement de terrain
        messagebox.showinfo("Info", "Fonctionnalité de changement de terrain à implémenter")
    
    def refresh(self):
        """Rafraîchit l'affichage des matchs"""
        if not self.main_window.current_tournament_id:
            self.round_info.config(text="Aucun tournoi sélectionné")
            return
        
        # Récupérer les informations du tournoi
        tournament = db_manager.get_tournament(self.main_window.current_tournament_id)
        if not tournament:
            return
        
        current_round = tournament.get('current_round', 0)
        self.round_info.config(text=f"Tour actuel: {current_round}")
        
        # Mettre à jour la liste des tours
        rounds = list(range(1, current_round + 1))
        self.round_combo['values'] = [f"Tour {r}" for r in rounds]
        
        if rounds:
            self.round_combo.current(len(rounds) - 1)  # Sélectionner le dernier tour
            self.load_matches_for_round(rounds[-1])


class MatchEditDialog:
    """Boîte de dialogue pour modifier un match"""
    
    def __init__(self, parent, match_data, tournament_manager):
        self.result = None
        self.match_data = match_data
        self.tournament_manager = tournament_manager
        
        # Création de la fenêtre
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Modifier le match")
        self.dialog.geometry("400x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrage de la fenêtre
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_ui()
        
        # Attendre la fermeture de la boîte de dialogue
        self.dialog.wait_window()
    
    def setup_ui(self):
        """Configure l'interface de la boîte de dialogue"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Titre du match
        title = f"{self.match_data['team1_name']} vs {self.match_data['team2_name']}"
        ttk.Label(main_frame, text=title, font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Scores
        ttk.Label(main_frame, text=self.match_data['team1_name']).grid(row=1, column=0, sticky='w', pady=5)
        self.score1_var = tk.StringVar(value=str(self.match_data.get('team1_score', 0)))
        score1_spin = ttk.Spinbox(main_frame, from_=0, to=20, textvariable=self.score1_var, width=5)
        score1_spin.grid(row=1, column=1, padx=5)
        
        ttk.Label(main_frame, text="-").grid(row=1, column=2, padx=5)
        
        self.score2_var = tk.StringVar(value=str(self.match_data.get('team2_score', 0)))
        score2_spin = ttk.Spinbox(main_frame, from_=0, to=20, textvariable=self.score2_var, width=5)
        score2_spin.grid(row=1, column=3, padx=5)
        
        ttk.Label(main_frame, text=self.match_data['team2_name']).grid(row=1, column=4, sticky='w', pady=5)
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=5, pady=20)
        
        ttk.Button(button_frame, text="Sauvegarder", command=self.save_match).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Annuler", command=self.dialog.destroy).grid(row=0, column=1, padx=5)
    
    def save_match(self):
        """Sauvegarde les modifications du match"""
        try:
            score1 = int(self.score1_var.get())
            score2 = int(self.score2_var.get())
            
            if score1 < 0 or score2 < 0:
                messagebox.showerror("Erreur", "Les scores doivent être positifs")
                return
            
            # Mettre à jour le match
            self.tournament_manager.update_match_result(self.match_data['id'], score1, score2)
            
            self.result = True
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Erreur", "Les scores doivent être des nombres entiers")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")
