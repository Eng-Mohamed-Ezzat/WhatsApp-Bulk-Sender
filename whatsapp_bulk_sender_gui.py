import pywhatkit as kit
import os
import sys
import time
import random as rd
import tkinter as tk
from tkinter import scrolledtext
import threading
from pathlib import Path
import webbrowser

class WhatsAppSenderGUI: 
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Bulk Sender 📱")
        self.root.geometry("750x900")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, False)
        
        # Get application startup path (where the .exe is located)
        if getattr(sys, 'frozen', False):
            self.base_path = sys._MEIPASS
            self.folder_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))
            self.folder_path = self.base_path
        
        # Set Window Icon
        try:
            icon_path = os.path.join(self.base_path, "whatsapp.png")
            if os.path.exists(icon_path):
                img = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, img)
        except Exception as e:
            print(f"Could not set window icon: {e}")
        
        # Configuration
        self.wait_time = 15
        self.tab_close = True
        self.is_running = False
        self.image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        
        self.setup_ui()
        self.scan_folder()  # Auto-scan on startup
        
    def setup_ui(self):
        # Header
        header = tk.Label(
            self.root,
            text="📱 WhatsApp Bulk Sender",
            font=("Segoe UI", 28, "bold"),
            bg="#1e1e2e",
            fg="#89b4fa"
        )
        header.pack(pady=20)
        
        # Folder info
        info_frame = tk.Frame(self.root, bg="#313244", bd=0)
        info_frame.pack(padx=30, pady=(0, 10), fill="x")
        
        tk.Label(
            info_frame,
            text=f"📁 Folder: {self.folder_path}",
            font=("Segoe UI", 10),
            bg="#313244",
            fg="#cdd6f4",
            anchor="w",
            padx=15,
            pady=10
        ).pack(fill="x")
        
        # File count label
        self.file_count_label = tk.Label(
            self.root,
            text="📋 Files found: 0",
            font=("Segoe UI", 12, "bold"),
            bg="#1e1e2e",
            fg="#a6e3a1"
        )
        self.file_count_label.pack(pady=10)
        
        # Log box
        log_frame = tk.LabelFrame(
            self.root,
            text="📝 Activity Log",
            font=("Segoe UI", 12, "bold"),
            bg="#313244",
            fg="#cdd6f4",
            padx=15,
            pady=15
        )
        log_frame.pack(padx=30, pady=10, fill="both", expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 10),
            bg="#45475a",
            fg="#a6e3a1",
            relief="flat",
            bd=0,
            wrap="word",
            height=15,
            state="disabled"
        )
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Developer credits frame
        credits_frame = tk.Frame(self.root, bg="#313244", bd=0)
        credits_frame.pack(padx=30, pady=(10, 5), fill="x")
        
        # Developer name header with Arabic text on the same line
        developer_row = tk.Frame(credits_frame, bg="#313244")
        developer_row.pack(fill="x", padx=15, pady=(10, 5))
        
        # Developer name (left side)
        tk.Label(
            developer_row,
            text="Developed By Eng. Mohamed Ezzat",
            font=("Segoe UI", 10, "bold"),
            bg="#313244",
            fg="#cdd6f4",
            anchor="w"
        ).pack(side="left")
        
        # Arabic text (right side)
        tk.Label(
            developer_row,
            text="سبحان الله وبحمده، سبحان الله العظيم",
            font=("Segoe UI", 12, "bold"),
            bg="#313244",
            fg="#a6e3a1",  # Green color to make it stand out
            anchor="e"
        ).pack(side="right")
        
        # Contact list container
        contact_list = tk.Frame(credits_frame, bg="#313244")
        contact_list. pack(anchor="w", padx=15, pady=(0, 10))
        
        # WhatsApp contact
        whatsapp_row = tk.Frame(contact_list, bg="#313244")
        whatsapp_row.pack(anchor="w", pady=2)
        
        whatsapp_link = tk.Label(
            whatsapp_row,
            text="💬 +201062048212",
            font=("Segoe UI", 9),
            bg="#313244",
            fg="#25D366",
            cursor="hand2"
        )
        whatsapp_link.pack(side="left")
        whatsapp_link.bind("<Button-1>", lambda e: self.open_whatsapp())
        
        # LinkedIn contact
        linkedin_row = tk. Frame(contact_list, bg="#313244")
        linkedin_row.pack(anchor="w", pady=2)
        
        linkedin_link = tk.Label(
            linkedin_row,
            text="🔗 LinkedIn",
            font=("Segoe UI", 9),
            bg="#313244",
            fg="#0A66C2",
            cursor="hand2"
        )
        linkedin_link.pack(side="left")
        linkedin_link. bind("<Button-1>", lambda e: self.open_linkedin())
        
        # Website contact
        website_row = tk.Frame(contact_list, bg="#313244")
        website_row. pack(anchor="w", pady=2)
        
        website_link = tk.Label(
            website_row,
            text="🌐 Website",
            font=("Segoe UI", 9),
            bg="#313244",
            fg="#89b4fa",
            cursor="hand2"
        )
        website_link.pack(side="left")
        website_link. bind("<Button-1>", lambda e: self.open_website())
        
        # Contact Card
        contact_row = tk.Frame(contact_list, bg="#313244")
        contact_row.pack(anchor="w", pady=2)
        
        contact_link = tk. Label(
            contact_row,
            text="📇 Contact",
            font=("Segoe UI", 9),
            bg="#313244",
            fg="#f9e2af",
            cursor="hand2"
        )
        contact_link.pack(side="left")
        contact_link.bind("<Button-1>", lambda e:  self.open_contact_card())
        
        # Buttons frame
        button_frame = tk. Frame(self.root, bg="#1e1e2e")
        button_frame.pack(pady=20)
        
        # Start button
        self.start_btn = tk.Button(
            button_frame,
            text="▶️ Start Sending",
            command=self.start_sending,
            font=("Segoe UI", 14, "bold"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            activebackground="#94e2d5",
            relief="flat",
            cursor="hand2",
            padx=40,
            pady=15,
            state="normal"
        )
        self.start_btn.pack(side="left", padx=10)
        
        # Stop button
        self. stop_btn = tk.Button(
            button_frame,
            text="⏹️ Stop",
            command=self.stop_sending,
            font=("Segoe UI", 14, "bold"),
            bg="#f38ba8",
            fg="#1e1e2e",
            activebackground="#eba0ac",
            relief="flat",
            cursor="hand2",
            padx=40,
            pady=15,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=10)
        
    def log(self, message, color=None):
        """Add message to log box"""
        self.log_text.configure(state="normal")
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text. see(tk.END)
        self.log_text.configure(state="disabled")
        self.root.update_idletasks()
        
    def scan_folder(self):
        """Scan folder for image files"""
        self.image_files = []
        
        if not os.path.exists(self.folder_path):
            self.log(f"✗ Folder not found: {self.folder_path}")
            return
            
        for file in os.listdir(self.folder_path):
            if os.path.splitext(file)[1].lower() in self.image_extensions:
                self.image_files.append(file)
        
        count = len(self.image_files)
        self.file_count_label.config(text=f"📋 Files found: {count}")
        
        self. log(f"✓ Found {count} image(s) in folder")
        self.log("Files to process:")
        for img_file in self.image_files:
            self.log(f"  - {img_file}")
            
        if count > 0:
            self.start_btn.config(state="normal")
        else:
            self.start_btn.config(state="disabled")
            self.log("\n⚠️ No images found.  Add images to the folder and restart.")
    
    def start_sending(self):
        """Start sending messages in background thread"""
        if not self.image_files:
            self.log("✗ No images to process!")
            return
            
        self.is_running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        
        # Run in separate thread to avoid freezing GUI
        thread = threading.Thread(target=self.send_messages_thread, daemon=True)
        thread.start()
        
    def stop_sending(self):
        """Stop sending messages"""
        self. is_running = False
        self.log("\n⏹️ Stopping... (will finish current message)")
        
    def send_messages_thread(self):
        """Send messages to all numbers"""
        try:
            total = len(self.image_files)
            self.log(f"\n🚀 Starting to send {total} message(s).. .\n")
            
            for idx, img_file in enumerate(self.image_files, 1):
                if not self.is_running:
                    self.log("✗ Stopped by user")
                    break
                
                # Extract phone number and caption from filename
                order = os.path.splitext(img_file)[0]
                try:
                    phone_number = order.split("_")[0].strip()
                    caption = order.split("_")[1].strip()
                except IndexError:
                    self. log(f"✗ Invalid filename format: {img_file}")
                    continue
                
                # Add country code if not present
                if not phone_number.startswith('+'):
                    phone_number = '+' + phone_number
                
                # Full path to image
                img_path = os.path.join(self.folder_path, img_file)
                
                self.log(f"\n[{idx}/{total}] Sending to {phone_number}...")
                self.log(f"Image: {img_file}")
                
                try:
                    kit.sendwhats_image(phone_number, img_path, caption, self.wait_time, self.tab_close)
                    self.log(f"✓ Message sent successfully to {phone_number}")
                    
                    # Add delay between messages to avoid being blocked
                    if idx < total and self.is_running:
                        delay = rd.randint(5, 10)  # Random delay between messages
                        self.log(f"⏳ Waiting {delay} seconds before next message...")
                        for i in range(delay):
                            if not self.is_running:
                                break
                            time.sleep(1)
                            
                except Exception as e: 
                    self.log(f"✗ Error sending to {phone_number}: {str(e)}")
                    continue
            
            if self.is_running:
                self.log("\n✅ All messages processed!")
            
        except Exception as e:
            self.log(f"\n✗ Fatal error: {str(e)}")
            
        finally:
            self. is_running = False
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
    
    def open_whatsapp(self):
        """Open WhatsApp with developer's phone"""
        phone = "+201062048212"
        webbrowser.open(f"https://wa.me/{phone.replace('+', '')}")
        self.log("📞 Opening WhatsApp...")
    
    def open_linkedin(self):
        """Open LinkedIn profile"""
        webbrowser.open("https://www.linkedin.com/in/eng-mohamed-ezzat/")
        self.log("🔗 Opening LinkedIn profile...")
    
    def open_website(self):
        """Open personal website"""
        webbrowser. open("https://eng-mohamed-ezzat.github.io/")
        self.log("🌐 Opening website...")
    
    def open_contact_card(self):
        """Open contact card"""
        webbrowser.open("https://eng-mohamed-ezzat.github.io/ContactCard/")
        self.log("📇 Opening contact card...")
    
    def on_closing(self):
        """Handle window close"""
        if self.is_running:
            self.is_running = False
            time.sleep(1)
        self.root.destroy()

# Main application
if __name__ == "__main__":
    root = tk. Tk()
    app = WhatsAppSenderGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()