"""
Widget de gestion des équipes et joueurs
Permet l'inscription et la gestion des participants
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from store import db_manager
import json

class TeamWidget:
    """Widget pour la gestion des équipes et joueurs"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du widget"""
        # Configuration de la grille
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)
        
        # Panel de gauche - Ajout d'équipes
        left_frame = ttk.LabelFrame(self.parent, text="Ajouter une équipe", padding="10")
        left_frame.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        # Nom de l'équipe (généré automatiquement)
        ttk.Label(left_frame, text="L'équipe sera nommée automatiquement").grid(row=0, column=0, columnspan=2, pady=5)
        
        # Liste des joueurs
        ttk.Label(left_frame, text="Joueurs:").grid(row=1, column=0, sticky='w', pady=5)
        
        # Frame pour les entrées de joueurs
        players_frame = ttk.Frame(left_frame)
        players_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=5)
        
        self.player_entries = []
        self.add_player_entry(players_frame, 0, "Joueur 1*")
        
        # Bouton pour ajouter plus de joueurs
        ttk.Button(left_frame, text="+ Ajouter un joueur", 
                  command=self.add_more_players).grid(row=3, column=0, pady=10)
        
        # Bouton pour créer l'équipe
        ttk.Button(left_frame, text="Créer l'équipe", 
                  command=self.create_team).grid(row=4, column=0, pady=10)
        
        # Panel de droite - Liste des équipes
        right_frame = ttk.LabelFrame(self.parent, text="Équipes inscrites", padding="10")
        right_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        # Tableau des équipes
        columns = ('Nom', 'Joueurs', 'Victoires', 'Défaites', 'Points +', 'Points -')
        self.teams_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.teams_tree.heading(col, text=col)
            self.teams_tree.column(col, width=100)
        
        # Scrollbar pour le tableau
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.teams_tree.yview)
        self.teams_tree.configure(yscrollcommand=scrollbar.set)
        
        self.teams_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Boutons de gestion
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(buttons_frame, text="Supprimer", 
                  command=self.delete_team).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Modifier", 
                  command=self.edit_team).grid(row=0, column=1, padx=5)
        
        # Configuration de la grille
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
    
    def add_player_entry(self, parent, row, label_text):
        """Ajoute une entrée pour un joueur"""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky='w', pady=2)
        entry_var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=entry_var, width=25)
        entry.grid(row=row, column=1, padx=5, pady=2)
        self.player_entries.append((entry_var, entry))
        return entry_var, entry
    
    def add_more_players(self):
        """Ajoute une entrée pour un joueur supplémentaire"""
        if len(self.player_entries) >= 4:
            messagebox.showwarning("Limite", "Maximum 4 joueurs par équipe")
            return
        
        # Trouver le frame des joueurs
        players_frame = self.player_entries[0][1].master
        row = len(self.player_entries)
        label_text = f"Joueur {row + 1}"
        
        self.add_player_entry(players_frame, row, label_text)
    
    def create_team(self):
        """Crée une nouvelle équipe"""
        if not self.main_window.current_tournament_id:
            messagebox.showwarning("Attention", "Aucun tournoi sélectionné")
            return
        
        # Récupérer les noms des joueurs
        players = []
        for entry_var, entry in self.player_entries:
            name = entry_var.get().strip()
            if name:
                players.append(name)
        
        if not players:
            messagebox.showwarning("Attention", "Au moins un joueur est requis")
            return
        
        # Générer un nom d'équipe automatique
        existing_teams = db_manager.get_teams_by_tournament(self.main_window.current_tournament_id)
        team_number = len(existing_teams) + 1
        team_name = f"Équipe {team_number}"
        
        # Créer l'équipe
        try:
            db_manager.create_team(self.main_window.current_tournament_id, team_name, players)
            
            # Réinitialiser les champs
            for entry_var, entry in self.player_entries:
                entry_var.set("")
            
            # Rafraîchir la liste
            self.refresh()
            
            self.main_window.update_status(f"Équipe '{team_name}' créée avec succès")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création de l'équipe: {str(e)}")
    
    def refresh(self):
        """Rafraîchit la liste des équipes"""
        if not self.main_window.current_tournament_id:
            return
        
        # Vider le tableau
        for item in self.teams_tree.get_children():
            self.teams_tree.delete(item)
        
        # Charger les équipes
        teams = db_manager.get_teams_by_tournament(self.main_window.current_tournament_id)
        
        for team in teams:
            players_str = ", ".join(team['players'])
            if len(players_str) > 30:
                players_str = players_str[:27] + "..."
            
            self.teams_tree.insert('', 'end', iid=team['id'], values=(
                team['name'],
                players_str,
                team.get('wins', 0),
                team.get('losses', 0),
                team.get('points_for', 0),
                team.get('points_against', 0)
            ))
    
    def delete_team(self):
        """Supprime l'équipe sélectionnée"""
        selection = self.teams_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Aucune équipe sélectionnée")
            return

        team_id = selection[0]
        codex/étendre-databasemanager-avec-delete_team-et-delete_tournamen
        team_name = self.teams_tree.item(team_id, 'values')[0]
        response = messagebox.askyesno(
            "Confirmation",
            f"Supprimer l'équipe '{team_name}' et ses matchs ?"
        )
        if response:
            try:
                db_manager.delete_team(team_id)
                self.main_window.refresh_all_widgets()
                self.main_window.update_status(
                    f"Équipe '{team_name}' supprimée")
            except Exception as e:
                messagebox.showerror("Erreur",
                                     f"Erreur lors de la suppression: {str(e)}")


        db_manager.delete_team(team_id)
        self.refresh()
        self.main_window.update_status("Équipe supprimée")
    
        main
    def edit_team(self):
        """Modifie l'équipe sélectionnée"""
        selection = self.teams_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Aucune équipe sélectionnée")
            return

        team_id = selection[0]
        codex/ajouter-méthode-update_team-à-databasemanager

        # Charger les données de l'équipe
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM teams WHERE id = ?', (team_id,))
            row = cursor.fetchone()

        if not row:
            messagebox.showerror("Erreur", "Équipe introuvable")
            return

        team_data = dict(row)
        team_data['players'] = json.loads(team_data['players']) if team_data['players'] else []

        dialog = TeamEditDialog(self.parent, team_data)
        if dialog.result:
            self.refresh()
            self.main_window.update_status("Équipe mise à jour")


