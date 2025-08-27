import tkinter as tk
from tkinter import messagebox, ttk
import random

class MathQuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz Game")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Game variables
        self.score = 0
        self.current_question = 0
        self.total_questions = 10  # Reduced for demonstration
        self.points_per_question = 2
        self.winning_score = 100
        self.skipped_questions = 0
        
        # Create questions database
        self.questions = self.generate_questions()
        
        # UI setup
        self.setup_ui()
        
        # Start with first question
        self.next_question()
    
    def generate_questions(self):
        questions = []
        # Question templates based on the image
        templates = [
            {
                "question": "What is the reciprocal of 1/x²?",
                "options": ["-1/x²", "x⁻²", "x²", "2x"],
                "correct_answer": 2  # x²
            },
            {
                "question": "What is the reciprocal of 5?",
                "options": ["-5", "0.2", "5", "0.5"],
                "correct_answer": 1  # 0.2
            },
            {
                "question": "What is the reciprocal of 2/3?",
                "options": ["-2/3", "3/2", "2/3", "1.5"],
                "correct_answer": 1  # 3/2
            },
            {
                "question": "What is the reciprocal of 0.25?",
                "options": ["-0.25", "4", "0.25", "2.5"],
                "correct_answer": 1  # 4
            },
            {
                "question": "What is the reciprocal of -4?",
                "options": ["4", "0.25", "-0.25", "-4"],
                "correct_answer": 2  # -0.25
            },
            {
                "question": "What is the reciprocal of 1?",
                "options": ["-1", "0", "1", "2"],
                "correct_answer": 2  # 1
            },
            {
                "question": "What is the reciprocal of 10?",
                "options": ["-10", "0.1", "10", "0.01"],
                "correct_answer": 1  # 0.1
            },
            {
                "question": "What is the reciprocal of 2x?",
                "options": ["-2x", "1/(2x)", "2x", "0.5x"],
                "correct_answer": 1  # 1/(2x)
            },
            {
                "question": "What is the reciprocal of a/b?",
                "options": ["-a/b", "b/a", "a/b", "1/(ab)"],
                "correct_answer": 1  # b/a
            },
            {
                "question": "What is the reciprocal of 0?",
                "options": ["0", "1", "Undefined", "Infinity"],
                "correct_answer": 2  # Undefined
            }
        ]
        
        # Randomize the order of questions
        random.shuffle(templates)
        return templates
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Math Quiz Game", font=('Arial', 24, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(expand=True, pady=20)
        
        # Score display
        self.score_label = tk.Label(header_frame, text=f"Score: {self.score}", 
                                   font=('Arial', 14), fg='white', bg='#2c3e50')
        self.score_label.pack(side=tk.RIGHT, padx=20)
        
        # Question counter
        self.counter_label = tk.Label(header_frame, text=f"Question: {self.current_question+1}/{self.total_questions}", 
                                     font=('Arial', 14), fg='white', bg='#2c3e50')
        self.counter_label.pack(side=tk.LEFT, padx=20)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=40, pady=40)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Question display
        self.question_label = tk.Label(main_frame, text="", font=('Arial', 18), 
                                      wraplength=600, justify=tk.CENTER, bg='#f0f0f0')
        self.question_label.pack(pady=(0, 30))
        
        # Options frame
        options_frame = tk.Frame(main_frame, bg='#f0f0f0')
        options_frame.pack(pady=20)
        
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(options_frame, text="", font=('Arial', 14), 
                           width=30, height=2, command=lambda idx=i: self.check_answer(idx),
                           bg='#ffffff', relief=tk.RAISED, bd=2)
            btn.pack(pady=10)
            self.option_buttons.append(btn)
        
        # Navigation frame
        nav_frame = tk.Frame(main_frame, bg='#f0f0f0')
        nav_frame.pack(pady=30)
        
        # Skip button
        self.skip_button = tk.Button(nav_frame, text="Skip Question", font=('Arial', 14), 
                                    command=self.skip_question, bg='#e67e22', fg='white', width=15, height=1)
        self.skip_button.pack(side=tk.LEFT, padx=10)
        
        # Next button
        self.next_button = tk.Button(nav_frame, text="Next Question", font=('Arial', 14), 
                                    command=self.next_question, state=tk.DISABLED,
                                    bg='#3498db', fg='white', width=15, height=1)
        self.next_button.pack(side=tk.RIGHT, padx=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, 
                                       length=600, mode='determinate')
        self.progress.pack(pady=20)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='#ecf0f1', height=40)
        footer_frame.pack(fill=tk.X)
        footer_frame.pack_propagate(False)
        
        copyright_label = tk.Label(footer_frame, text="Copyright © 2025 Math Quiz Game", 
                                  font=('Arial', 10), fg='#7f8c8d', bg='#ecf0f1')
        copyright_label.pack(side=tk.LEFT, padx=20)
        
        # Just for UI similarity - not functional
        activate_label = tk.Label(footer_frame, text="Activate Windows\nGo to Settings to activate Windows", 
                                 font=('Arial', 8), fg='#7f8c8d', bg='#ecf0f1', justify=tk.RIGHT)
        activate_label.pack(side=tk.RIGHT, padx=20)
    
    def next_question(self):
        if self.current_question < self.total_questions:
            # Enable option buttons
            for btn in self.option_buttons:
                btn.config(state=tk.NORMAL, bg='#ffffff')
            
            # Update question
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data['question'])
            
            # Update options
            for i, option in enumerate(question_data['options']):
                self.option_buttons[i].config(text=option)
            
            # Update counter
            self.counter_label.config(text=f"Question: {self.current_question+1}/{self.total_questions}")
            
            # Update progress bar
            self.progress['value'] = (self.current_question / self.total_questions) * 100
            
            # Disable next button until answer is selected
            self.next_button.config(state=tk.DISABLED)
            
            # Enable skip button
            self.skip_button.config(state=tk.NORMAL)
        else:
            self.end_game()
    
    def check_answer(self, selected_index):
        # Disable all option buttons to prevent changing answer
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)
        
        # Disable skip button
        self.skip_button.config(state=tk.DISABLED)
        
        # Check if answer is correct
        correct_index = self.questions[self.current_question]['correct_answer']
        if selected_index == correct_index:
            self.score += self.points_per_question
            self.option_buttons[selected_index].config(bg='#2ecc71')  # Green for correct
        else:
            self.option_buttons[selected_index].config(bg='#e74c3c')  # Red for incorrect
            self.option_buttons[correct_index].config(bg='#2ecc71')   # Highlight correct answer
        
        # Update score
        self.score_label.config(text=f"Score: {self.score}")
        
        # Enable next button
        self.next_button.config(state=tk.NORMAL)
        
        # Move to next question after a brief delay
        if self.score >= self.winning_score:
            self.root.after(1500, self.win_game)
        elif self.current_question + 1 >= self.total_questions:
            self.root.after(1500, self.end_game)
        else:
            self.root.after(1500, self.advance_question)
    
    def skip_question(self):
        self.skipped_questions += 1
        self.advance_question()
    
    def advance_question(self):
        self.current_question += 1
        self.next_question()
    
    def win_game(self):
        messagebox.showinfo("Congratulations!", f"You won the game with a score of {self.score} points!\n\nSkipped questions: {self.skipped_questions}")
        self.play_again()
    
    def end_game(self):
        messagebox.showinfo("Game Over", f"Your final score is {self.score} points.\n\nSkipped questions: {self.skipped_questions}")
        self.play_again()
    
    def play_again(self):
        answer = messagebox.askyesno("Play Again?", "Would you like to play again?")
        if answer:
            self.score = 0
            self.current_question = 0
            self.skipped_questions = 0
            self.score_label.config(text=f"Score: {self.score}")
            self.questions = self.generate_questions()  # Regenerate questions
            self.next_question()
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = MathQuizGame(root)
    root.mainloop()