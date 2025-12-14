import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, PngImagePlugin
import numpy as np
import base64
import os
import json
from cryptography.fernet import Fernet
import hashlib

class ImagePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Get colors from controller
        self.COLORS = controller.COLORS
        
        # State variables
        self.source_image_path = ""
        self.output_image_path = ""
        self.encoded_image_path = ""
        self.current_image = None
        
        # Setup page
        self.setup_page()
    
    def setup_page(self):
        """Setup all page elements"""
        # Configure frame
        self.configure(bg=self.COLORS['bg'])
        
        # ===== PAGE HEADER =====
        self.setup_header()
        
        # ===== MAIN CONTENT (TWO COLUMNS) =====
        self.setup_main_content()
        
        # ===== PAGE FOOTER =====
        self.setup_footer()
    
    def setup_header(self):
        """Setup page header"""
        header_frame = tk.Frame(self, bg=self.COLORS['bg'], height=80)
        header_frame.pack(fill="x", pady=(10, 0))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🖼️ ADVANCED IMAGE STEGANOGRAPHY",
            font=("Courier New", 22, "bold"),
            fg=self.COLORS['primary'],
            bg=self.COLORS['bg']
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Hide & Extract Messages in PNG Images | LSB &  Chunk Methods",
            font=("Segoe UI", 11),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['bg']
        )
        subtitle_label.pack()
        
        # Method info
        method_info = tk.Label(
            header_frame,
            text="📌 LSB: Traditional pixel-based | 📌 Injection : Custom PNG chunk",
            font=("Segoe UI", 10, "italic"),
            fg="#ffaa00",
            bg=self.COLORS['bg']
        )
        method_info.pack(pady=(5, 0))
        
        # Separator
        separator = tk.Frame(
            header_frame,
            height=2,
            bg=self.COLORS['primary']
        )
        separator.pack(fill="x", pady=(10, 0))
    
    def setup_main_content(self):
        """Setup two-column main content"""
        main_frame = tk.Frame(self, bg=self.COLORS['bg'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configure grid for two columns
        main_frame.grid_columnconfigure(0, weight=1, uniform="col")
        main_frame.grid_columnconfigure(1, weight=1, uniform="col")
        main_frame.grid_rowconfigure(0, weight=1)
        
        # ===== LEFT COLUMN - HIDE SECTION =====
        hide_frame = tk.LabelFrame(
            main_frame,
            text=" 🔒 ENCODE MESSAGE ",
            font=("Courier New", 14, "bold"),
            fg=self.COLORS['primary'],
            bg=self.COLORS['card_bg'],
            relief="groove",
            bd=2,
            padx=15,
            pady=15
        )
        hide_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # ===== RIGHT COLUMN - EXTRACT SECTION =====
        extract_frame = tk.LabelFrame(
            main_frame,
            text=" 🔓 DECODE MESSAGE ",
            font=("Courier New", 14, "bold"),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            relief="groove",
            bd=2,
            padx=15,
            pady=15
        )
        extract_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Fill both sections
        self.setup_hide_section(hide_frame)
        self.setup_extract_section(extract_frame)
    
    def setup_hide_section(self, parent):
        """Setup left column - Hide section"""
        # ===== SOURCE IMAGE SELECTION =====
        tk.Label(
            parent,
            text="Source PNG Image:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        source_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        source_frame.pack(fill="x", pady=(0, 10))
        
        self.source_entry = tk.Entry(
            source_frame,
            font=("Segoe UI", 10),
            fg=self.COLORS['text'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            width=30,
            relief="sunken"
        )
        self.source_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.source_entry.insert(0, "Select source PNG image...")
        self.source_entry.config(fg="#666666")
        
        # Add placeholder functionality
        self.source_entry.bind("<FocusIn>", self.on_source_focus_in)
        self.source_entry.bind("<FocusOut>", self.on_source_focus_out)
        
        tk.Button(
            source_frame,
            text="📁",
            font=("Arial", 11),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=4,
            command=self.select_source_image
        ).pack(side="right")
        
        # ===== OUTPUT IMAGE SELECTION =====
        tk.Label(
            parent,
            text="Output PNG Image:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        output_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        output_frame.pack(fill="x", pady=(0, 10))
        
        self.output_entry = tk.Entry(
            output_frame,
            font=("Segoe UI", 10),
            fg=self.COLORS['text'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            width=30,
            relief="sunken"
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.output_entry.insert(0, "Save encoded image as PNG...")
        self.output_entry.config(fg="#666666")
        
        # Add placeholder functionality
        self.output_entry.bind("<FocusIn>", self.on_output_focus_in)
        self.output_entry.bind("<FocusOut>", self.on_output_focus_out)
        
        tk.Button(
            output_frame,
            text="📁",
            font=("Arial", 11),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=4,
            command=self.select_output_image
        ).pack(side="right")
        
        # ===== METHOD SELECTION =====
        method_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        method_frame.pack(fill="x", pady=(0, 10))
        
        # Method selection
        tk.Label(
            method_frame,
            text="Method:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        self.method_var = tk.StringVar(value="LSB")
        
        method_subframe = tk.Frame(method_frame, bg=self.COLORS['card_bg'])
        method_subframe.pack(fill="x", pady=(0, 10))
        
        methods = [
            ("LSB (Pixel-based Hiding - 1 bit per channel)", "LSB"),
            ("Metadata Chunk (PNG Chunk)", "Metadata")
        ]
        
        for text, value in methods:
            rb = tk.Radiobutton(
                method_subframe,
                text=text,
                variable=self.method_var,
                value=value,
                font=("Segoe UI", 9),
                fg=self.COLORS['text'],
                bg=self.COLORS['card_bg'],
                activebackground=self.COLORS['card_bg'],
                activeforeground=self.COLORS['primary'],
                selectcolor=self.COLORS['bg'],
                cursor="hand2",
                command=self.on_method_change
            )
            rb.pack(anchor="w", pady=2)
        
        # LSB info label
        self.lsb_info_label = tk.Label(
            method_frame,
            text="1 LSB bit per RGB channel (3 bits per pixel)",
            font=("Segoe UI", 9, "italic"),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg']
        )
        
        # ===== PASSWORD FIELD =====
        self.password_label = tk.Label(
            parent,
            text="Encryption Key:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        )
        self.password_label.pack(anchor="w", pady=(0, 5))
        
        password_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        password_frame.pack(fill="x", pady=(0, 10))
        
        self.hide_password = tk.Entry(
            password_frame,
            font=("Consolas", 10),
            fg=self.COLORS['primary'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            show="•",
            width=25,
            relief="sunken"
        )
        self.hide_password.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.hide_password_show = False
        tk.Button(
            password_frame,
            text="👁",
            font=("Arial", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=3,
            command=self.toggle_hide_password
        ).pack(side="left")
        
        # ===== SECRET MESSAGE =====
        tk.Label(
            parent,
            text="Secret Message:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        # Text widget with scrollbar
        text_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        text_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.secret_text = tk.Text(
            text_frame,
            font=("Consolas", 10),
            fg=self.COLORS['text'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            width=40,
            height=6,
            wrap="word",
            relief="sunken"
        )
        self.secret_text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame, command=self.secret_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.secret_text.config(yscrollcommand=scrollbar.set)
        
        # Character counter
        self.hide_char_count = tk.Label(
            parent,
            text="Characters: 0",
            font=("Segoe UI", 9),
            fg="#666666",
            bg=self.COLORS['card_bg']
        )
        self.hide_char_count.pack(anchor="e", pady=(0, 10))
        
        # Bind key release to update counter
        self.secret_text.bind("<KeyRelease>", self.update_hide_counter)
        
        # ===== ENCODE BUTTON =====
        encode_btn = tk.Button(
            parent,
            text="🔒 ENCRYPT & ENCODE",
            font=("Segoe UI", 11, "bold"),
            fg=self.COLORS['bg'],
            bg=self.COLORS['accent'],
            activeforeground=self.COLORS['bg'],
            activebackground=self.COLORS['primary'],
            borderwidth=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.encode_message
        )
        encode_btn.pack(pady=(5, 0))
        
        # Hover effect
        encode_btn.bind("<Enter>", lambda e: encode_btn.config(bg=self.COLORS['primary']))
        encode_btn.bind("<Leave>", lambda e: encode_btn.config(bg=self.COLORS['accent']))
        
        # استدعاء on_method_change لتهيئة العرض الأولي
        self.on_method_change()
    
    def setup_extract_section(self, parent):
        """Setup right column - Extract section"""
        # ===== ENCODED IMAGE SELECTION =====
        tk.Label(
            parent,
            text="Encoded PNG Image:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        encoded_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        encoded_frame.pack(fill="x", pady=(0, 10))
        
        self.encoded_entry = tk.Entry(
            encoded_frame,
            font=("Segoe UI", 10),
            fg=self.COLORS['text'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            width=30,
            relief="sunken"
        )
        self.encoded_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.encoded_entry.insert(0, "Select encoded PNG image...")
        self.encoded_entry.config(fg="#666666")
        
        # Add placeholder functionality
        self.encoded_entry.bind("<FocusIn>", self.on_encoded_focus_in)
        self.encoded_entry.bind("<FocusOut>", self.on_encoded_focus_out)
        
        tk.Button(
            encoded_frame,
            text="📁",
            font=("Arial", 11),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=4,
            command=self.select_encoded_image
        ).pack(side="right")
        
        # ===== DECODING METHOD SELECTION =====
        tk.Label(
            parent,
            text="Decoding Method:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        self.decode_method_var = tk.StringVar(value="Auto")
        
        decode_method_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        decode_method_frame.pack(fill="x", pady=(0, 10))
        
        decode_methods = [
            ("Auto Detect (Recommended)", "Auto"),
        ]
        
        for text, value in decode_methods:
            rb = tk.Radiobutton(
                decode_method_frame,
                text=text,
                variable=self.decode_method_var,
                value=value,
                font=("Segoe UI", 9),
                fg=self.COLORS['text'],
                bg=self.COLORS['card_bg'],
                activebackground=self.COLORS['card_bg'],
                activeforeground=self.COLORS['primary'],
                selectcolor=self.COLORS['bg'],
                cursor="hand2"
            )
            rb.pack(anchor="w", pady=2)
        
        # ===== PASSWORD FIELD =====
        tk.Label(
            parent,
            text="Decryption Key:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        decode_password_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        decode_password_frame.pack(fill="x", pady=(0, 10))
        
        self.extract_password = tk.Entry(
            decode_password_frame,
            font=("Consolas", 10),
            fg=self.COLORS['primary'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            show="•",
            width=25,
            relief="sunken"
        )
        self.extract_password.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.extract_password_show = False
        tk.Button(
            decode_password_frame,
            text="👁",
            font=("Arial", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=3,
            command=self.toggle_extract_password
        ).pack(side="left")
        
        # Copy password button
        tk.Button(
            decode_password_frame,
            text="📋",
            font=("Arial", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            width=3,
            command=self.copy_password_from_hide
        ).pack(side="left", padx=(5, 0))
        
        # ===== DECODE BUTTON =====
        decode_btn = tk.Button(
            parent,
            text="🔓 DECRYPT & DECODE",
            font=("Segoe UI", 11, "bold"),
            fg=self.COLORS['bg'],
            bg=self.COLORS['secondary'],
            activeforeground=self.COLORS['bg'],
            activebackground=self.COLORS['primary'],
            borderwidth=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.decode_message
        )
        decode_btn.pack(pady=(0, 10))
        
        # Hover effect
        decode_btn.bind("<Enter>", lambda e: decode_btn.config(bg=self.COLORS['primary']))
        decode_btn.bind("<Leave>", lambda e: decode_btn.config(bg=self.COLORS['secondary']))
        
        # ===== RESULT AREA =====
        result_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        result_frame.pack(fill="both", expand=True)
        
        tk.Label(
            result_frame,
            text="Extracted Message:",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLORS['text'],
            bg=self.COLORS['card_bg']
        ).pack(anchor="w", pady=(0, 5))
        
        # Text widget for results with scrollbar
        result_text_frame = tk.Frame(result_frame, bg=self.COLORS['card_bg'])
        result_text_frame.pack(fill="both", expand=True)
        
        self.result_text = tk.Text(
            result_text_frame,
            font=("Consolas", 10),
            fg=self.COLORS['text'],
            bg="#0f151f",
            insertbackground=self.COLORS['primary'],
            width=40,
            height=6,
            wrap="word",
            state="disabled",
            relief="sunken"
        )
        self.result_text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        result_scrollbar = tk.Scrollbar(result_text_frame, command=self.result_text.yview)
        result_scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=result_scrollbar.set)
        
        # Result counter and method info
        self.result_info_frame = tk.Frame(result_frame, bg=self.COLORS['card_bg'])
        self.result_info_frame.pack(fill="x", pady=(5, 0))
        
        self.result_char_count = tk.Label(
            self.result_info_frame,
            text="Characters: 0",
            font=("Segoe UI", 9),
            fg="#666666",
            bg=self.COLORS['card_bg']
        )
        self.result_char_count.pack(side="left")
        
        self.result_method_label = tk.Label(
            self.result_info_frame,
            text="Method: Unknown",
            font=("Segoe UI", 9, "italic"),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg']
        )
        self.result_method_label.pack(side="right")
        
        # ===== ACTION BUTTONS =====
        action_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        action_frame.pack(fill="x", pady=(10, 0))
        
        # Copy button
        tk.Button(
            action_frame,
            text="📋 Copy",
            font=("Segoe UI", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            command=self.copy_result_to_clipboard
        ).pack(side="left", padx=(0, 5))
        
        # Save button
        tk.Button(
            action_frame,
            text="💾 Save",
            font=("Segoe UI", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            command=self.save_extracted_message
        ).pack(side="left", padx=(0, 5))
        
        # Clear button
        tk.Button(
            action_frame,
            text="🗑️ Clear",
            font=("Segoe UI", 9),
            fg=self.COLORS['accent'],
            bg=self.COLORS['card_bg'],
            activeforeground=self.COLORS['primary'],
            activebackground="#2a3546",
            borderwidth=1,
            relief="raised",
            cursor="hand2",
            command=self.clear_extract_section
        ).pack(side="left")
    
    def setup_footer(self):
        """Setup page footer"""
        footer_frame = tk.Frame(self, bg=self.COLORS['bg'], height=50)
        footer_frame.pack(fill="x", side="bottom", pady=(0, 10))
        
        # Status bar
        self.status_label = tk.Label(
            footer_frame,
            text="Ready",
            font=("Segoe UI", 9),
            fg=self.COLORS['secondary'],
            bg=self.COLORS['bg']
        )
        self.status_label.pack(side="left", padx=20)
        
        # Method info
        method_info = tk.Label(
            footer_frame,
            text="🔧 LSB: 1-bit per channel | 🔧 Metadata: PNG Chunk",
            font=("Segoe UI", 9),
            fg="#666666",
            bg=self.COLORS['bg']
        )
        method_info.pack(side="left", padx=20, expand=True)
        
        # Clear all button
        clear_all_btn = tk.Button(
            footer_frame,
            text="🗑️ Clear All",
            font=("Segoe UI", 9),
            fg=self.COLORS['accent'],
            bg=self.COLORS['bg'],
            activeforeground=self.COLORS['primary'],
            activebackground=self.COLORS['bg'],
            borderwidth=0,
            cursor="hand2",
            command=self.clear_all_fields
        )
        clear_all_btn.pack(side="right", padx=20)
    
    # ===== EVENT HANDLERS =====
    
    def on_source_focus_in(self, event=None):
        """Handle source entry focus in"""
        if self.source_entry.get() == "Select source PNG image...":
            self.source_entry.delete(0, tk.END)
            self.source_entry.config(fg=self.COLORS['text'])
    
    def on_source_focus_out(self, event=None):
        """Handle source entry focus out"""
        if self.source_entry.get() == "":
            self.source_entry.insert(0, "Select source PNG image...")
            self.source_entry.config(fg="#666666")
    
    def on_output_focus_in(self, event=None):
        """Handle output entry focus in"""
        if self.output_entry.get() == "Save encoded image as PNG...":
            self.output_entry.delete(0, tk.END)
            self.output_entry.config(fg=self.COLORS['text'])
    
    def on_output_focus_out(self, event=None):
        """Handle output entry focus out"""
        if self.output_entry.get() == "":
            self.output_entry.insert(0, "Save encoded image as PNG...")
            self.output_entry.config(fg="#666666")
    
    def on_encoded_focus_in(self, event=None):
        """Handle encoded entry focus in"""
        if self.encoded_entry.get() == "Select encoded PNG image...":
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.config(fg=self.COLORS['text'])
    
    def on_encoded_focus_out(self, event=None):
        """Handle encoded entry focus out"""
        if self.encoded_entry.get() == "":
            self.encoded_entry.insert(0, "Select encoded PNG image...")
            self.encoded_entry.config(fg="#666666")
    
    def on_method_change(self):
        """Show/Hide LSB info based on selected method"""
        if self.method_var.get() == "LSB":
            # عرض معلومات LSB
            if not self.lsb_info_label.winfo_ismapped():
                self.lsb_info_label.pack(anchor="w", pady=(0, 10))
        else:
            # إخفاء معلومات LSB
            if self.lsb_info_label.winfo_ismapped():
                self.lsb_info_label.pack_forget()
    
    # ===== FILE SELECTION METHODS =====
    
    def select_source_image(self):
        """Select source image (PNG only)"""
        file_path = filedialog.askopenfilename(
            title="Select Source PNG Image",
            filetypes=[
                ("PNG Images", "*.png"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            # Check if file is PNG
            if not file_path.lower().endswith('.png'):
                messagebox.showwarning("Invalid Format", "Please select a PNG image file.")
                return
            
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, file_path)
            self.source_entry.config(fg=self.COLORS['text'])
            self.source_image_path = file_path
            self.update_status(f"Source selected: {os.path.basename(file_path)}")
            
            # Load and display image info
            try:
                img = Image.open(file_path)
                self.current_image = img
                info = f"Size: {img.size[0]}x{img.size[1]} | Mode: {img.mode} | Format: {img.format}"
                self.update_status(info, "info")
                
                # Calculate LSB capacity
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                pixels = list(img.getdata())
                capacity = len(pixels) * 3 // 8  # 3 bits per pixel, 8 bits per byte
                self.update_status(f"LSB capacity: ~{capacity} characters", "info")
            except Exception as e:
                self.update_status(f"Error loading image: {str(e)}", "error")
    
    def select_output_image(self):
        """Select output image path (PNG only)"""
        file_path = filedialog.asksaveasfilename(
            title="Save Encoded PNG Image As",
            defaultextension=".png",
            filetypes=[
                ("PNG Images", "*.png"),
            ]
        )
        if file_path:
            # Ensure .png extension
            if not file_path.lower().endswith('.png'):
                file_path += '.png'
            
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)
            self.output_entry.config(fg=self.COLORS['text'])
            self.output_image_path = file_path
    
    def select_encoded_image(self):
        """Select encoded image for decoding (PNG only)"""
        file_path = filedialog.askopenfilename(
            title="Select Encoded PNG Image",
            filetypes=[
                ("PNG Images", "*.png"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            # Check if file is PNG
            if not file_path.lower().endswith('.png'):
                messagebox.showwarning("Invalid Format", "Please select a PNG image file.")
                return
            
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.insert(0, file_path)
            self.encoded_entry.config(fg=self.COLORS['text'])
            self.encoded_image_path = file_path
            self.update_status(f"Encoded image selected: {os.path.basename(file_path)}")
    
    # ===== PASSWORD METHODS =====
    
    def toggle_hide_password(self):
        """Toggle hide password visibility"""
        self.hide_password_show = not self.hide_password_show
        self.hide_password.config(show="" if self.hide_password_show else "•")
    
    def toggle_extract_password(self):
        """Toggle extract password visibility"""
        self.extract_password_show = not self.extract_password_show
        self.extract_password.config(show="" if self.extract_password_show else "•")
    
    def copy_password_from_hide(self):
        """Copy password from hide section to extract section"""
        password = self.hide_password.get()
        if password:
            self.extract_password.delete(0, tk.END)
            self.extract_password.insert(0, password)
            self.update_status("Password copied to extract field", "info")
    
    # ===== COUNTER METHODS =====
    
    def update_hide_counter(self, event=None):
        """Update hide section character counter"""
        text = self.secret_text.get("1.0", "end-1c")
        count = len(text)
        self.hide_char_count.config(text=f"Characters: {count}")
        
        # Change color based on length
        method = self.method_var.get()
        if method == "LSB" and self.current_image:
            max_chars = self.calculate_lsb_capacity()
            if count > max_chars:
                self.hide_char_count.config(fg=self.COLORS['accent'])
                self.hide_char_count.config(text=f"Characters: {count} (Exceeds capacity: {max_chars})")
            elif count > max_chars * 0.8:
                self.hide_char_count.config(fg="#ffaa00")
            else:
                self.hide_char_count.config(fg="#666666")
        else:  # Metadata
            if count > 10000:
                self.hide_char_count.config(fg=self.COLORS['accent'])
            elif count > 5000:
                self.hide_char_count.config(fg="#ffaa00")
            else:
                self.hide_char_count.config(fg="#666666")
    
    def calculate_lsb_capacity(self):
        """Calculate LSB capacity for current image"""
        if not self.source_image_path:
            return 0
        
        try:
            img = Image.open(self.source_image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            pixels = list(img.getdata())
            
            # Total bits available (3 bits per pixel)
            total_bits = len(pixels) * 3
            # Convert to characters (8 bits per char)
            # Account for ###END### marker (8*8 = 64 bits)
            max_chars = (total_bits - 64) // 8
            
            return max_chars
        except:
            return 0
    
    def update_result_counter(self, method="Unknown"):
        """Update result section character counter"""
        self.result_text.config(state="normal")
        text = self.result_text.get("1.0", "end-1c").strip()
        self.result_text.config(state="disabled")
        
        count = len(text)
        if text.startswith("Error:"):
            self.result_char_count.config(text="Error in extraction", fg=self.COLORS['accent'])
            self.result_method_label.config(text="Method: Failed")
        else:
            self.result_char_count.config(text=f"Characters: {count}", fg="#666666")
            self.result_method_label.config(text=f"Method: {method}")
    
    # ===== CRYPTOGRAPHY METHODS (USING FERNET) =====
    
    def generate_key(self, password: str) -> bytes:
        """Generate a Fernet key from a password"""
        # Use SHA256 to create consistent 32-byte key
        password_bytes = password.encode('utf-8')
        # Hash the password to get 32 bytes
        hashed = hashlib.sha256(password_bytes).digest()
        # Convert to base64 url-safe
        key = base64.urlsafe_b64encode(hashed)
        return key
    
    def encrypt_message(self, message: str, password: str) -> str:
        """Encrypt message using Fernet"""
        try:
            key = self.generate_key(password)
            f = Fernet(key)
            token = f.encrypt(message.encode('utf-8'))
            return token.decode('utf-8')
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def decrypt_message(self, token: str, password: str) -> str:
        """Decrypt message using Fernet"""
        try:
            key = self.generate_key(password)
            f = Fernet(key)
            message = f.decrypt(token.encode('utf-8'))
            return message.decode('utf-8')
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")
    
    # ===== LSB STEGANOGRAPHY METHODS (IMPROVED) =====
    
    def lsb_encode(self, image_path, message):
        """LSB encoding method using Fernet"""
        try:
            img = Image.open(image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Encrypt the message
            password = self.hide_password.get()
            encrypted_message = self.encrypt_message(message, password) + "###END###"
            
            # Convert to binary
            binary_message = ''.join(format(ord(c), '08b') for c in encrypted_message)
            
            pixels = list(img.getdata())
            new_pixels = []
            
            idx = 0
            for pixel in pixels:
                new_pixel = list(pixel)
                for i in range(3):  # RGB channels
                    if idx < len(binary_message):
                        # Set LSB bit
                        new_pixel[i] = (new_pixel[i] & ~1) | int(binary_message[idx])
                        idx += 1
                new_pixels.append(tuple(new_pixel))
            
            if idx < len(binary_message):
                raise ValueError(f"Message too long! Capacity: {idx//8} chars, Needed: {len(binary_message)//8} chars")
            
            # Create new image
            new_img = Image.new('RGB', img.size)
            new_img.putdata(new_pixels)
            
            return new_img
            
        except Exception as e:
            raise Exception(f"LSB encoding failed: {str(e)}")
    
    def lsb_decode(self, image_path):
        """LSB decoding method"""
        try:
            img = Image.open(image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            pixels = list(img.getdata())
            binary_message = ""
            
            # Extract LSB bits
            for pixel in pixels:
                for i in range(3):
                    binary_message += str(pixel[i] & 1)
            
            # Convert binary to string
            chars = []
            for i in range(0, len(binary_message), 8):
                byte = binary_message[i:i+8]
                if len(byte) < 8:
                    break
                chars.append(chr(int(byte, 2)))
                if ''.join(chars[-8:]).endswith("###END###"):  # نهاية الرسالة
                    break
            
            encrypted_message = ''.join(chars).replace("###END###", "")
            return encrypted_message
            
        except Exception as e:
            raise Exception(f"LSB decoding failed: {str(e)}")
    
    # ===== METADATA CHUNK METHODS =====
    
    def metadata_encode(self, image_path, message):
        """Metadata chunk encoding method"""
        try:
            # Open the image
            img = Image.open(image_path)
            
            # Create a copy to preserve original
            img_copy = img.copy()
            
            # Encrypt the message
            password = self.hide_password.get()
            encrypted_message = self.encrypt_message(message, password)
            
            # Prepare metadata
            metadata = {
                'stego': 'true',
                'method': 'metadata_chunk',
                'timestamp': os.path.getmtime(image_path),
                'message_length': len(message),
                'encrypted_message': encrypted_message
            }
            
            # Convert metadata to string
            metadata_str = json.dumps(metadata)
            
            # Create metadata text with marker
            metadata_text = f"STEGO_METADATA:{metadata_str}"
            
            # Save with metadata
            png_info = PngImagePlugin.PngInfo()
            png_info.add_text("StegoData", metadata_text)
            
            return img_copy, png_info
            
        except Exception as e:
            raise Exception(f"Metadata encoding failed: {str(e)}")
    
    def metadata_decode(self, image_path):
        """Metadata chunk decoding method"""
        try:
            # Open image with metadata
            img = Image.open(image_path)
            
            # Try to extract metadata
            metadata = img.info
            
            # Look for our custom metadata
            if 'StegoData' in metadata:
                metadata_text = metadata['StegoData']
                if metadata_text.startswith('STEGO_METADATA:'):
                    metadata_str = metadata_text[15:]  # Remove prefix
                    metadata_dict = json.loads(metadata_str)
                    
                    if metadata_dict.get('stego') == 'true':
                        encrypted_message = metadata_dict['encrypted_message']
                        return encrypted_message
            
            # Check in text chunks
            for key in metadata:
                if isinstance(metadata[key], str) and 'STEGO_METADATA:' in metadata[key]:
                    metadata_text = metadata[key]
                    metadata_str = metadata_text.split('STEGO_METADATA:')[1]
                    metadata_dict = json.loads(metadata_str)
                    
                    if metadata_dict.get('stego') == 'true':
                        encrypted_message = metadata_dict['encrypted_message']
                        return encrypted_message
            
            raise Exception("No steganography metadata found")
            
        except Exception as e:
            raise Exception(f"Metadata decoding failed: {str(e)}")
    
    # ===== MAIN FUNCTIONS =====
    
    def encode_message(self):
        """Encode (hide) message in image"""
        try:
            # Get inputs
            source_file = self.source_entry.get()
            output_file = self.output_entry.get()
            secret_text = self.secret_text.get("1.0", "end-1c").strip()
            password = self.hide_password.get()
            method = self.method_var.get()
            
            # Validate inputs
            validation_errors = []
            
            if not source_file or "Select source PNG image" in source_file:
                validation_errors.append("Please select a source PNG image.")
            
            if not output_file or "Save encoded image as PNG" in output_file:
                validation_errors.append("Please specify output PNG file path.")
            
            if not secret_text:
                validation_errors.append("Please enter a secret message.")
            
            if not password:
                validation_errors.append("Encryption key is required.")
            
            # Check file extension
            if source_file and not source_file.lower().endswith('.png'):
                validation_errors.append("Source file must be a PNG image.")
            
            if output_file and not output_file.lower().endswith('.png'):
                output_file += '.png'
                self.output_entry.delete(0, tk.END)
                self.output_entry.insert(0, output_file)
            
            if validation_errors:
                messagebox.showwarning("Input Error", "\n".join(validation_errors))
                return
            
            # Check image size for LSB
            if method == "LSB":
                capacity = self.calculate_lsb_capacity()
                if len(secret_text) > capacity:
                    messagebox.showwarning(
                        "Capacity Warning",
                        f"Image too small for message with LSB.\n\n"
                        f"Image capacity: {capacity} characters\n"
                        f"Message length: {len(secret_text)} characters\n\n"
                        f"Suggestions:\n"
                        f"• Use Metadata method instead\n"
                        f"• Use a larger image\n"
                        f"• Shorten your message"
                    )
                    return
            
            # Encode based on method
            if method == "LSB":
                encoded_image = self.lsb_encode(source_file, secret_text)
                encoded_image.save(output_file, format='PNG')
            else:  # Metadata
                encoded_image, png_info = self.metadata_encode(source_file, secret_text)
                encoded_image.save(output_file, format='PNG', pnginfo=png_info)
            
            # Show success
            img_size = os.path.getsize(output_file) / 1024  # KB
            messagebox.showinfo(
                "Success",
                f"✅ Message encoded successfully!\n\n"
                f"• Method: {method}\n"
                f"• Output: {os.path.basename(output_file)}\n"
                f"• Size: {img_size:.1f} KB\n"
                f"• Message length: {len(secret_text)} characters\n\n"
                f"⚠️ Remember your encryption key for extraction!"
            )
            
            # Auto-fill encoded image field
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.insert(0, output_file)
            self.encoded_entry.config(fg=self.COLORS['text'])
            
            # Auto-fill extract password
            self.extract_password.delete(0, tk.END)
            self.extract_password.insert(0, password)
            
            self.update_status(f"Message encoded with {method} method", "success")
            
        except ValueError as e:
            messagebox.showerror("Capacity Error", str(e))
            self.update_status("Encoding failed - capacity exceeded", "error")
        except Exception as e:
            messagebox.showerror("Encoding Error", f"An error occurred:\n\n{str(e)}")
            self.update_status("Encoding failed", "error")
    
    def decode_message(self):
        """Decode (extract) message from image"""
        try:
            # Get inputs
            encoded_file = self.encoded_entry.get()
            password = self.extract_password.get()
            
            # Validate inputs
            if not encoded_file or "Select encoded PNG image" in encoded_file:
                messagebox.showwarning("Input Error", "Please select an encoded PNG image.")
                return
            
            if not password:
                messagebox.showwarning("Security Error", "Decryption key is required.")
                return
            
            # Check file extension
            if not encoded_file.lower().endswith('.png'):
                messagebox.showwarning("Invalid Format", "Only PNG files are supported.")
                return
            
            extracted_encrypted = ""
            method_used = "Unknown"
            decoded_successfully = False
            
            # Try Metadata method first
            try:
                extracted_encrypted = self.metadata_decode(encoded_file)
                if extracted_encrypted:
                    method_used = "Metadata"
                    decoded_successfully = True
            except Exception as e:
                print(f"Metadata decode failed: {e}")
                pass
            
            # If metadata failed, try LSB method
            if not decoded_successfully:
                try:
                    extracted_encrypted = self.lsb_decode(encoded_file)
                    if extracted_encrypted:
                        method_used = "LSB"
                        decoded_successfully = True
                except Exception as e:
                    print(f"LSB decode failed: {e}")
                    pass
            
            if not decoded_successfully or not extracted_encrypted:
                raise Exception("Could not extract message. Image may not contain hidden data.")
            
            # Decrypt the message
            decrypted_text = self.decrypt_message(extracted_encrypted, password)
            
            # Display result
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", decrypted_text)
            self.result_text.config(state="disabled")
            
            # Update counter and method info
            self.update_result_counter(method_used)
            
            # Update status
            self.update_status(f"Message extracted ({len(decrypted_text)} chars) using {method_used}", "success")
            
        except Exception as e:
            error_msg = str(e)
            
            # Display error in result area
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", f"Error: {error_msg}")
            self.result_text.config(state="disabled")
            
            # Update counter
            self.update_result_counter("Failed")
            
            # Show appropriate error message
            if "password" in error_msg.lower() or "decrypt" in error_msg.lower():
                messagebox.showerror("Decryption Error", "Incorrect decryption key!")
            elif "capacity" in error_msg.lower():
                messagebox.showerror("Capacity Error", error_msg)
            elif "PNG" in error_msg:
                messagebox.showerror("Format Error", "Please use PNG format only.")
            else:
                messagebox.showerror("Decoding Error", f"Failed to decode message:\n\n{error_msg}")
            
            self.update_status("Decoding failed", "error")
    
    # ===== UTILITY FUNCTIONS =====
    
    def copy_result_to_clipboard(self):
        """Copy extracted message to clipboard"""
        self.result_text.config(state="normal")
        text = self.result_text.get("1.0", "end-1c").strip()
        self.result_text.config(state="disabled")
        
        if text and not text.startswith("Error:"):
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update_status("Copied to clipboard", "success")
        elif text.startswith("Error:"):
            messagebox.showwarning("Cannot Copy", "Cannot copy error message.")
    
    def save_extracted_message(self):
        """Save extracted message to file"""
        self.result_text.config(state="normal")
        text = self.result_text.get("1.0", "end-1c").strip()
        self.result_text.config(state="disabled")
        
        if text and not text.startswith("Error:"):
            file_path = filedialog.asksaveasfilename(
                title="Save Extracted Message",
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    self.update_status(f"Message saved to {os.path.basename(file_path)}", "success")
                except Exception as e:
                    messagebox.showerror("Save Error", f"Failed to save file:\n{str(e)}")
        elif text.startswith("Error:"):
            messagebox.showwarning("Cannot Save", "Cannot save error message.")
    
    def clear_extract_section(self):
        """Clear only extract section fields"""
        self.encoded_entry.delete(0, tk.END)
        self.encoded_entry.insert(0, "Select encoded PNG image...")
        self.encoded_entry.config(fg="#666666")
        
        self.extract_password.delete(0, tk.END)
        
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")
        
        self.result_char_count.config(text="Characters: 0", fg="#666666")
        self.result_method_label.config(text="Method: Unknown")
        
        self.encoded_image_path = ""
        
        self.update_status("Extract section cleared", "info")
    
    def clear_all_fields(self):
        """Clear all fields in both sections"""
        # Clear hide section
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, "Select source PNG image...")
        self.source_entry.config(fg="#666666")
        
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, "Save encoded image as PNG...")
        self.output_entry.config(fg="#666666")
        
        self.hide_password.delete(0, tk.END)
        
        self.secret_text.delete("1.0", tk.END)
        self.hide_char_count.config(text="Characters: 0", fg="#666666")
        
        # Clear extract section
        self.clear_extract_section()
        
        # Reset state variables
        self.source_image_path = ""
        self.output_image_path = ""
        self.current_image = None
        
        # Reset method selections
        self.method_var.set("LSB")
        self.decode_method_var.set("Auto")
        
        self.update_status("All fields cleared", "info")
    
    def update_status(self, message, status_type="info"):
        """Update status label"""
        colors = {
            "info": self.COLORS['secondary'],
            "success": self.COLORS['primary'],
            "error": self.COLORS['accent'],
            "warning": "#ffaa00"
        }
        
        color = colors.get(status_type, self.COLORS['secondary'])
        self.status_label.config(text=message, fg=color)


