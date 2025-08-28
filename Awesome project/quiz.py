import tkinter as tk
from tkinter import messagebox
import random

class MathQuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz Game")
        self.root.geometry("800x600")
        self.root.configure(bg='white')
        
        # Quiz variables
        self.total_questions = 50
        self.current_question = 0
        self.score = 0
        self.questions = []
        
        # Create UI elements
        self.create_widgets()
        
        # Generate questions
        self.generate_questions()
        
        # Display first question
        self.show_question()
    
    def create_widgets(self):
        # Header with blue background
        header_frame = tk.Frame(self.root, bg='#4a7abc', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Math Quiz Game", font=('Arial', 24, 'bold'), 
                              fg='white', bg='#4a7abc')
        title_label.pack(expand=True)
        
        # Progress frame
        progress_frame = tk.Frame(self.root, bg='white')
        progress_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        self.progress_label = tk.Label(progress_frame, text="Question 1 of 50", 
                                      font=('Arial', 14), bg='white')
        self.progress_label.pack(side='left')
        
        self.score_label = tk.Label(progress_frame, text="Score: 0/0", 
                                   font=('Arial', 14), bg='white')
        self.score_label.pack(side='right')
        
        # Question frame with blue border
        question_frame = tk.Frame(self.root, bg='white', relief='solid', bd=2, highlightbackground='#4a7abc', highlightthickness=2)
        question_frame.pack(fill='x', padx=50, pady=(0, 20))
        
        self.question_label = tk.Label(question_frame, text="", font=('Arial', 16), 
                                      bg='white', wraplength=600, padx=20, pady=20)
        self.question_label.pack()
        
        # Options frame
        self.options_frame = tk.Frame(self.root, bg='white')
        self.options_frame.pack(fill='both', expand=True, padx=50, pady=20)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='white')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        self.next_button = tk.Button(button_frame, text="Next Question", font=('Arial', 14),
                                    command=self.next_question, state='disabled', 
                                    bg='#4a7abc', fg='white', padx=20, pady=10,
                                    activebackground='#3a5b9c', activeforeground='white')
        self.next_button.pack(side='right')
        
        self.feedback_label = tk.Label(button_frame, text="", font=('Arial', 14), bg='white')
        self.feedback_label.pack(side='left')
    
    def generate_questions(self):
        # Generate 50 math questions with options
        operations = ['+', '-', '*', '/']
        
        for i in range(self.total_questions):
            op = random.choice(operations)
            
            if op == '+':
                a = random.randint(1, 100)
                b = random.randint(1, 100)
                answer = a + b
                question = f"What is {a} + {b}?"
            elif op == '-':
                a = random.randint(1, 100)
                b = random.randint(1, 100)
                # Ensure no negative results
                if a < b:
                    a, b = b, a
                answer = a - b
                question = f"What is {a} - {b}?"
            elif op == '*':
                a = random.randint(1, 12)
                b = random.randint(1, 12)
                answer = a * b
                question = f"What is {a} × {b}?"
            else:  # division
                b = random.randint(1, 12)
                answer = random.randint(1, 12)
                a = b * answer  # Ensure integer result
                question = f"What is {a} ÷ {b}?"
            
            # Generate options
            options = [answer]
            while len(options) < 4:
                # Generate wrong answers that are close to the correct one
                wrong = answer + random.randint(-10, 10)
                if wrong != answer and wrong not in options and wrong > 0:
                    options.append(wrong)
            
            random.shuffle(options)
            
            # Map options to letters
            option_letters = ['A', 'B', 'C', 'D']
            option_texts = [f"{option_letters[i]}. {option}" for i, option in enumerate(options)]
            
            # Store the question data
            self.questions.append({
                'question': question,
                'options': option_texts,
                'answer': answer,
                'correct_index': options.index(answer),
                'user_answer': None,
                'answered': False  # Track if this question has been answered
            })
    
    def show_question(self):
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Get current question data
        question_data = self.questions[self.current_question]
        
        # Update progress and score
        self.progress_label.config(text=f"Question {self.current_question + 1} of {self.total_questions}")
        self.score_label.config(text=f"Score: {self.score}/{self.current_question}")
        
        # Display question
        self.question_label.config(text=question_data['question'])
        
        # Display options with blue borders
        self.option_vars = []
        for i, option_text in enumerate(question_data['options']):
            # Create a frame for each option with a blue border
            option_frame = tk.Frame(self.options_frame, bg='white', relief='solid', bd=1, 
                                   highlightbackground='#4a7abc', highlightthickness=1)
            option_frame.pack(fill='x', pady=5)
            
            var = tk.StringVar(value="")
            radio = tk.Radiobutton(option_frame, text=option_text, variable=var, 
                                  value=chr(65+i), font=('Arial', 14), bg='white',
                                  command=lambda v=var: self.option_selected(v),
                                  activebackground='#e6f0ff')
            radio.pack(anchor='w', padx=20, pady=10)
            self.option_vars.append(var)
            
            # If user already answered this question, show their selection
            if question_data['user_answer'] == chr(65+i):
                radio.select()
        
        # Reset feedback and next button
        self.feedback_label.config(text="")
        self.next_button.config(state='disabled')
    
    def option_selected(self, var):
        # Get the selected option
        selected_option = var.get()
        question_data = self.questions[self.current_question]
        
        # Store the user's answer
        question_data['user_answer'] = selected_option
        
        # Check if answer is correct
        if ord(selected_option) - 65 == question_data['correct_index']:
            self.feedback_label.config(text="Correct!", fg='green')
            # Only increment score if this is the first time answering this question
            if not question_data['answered']:
                self.score += 1
                question_data['answered'] = True
        else:
            correct_letter = chr(65 + question_data['correct_index'])
            self.feedback_label.config(text=f"Incorrect! The correct answer is {correct_letter}", fg='red')
            # Mark as answered but don't increment score
            question_data['answered'] = True
        
        # Update score display
        self.score_label.config(text=f"Score: {self.score}/{self.current_question + 1}")
        
        # Enable next button
        self.next_button.config(state='normal')
    
    def next_question(self):
        # Move to next question or end quiz
        self.current_question += 1
        
        if self.current_question < self.total_questions:
            self.show_question()
        else:
            self.end_quiz()
    
    def end_quiz(self):
        # Calculate final score
        final_score = self.score
        percentage = (final_score / self.total_questions) * 100
        
        # Show results
        messagebox.showinfo("Quiz Completed", 
                           f"Your final score: {final_score}/{self.total_questions}\n"
                           f"Percentage: {percentage:.1f}%")
        
        # Ask if user wants to play again
        play_again = messagebox.askyesno("Play Again?", "Would you like to play again?")
        
        if play_again:
            # Reset quiz
            self.current_question = 0
            self.score = 0
            self.questions = []
            self.generate_questions()
            self.show_question()
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizGame(root)
    root.mainloop()