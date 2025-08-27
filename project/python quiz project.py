import tkinter as tk
from tkinter import messagebox, font
import random
from PIL import Image, ImageTk

class MillionaireQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Isaac's Millionaire Quiz")
        self.root.geometry("1400x700")
        self.root.configure(bg="#2a0a1a")
        
        # Initialize game variables
        self.level = 1
        self.question_count = 0
        self.points = 0
        self.base_point_value = 50000  # Starting at ₦50,000
        self.current_point_value = self.base_point_value
        self.questions = self.load_questions()
        self.used_questions = set()
        self.current_question = None
        self.points_history = []
        
        # Hint usage tracking
        self.call_friend_used = 0
        self.ask_audience_used = 0
        self.fifty_fifty_used = 0
        self.max_hint_uses = 2
        
        # Create UI
        self.create_widgets()
        self.load_question()
        
    def create_widgets(self):
        # Main container frame
        main_frame = tk.Frame(self.root, bg="#0a0a2a")
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left side - Placeholder image
        left_image_frame = tk.Frame(main_frame, bg="#0a0a2a", width=300)
        left_image_frame.pack(side='left', fill='y', padx=(0, 20))
        left_image_frame.pack_propagate(False)
        
         # Left side - Placeholder image
        left_image_frame = tk.Frame(main_frame, bg="#0a0a2a", width=310)
        left_image_frame.pack(side='left', fill='y', padx=(0, 21))
        left_image_frame.pack_propagate(False)
        
        # Load your image file instead of creating a placeholder
        try:
            # REPLACE "path/to/your/image.jpg" WITH "millionaire background.jfif"
            your_image = Image.open("millionaire background.jfif")
            your_image = your_image.resize((500, 250), Image.LANCZOS)  # Resize if needed
            self.placeholder_photo = ImageTk.PhotoImage(your_image)
        except:
            # Fallback to placeholder if image loading fails
            placeholder_img = Image.new('RGB', (250, 250), color='#1a1a3a')
            self.placeholder_photo = ImageTk.PhotoImage(placeholder_img)
        
        placeholder_label = tk.Label(left_image_frame, image=self.placeholder_photo, bg="#0a0a2a")
        placeholder_label.pack(pady=20)
        
        # Add text to placeholder (optional - you can remove this if you want)
        placeholder_text = tk.Label(left_image_frame, text="", 
                                   font=("Arial", 16, "bold"), fg="white", bg="#0a0a2a")
        placeholder_text.pack(pady=10)
        
        # Center - Game content
        center_frame = tk.Frame(main_frame, bg="#0a0a2a")
        center_frame.pack(side='left', fill='both', expand=True)
        
        # Right side - Points history
        right_frame = tk.Frame(main_frame, bg="#0a0a2a", width=300)
        right_frame.pack(side='right', fill='y', padx=(20, 0))
        right_frame.pack_propagate(False)
        
        # Title
        title_font = font.Font(family="Arial", size=24, weight="bold")
        title_label = tk.Label(center_frame, text="Isaac's Millionaire Quiz", font=title_font, 
                              fg="white", bg="#0a0a2a")
        title_label.pack(pady=20)
        
        # Points and level display
        info_font = font.Font(family="Arial", size=14)
        self.points_label = tk.Label(center_frame, text=f"Total Prize: ₦{self.points:,}", font=info_font, 
                                    fg="gold", bg="#0a0a2a")
        self.points_label.pack(pady=5)
        
        self.value_label = tk.Label(center_frame, text=f"Current Question Value: ₦{self.current_point_value:,}", 
                                   font=info_font, fg="cyan", bg="#0a0a2a")
        self.value_label.pack(pady=5)
        
        self.level_label = tk.Label(center_frame, text=f"Level: {self.level}/50", font=info_font, 
                                   fg="white", bg="#0a0a2a")
        self.level_label.pack(pady=5)
        
        # Question frame
        self.question_frame = tk.Frame(center_frame, bg="#0a0a2a", height=150)
        self.question_frame.pack(pady=20, fill='x')
        
        question_font = font.Font(family="Arial", size=16)
        self.question_label = tk.Label(self.question_frame, text="", font=question_font, 
                                      fg="white", bg="#0a0a2a", wraplength=600, justify='center')
        self.question_label.pack(pady=20)
        
        # Hint buttons frame
        self.hint_frame = tk.Frame(self.question_frame, bg="#0a0a2a")
        self.hint_frame.pack(pady=10)
        
        # First hint button - Call a Friend
        self.call_friend_button = tk.Button(self.hint_frame, text="📞", font=("Arial", 16), 
                                          command=self.call_friend, bg="#0a0a2a", fg="#FFD700", 
                                          border=1, relief='solid', width=3)
        self.call_friend_button.pack(side='left', padx=5)
        self.call_friend_label = tk.Label(self.hint_frame, text=f"{self.max_hint_uses - self.call_friend_used}", 
                                       font=("Arial", 10), fg="white", bg="#0a0a2a")
        self.call_friend_label.pack(side='left', padx=(0, 10))
        
        # Second hint button - Ask the Audience
        self.ask_audience_button = tk.Button(self.hint_frame, text="👥", font=("Arial", 16), 
                                           command=self.ask_audience, bg="#0a0a2a", fg="#FFD700", 
                                           border=1, relief='solid', width=3)
        self.ask_audience_button.pack(side='left', padx=5)
        self.ask_audience_label = tk.Label(self.hint_frame, text=f"{self.max_hint_uses - self.ask_audience_used}", 
                                        font=("Arial", 10), fg="white", bg="#0a0a2a")
        self.ask_audience_label.pack(side='left', padx=(0, 10))
        
        # Third hint button - 50/50
        self.fifty_fifty_button = tk.Button(self.hint_frame, text="½", font=("Arial", 16), 
                                          command=self.fifty_fifty, bg="#0a0a2a", fg="#FFD700", 
                                          border=1, relief='solid', width=3)
        self.fifty_fifty_button.pack(side='left', padx=5)
        self.fifty_fifty_label = tk.Label(self.hint_frame, text=f"{self.max_hint_uses - self.fifty_fifty_used}", 
                                       font=("Arial", 10), fg="white", bg="#0a0a2a")
        self.fifty_fifty_label.pack(side='left', padx=(0, 10))
        
        # Options frame
        self.options_frame = tk.Frame(center_frame, bg="#0a0a2a")
        self.options_frame.pack(pady=20)
        
        self.option_buttons = []
        option_font = font.Font(family="Arial", size=14)
        for i in range(4):
            btn = tk.Button(self.options_frame, text="", font=option_font, 
                           width=25, height=2, command=lambda i=i: self.check_answer(i),
                           bg="#1a1a3a", fg="white", activebackground="#2a2a5a",
                           relief='raised', borderwidth=2)
            btn.grid(row=i//2, column=i%2, padx=15, pady=15)
            self.option_buttons.append(btn)
            
        # Points history section
        history_title_font = font.Font(family="Arial", size=16, weight="bold")
        history_title = tk.Label(right_frame, text="Points History", font=history_title_font,
                                fg="white", bg="#0a0a2a")
        history_title.pack(pady=(20, 10))
        
        # Create a canvas with scrollbar for the points history
        history_canvas = tk.Canvas(right_frame, bg="#0a0a2a", highlightthickness=0)
        scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=history_canvas.yview)
        self.history_scrollable_frame = tk.Frame(history_canvas, bg="#0a0a2a")
        
        self.history_scrollable_frame.bind(
            "<Configure>",
            lambda e: history_canvas.configure(scrollregion=history_canvas.bbox("all"))
        )
        
        history_canvas.create_window((0, 0), window=self.history_scrollable_frame, anchor="nw")
        history_canvas.configure(yscrollcommand=scrollbar.set)
        
        history_canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        scrollbar.pack(side="right", fill="y")
        
        # Store reference to update later
        self.history_canvas = history_canvas
        self.history_frame = self.history_scrollable_frame
    
    def update_point_value(self):
        # Increase point value by ₦50,000 after every 2 questions
        if self.question_count > 0 and self.question_count % 2 == 0:
            self.base_point_value += 50000
        
        # Set current point value
        self.current_point_value = self.base_point_value
            
        self.value_label.config(text=f"Current Question Value: ₦{self.current_point_value:,}")
    
    def update_points_history(self):
        # Clear previous history
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # Add earned points
        for i, points in enumerate(self.points_history):
            row_frame = tk.Frame(self.history_frame, bg="#0a0a2a")
            row_frame.pack(fill='x', pady=2)
            
            question_label = tk.Label(row_frame, text=f"Q{i+1}:", font=("Arial", 10), 
                                     fg="white", bg="#0a0a2a", width=5, anchor='w')
            question_label.pack(side='left')
            
            points_label = tk.Label(row_frame, text=f"₦{points:,}", font=("Arial", 10, "bold"), 
                                  fg="green", bg="#0a0a2a", width=10, anchor='w')
            points_label.pack(side='left')
        
        # Add separator if there are earned points
        if self.points_history:
            separator = tk.Frame(self.history_frame, height=2, bg="#333355")
            separator.pack(fill='x', pady=5)
        
        # Add upcoming points (next 5 questions)
        upcoming_value = self.current_point_value
        for i in range(5):
            row_frame = tk.Frame(self.history_frame, bg="#0a0a2a")
            row_frame.pack(fill='x', pady=2)
            
            question_num = len(self.points_history) + i + 1
            question_label = tk.Label(row_frame, text=f"Q{question_num}:", font=("Arial", 10), 
                                     fg="white", bg="#0a0a2a", width=5, anchor='w')
            question_label.pack(side='left')
            
            # Calculate potential value for this question
            if i > 0 and (len(self.points_history) + i) % 2 == 0:
                upcoming_value += 50000
            
            points_label = tk.Label(row_frame, text=f"₦{upcoming_value:,}", font=("Arial", 10), 
                                  fg="cyan", bg="#0a0a2a", width=10, anchor='w')
            points_label.pack(side='left')
        
        # Update scroll region
        self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))
    
    def call_friend(self):
        if self.call_friend_used >= self.max_hint_uses:
            messagebox.showinfo("Hint Used", "You've already used all your Call a Friend hints!")
            return
            
        self.call_friend_used += 1
        self.call_friend_label.config(text=f"{self.max_hint_uses - self.call_friend_used}")
        
        # Friend gives a random answer (could be right or wrong)
        options = self.current_question["options"]
        friend_answer = random.choice(options)
        
        # Friend is more likely to be correct (60% chance)
        if random.random() < 0.6:
            correct_idx = self.current_question["correct"]
            friend_answer = options[correct_idx]
        
        messagebox.showinfo("Call a Friend", f"Your friend says: 'I think the answer is {friend_answer}'")
    
    def ask_audience(self):
        if self.ask_audience_used >= self.max_hint_uses:
            messagebox.showinfo("Hint Used", "You've already used all your Ask the Audience hints!")
            return
            
        self.ask_audience_used += 1
        self.ask_audience_label.config(text=f"{self.max_hint_uses - self.ask_audience_used}")
        
        # Generate audience poll percentages
        options = self.current_question["options"]
        correct_idx = self.current_question["correct"]
        
        # Audience is more likely to be correct
        percentages = [random.randint(5, 30) for _ in range(4)]
        percentages[correct_idx] += random.randint(20, 40)
        
        # Normalize to 100%
        total = sum(percentages)
        percentages = [int(p * 100 / total) for p in percentages]
        
        # Create audience poll message
        poll_message = "Audience Poll Results:\n"
        for i, option in enumerate(options):
            poll_message += f"{option}: {percentages[i]}%\n"
            
        messagebox.showinfo("Ask the Audience", poll_message)
    
    def fifty_fifty(self):
        if self.fifty_fifty_used >= self.max_hint_uses:
            messagebox.showinfo("Hint Used", "You've already used all your 50/50 hints!")
            return
            
        self.fifty_fifty_used += 1
        self.fifty_fifty_label.config(text=f"{self.max_hint_uses - self.fifty_fifty_used}")
        
        # Get correct answer index
        correct_idx = self.current_question["correct"]
        
        # Get incorrect options to remove
        incorrect_indices = [i for i in range(4) if i != correct_idx]
        to_remove = random.sample(incorrect_indices, 2)
        
        # Disable the removed options
        for idx in to_remove:
            self.option_buttons[idx].config(state="disabled", bg="#555577")
        
        messagebox.showinfo("50/50", "Two incorrect answers have been removed!")
    
    def load_questions(self):
        # 50 different questions
        questions = [
            {
                "question": "Which country made the first car?",
                "options": ["America", "Germany", "France", "Italy"],
                "correct": 1,
                "hint": "This European country is known for its engineering and automotive industry."
            },
            {
                "question": "What is the capital of Australia?",
                "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
                "correct": 2,
                "hint": "It's not the largest city, but it was specifically designed to be the capital."
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct": 1,
                "hint": "It's the fourth planet from the Sun in our solar system."
            },
            {
                "question": "Who painted the Mona Lisa?",
                "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
                "correct": 2,
                "hint": "This Italian Renaissance artist was also a scientist and inventor."
            },
            {
                "question": "What is the largest ocean on Earth?",
                "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
                "correct": 3,
                "hint": "It covers about one-third of the Earth's surface."
            },
            {
                "question": "Which element has the chemical symbol 'O'?",
                "options": ["Gold", "Oxygen", "Osmium", "Oganesson"],
                "correct": 1,
                "hint": "This element is essential for human respiration."
            },
            {
                "question": "In which year did World War II end?",
                "options": ["1943", "1945", "1947", "1950"],
                "correct": 1,
                "hint": "The war ended with the surrender of Japan in this year."
            },
            {
                "question": "What is the largest mammal in the world?",
                "options": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
                "correct": 1,
                "hint": "This marine mammal is also the largest animal known to have ever existed."
            },
            {
                "question": "Which language is spoken in Brazil?",
                "options": ["Spanish", "Portuguese", "French", "English"],
                "correct": 1,
                "hint": "This European language was brought to the country by colonizers."
            },
            {
                "question": "Who wrote 'Romeo and Juliet'?",
                "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                "correct": 1,
                "hint": "This English playwright is often called England's national poet."
            },
            {
                "question": "What is the currency of Japan?",
                "options": ["Yuan", "Won", "Yen", "Ringgit"],
                "correct": 2,
                "hint": "This currency's symbol is ¥."
            },
            {
                "question": "Which gas do plants absorb from the atmosphere?",
                "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
                "correct": 2,
                "hint": "Plants use this gas during photosynthesis to produce food."
            },
            {
                "question": "How many sides does a hexagon have?",
                "options": ["5", "6", "7", "8"],
                "correct": 1,
                "hint": "The prefix 'hexa-' means six."
            },
            {
                "question": "Who was the first woman to win a Nobel Prize?",
                "options": ["Marie Curie", "Rosalind Franklin", "Dorothy Crowfoot Hodgkin", "Maria Goeppert-Mayer"],
                "correct": 0,
                "hint": "She won the prize in Physics in 1903 and later in Chemistry."
            },
            {
                "question": "What is the main ingredient in guacamole?",
                "options": ["Banana", "Avocado", "Cucumber", "Peas"],
                "correct": 1,
                "hint": "This fruit has a large pit and creamy green flesh."
            },
            {
                "question": "Which planet is closest to the Sun?",
                "options": ["Venus", "Earth", "Mercury", "Mars"],
                "correct": 2,
                "hint": "It's the smallest planet in our solar system."
            },
            {
                "question": "In what city is the Eiffel Tower located?",
                "options": ["London", "Rome", "Paris", "Berlin"],
                "correct": 2,
                "hint": "This city is known as the 'City of Light'."
            },
            {
                "question": "What is the hardest natural substance on Earth?",
                "options": ["Gold", "Iron", "Diamond", "Platinum"],
                "correct": 2,
                "hint": "This substance is a form of carbon and is used in jewelry."
            },
            {
                "question": "Which animal is known as the 'Ship of the Desert'?",
                "options": ["Horse", "Camel", "Elephant", "Donkey"],
                "correct": 1,
                "hint": "This animal can survive long periods without water in arid environments."
            },
            {
                "question": "Who discovered penicillin?",
                "options": ["Marie Curie", "Alexander Fleming", "Louis Pasteur", "Robert Koch"],
                "correct": 1,
                "hint": "This Scottish scientist discovered the antibiotic in 1928."
            },
            {
                "question": "What is the largest organ in the human body?",
                "options": ["Liver", "Heart", "Skin", "Lungs"],
                "correct": 2,
                "hint": "It protects our internal organs from the external environment."
            },
            {
                "question": "Which country is known as the Land of the Rising Sun?",
                "options": ["China", "Thailand", "Japan", "South Korea"],
                "correct": 2,
                "hint": "This island nation has a flag with a red circle on a white background."
            },
            {
                "question": "How many elements are in the periodic table?",
                "options": ["108", "118", "128", "138"],
                "correct": 1,
                "hint": "As of 2023, this number represents all known elements."
            },
            {
                "question": "What is the smallest bone in the human body?",
                "options": ["Stapes", "Femur", "Radius", "Tibia"],
                "correct": 0,
                "hint": "This bone is located in the middle ear."
            },
            {
                "question": "Which planet has the most moons?",
                "options": ["Jupiter", "Saturn", "Uranus", "Neptune"],
                "correct": 1,
                "hint": "This planet is known for its spectacular ring system."
            },
            {
                "question": "What is the chemical formula for water?",
                "options": ["HO", "H2O", "H2O2", "H3O"],
                "correct": 1,
                "hint": "It consists of two hydrogen atoms and one oxygen atom."
            },
            {
                "question": "Who was the first President of the United States?",
                "options": ["Thomas Jefferson", "George Washington", "John Adams", "Abraham Lincoln"],
                "correct": 1,
                "hint": "His image appears on the one-dollar bill and the quarter."
            },
            {
                "question": "Which ocean is the smallest?",
                "options": ["Atlantic", "Indian", "Arctic", "Southern"],
                "correct": 2,
                "hint": "This ocean is located around the North Pole."
            },
            {
                "question": "What is the capital of Canada?",
                "options": ["Toronto", "Vancouver", "Ottawa", "Montreal"],
                "correct": 2,
                "hint": "This city is located in the province of Ontario."
            },
            {
                "question": "Which animal can be seen on the Porsche logo?",
                "options": ["Lion", "Eagle", "Horse", "Bull"],
                "correct": 2,
                "hint": "This animal is known for its speed and grace."
            },
            {
                "question": "What is the main component of the Sun?",
                "options": ["Helium", "Hydrogen", "Oxygen", "Carbon"],
                "correct": 1,
                "hint": "This element is the lightest and most abundant in the universe."
            },
            {
                "question": "How many time zones does Russia have?",
                "options": ["5", "7", "9", "11"],
                "correct": 3,
                "hint": "It's the country with the most time zones in the world."
            },
            {
                "question": "Which fruit is known as the 'king of fruits'?",
                "options": ["Mango", "Durian", "Pineapple", "Banana"],
                "correct": 1,
                "hint": "This fruit has a strong odor and a thorn-covered rind."
            },
            {
                "question": "What is the largest desert in the world?",
                "options": ["Gobi", "Sahara", "Arabian", "Antarctic"],
                "correct": 3,
                "hint": "This desert is located at the South Pole."
            },
            {
                "question": "Which blood type is known as the universal donor?",
                "options": ["A+", "B-", "AB+", "O-"],
                "correct": 3,
                "hint": "This blood type can be donated to anyone regardless of their blood type."
            },
            {
                "question": "What is the tallest mountain in the world?",
                "options": ["K2", "Mount Everest", "Kangchenjunga", "Lhotse"],
                "correct": 1,
                "hint": "This mountain is located in the Himalayas on the border between Nepal and China."
            },
            {
                "question": "Which planet is known for its prominent rings?",
                "options": ["Jupiter", "Saturn", "Uranus", "Neptune"],
                "correct": 1,
                "hint": "This planet is the second largest in our solar system."
            },
            {
                "question": "What is the largest bird in the world?",
                "options": ["Eagle", "Albatross", "Ostrich", "Emu"],
                "correct": 2,
                "hint": "This bird cannot fly but can run very fast."
            },
            {
                "question": "Which language has the most native speakers?",
                "options": ["English", "Spanish", "Hindi", "Mandarin Chinese"],
                "correct": 3,
                "hint": "This language is primarily spoken in China."
            },
            {
                "question": "What is the largest type of big cat?",
                "options": ["Lion", "Tiger", "Jaguar", "Leopard"],
                "correct": 1,
                "hint": "This striped cat is the national animal of several Asian countries."
            },
            {
                "question": "Which element is liquid at room temperature?",
                "options": ["Bromine", "Chlorine", "Iodine", "Fluorine"],
                "correct": 0,
                "hint": "This element has a reddish-brown color and a strong odor."
            },
            {
                "question": "What is the capital of Egypt?",
                "options": ["Alexandria", "Giza", "Cairo", "Luxor"],
                "correct": 2,
                "hint": "This city is located near the Nile Delta."
            },
            {
                "question": "How many hearts does an octopus have?",
                "options": ["1", "2", "3", "4"],
                "correct": 2,
                "hint": "This sea creature has blue blood and three hearts."
            },
            {
                "question": "Which planet is the hottest in our solar system?",
                "options": ["Mercury", "Venus", "Mars", "Jupiter"],
                "correct": 1,
                "hint": "This planet has a thick atmosphere that traps heat."
            },
            {
                "question": "What is the largest species of shark?",
                "options": ["Great White Shark", "Tiger Shark", "Whale Shark", "Hammerhead Shark"],
                "correct": 2,
                "hint": "This shark is a filter feeder and the largest fish in the world."
            },
            {
                "question": "Which country invented tea?",
                "options": ["India", "Japan", "China", "England"],
                "correct": 2,
                "hint": "This country has a long history of tea cultivation and consumption."
            },
            {
                "question": "What is the smallest country in the world?",
                "options": ["Monaco", "Vatican City", "San Marino", "Liechtenstein"],
                "correct": 1,
                "hint": "This country is located entirely within the city of Rome."
            },
            {
                "question": "Which animal has the longest lifespan?",
                "options": ["Galapagos Tortoise", "Bowhead Whale", "Greenland Shark", "African Elephant"],
                "correct": 2,
                "hint": "This deep-sea shark can live for over 400 years."
            },
            {
                "question": "What is the most abundant gas in Earth's atmosphere?",
                "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Argon"],
                "correct": 2,
                "hint": "This gas makes up about 78% of the air we breathe."
            },
            {
                "question": "Which planet has the most volcanic activity?",
                "options": ["Earth", "Mars", "Venus", "Io (moon of Jupiter)"],
                "correct": 3,
                "hint": "This celestial body is not a planet but a moon with hundreds of active volcanoes."
            },
            {
                "question": "What is the largest internal organ in the human body?",
                "options": ["Brain", "Liver", "Heart", "Lungs"],
                "correct": 1,
                "hint": "This organ detoxifies chemicals and metabolizes drugs."
            }
        ]
        
        return questions
    
    def get_unused_question(self):
        # Get a question that hasn't been used yet
        available_questions = [q for i, q in enumerate(self.questions) if i not in self.used_questions]
        
        if not available_questions:
            # If all questions have been used, reset the used questions set
            self.used_questions = set()
            available_questions = self.questions
        
        # Select a random question from available ones
        question = random.choice(available_questions)
        question_index = self.questions.index(question)
        self.used_questions.add(question_index)
        
        return question
    
    def load_question(self):
        # Get an unused question
        self.current_question = self.get_unused_question()
        
        # Update UI
        self.question_label.config(text=self.current_question["question"])
        
        # Update option buttons
        options = self.current_question["options"]
        for i, btn in enumerate(self.option_buttons):
            btn.config(text=options[i], state="normal", bg="#1a353a")
            
        # Update point value for this question
        self.update_point_value()
        
        # Update points history display
        self.update_points_history()
    
    def check_answer(self, selected_index):
        if selected_index == self.current_question["correct"]:
            # Add points for correct answer
            earned_points = self.current_point_value
            self.points += earned_points
            self.points_history.append(earned_points)
            self.points_label.config(text=f"Total Prize: ₦{self.points:,}")
            
            # Increase question count
            self.question_count += 1
            
            if self.level < 50:
                self.level += 1
                self.level_label.config(text=f"Level: {self.level}/50")
                self.load_question()
            else:
                messagebox.showinfo("Congratulations!", 
                                  f"You've completed all levels with ₦{self.points:,}!")
                self.root.destroy()
        else:
            correct_answer = self.current_question["options"][self.current_question["correct"]]
            messagebox.showerror("Wrong Answer", 
                               f"That's incorrect! The correct answer was: {correct_answer}\n"
                               f"You leave with ₦{self.points:,}!")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MillionaireQuiz(root)
    root.mainloop()