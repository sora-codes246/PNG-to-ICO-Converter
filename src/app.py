import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import threading
import subprocess


# ============================================================
# CONFIGURATION
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_NAME = "PNG → ICO Converter"


# ============================================================
# MAIN APPLICATION
# ============================================================

class PNGtoICOApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("1050x700")
        self.minsize(900, 620)

        self.selected_image_path = None
        self.preview_image = None
        self.output_path = None

        self.setup_ui()

    # ========================================================
    # UI SETUP
    # ========================================================

    def setup_ui(self):

        self.configure(bg="#0b0f19")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ====================================================
        # HEADER
        # ====================================================

        header = ctk.CTkFrame(
            self,
            height=80,
            corner_radius=0,
            fg_color="#111827"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        header.grid_columnconfigure(1, weight=1)

        logo = ctk.CTkLabel(
            header,
            text="◈",
            font=("Segoe UI", 32, "bold"),
            text_color="#60a5fa"
        )

        logo.grid(
            row=0,
            column=0,
            padx=(30, 12),
            pady=15
        )

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_frame.grid(
            row=0,
            column=1,
            sticky="w"
        )

        title = ctk.CTkLabel(
            title_frame,
            text="PNG → ICO Converter",
            font=("Segoe UI", 23, "bold"),
            text_color="#f8fafc"
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            title_frame,
            text="Create Windows icons from your images",
            font=("Segoe UI", 12),
            text_color="#94a3b8"
        )

        subtitle.pack(anchor="w")

        version = ctk.CTkLabel(
            header,
            text="v1.0",
            font=("Segoe UI", 11),
            text_color="#64748b"
        )

        version.grid(
            row=0,
            column=2,
            padx=30
        )

        # ====================================================
        # CONTENT
        # ====================================================

        content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=25
        )

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        # ====================================================
        # LEFT PANEL
        # ====================================================

        left_panel = ctk.CTkFrame(
            content,
            corner_radius=18,
            fg_color="#111827"
        )

        left_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12)
        )

        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)

        left_title = ctk.CTkLabel(
            left_panel,
            text="IMAGE",
            font=("Segoe UI", 12, "bold"),
            text_color="#64748b"
        )

        left_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=25,
            pady=(25, 10)
        )

        # ====================================================
        # IMAGE PREVIEW
        # ====================================================

        self.preview_frame = ctk.CTkFrame(
            left_panel,
            corner_radius=12,
            fg_color="#0b0f19"
        )

        self.preview_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=10
        )

        self.preview_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.preview_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="🖼️\n\nNo image selected\n\nClick Browse Image to choose a file",
            font=("Segoe UI", 16),
            text_color="#64748b",
            justify="center",
            fg_color="transparent"
        )

        self.preview_label.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # ====================================================
        # IMAGE INFO
        # ====================================================

        self.image_info = ctk.CTkLabel(
            left_panel,
            text="No image selected",
            font=("Segoe UI", 11),
            text_color="#64748b"
        )

        self.image_info.grid(
            row=2,
            column=0,
            pady=(2, 5)
        )

        # ====================================================
        # BROWSE
        # ====================================================

        self.browse_button = ctk.CTkButton(
            left_panel,
            text="📂  Browse Image",
            height=45,
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            command=self.select_image
        )

        self.browse_button.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=(5, 25)
        )

        # ====================================================
        # RIGHT PANEL
        # ====================================================

        right_panel = ctk.CTkFrame(
            content,
            corner_radius=18,
            fg_color="#111827"
        )

        right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(12, 0)
        )

        right_panel.grid_columnconfigure(
            0,
            weight=1
        )

        settings_title = ctk.CTkLabel(
            right_panel,
            text="ICO SETTINGS",
            font=("Segoe UI", 12, "bold"),
            text_color="#64748b"
        )

        settings_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=25,
            pady=(25, 20)
        )

        # ====================================================
        # SIZE
        # ====================================================

        size_label = ctk.CTkLabel(
            right_panel,
            text="Icon Size",
            font=("Segoe UI", 13, "bold")
        )

        size_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=25
        )

        self.size_menu = ctk.CTkOptionMenu(
            right_panel,
            values=[
                "16 × 16",
                "32 × 32",
                "48 × 48",
                "64 × 64",
                "128 × 128",
                "256 × 256",
                "Multi-size ICO"
            ],
            height=42,
            corner_radius=10
        )

        self.size_menu.set("256 × 256")

        self.size_menu.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=(8, 20)
        )

        # ====================================================
        # TRANSPARENCY
        # ====================================================

        self.transparency = ctk.CTkCheckBox(
            right_panel,
            text="Preserve transparency",
            font=("Segoe UI", 13)
        )

        self.transparency.select()

        self.transparency.grid(
            row=3,
            column=0,
            sticky="w",
            padx=25,
            pady=10
        )

        # ====================================================
        # OUTPUT
        # ====================================================

        output_label = ctk.CTkLabel(
            right_panel,
            text="Output Location",
            font=("Segoe UI", 13, "bold")
        )

        output_label.grid(
            row=4,
            column=0,
            sticky="w",
            padx=25,
            pady=(25, 8)
        )

        self.output_entry = ctk.CTkEntry(
            right_panel,
            height=42,
            corner_radius=10,
            placeholder_text="Same folder as source image"
        )

        self.output_entry.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=25
        )

        self.output_button = ctk.CTkButton(
            right_panel,
            text="Choose Folder",
            height=38,
            corner_radius=10,
            fg_color="#1e293b",
            hover_color="#334155",
            command=self.choose_output
        )

        self.output_button.grid(
            row=6,
            column=0,
            sticky="ew",
            padx=25,
            pady=(8, 20)
        )

        # ====================================================
        # CONVERT
        # ====================================================

        self.convert_button = ctk.CTkButton(
            right_panel,
            text="✨  CONVERT TO ICO",
            height=55,
            corner_radius=12,
            font=("Segoe UI", 15, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.convert_image
        )

        self.convert_button.grid(
            row=7,
            column=0,
            sticky="ew",
            padx=25,
            pady=(10, 10)
        )

        # ====================================================
        # PROGRESS
        # ====================================================

        self.progress = ctk.CTkProgressBar(
            right_panel,
            height=8,
            corner_radius=5
        )

        self.progress.set(0)

        self.progress.grid(
            row=8,
            column=0,
            sticky="ew",
            padx=25,
            pady=(10, 5)
        )

        # ====================================================
        # STATUS
        # ====================================================

        self.status_label = ctk.CTkLabel(
            right_panel,
            text="Ready",
            font=("Segoe UI", 12),
            text_color="#64748b"
        )

        self.status_label.grid(
            row=9,
            column=0,
            pady=(5, 20)
        )

    # ========================================================
    # SELECT IMAGE
    # ========================================================

    def select_image(self):

        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("PNG Images", "*.png"),
                (
                    "Image Files",
                    "*.png;*.jpg;*.jpeg;*.webp;*.bmp"
                ),
                ("All Files", "*.*")
            ]
        )

        if path:
            self.load_image(path)

    # ========================================================
    # LOAD IMAGE
    # ========================================================

    def load_image(self, path):

        try:

            image = Image.open(path)

            self.selected_image_path = path

            preview = image.copy()

            preview.thumbnail(
                (400, 400)
            )

            self.preview_image = ImageTk.PhotoImage(
                preview
            )

            self.preview_label.configure(
                image=self.preview_image,
                text=""
            )

            width, height = image.size

            file_size = os.path.getsize(path)

            if file_size < 1024 * 1024:

                size_text = (
                    f"{file_size / 1024:.1f} KB"
                )

            else:

                size_text = (
                    f"{file_size / (1024 * 1024):.1f} MB"
                )

            self.image_info.configure(
                text=f"{width} × {height} px  •  {size_text}"
            )

            self.status_label.configure(
                text=f"✓ Loaded {os.path.basename(path)}",
                text_color="#60a5fa"
            )

        except Exception as error:

            messagebox.showerror(
                "Unable to load image",
                f"Could not load the image.\n\n{error}"
            )

    # ========================================================
    # OUTPUT
    # ========================================================

    def choose_output(self):

        folder = filedialog.askdirectory(
            title="Choose Output Folder"
        )

        if folder:

            self.output_entry.delete(
                0,
                "end"
            )

            self.output_entry.insert(
                0,
                folder
            )

            self.status_label.configure(
                text="Output folder selected"
            )

    # ========================================================
    # CONVERT
    # ========================================================

    def convert_image(self):

        if not self.selected_image_path:

            messagebox.showwarning(
                "No Image Selected",
                "Please select an image first."
            )

            return

        self.convert_button.configure(
            state="disabled",
            text="⏳  CONVERTING..."
        )

        self.browse_button.configure(
            state="disabled"
        )

        self.output_button.configure(
            state="disabled"
        )

        self.size_menu.configure(
            state="disabled"
        )

        self.progress.set(0)

        self.status_label.configure(
            text="Starting conversion...",
            text_color="#60a5fa"
        )

        threading.Thread(
            target=self.perform_conversion,
            daemon=True
        ).start()

    # ========================================================
    # CONVERSION ENGINE
    # ========================================================

    def perform_conversion(self):

        try:

            self.after(
                0,
                lambda: self.update_progress(
                    0.15,
                    "Reading image..."
                )
            )

            image = Image.open(
                self.selected_image_path
            )

            if self.transparency.get():

                image = image.convert("RGBA")

            else:

                image = image.convert("RGB")

            self.after(
                0,
                lambda: self.update_progress(
                    0.35,
                    "Preparing icon..."
                )
            )

            selected_size = self.size_menu.get()

            if selected_size == "Multi-size ICO":

                sizes = [
                    (16, 16),
                    (32, 32),
                    (48, 48),
                    (64, 64),
                    (128, 128),
                    (256, 256)
                ]

            else:

                size_number = int(
                    selected_size.split("×")[0].strip()
                )

                sizes = [
                    (size_number, size_number)
                ]

            self.after(
                0,
                lambda: self.update_progress(
                    0.55,
                    "Generating icon..."
                )
            )

            source_directory = os.path.dirname(
                self.selected_image_path
            )

            custom_directory = (
                self.output_entry.get().strip()
            )

            if custom_directory:

                output_directory = custom_directory

            else:

                output_directory = source_directory

            os.makedirs(
                output_directory,
                exist_ok=True
            )

            base_name = os.path.splitext(
                os.path.basename(
                    self.selected_image_path
                )
            )[0]

            output_path = os.path.join(
                output_directory,
                base_name + ".ico"
            )

            self.after(
                0,
                lambda: self.update_progress(
                    0.75,
                    "Writing ICO file..."
                )
            )

            image.save(
                output_path,
                format="ICO",
                sizes=sizes
            )

            self.output_path = output_path

            self.after(
                0,
                lambda: self.update_progress(
                    1.0,
                    "Conversion complete!"
                )
            )

            self.after(
                400,
                self.show_success
            )

        except Exception as error:

            self.after(
                0,
                lambda: self.conversion_error(
                    str(error)
                )
            )

    # ========================================================
    # PROGRESS
    # ========================================================

    def update_progress(self, value, text):

        self.progress.set(value)

        self.status_label.configure(
            text=text
        )

    # ========================================================
    # SUCCESS
    # ========================================================

    def show_success(self):

        self.convert_button.configure(
            state="normal",
            text="✨  CONVERT TO ICO"
        )

        self.browse_button.configure(
            state="normal"
        )

        self.output_button.configure(
            state="normal"
        )

        self.size_menu.configure(
            state="normal"
        )

        success = ctk.CTkToplevel(
            self
        )

        success.title(
            "Conversion Complete"
        )

        success.geometry(
            "520x390"
        )

        success.resizable(
            False,
            False
        )

        success.configure(
            fg_color="#0b0f19"
        )

        success.transient(self)
        success.grab_set()

        check = ctk.CTkLabel(
            success,
            text="✓",
            font=("Segoe UI", 52, "bold"),
            text_color="#4ade80"
        )

        check.pack(
            pady=(30, 5)
        )

        title = ctk.CTkLabel(
            success,
            text="Conversion Complete!",
            font=("Segoe UI", 22, "bold"),
            text_color="#f8fafc"
        )

        title.pack()

        filename = ctk.CTkLabel(
            success,
            text=os.path.basename(
                self.output_path
            ),
            font=("Segoe UI", 13),
            text_color="#60a5fa"
        )

        filename.pack(
            pady=(8, 15)
        )

        path_label = ctk.CTkLabel(
            success,
            text=self.output_path,
            font=("Segoe UI", 10),
            text_color="#64748b",
            wraplength=450
        )

        path_label.pack(
            padx=25,
            pady=5
        )

        open_button = ctk.CTkButton(
            success,
            text="📂  Open Output Folder",
            height=45,
            corner_radius=10,
            command=self.open_output_folder
        )

        open_button.pack(
            fill="x",
            padx=45,
            pady=(20, 8)
        )

        done_button = ctk.CTkButton(
            success,
            text="Done",
            height=40,
            corner_radius=10,
            fg_color="#1e293b",
            hover_color="#334155",
            command=success.destroy
        )

        done_button.pack(
            fill="x",
            padx=45
        )

        self.status_label.configure(
            text="✓ Conversion complete",
            text_color="#4ade80"
        )

    # ========================================================
    # OPEN OUTPUT
    # ========================================================

    def open_output_folder(self):

        if not self.output_path:
            return

        try:

            subprocess.Popen(
                [
                    "explorer",
                    "/select,",
                    self.output_path
                ]
            )

        except Exception:

            os.startfile(
                os.path.dirname(
                    self.output_path
                )
            )

    # ========================================================
    # ERROR
    # ========================================================

    def conversion_error(self, error):

        self.convert_button.configure(
            state="normal",
            text="✨  CONVERT TO ICO"
        )

        self.browse_button.configure(
            state="normal"
        )

        self.output_button.configure(
            state="normal"
        )

        self.size_menu.configure(
            state="normal"
        )

        self.progress.set(0)

        self.status_label.configure(
            text="Conversion failed",
            text_color="#f87171"
        )

        messagebox.showerror(
            "Conversion Failed",
            f"Something went wrong.\n\n{error}"
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    app = PNGtoICOApp()

    app.mainloop()