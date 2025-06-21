"""
Interface graphique principale de Pétanque Manager
Gère la fenêtre principale et les onglets
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from store import db_manager
from widgets.team_widget import TeamWidget
from widgets.match_widget import MatchWidget
from widgets.standings_widget import StandingsWidget
from tournament import TournamentManager

class MainWindow:
    """Fenêtre principale de l'application"""
    
    def __init__(self, root):
        self.root = root
        self.current_tournament_id = None
        self.tournament_manager = TournamentManager()
        self.theme = 'light'  # 'light' ou 'dark'
        
        self.setup_ui()
        self.setup_menu()
        self.load_tournaments()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Configuration de la grille principale
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Bandeau d'entête
        self.setup_header()
        
        # Zone principale avec onglets
        self.setup_tabs()
        
        # Barre de statut
        self.setup_status_bar()
    
    def setup_header(self):
        """Configure le bandeau d'entête"""
        header_frame = ttk.Frame(self.root, style='Header.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        
        # Logo (si disponible)
        logo_path = 'resources/logo.png'
        if os.path.exists(logo_path):
            try:
                logo_image = tk.PhotoImage(file=logo_path)
                # Redimensionner le logo
                logo_image = logo_image.subsample(2, 2)  # Divise par 2
                logo_label = ttk.Label(header_frame, image=logo_image)
                logo_label.image = logo_image  # Garde une référence
                logo_label.grid(row=0, column=0, padx=10)
            except tk.TclError:
                pass
        
        # Titre principal
        title_label = ttk.Label(header_frame, text="Pétanque Manager", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=1, padx=20)
        
        # Sélecteur de tournoi
        ttk.Label(header_frame, text="Tournoi actuel:").grid(row=0, column=2, padx=10)
        self.tournament_var = tk.StringVar()
        self.tournament_combo = ttk.Combobox(header_frame, textvariable=self.tournament_var,
                                           state='readonly', width=30)
        self.tournament_combo.grid(row=0, column=3, padx=5)
        self.tournament_combo.bind('<<ComboboxSelected>>', self.on_tournament_change)
        
        # Boutons de gestion des tournois
        ttk.Button(header_frame, text="Nouveau Tournoi", 
                  command=self.create_tournament).grid(row=0, column=4, padx=5)
        ttk.Button(header_frame, text="Supprimer", 
                  command=self.delete_tournament).grid(row=0, column=5, padx=5)
    
    def setup_tabs(self):
        """Configure les onglets principaux"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
        
        # Onglet Équipes/Joueurs
        self.team_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.team_frame, text='Équipes / Joueurs')
        self.team_widget = TeamWidget(self.team_frame, self)
        
        # Onglet Matchs
        self.match_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.match_frame, text='Matchs')
        self.match_widget = MatchWidget(self.match_frame, self)
        
        # Onglet Classement
        self.standings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.standings_frame, text='Classement')
        self.standings_widget = StandingsWidget(self.standings_frame, self)
    
    def setup_status_bar(self):
        """Configure la barre de statut"""
        self.status_var = tk.StringVar()
        self.status_var.set("Prêt")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, sticky='ew', padx=5, pady=2)
    
    def setup_menu(self):
        """Configure la barre de menus"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau Tournoi", command=self.create_tournament)
        file_menu.add_separator()
        file_menu.add_command(label="Exporter PDF", command=self.export_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        
        # Menu Affichage
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Affichage", menu=view_menu)
        view_menu.add_command(label="Thème Clair", command=lambda: self.change_theme('light'))
        view_menu.add_command(label="Thème Sombre", command=lambda: self.change_theme('dark'))
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command=self.show_about)
    
    def load_tournaments(self):
        """Charge la liste des tournois"""
        tournaments = db_manager.get_all_tournaments()
        tournament_names = [f"{t['name']} ({t['type']})" for t in tournaments]
        self.tournament_combo['values'] = tournament_names
        
        if tournaments:
            self.tournament_combo.current(0)
            self.current_tournament_id = tournaments[0]['id']
            self.on_tournament_change()
    
    def create_tournament(self):
        """Ouvre la boîte de dialogue pour créer un tournoi"""
        dialog = TournamentDialog(self.root, self)
        if dialog.result:
            self.load_tournaments()
            # Sélectionner le nouveau tournoi
            tournaments = db_manager.get_all_tournaments()
            if tournaments:
                self.tournament_combo.current(0)
                self.current_tournament_id = tournaments[0]['id']
                self.on_tournament_change()
    
    def delete_tournament(self):
        """Supprime le tournoi actuel"""
        if not self.current_tournament_id:
            messagebox.showwarning("Attention", "Aucun tournoi sélectionné")
            return
        
        tournament = db_manager.get_tournament(self.current_tournament_id)
        if tournament:
            response = messagebox.askyesno("Confirmation", 
                                         f"Êtes-vous sûr de vouloir supprimer le tournoi '{tournament['name']}'?")
            if response:
                # TODO: Implémenter la suppression
                messagebox.showinfo("Info", "Fonctionnalité de suppression à implémenter")
    
    def on_tournament_change(self, event=None):
        """Appelé quand le tournoi sélectionné change"""
        selection = self.tournament_combo.current()
        if selection >= 0:
            tournaments = db_manager.get_all_tournaments()
            if selection < len(tournaments):
                self.current_tournament_id = tournaments[selection]['id']
                self.refresh_all_widgets()
    
    def refresh_all_widgets(self):
        """Rafraîchit tous les widgets avec les nouvelles données"""
        if self.current_tournament_id:
            self.team_widget.refresh()
            self.match_widget.refresh()
            self.standings_widget.refresh()
    
    def change_theme(self, theme):
        """Change le thème de l'application"""
        self.theme = theme
        style = ttk.Style()
        
        if theme == 'dark':
            # Configuration du thème sombre
            style.theme_use('alt')
            self.root.configure(bg='#2b2b2b')
        else:
            # Configuration du thème clair
            style.theme_use('clam')
            self.root.configure(bg='#f0f0f0')
        
        self.status_var.set(f"Thème {theme} appliqué")
    
    def export_pdf(self):
        """Exporte le classement en PDF"""
        if not self.current_tournament_id:
            messagebox.showwarning("Attention", "Aucun tournoi sélectionné")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.standings_widget.export_to_pdf(filename)
                messagebox.showinfo("Succès", f"Export réussi vers {filename}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'export: {str(e)}")
    
    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        messagebox.showinfo("À propos", 
                           "Pétanque Manager v1.0\n\n"
                           "Application de gestion de tournois de pétanque\n"
                           "Formats supportés: Tête-à-tête, Doublette, Triplette, Quadrette, Mêlée")
    
    def update_status(self, message):
        """Met à jour la barre de statut"""
        self.status_var.set(message)
        self.root.after(3000, lambda: self.status_var.set("Prêt"))


