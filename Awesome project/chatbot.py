import tkinter as tk
from tkinter import scrolledtext, font
import random
import time

class NotionAIChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Notion AI Assistant")
        self.root.geometry("500x600")
        self.root.configure(bg="#FFFFFF")
        
        # Configure styles to match the image exactly
        self.chat_bg = "#FFFFFF"
        self.bot_msg_bg = "#F5F5F5"
        self.user_msg_bg = "#E8EDFF"
        self.text_color = "#000000"
        self.suggestion_bg = "#F7F7F7"
        self.suggestion_border = "#E0E0E0"
        self.input_bg = "#FFFFFF"
        self.header_bg = "#FFFFFF"
        self.placeholder_color = "#888888"
        
        # Conversation state tracking
        self.conversation_state = "neutral"
        self.user_name = "Alex"
        self.last_interaction_time = time.time()
        
        # Pre-trained responses with expanded conversation capabilities
        self.responses = {
            "greeting": [
                f"Hi {self.user_name}! How can I help you today?",
                f"Hello {self.user_name}! What would you like to work on?",
                f"Hey there {self.user_name}! Ready to be productive?",
                f"Good to see you {self.user_name}! What can I assist with?"
            ],
            "how_are_you": [
                "I'm functioning well, thank you for asking! As an AI, I don't have feelings, but I'm fully operational and ready to help you with your tasks. How about you?",
                "I'm running smoothly today! Ready to help you be productive. How are you doing?",
                "All systems operational! I'm here and ready to assist. How's your day going?",
                "I'm doing great - always available when you need me! How are things with you?"
            ],
            "how_is_day": [
                "My day is productive as always! I've been helping users organize their work and brainstorm ideas. What about your day?",
                "It's been a good day so far! I've assisted with several interesting projects. How's your day progressing?",
                "No days off for an AI assistant! I'm here 24/7. Has your day been productive so far?",
                "My day is what I make of it - helping you be more efficient! How has your day been?"
            ],
            "good_day": [
                "That's wonderful to hear! A positive mindset really boosts productivity.",
                "Great! When we're having a good day, we can accomplish so much more.",
                "I'm glad to hear that! Would you like to make it even more productive?",
                "Excellent! Let's channel that positive energy into your work."
            ],
            "bad_day": [
                "I'm sorry to hear that. Sometimes taking a short break can help refresh your perspective.",
                "Don't worry, we all have those days. Maybe I can help with something to make it better?",
                "I understand. Would focusing on a specific task help take your mind off things?",
                "Remember that tomorrow is a new day. Is there something I can help with right now?"
            ],
            "ask_question": [
                "I'd be happy to answer your question. Could you please provide more details?",
                "That's an interesting question. Based on my knowledge, I'd say...",
                "Great question! Here's what you need to know about that topic..."
            ],
            "draft_anything": [
                "I'd be happy to help you draft that. What specific content are you looking to create?",
                "Let me create a draft for you. Here's a starting point...",
                "I can help with drafting. Based on your needs, I suggest..."
            ],
            "brainstorm_ideas": [
                "Let's brainstorm some ideas together. Here are a few initial thoughts...",
                "Great! I love brainstorming. Here are some concepts to consider...",
                "Based on your topic, here are some innovative ideas to explore..."
            ],
            "farewell": [
                "Goodbye! Let me know if you need anything else.",
                "See you later! Feel free to come back if you have more questions.",
                "Have a great day! Don't hesitate to reach out if you need help.",
                "Talk to you soon! I'm here whenever you need assistance."
            ],
            "thanks": [
                "You're welcome! Happy to help.",
                "Anytime! That's what I'm here for.",
                "Glad I could assist! Let me know if you need anything else.",
                "My pleasure! Is there anything else you'd like help with?"
            ],
            "default": [
                "I'd be happy to help with that. Could you provide more details?",
                "That's an interesting request. Let me think about how I can assist...",
                "I can help with that. Here's what I suggest...",
                "Let me see how I can best assist you with this..."
            ]
        }
        
        # Knowledge base for various topics
        self.knowledge = {
            "productivity": [
                "Research shows that taking regular breaks actually improves focus and productivity.",
                "The Pomodoro Technique (25 minutes of work followed by a 5-minute break) is highly effective for maintaining concentration.",
                "Prioritizing your tasks using the Eisenhower Matrix can help you focus on what's truly important.",
                "A cluttered workspace can lead to a cluttered mind. Consider organizing your digital workspace for better focus."
            ],
            "notion_tips": [
                "You can use templates in Notion to quickly create pages for common projects.",
                "Linking databases in Notion allows you to create powerful relationships between different types of information.",
                "The toggle list feature in Notion is great for organizing information without clutter.",
                "You can use @ mentions in Notion to link to other pages, people, or dates."
            ],
            "time_management": [
                "Time blocking is an effective method for managing your schedule and ensuring important tasks get done.",
                "The 2-minute rule: if a task takes less than 2 minutes, do it immediately rather than putting it off.",
                "Setting specific, achievable goals for each day increases the likelihood of accomplishing them.",
                "Reviewing your week every Friday helps you prepare for a productive week ahead."
            ]
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.header_bg, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="Notion AI", font=("Arial", 16, "bold"), 
                               fg=self.text_color, bg=self.header_bg)
        header_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Chat area
        chat_container = tk.Frame(self.root, bg=self.chat_bg)
        chat_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        self.chat_area = scrolledtext.ScrolledText(chat_container, wrap=tk.WORD, width=50, height=15,
                                                  bg=self.chat_bg, fg=self.text_color, 
                                                  font=("Arial", 12), relief=tk.FLAT, bd=0,
                                                  padx=20, pady=20)
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.chat_area.config(state=tk.DISABLED)
        
        # Add welcome message
        self.add_message(random.choice(self.responses["greeting"]), is_user=False)
        
        # Suggested prompts
        suggestions_frame = tk.Frame(self.root, bg=self.chat_bg)
        suggestions_frame.pack(fill=tk.X, padx=20, pady=(10, 15))
        
        suggestions_label = tk.Label(suggestions_frame, text="Suggested", font=("Arial", 10, "bold"),
                                    fg="#666666", bg=self.chat_bg, anchor="w")
        suggestions_label.pack(fill=tk.X, pady=(0, 8))
        
        suggestions = [
            "How are you?",
            "How's your day going?",
            "Tell me about productivity"
        ]
        
        for suggestion in suggestions:
            suggestion_btn = tk.Button(suggestions_frame, text=f"• {suggestion}", font=("Arial", 10),
                                      fg=self.text_color, bg=self.suggestion_bg, relief=tk.FLAT,
                                      bd=1, highlightbackground=self.suggestion_border, 
                                      padx=12, pady=8, anchor="w", justify=tk.LEFT,
                                      command=lambda s=suggestion: self.suggestion_clicked(s))
            suggestion_btn.pack(fill=tk.X, pady=(5, 0))
        
        # Input area
        input_frame = tk.Frame(self.root, bg=self.chat_bg, height=50)
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        input_frame.pack_propagate(False)
        
        input_container = tk.Frame(input_frame, bg=self.input_bg, highlightbackground="#E0E0E0", 
                                  highlightthickness=1, highlightcolor="#E0E0E0")
        input_container.pack(fill=tk.BOTH, expand=True)
        
        self.input_entry = tk.Entry(input_container, font=("Arial", 12),
                              bg=self.input_bg, fg=self.text_color, relief=tk.FLAT, bd=0)
        self.input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        self.input_entry.bind("<Return>", self.send_message)
        
        self.input_entry.insert(0, "Ask anything or type / for commands")
        self.input_entry.config(fg=self.placeholder_color)
        
        def on_entry_click(event):
            if self.input_entry.get() == "Ask anything or type / for commands":
                self.input_entry.delete(0, tk.END)
                self.input_entry.config(fg=self.text_color)
                
        def on_focusout(event):
            if self.input_entry.get() == '':
                self.input_entry.insert(0, "Ask anything or type / for commands")
                self.input_entry.config(fg=self.placeholder_color)
                
        self.input_entry.bind('<FocusIn>', on_entry_click)
        self.input_entry.bind('<FocusOut>', on_focusout)
        
        send_btn = tk.Button(input_container, text="→", font=("Arial", 14), 
                            bg="#444791", fg="#FFFFFF", relief=tk.FLAT, width=3,
                            command=self.send_message)
        send_btn.pack(side=tk.RIGHT, padx=(5, 10), pady=10)
    
    def suggestion_clicked(self, suggestion):
        self.input_entry.delete(0, tk.END)
        self.input_entry.config(fg=self.text_color)
        self.input_entry.insert(0, suggestion)
        self.send_message()
    
    def send_message(self, event=None):
        message = self.input_entry.get().strip()
        if not message or message == "Ask anything or type / for commands":
            return
            
        self.add_message(message, is_user=True)
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, "Ask anything or type / for commands")
        self.input_entry.config(fg=self.placeholder_color)
        
        # Update last interaction time
        self.last_interaction_time = time.time()
        
        # Generate AI response after a short delay
        self.root.after(500, self.generate_response, message)
    
    def generate_response(self, user_message):
        # Convert to lowercase for easier matching
        lower_message = user_message.lower()
        
        # Determine conversation context and generate appropriate response
        if any(word in lower_message for word in ["hi", "hello", "hey", "greetings"]):
            response = random.choice(self.responses["greeting"])
            self.conversation_state = "greeted"
            
        elif any(word in lower_message for word in ["how are you", "how're you", "how do you feel"]):
            response = random.choice(self.responses["how_are_you"])
            self.conversation_state = "asked_about_me"
            
        elif any(word in lower_message for word in ["how is your day", "how's your day", "how was your day"]):
            response = random.choice(self.responses["how_is_day"])
            self.conversation_state = "asked_about_day"
            
        elif any(word in lower_message for word in ["good", "great", "excellent", "wonderful", "fine", "okay"]) and self.conversation_state in ["asked_about_me", "asked_about_day"]:
            response = random.choice(self.responses["good_day"])
            # Add a productivity tip after positive response
            response += " " + random.choice(self.knowledge["productivity"])
            self.conversation_state = "neutral"
            
        elif any(word in lower_message for word in ["bad", "not good", "terrible", "awful", "tired", "stress"]) and self.conversation_state in ["asked_about_me", "asked_about_day"]:
            response = random.choice(self.responses["bad_day"])
            # Add a helpful tip
            response += " " + random.choice(self.knowledge["time_management"])
            self.conversation_state = "neutral"
            
        elif any(word in lower_message for word in ["bye", "goodbye", "see you", "farewell"]):
            response = random.choice(self.responses["farewell"])
            self.conversation_state = "neutral"
            
        elif any(word in lower_message for word in ["thank", "thanks", "appreciate"]):
            response = random.choice(self.responses["thanks"])
            self.conversation_state = "neutral"
            
        elif "productivity" in lower_message:
            response = "I know quite a bit about productivity! " + random.choice(self.knowledge["productivity"])
            self.conversation_state = "sharing_knowledge"
            
        elif "notion" in lower_message:
            response = "Here's a Notion tip for you: " + random.choice(self.knowledge["notion_tips"])
            self.conversation_state = "sharing_knowledge"
            
        elif "time management" in lower_message:
            response = "Time management is crucial for productivity. " + random.choice(self.knowledge["time_management"])
            self.conversation_state = "sharing_knowledge"
            
        elif any(word in lower_message for word in ["ask", "question"]):
            response = random.choice(self.responses["ask_question"])
            self.conversation_state = "answering_question"
            
        elif any(word in lower_message for word in ["draft", "write", "create"]):
            response = random.choice(self.responses["draft_anything"])
            self.conversation_state = "drafting"
            
        elif any(word in lower_message for word in ["brainstorm", "idea", "ideas"]):
            response = random.choice(self.responses["brainstorm_ideas"])
            self.conversation_state = "brainstorming"
            
        else:
            response = random.choice(self.responses["default"])
            self.conversation_state = "neutral"
        
        self.add_message(response, is_user=False)
    
    def add_message(self, message, is_user=True):
        self.chat_area.config(state=tk.NORMAL)
        
        # Configure tag for message alignment
        if is_user:
            bg_color = self.user_msg_bg
            align = "right"
        else:
            bg_color = self.bot_msg_bg
            align = "left"
        
        # Create message frame
        message_frame = tk.Frame(self.chat_area, bg=self.chat_bg, padx=0, pady=5)
        
        # Create message label
        message_label = tk.Label(message_frame, text=message, wraplength=300, justify=tk.LEFT,
                                bg=bg_color, fg=self.text_color, font=("Arial", 11),
                                padx=12, pady=8, relief=tk.FLAT, bd=0)
        
        if align == "right":
            message_label.pack(side=tk.RIGHT)
        else:
            message_label.pack(side=tk.LEFT)
        
        # Add message to chat area
        self.chat_area.window_create(tk.END, window=message_frame)
        self.chat_area.insert(tk.END, "\n")
        
        # Auto-scroll to bottom
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = NotionAIChatbot(root)
    root.mainloop()