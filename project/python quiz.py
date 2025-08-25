import tkinter as tk
from tkinter import messagebox, font
import random

class MillionaireQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Isaac's Millionaire Quiz")
        self.root.geometry("1200x700")  # Wider window to accommodate points history
        self.root.configure(bg="#0a0a2a")
        
        # Initialize game variables
        self.level = 1
        self.question_count = 0
        self.points = 0
        self.base_point_value = 10  # Starting point value
        self.current_point_value = self.base_point_value
        self.questions = self.load_questions()
        self.current_question = None
        self.points_history = []  # To track points earned per question
        
        # Create UI
        self.create_widgets()
        self.load_question()
        
    def create_widgets(self):
        # Main container frame
        main_frame = tk.Frame(self.root, bg="#0a0a2a")
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left side - Game content
        left_frame = tk.Frame(main_frame, bg="#0a0a2a")
        left_frame.pack(side='left', fill='both', expand=True)
        
        # Right side - Points history
        right_frame = tk.Frame(main_frame, bg="#0a0a2a", width=300)
        right_frame.pack(side='right', fill='y', padx=(20, 0))
        right_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Title
        title_font = font.Font(family="Arial", size=24, weight="bold")
        title_label = tk.Label(left_frame, text="Isaac's Millionaire Quiz", font=title_font, 
                              fg="white", bg="#0a0a2a")
        title_label.pack(pady=20)
        
        # Points and level display
        info_font = font.Font(family="Arial", size=14)
        self.points_label = tk.Label(left_frame, text=f"Total Prize: ${self.points:,}", font=info_font, 
                                    fg="gold", bg="#0a0a2a")
        self.points_label.pack(pady=5)
        
        self.value_label = tk.Label(left_frame, text=f"Current Question Value: ${self.current_point_value:,}", 
                                   font=info_font, fg="cyan", bg="#0a0a2a")
        self.value_label.pack(pady=5)
        
        self.level_label = tk.Label(left_frame, text=f"Level: {self.level}/70", font=info_font, 
                                   fg="white", bg="#0a0a2a")
        self.level_label.pack(pady=5)
        
        # Question frame
        self.question_frame = tk.Frame(left_frame, bg="#0a0a2a", height=150)
        self.question_frame.pack(pady=20, fill='x')
        
        question_font = font.Font(family="Arial", size=16)
        self.question_label = tk.Label(self.question_frame, text="", font=question_font, 
                                      fg="white", bg="#0a0a2a", wraplength=600, justify='center')
        self.question_label.pack(pady=20)
        
        # Hint button
        self.hint_button = tk.Button(self.question_frame, text="💡 Hint", font=info_font, 
                                    command=self.show_hint, bg="#0a0a2a", fg="yellow", 
                                    border=1, relief='solid')
        self.hint_button.pack(pady=10)
        
        # Options frame
        self.options_frame = tk.Frame(left_frame, bg="#0a0a2a")
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
        # Increase point value by $5 after every 4 questions
        if self.question_count > 0 and self.question_count % 4 == 0:
            self.base_point_value += 5
        
        # Set current point value with some randomness (±$2)
        self.current_point_value = self.base_point_value + random.randint(-2, 2)
        if self.current_point_value < 5:  # Ensure minimum value
            self.current_point_value = 5
            
        self.value_label.config(text=f"Current Question Value: ${self.current_point_value:,}")
    
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
            
            points_label = tk.Label(row_frame, text=f"${points:,}", font=("Arial", 10, "bold"), 
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
            if i > 0 and (len(self.points_history) + i) % 4 == 0:
                upcoming_value += 5
            
            points_label = tk.Label(row_frame, text=f"${upcoming_value:,}", font=("Arial", 10), 
                                  fg="cyan", bg="#0a0a2a", width=10, anchor='w')
            points_label.pack(side='left')
        
        # Update scroll region
        self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))
    
    def load_questions(self):
        # Sample questions - in a real game, you'd have 70 levels with 20 questions each
        questions = [
            {
                "question": "Which country made the first car?",
                "options": ["America", "Germany", "France", "Italy"],
                "correct": 1,  # Germany
                "hint": "This European country is known for its engineering and automotive industry."
            },
            {
                "question": "What is the capital of Australia?",
                "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
                "correct": 2,  # Canberra
                "hint": "It's not the largest city, but it was specifically designed to be the capital."
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct": 1,  # Mars
                "hint": "It's the fourth planet from the Sun in our solar system."
            },
            {  
                "question": "Who painted the Mona Lisa?",
                "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
                "correct": 2,  # Leonardo da Vinci
                "hint": "This Italian Renaissance artist was also a scientist and inventor."
            },
            {
                "question": "What is the largest ocean on Earth?",
                "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
                "correct": 3,  # Pacific Ocean
                "hint": "It covers about one-third of the Earth's surface."
            },
            {
                "question": "Which element has the chemical symbol 'O'?",
                "options": ["Gold", "Oxygen", "Osmium", "Oganesson"],
                "correct": 1,  # Oxygen
                "hint": "This element is essential for human respiration."
            },
            {
                "question": "In which year did World War II end?",
                "options": ["1943", "1945", "1947", "1950"],
                "correct": 1,  # 1945
                "hint": "The war ended with the surrender of Japan in this year."
            },
            {
                "question": "What is the largest mammal in the world?",
                "options": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
                "correct": 1,  # Blue Whale
                "hint": "This marine mammal is also the largest animal known to have ever existed."
            },
            {
                "question": "Which language is spoken in Brazil?",
                "options": ["Spanish", "Portuguese", "French", "English"],
                "correct": 1,  # Portuguese
                "hint": "This European language was brought to the country by colonizers."
            },
            {
                "question": "Who wrote 'Romeo and Juliet'?",
                "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                "correct": 1,  # William Shakespeare
                "hint": "This English playwright is often called England's national poet."
            },
            {
                "question": "What is the currency of Japan?",
                "options": ["Yuan", "Won", "Yen", "Ringgit"],
                "correct": 2,  # Yen
                "hint": "This currency's symbol is ¥."
            },
            {
                "question": "Which gas do plants absorb from the atmosphere?",
                "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
                "correct": 2,  # Carbon Dioxide
                "hint": "Plants use this gas during photosynthesis to produce food."
            },
            {
                "question": "How many sides does a hexagon have?",
                "options": ["5", "6", "7", "8"],
                "correct": 1,  # 6
                "hint": "The prefix 'hexa-' means six."
            },
            {
                "question": "Who was the first woman to win a Nobel Prize?",
                "options": ["Marie Curie", "Rosalind Franklin", "Dorothy Crowfoot Hodgkin", "Maria Goeppert-Mayer"],
                "correct": 0,  # Marie Curie
                "hint": "She won the prize in Physics in 1903 and later in Chemistry."
            },
            {
                "question": "What is the main ingredient in guacamole?",
                "options": ["Banana", "Avocado", "Cucumber", "Peas"],
                "correct": 1,  # Avocado
                "hint": "This fruit has a large pit and creamy green flesh."
            },
            {
                "question": "Which planet is closest to the Sun?",
                "options": ["Venus", "Earth", "Mercury", "Mars"],
                "correct": 2,  # Mercury
                "hint": "It's the smallest planet in our solar system."
            },
            {
                "question": "In what city is the Eiffel Tower located?",
                "options": ["London", "Rome", "Paris", "Berlin"],
                "correct": 2,  # Paris
                "hint": "This city is known as the 'City of Light'."
            },
            {
                "question": "What is the hardest natural substance on Earth?",
                "options": ["Gold", "Iron", "Diamond", "Platinum"],
                "correct": 2,  # Diamond
                "hint": "This substance is a form of carbon and is used in jewelry."
            },
            {
                "question": "Which animal is known as the 'Ship of the Desert'?",
                "options": ["Horse", "Camel", "Elephant", "Donkey"],
                "correct": 1,  # Camel
                "hint": "This animal can survive long periods without water in arid environments."
            },
            {
                "question": "Who discovered penicillin?",
                "options": ["Marie Curie", "Alexander Fleming", "Louis Pasteur", "Robert Koch"],
                "correct": 1,  # Alexander Fleming
                "hint": "This Scottish scientist discovered the antibiotic in 1928."
            }
        ]
        
        # For the full game, we would have 70 levels with 20 questions each
        # For this example, we'll just use the same 20 questions for all levels
        all_levels_questions = []
        for level in range(40):
            # Shuffle the questions for each level to make it more interesting
            shuffled_questions = questions.copy()
            random.shuffle(shuffled_questions)
            all_levels_questions.append(shuffled_questions)
            
        return all_levels_questions
    
    def load_question(self):
        # Get a random question from the current level
        level_questions = self.questions[self.level-1]
        self.current_question = random.choice(level_questions)
        
        # Update UI
        self.question_label.config(text=self.current_question["question"])
        
        # Update option buttons
        options = self.current_question["options"]
        for i, btn in enumerate(self.option_buttons):
            btn.config(text=options[i])
            
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
            self.points_label.config(text=f"Total Prize: ${self.points:,}")
            
            # Increase question count
            self.question_count += 1
            
            if self.level < 40:
                self.level += 1
                self.level_label.config(text=f"Level: {self.level}/70")
                self.load_question()
            else:
                messagebox.showinfo("Congratulations!", 
                                  f"You've completed all levels with ${self.points:,}!")
                self.root.destroy()
        else:
            correct_answer = self.current_question["options"][self.current_question["correct"]]
            messagebox.showerror("Wrong Answer", 
                               f"That's incorrect! The correct answer was: {correct_answer}\n"
                               f"You leave with ${self.points:,}!")
            self.root.destroy()
    
    def show_hint(self):
        messagebox.showinfo("Hint", self.current_question["hint"])

if __name__ == "__main__":
    root = tk.Tk()
    app = MillionaireQuiz(root)
    root.mainloop()