class TournamentDialog:
    """Boîte de dialogue pour créer un tournoi"""
    
    def __init__(self, parent, main_window):
        self.result = None
        self.main_window = main_window
        
        # Création de la fenêtre
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nouveau Tournoi")
        self.dialog.geometry("400x300")
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
        
        # Nom du tournoi
        ttk.Label(main_frame, text="Nom du tournoi:").grid(row=0, column=0, sticky='w', pady=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)
        name_entry.focus()
        
        # Type de tournoi
        ttk.Label(main_frame, text="Type de tournoi:").grid(row=2, column=0, sticky='w', pady=5)
        self.type_var = tk.StringVar(value="doublette")
        type_combo = ttk.Combobox(main_frame, textvariable=self.type_var, 
                                 values=["tete_a_tete", "doublette", "triplette", "quadrette", "melee"],
                                 state='readonly')
        type_combo.grid(row=3, column=0, columnspan=2, sticky='ew', pady=5)
        
        # Nombre de terrains
        ttk.Label(main_frame, text="Nombre de terrains:").grid(row=4, column=0, sticky='w', pady=5)
        self.courts_var = tk.StringVar(value="4")
        courts_spin = ttk.Spinbox(main_frame, from_=1, to=20, textvariable=self.courts_var, width=10)
        courts_spin.grid(row=5, column=0, sticky='w', pady=5)
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Créer", command=self.create_tournament).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Annuler", command=self.dialog.destroy).grid(row=0, column=1, padx=5)
        
        # Configuration de la grille
        main_frame.grid_columnconfigure(0, weight=1)
    
    def create_tournament(self):
        """Crée le tournoi avec les paramètres saisis"""
        name = self.name_var.get().strip()
        tournament_type = self.type_var.get()
        
        try:
            num_courts = int(self.courts_var.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le nombre de terrains doit être un nombre entier")
            return
        
        if not name:
            messagebox.showerror("Erreur", "Le nom du tournoi est obligatoire")
            return
        
        if num_courts < 1:
            messagebox.showerror("Erreur", "Le nombre de terrains doit être au moins 1")
            return
        
        # Créer le tournoi
        tournament_id = db_manager.create_tournament(name, tournament_type, num_courts)
        self.result = tournament_id
        
        self.main_window.update_status(f"Tournoi '{name}' créé avec succès")
        self.dialog.destroy()