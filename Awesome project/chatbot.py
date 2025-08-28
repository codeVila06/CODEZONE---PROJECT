import tkinter as tk
from tkinter import scrolledtext, font
import random

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
        
        # Pre-trained responses
        self.responses = {
            "Ask a question": [
                "I'd be happy to answer your question. Could you please provide more details?",
                "That's an interesting question. Based on my knowledge, I'd say...",
                "Great question! Here's what you need to know about that topic..."
            ],
            "Draft anything": [
                "I'd be happy to help you draft that. What specific content are you looking to create?",
                "Let me create a draft for you. Here's a starting point...",
                "I can help with drafting. Based on your needs, I suggest..."
            ],
            "Brainstorm ideas": [
                "Let's brainstorm some ideas together. Here are a few initial thoughts...",
                "Great! I love brainstorming. Here are some concepts to consider...",
                "Based on your topic, here are some innovative ideas to explore..."
            ]
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.header_bg, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="Notion AI", font=("Arial", 16, "bold"),) 
        header_label = tk.Label(header_frame, text="chatAwesome AI", font=("Arial", 16, "bold"), 
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
        self.add_message("Hi Alex! How can I help you today?", is_user=False)
        
        # Suggested prompts
        suggestions_frame = tk.Frame(self.root, bg=self.chat_bg)
        suggestions_frame.pack(fill=tk.X, padx=20, pady=(10, 15))
        
        suggestions_label = tk.Label(suggestions_frame, text="Suggested", font=("Arial", 10, "bold"),
                                    fg="#666666", bg=self.chat_bg, anchor="w")
        suggestions_label.pack(fill=tk.X, pady=(0, 8))
        
        suggestions = [
            "Ask a question",
            "Draft anything",
            "Brainstorm ideas"
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
        
        # Generate AI response after a short delay
        self.root.after(500, self.generate_response, message)
    
    def generate_response(self, user_message):
        # Find the best matching prompt
        best_match = None
        for prompt in self.responses.keys():
            if prompt.lower() in user_message.lower():
                best_match = prompt
                break
                
        # If no direct match, use a general response
        if not best_match:
            general_responses = [
                "I'd be happy to help with that. Could you provide more details?",
                "That's an interesting request. Let me think about how I can assist...",
                "I can help with that. Here's what I suggest..."
            ]
            response = random.choice(general_responses)
        else:
            # Select a random response from the matching category
            response = random.choice(self.responses[best_match])
            
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