import tkinter as tk
from tkinter import ttk, messagebox
import random
import io
import base64

class CareerPathGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Career Path Challenge - Guess the Player")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a3a5f")
        
        # Football player database with career paths
        self.players = [
            {
                "name": "Lionel Messi",
                "career_path": [
                    {"club": "Barcelona", "years": "2004-2021", "apps": 778, "goals": 672},
                    {"club": "Paris Saint-Germain", "years": "2021-2023", "apps": 75, "goals": 32},
                    {"club": "Inter Miami", "years": "2023-present", "apps": 30, "goals": 25}
                ],
                "nationality": "Argentina",
                "position": "Forward",
                "image": "messi_img"
            },
            {
                "name": "Cristiano Ronaldo",
                "career_path": [
                    {"club": "Sporting CP", "years": "2002-2003", "apps": 31, "goals": 5},
                    {"club": "Manchester United", "years": "2003-2009", "apps": 292, "goals": 118},
                    {"club": "Real Madrid", "years": "2009-2018", "apps": 438, "goals": 450},
                    {"club": "Juventus", "years": "2018-2021", "apps": 134, "goals": 101},
                    {"club": "Manchester United", "years": "2021-2022", "apps": 40, "goals": 19},
                    {"club": "Al Nassr", "years": "2023-present", "apps": 50, "goals": 44}
                ],
                "nationality": "Portugal",
                "position": "Forward",
                "image": "ronaldo_img"
            },
            {
                "name": "Neymar Jr",
                "career_path": [
                    {"club": "Santos", "years": "2009-2013", "apps": 225, "goals": 136},
                    {"club": "Barcelona", "years": "2013-2017", "apps": 186, "goals": 105},
                    {"club": "Paris Saint-Germain", "years": "2017-2023", "apps": 173, "goals": 118},
                    {"club": "Al Hilal", "years": "2023-present", "apps": 25, "goals": 15}
                ],
                "nationality": "Brazil",
                "position": "Forward",
                "image": "neymar_img"
            },
            {
                "name": "Kevin De Bruyne",
                "career_path": [
                    {"club": "Genk", "years": "2008-2012", "apps": 113, "goals": 17},
                    {"club": "Chelsea", "years": "2012-2014", "apps": 9, "goals": 0},
                    {"club": "Werder Bremen", "years": "2012-2013", "apps": 33, "goals": 10},
                    {"club": "Wolfsburg", "years": "2014-2015", "apps": 72, "goals": 20},
                    {"club": "Manchester City", "years": "2015-present", "apps": 350, "goals": 96}
                ],
                "nationality": "Belgium",
                "position": "Midfielder",
                "image": "debruyne_img"
            },
            {
                "name": "Robert Lewandowski",
                "career_path": [
                    {"club": "Znicz Pruszków", "years": "2006-2008", "apps": 59, "goals": 36},
                    {"club": "Lech Poznań", "years": "2008-2010", "apps": 82, "goals": 41},
                    {"club": "Borussia Dortmund", "years": "2010-2014", "apps": 187, "goals": 103},
                    {"club": "Bayern Munich", "years": "2014-2022", "apps": 375, "goals": 344},
                    {"club": "Barcelona", "years": "2022-present", "apps": 85, "goals": 55}
                ],
                "nationality": "Poland",
                "position": "Forward",
                "image": "lewandowski_img"
            }
        ]
        
        # Game state
        self.secret_player = None
        self.clues_revealed = 0
        self.max_clues = 5
        self.guesses = 0
        self.max_guesses = 6
        self.score = 0
        self.game_active = False
        
        # Setup UI
        self.setup_ui()
        
        # Start new game
        self.start_new_game()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#0a2a4f", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="CAREER PATH CHALLENGE", font=("Arial", 20, "bold"), 
                fg="white", bg="#0a2a4f").pack(side=tk.LEFT, padx=20)
        
        self.score_label = tk.Label(header_frame, text=f"Score: {self.score}", 
                                   font=("Arial", 14), fg="white", bg="#0a2a4f")
        self.score_label.pack(side=tk.RIGHT, padx=20)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#1a3a5f")
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="Guess the Footballer by Career Path", 
                              font=("Arial", 18, "bold"), fg="white", bg="#1a3a5f")
        title_label.pack(pady=(0, 20))
        
        # Clues frame
        clues_frame = tk.Frame(content_frame, bg="#2a4a6f", relief=tk.RAISED, bd=2)
        clues_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(clues_frame, text="Career Path Clues", font=("Arial", 14, "bold"), 
                fg="white", bg="#2a4a6f").pack(pady=10)
        
        self.clue_labels = []
        for i in range(self.max_clues):
            label = tk.Label(clues_frame, text="", font=("Arial", 12), 
                            bg="#2a4a6f", fg="white", justify=tk.LEFT, anchor="w")
            label.pack(fill=tk.X, padx=20, pady=5)
            self.clue_labels.append(label)
        
        # Guess frame
        guess_frame = tk.Frame(content_frame, bg="#1a3a5f")
        guess_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(guess_frame, text="Make a Guess:", font=("Arial", 12), 
                fg="white", bg="#1a3a5f").pack(side=tk.LEFT, padx=(0, 10))
        
        self.guess_var = tk.StringVar()
        guess_entry = tk.Entry(guess_frame, textvariable=self.guess_var, font=("Arial", 12), width=25)
        guess_entry.pack(side=tk.LEFT, padx=(0, 10))
        guess_entry.bind("<Return>", lambda e: self.submit_guess())
        
        submit_btn = tk.Button(guess_frame, text="Submit Guess", command=self.submit_guess,
                              font=("Arial", 12), bg="#2ecc71", fg="white")
        submit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Controls frame
        controls_frame = tk.Frame(content_frame, bg="#1a3a5f")
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.clue_btn = tk.Button(controls_frame, text="Reveal Next Clue", command=self.reveal_clue,
                                 font=("Arial", 12), bg="#3498db", fg="white", width=15)
        self.clue_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.skip_btn = tk.Button(controls_frame, text="Skip Player", command=self.skip_player,
                                 font=("Arial", 12), bg="#e74c3c", fg="white", width=15)
        self.skip_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.new_game_btn = tk.Button(controls_frame, text="New Game", command=self.start_new_game,
                                     font=("Arial", 12), bg="#f39c12", fg="white", width=15)
        self.new_game_btn.pack(side=tk.LEFT)
        
        # Status frame
        status_frame = tk.Frame(content_frame, bg="#1a3a5f")
        status_frame.pack(fill=tk.X)
        
        self.guesses_label = tk.Label(status_frame, text=f"Guesses left: {self.max_guesses}", 
                                     font=("Arial", 12), fg="white", bg="#1a3a5f")
        self.guesses_label.pack(side=tk.LEFT)
        
        self.clues_label = tk.Label(status_frame, text=f"Clues revealed: 0/{self.max_clues}", 
                                   font=("Arial", 12), fg="white", bg="#1a3a5f")
        self.clues_label.pack(side=tk.RIGHT)
        
        # Result frame (initially hidden)
        self.result_frame = tk.Frame(content_frame, bg="#2a4a6f", relief=tk.RAISED, bd=2)
        
        self.result_title = tk.Label(self.result_frame, text="", font=("Arial", 16, "bold"), 
                                    fg="white", bg="#2a4a6f")
        self.result_title.pack(pady=10)
        
        self.result_info = tk.Label(self.result_frame, text="", font=("Arial", 12), 
                                   fg="white", bg="#2a4a6f", justify=tk.LEFT)
        self.result_info.pack(pady=10, padx=20)
        
        # Player image placeholder
        self.player_image_label = tk.Label(self.result_frame, text="Player Image", 
                                          font=("Arial", 10), fg="white", bg="#2a4a6f",
                                          width=30, height=10, relief=tk.SUNKEN)
        self.player_image_label.pack(pady=10)
    
    def start_new_game(self):
        self.secret_player = random.choice(self.players)
        self.clues_revealed = 0
        self.guesses = 0
        self.game_active = True
        
        # Hide result frame
        self.result_frame.pack_forget()
        
        # Clear clues
        for label in self.clue_labels:
            label.config(text="")
        
        # Update UI
        self.update_ui()
        
        # Reveal first clue automatically
        self.reveal_clue()
    
    def update_ui(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.guesses_label.config(text=f"Guesses left: {self.max_guesses - self.guesses}")
        self.clues_label.config(text=f"Clues revealed: {self.clues_revealed}/{self.max_clues}")
        
        # Enable/disable buttons based on game state
        if self.clues_revealed >= self.max_clues:
            self.clue_btn.config(state=tk.DISABLED)
        else:
            self.clue_btn.config(state=tk.NORMAL)
    
    def reveal_clue(self):
        if not self.game_active or self.clues_revealed >= self.max_clues:
            return
        
        clue_text = ""
        if self.clues_revealed == 0:
            # First clue: Nationality and position
            clue_text = f"Nationality: {self.secret_player['nationality']}\nPosition: {self.secret_player['position']}"
        elif self.clues_revealed == 1:
            # Second clue: First club
            first_club = self.secret_player['career_path'][0]
            clue_text = f"Started career at: {first_club['club']} ({first_club['years']})"
        elif self.clues_revealed == 2:
            # Third clue: Current club
            current_club = self.secret_player['career_path'][-1]
            clue_text = f"Currently plays for: {current_club['club']} ({current_club['years']})"
        elif self.clues_revealed == 3:
            # Fourth clue: Career stats
            total_apps = sum(club['apps'] for club in self.secret_player['career_path'])
            total_goals = sum(club['goals'] for club in self.secret_player['career_path'])
            clue_text = f"Career stats: {total_apps} apps, {total_goals} goals"
        else:
            # Fifth clue: Another club in career
            if len(self.secret_player['career_path']) > 2:
                mid_club = self.secret_player['career_path'][1]
                clue_text = f"Also played for: {mid_club['club']} ({mid_club['years']})"
            else:
                # Fallback if player only has two clubs
                clue_text = f"Played for {len(self.secret_player['career_path'])} clubs in career"
        
        self.clue_labels[self.clues_revealed].config(text=clue_text)
        self.clues_revealed += 1
        self.update_ui()
    
    def submit_guess(self):
        if not self.game_active:
            return
        
        guess = self.guess_var.get().strip()
        if not guess:
            messagebox.showinfo("Input Error", "Please enter a player name.")
            return
        
        self.guesses += 1
        self.guess_var.set("")
        
        if guess.lower() == self.secret_player["name"].lower():
            # Correct guess
            self.score += (self.max_clues - self.clues_revealed + 1) * 100
            self.show_result(win=True)
        else:
            # Incorrect guess
            if self.guesses >= self.max_guesses:
                # Out of guesses
                self.show_result(win=False)
            else:
                messagebox.showinfo("Incorrect", f"Wrong guess! You have {self.max_guesses - self.guesses} guesses left.")
                self.update_ui()
    
    def skip_player(self):
        if not self.game_active:
            return
        
        self.show_result(win=False)
    
    def show_result(self, win):
        self.game_active = False
        
        # Show result frame
        self.result_frame.pack(fill=tk.X, pady=(20, 0))
        
        if win:
            self.result_title.config(text=f"Correct! It's {self.secret_player['name']}")
        else:
            self.result_title.config(text=f"Game Over! It was {self.secret_player['name']}")
        
        # Build career path text
        career_text = "Career Path:\n"
        for club in self.secret_player['career_path']:
            career_text += f"- {club['club']} ({club['years']}): {club['apps']} apps, {club['goals']} goals\n"
        
        # Add nationality and position
        career_text += f"\nNationality: {self.secret_player['nationality']}\n"
        career_text += f"Position: {self.secret_player['position']}"
        
        self.result_info.config(text=career_text)
        
        # Update score display
        self.update_ui()

if __name__ == "__main__":
    root = tk.Tk()
    game = CareerPathGuessingGame(root)
    root.mainloop()