class TeamEditDialog:
    """Boîte de dialogue pour modifier une équipe"""

    def __init__(self, parent, team_data):
        self.result = None
        self.team_data = team_data

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Modifier l'équipe")
        self.dialog.geometry("350x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        self.setup_ui()
        self.dialog.wait_window()

    def setup_ui(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky='nsew')

        ttk.Label(main_frame, text="Nom de l'équipe:").grid(row=0, column=0, sticky='w', pady=5)
        self.name_var = tk.StringVar(value=self.team_data.get('name', ''))
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)

        ttk.Label(main_frame, text="Joueurs:").grid(row=2, column=0, sticky='w', pady=5)
        self.player_vars = []
        players = self.team_data.get('players', [])
        for i in range(4):
            ttk.Label(main_frame, text=f"Joueur {i+1}").grid(row=3+i, column=0, sticky='w', pady=2)
            var = tk.StringVar(value=players[i] if i < len(players) else '')
            entry = ttk.Entry(main_frame, textvariable=var, width=25)
            entry.grid(row=3+i, column=1, sticky='w', pady=2)
            self.player_vars.append(var)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Sauvegarder", command=self.save).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Annuler", command=self.dialog.destroy).grid(row=0, column=1, padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def save(self):
        name = self.name_var.get().strip()
        players = [var.get().strip() for var in self.player_vars if var.get().strip()]

        if not name:
            messagebox.showerror("Erreur", "Le nom de l'équipe est obligatoire")
            return

        try:
            db_manager.update_team(self.team_data['id'], name, players)
            self.result = True
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour: {str(e)}")

        item = self.teams_tree.item(team_id)
        current_name = item['values'][0]
        current_players = item['values'][1]

        new_name = simpledialog.askstring("Nom de l'équipe",
                                         "Nouveau nom:",
                                         initialvalue=current_name,
                                         parent=self.parent)
        if new_name is None:
            return

        players_str = simpledialog.askstring(
            "Joueurs",
            "Liste des joueurs (séparés par des virgules):",
            initialvalue=current_players,
            parent=self.parent
        )
        if players_str is None:
            return

        players_list = [p.strip() for p in players_str.split(',') if p.strip()]
        db_manager.update_team(team_id, name=new_name, players=players_list)
        self.refresh()
        self.main_window.update_status("Équipe modifiée")
        main
