import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import time

class StickmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Supreme Duelist Stickman")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Game variables
        self.game_mode = tk.StringVar(value="2 players")
        self.difficulty = tk.StringVar(value="Medium")
        
        # Weapons with special abilities
        self.weapons = {
            "Sword": {"damage": 15, "cooldown": 20, "special": "Whirlwind Attack", "color": "silver"},
            "Trident": {"damage": 20, "cooldown": 30, "special": "Water Wave", "color": "blue"},
            "Cards": {"damage": 10, "cooldown": 10, "special": "Card Throw", "color": "red"},
            "Axe": {"damage": 25, "cooldown": 40, "special": "Power Strike", "color": "brown"}
        }
        self.selected_weapon = tk.StringVar(value="Sword")
        
        # Player stats
        self.player1_health = 100
        self.player2_health = 100
        self.player1_score = 0
        self.player2_score = 0
        
        # Game state
        self.game_running = False
        self.ai_enemies = []
        
        # Create main menu
        self.create_main_menu()
        
    def create_main_menu(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Title
        title_label = ttk.Label(self.root, text="SUPREME DUELIST STICKMAN", 
                               font=("Arial", 24, "bold"), foreground="red")
        title_label.pack(pady=20)
        
        # Game mode selection
        mode_frame = ttk.LabelFrame(self.root, text="Game Mode", padding=10)
        mode_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Radiobutton(mode_frame, text="1 Player", variable=self.game_mode, 
                       value="1 player").pack(anchor="w", pady=5)
        ttk.Radiobutton(mode_frame, text="2 Players", variable=self.game_mode, 
                       value="2 players").pack(anchor="w", pady=5)
        ttk.Radiobutton(mode_frame, text="Survival", variable=self.game_mode, 
                       value="survival").pack(anchor="w", pady=5)
        
        # Difficulty selection
        difficulty_frame = ttk.LabelFrame(self.root, text="Difficulty", padding=10)
        difficulty_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Radiobutton(difficulty_frame, text="Easy", variable=self.difficulty, 
                       value="Easy").pack(anchor="w", pady=5)
        ttk.Radiobutton(difficulty_frame, text="Medium", variable=self.difficulty, 
                       value="Medium").pack(anchor="w", pady=5)
        ttk.Radiobutton(difficulty_frame, text="Hard", variable=self.difficulty, 
                       value="Hard").pack(anchor="w", pady=5)
        
        # Weapon selection
        weapon_frame = ttk.LabelFrame(self.root, text="Select Weapon", padding=10)
        weapon_frame.pack(pady=10, padx=20, fill="x")
        
        for weapon in self.weapons:
            ttk.Radiobutton(weapon_frame, text=f"{weapon} ({self.weapons[weapon]['special']})", 
                           variable=self.selected_weapon, value=weapon).pack(anchor="w", pady=5)
        
        # Start button
        start_button = ttk.Button(self.root, text="Start Game", command=self.start_game)
        start_button.pack(pady=20)
        
        # Instructions
        instructions = ttk.Label(self.root, text="Controls:\nPlayer 1 - A/D to move, W to jump, Space to attack\n" +
                                "Player 2 - Left/Right to move, Up to jump, Enter to attack\n" +
                                "Special Attack - Hold Shift + Attack key",
                                font=("Arial", 10), justify="left")
        instructions.pack(pady=10)
        
        # Score display
        score_frame = ttk.Frame(self.root)
        score_frame.pack(pady=10)
        
        ttk.Label(score_frame, text=f"Player 1 Wins: {self.player1_score}", font=("Arial", 12)).grid(row=0, column=0, padx=20)
        ttk.Label(score_frame, text=f"Player 2 Wins: {self.player2_score}", font=("Arial", 12)).grid(row=0, column=1, padx=20)
        
    def start_game(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create game canvas
        self.canvas = tk.Canvas(self.root, width=1000, height=600, bg="lightblue")
        self.canvas.pack(pady=10)
        
        # Draw ground
        self.canvas.create_rectangle(0, 500, 1000, 600, fill="green", outline="")
        
        # Draw platforms
        self.canvas.create_rectangle(200, 400, 400, 410, fill="brown", outline="")
        self.canvas.create_rectangle(600, 400, 800, 410, fill="brown", outline="")
        self.canvas.create_rectangle(400, 300, 600, 310, fill="brown", outline="")
        
        # Initialize players
        self.player1 = {
            "x": 200, "y": 450, "width": 30, "height": 50, 
            "color": "blue", "velocity_y": 0, "on_ground": True,
            "facing": "right", "health": 100, "weapon": self.selected_weapon.get(),
            "attacking": False, "attack_timer": 0, "special_charging": False
        }
        
        self.player2 = {
            "x": 800, "y": 450, "width": 30, "height": 50, 
            "color": "red", "velocity_y": 0, "on_ground": True,
            "facing": "left", "health": 100, "weapon": self.selected_weapon.get(),
            "attacking": False, "attack_timer": 0, "special_charging": False
        }
        
        # Draw players
        self.draw_player(self.player1)
        self.draw_player(self.player2)
        
        # Health bars
        self.player1_health_bar = self.canvas.create_rectangle(50, 30, 250, 50, fill="green", outline="black")
        self.player2_health_bar = self.canvas.create_rectangle(750, 30, 950, 50, fill="green", outline="black")
        
        self.canvas.create_text(150, 20, text="Player 1", font=("Arial", 14, "bold"))
        self.canvas.create_text(850, 20, text="Player 2", font=("Arial", 14, "bold"))
        
        # Weapon display
        self.weapon_text = self.canvas.create_text(500, 30, text=f"Weapon: {self.selected_weapon.get()}", 
                                                  font=("Arial", 14, "bold"))
        
        # Game mode specific setup
        if self.game_mode.get() == "survival":
            self.wave = 1
            self.enemies_defeated = 0
            self.spawn_enemies()
            
        # Control instructions
        self.canvas.create_text(500, 570, text="Player 1: A/D - Move, W - Jump, Space - Attack | Player 2: Left/Right - Move, Up - Jump, Enter - Attack", 
                               font=("Arial", 10))
        
        # Back button
        back_button = ttk.Button(self.root, text="Back to Menu", command=self.create_main_menu)
        back_button.pack(pady=10)
        
        # Bind keys
        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.root.focus_set()
        
        # Start game loop
        self.game_running = True
        self.game_loop()
        
    def draw_player(self, player):
        # Draw stick figure
        x, y = player["x"], player["y"]
        color = player["color"]
        
        # Body
        player["body"] = self.canvas.create_oval(x-15, y-25, x+15, y+25, fill=color, outline="black")
        
        # Head
        player["head"] = self.canvas.create_oval(x-10, y-45, x+10, y-25, fill="peachpuff", outline="black")
        
        # Arms
        arm_angle = 45 if player["facing"] == "right" else 135
        arm_length = 20
        
        arm_x = arm_length * math.cos(math.radians(arm_angle))
        arm_y = arm_length * math.sin(math.radians(arm_angle))
        
        player["arm1"] = self.canvas.create_line(x, y-15, x+arm_x, y-15-arm_y, width=3, fill="black")
        player["arm2"] = self.canvas.create_line(x, y-15, x-arm_x, y-15-arm_y, width=3, fill="black")
        
        # Legs
        leg_angle = 30 if player["facing"] == "right" else 150
        leg_length = 25
        
        leg_x = leg_length * math.cos(math.radians(leg_angle))
        leg_y = leg_length * math.sin(math.radians(leg_angle))
        
        player["leg1"] = self.canvas.create_line(x, y+25, x+leg_x, y+25+leg_y, width=3, fill="black")
        player["leg2"] = self.canvas.create_line(x, y+25, x-leg_x, y+25+leg_y, width=3, fill="black")
        
        # Weapon
        weapon_x = x + (30 if player["facing"] == "right" else -30)
        weapon_color = self.weapons[player["weapon"]]["color"]
        
        if player["weapon"] == "Sword":
            player["weapon_img"] = self.canvas.create_line(x, y-15, weapon_x, y-15, width=3, fill=weapon_color)
            player["weapon_tip"] = self.canvas.create_oval(weapon_x-5, y-20, weapon_x+5, y-10, fill=weapon_color, outline="")
        elif player["weapon"] == "Trident":
            player["weapon_img"] = self.canvas.create_line(x, y-15, weapon_x, y-15, width=3, fill=weapon_color)
            # Draw trident tips
            for i in range(-1, 2):
                self.canvas.create_line(weapon_x, y-15, weapon_x+10, y-20+i*5, width=2, fill=weapon_color)
        elif player["weapon"] == "Cards":
            player["weapon_img"] = self.canvas.create_rectangle(x, y-20, weapon_x, y-10, fill=weapon_color, outline="black")
        elif player["weapon"] == "Axe":
            player["weapon_img"] = self.canvas.create_line(x, y-15, weapon_x, y-15, width=3, fill=weapon_color)
            # Draw axe head
            self.canvas.create_polygon(weapon_x, y-15, weapon_x+10, y-25, weapon_x+15, y-15, fill=weapon_color, outline="black")
            
    def update_player(self, player):
        # Update player position and appearance
        x, y = player["x"], player["y"]
        color = player["color"]
        
        # Update body
        self.canvas.coords(player["body"], x-15, y-25, x+15, y+25)
        
        # Update head
        self.canvas.coords(player["head"], x-10, y-45, x+10, y-25)
        
        # Update arms
        arm_angle = 45 if player["facing"] == "right" else 135
        if player["attacking"]:
            arm_angle = 10 if player["facing"] == "right" else 170
            
        arm_length = 20
        
        arm_x = arm_length * math.cos(math.radians(arm_angle))
        arm_y = arm_length * math.sin(math.radians(arm_angle))
        
        self.canvas.coords(player["arm1"], x, y-15, x+arm_x, y-15-arm_y)
        self.canvas.coords(player["arm2"], x, y-15, x-arm_x, y-15-arm_y)
        
        # Update legs
        leg_angle = 30 if player["facing"] == "right" else 150
        leg_length = 25
        
        leg_x = leg_length * math.cos(math.radians(leg_angle))
        leg_y = leg_length * math.sin(math.radians(leg_angle))
        
        self.canvas.coords(player["leg1"], x, y+25, x+leg_x, y+25+leg_y)
        self.canvas.coords(player["leg2"], x, y+25, x-leg_x, y+25+leg_y)
        
        # Update weapon
        weapon_x = x + (30 if player["facing"] == "right" else -30)
        weapon_color = self.weapons[player["weapon"]]["color"]
        
        if player["weapon"] == "Sword":
            self.canvas.coords(player["weapon_img"], x, y-15, weapon_x, y-15)
            self.canvas.coords(player["weapon_tip"], weapon_x-5, y-20, weapon_x+5, y-10)
        elif player["weapon"] == "Trident":
            self.canvas.coords(player["weapon_img"], x, y-15, weapon_x, y-15)
            # TODO: Update trident tips
        elif player["weapon"] == "Cards":
            self.canvas.coords(player["weapon_img"], x, y-20, weapon_x, y-10)
        elif player["weapon"] == "Axe":
            self.canvas.coords(player["weapon_img"], x, y-15, weapon_x, y-15)
            # TODO: Update axe head
            
    def key_down(self, event):
        # Player 1 controls
        if event.keysym == "a":
            self.player1["x"] -= 10
            self.player1["facing"] = "left"
        elif event.keysym == "d":
            self.player1["x"] += 10
            self.player1["facing"] = "right"
        elif event.keysym == "w" and self.player1["on_ground"]:
            self.player1["velocity_y"] = -15
            self.player1["on_ground"] = False
        elif event.keysym == "space":
            self.player1["attacking"] = True
            self.player1["attack_timer"] = 10
            self.attack(self.player1, self.player2)
            
        # Player 2 controls
        if event.keysym == "Left":
            self.player2["x"] -= 10
            self.player2["facing"] = "right"
        elif event.keysym == "Right":
            self.player2["x"] += 10
            self.player2["facing"] = "left"
        elif event.keysym == "Up" and self.player2["on_ground"]:
            self.player2["velocity_y"] = -15
            self.player2["on_ground"] = False
        elif event.keysym == "Return":
            self.player2["attacking"] = True
            self.player2["attack_timer"] = 10
            self.attack(self.player2, self.player1)
            
        # Special attacks
        if event.keysym == "Shift_L":
            self.player1["special_charging"] = True
        elif event.keysym == "Shift_R":
            self.player2["special_charging"] = True
            
        # Boundary checking
        self.player1["x"] = max(15, min(985, self.player1["x"]))
        self.player2["x"] = max(15, min(985, self.player2["x"]))
        
        # Update player positions
        self.update_player(self.player1)
        self.update_player(self.player2)
        
    def key_up(self, event):
        if event.keysym == "space":
            self.player1["attacking"] = False
        elif event.keysym == "Return":
            self.player2["attacking"] = False
        elif event.keysym == "Shift_L":
            self.player1["special_charging"] = False
            if self.player1["attacking"]:
                self.special_attack(self.player1, self.player2)
        elif event.keysym == "Shift_R":
            self.player2["special_charging"] = False
            if self.player2["attacking"]:
                self.special_attack(self.player2, self.player1)
                
    def attack(self, attacker, defender):
        # Check if attack hits
        attack_range = 50
        direction = 1 if attacker["facing"] == "right" else -1
        
        if (abs(defender["x"] - attacker["x"]) < attack_range and 
            abs(defender["y"] - attacker["y"]) < 50):
            # Apply damage
            damage = self.weapons[attacker["weapon"]]["damage"]
            if attacker["special_charging"]:
                damage *= 1.5
                
            defender["health"] -= damage
            
            # Update health bar
            if defender == self.player1:
                self.canvas.coords(self.player1_health_bar, 50, 30, 50 + 2 * defender["health"], 50)
            else:
                self.canvas.coords(self.player2_health_bar, 750, 30, 750 + 2 * defender["health"], 50)
                
            # Check for knockout
            if defender["health"] <= 0:
                self.ko(attacker, defender)
                
    def special_attack(self, attacker, defender):
        # Perform special attack based on weapon
        weapon = attacker["weapon"]
        
        if weapon == "Sword":
            # Whirlwind attack - hits multiple times
            for _ in range(3):
                self.attack(attacker, defender)
        elif weapon == "Trident":
            # Water wave - pushes opponent back
            if abs(defender["x"] - attacker["x"]) < 70:
                direction = 1 if attacker["facing"] == "right" else -1
                defender["x"] += 50 * direction
                self.attack(attacker, defender)
        elif weapon == "Cards":
            # Card throw - ranged attack
            if abs(defender["x"] - attacker["x"]) < 150:
                self.attack(attacker, defender)
        elif weapon == "Axe":
            # Power strike - high damage
            self.attack(attacker, defender)
            self.attack(attacker, defender)  # Double damage
            
    def ko(self, attacker, defender):
        # Handle knockout
        if self.game_mode.get() == "2 players" or self.game_mode.get() == "1 player":
            if attacker == self.player1:
                self.player1_score += 1
            else:
                self.player2_score += 1
                
            messagebox.showinfo("Knockout!", f"{'Player 1' if attacker == self.player1 else 'Player 2'} wins!")
            self.create_main_menu()
        elif self.game_mode.get() == "survival":
            if defender != self.player1:
                self.enemies_defeated += 1
                if self.enemies_defeated >= self.wave * 3:
                    self.wave += 1
                    self.enemies_defeated = 0
                    messagebox.showinfo("Wave Complete", f"Wave {self.wave-1} complete! Starting wave {self.wave}")
                    self.spawn_enemies()
            else:
                messagebox.showinfo("Game Over", f"You survived {self.wave-1} waves!")
                self.create_main_menu()
                
    def spawn_enemies(self):
        # Spawn enemies for survival mode
        self.ai_enemies = []
        for i in range(self.wave * 3):
            enemy = {
                "x": random.randint(100, 900), "y": 450, "width": 30, "height": 50, 
                "color": "purple", "velocity_y": 0, "on_ground": True,
                "facing": "left", "health": 50, "weapon": random.choice(list(self.weapons.keys())),
                "attacking": False, "attack_timer": 0, "ai_timer": random.randint(10, 50)
            }
            self.ai_enemies.append(enemy)
            self.draw_player(enemy)
            
    def update_ai(self):
        # Update AI enemies for survival mode
        for enemy in self.ai_enemies:
            enemy["ai_timer"] -= 1
            
            if enemy["ai_timer"] <= 0:
                # Move toward player
                if enemy["x"] < self.player1["x"]:
                    enemy["x"] += 5
                    enemy["facing"] = "right"
                else:
                    enemy["x"] -= 5
                    enemy["facing"] = "left"
                    
                # Jump occasionally
                if random.random() < 0.1 and enemy["on_ground"]:
                    enemy["velocity_y"] = -15
                    enemy["on_ground"] = False
                    
                # Attack if close
                if abs(enemy["x"] - self.player1["x"]) < 60:
                    enemy["attacking"] = True
                    enemy["attack_timer"] = 10
                    self.attack(enemy, self.player1)
                    
                enemy["ai_timer"] = random.randint(10, 50)
                
            # Update enemy position
            self.update_player(enemy)
            
    def game_loop(self):
        if not self.game_running:
            return
            
        # Apply gravity
        for player in [self.player1, self.player2] + self.ai_enemies:
            player["velocity_y"] += 0.5
            player["y"] += player["velocity_y"]
            
            # Ground collision
            if player["y"] >= 450:
                player["y"] = 450
                player["velocity_y"] = 0
                player["on_ground"] = True
                
            # Platform collision
            for platform in [(200, 400, 400, 410), (600, 400, 800, 410), (400, 300, 600, 310)]:
                x1, y1, x2, y2 = platform
                if (player["x"] > x1 and player["x"] < x2 and 
                    player["y"] + 25 > y1 and player["y"] + 25 < y2 and player["velocity_y"] > 0):
                    player["y"] = y1 - 25
                    player["velocity_y"] = 0
                    player["on_ground"] = True
                    
        # Update attack timers
        if self.player1["attack_timer"] > 0:
            self.player1["attack_timer"] -= 1
        else:
            self.player1["attacking"] = False
            
        if self.player2["attack_timer"] > 0:
            self.player2["attack_timer"] -= 1
        else:
            self.player2["attacking"] = False
            
        # Update AI in survival mode
        if self.game_mode.get() == "survival":
            self.update_ai()
            
        # Update players
        self.update_player(self.player1)
        self.update_player(self.player2)
        
        # Schedule next update
        self.root.after(16, self.game_loop)  # ~60 FPS

# Create the main window
root = tk.Tk()
game = StickmanGame(root)
root.mainloop()