import sys
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from PIL import Image, ImageGrab

# Adjust paths to run cleanly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from i18n import I18N
from widgets import DigitalRainCanvas, ScanningEffect, CyberButton
from automation import GlobalHotkeyTracker, AutoClicker, MacroRecorder, SmartClipboard
from vault import SecureVault

class NeoGenCyberToolbox(ctk.CTk):
    """
    NEO-GEN CYBER TOOLBOX Main Application Frame.
    Sleek custom styles, dynamic multi-language instant-switching,
    real-time automated tests, animations and matrix background rain.
    """
    def __init__(self):
        super().__init__()

        # Configure initial screen values
        self.title("NEO-GEN CYBER TOOLBOX")
        self.geometry("1100x750")
        self.configure(fg_color="#000000")

        # Initialize modules
        self.i18n = I18N("en")
        self.auto_clicker = AutoClicker()
        self.macro_recorder = MacroRecorder()
        self.clipboard = SmartClipboard()

        self.last_coords = (0, 0)
        self.macro_is_recording = False

        # Start Global F9 Hotkey listener
        self.hotkey_tracker = GlobalHotkeyTracker(self.on_f9_captured)
        self.hotkey_tracker.start()

        # Setup modern dark theme variables
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        # Build UI layout
        self.build_ui()

        # Register i18n update handler
        self.i18n.register_callback(self.refresh_ui_text)
        self.refresh_ui_text()

    def build_ui(self):
        # Background matrix rain
        self.bg_canvas = DigitalRainCanvas(self)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Main overlay container frame
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(x=20, y=20, relwidth=0.96, relheight=0.94)

        # Title Header
        self.title_label = ctk.CTkLabel(
            self.main_container,
            text=self.i18n.get("app_title"),
            font=("Courier", 26, "bold"),
            text_color="#00FF00"
        )
        self.title_label.pack(pady=10)

        # Dynamic Tab Controller
        self.tab_view = ctk.CTkTabview(
            self.main_container,
            fg_color="#000b00",
            segmented_button_fg_color="#001400",
            segmented_button_selected_color="#00FF00",
            segmented_button_selected_hover_color="#008800",
            segmented_button_unselected_color="#002200",
            segmented_button_unselected_hover_color="#004400",
            text_color="#00FF00"
        )
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_view.add("AUTOMATION")
        self.tab_view.add("THE VAULT")
        self.tab_view.add("SYSTEM LOCALE")

        self.setup_automation_tab()
        self.setup_vault_tab()
        self.setup_i18n_tab()

    def setup_automation_tab(self):
        tab = self.tab_view.tab("AUTOMATION")

        # Left Panel (F9 Coordinates & Clicker)
        left_frame = ctk.CTkFrame(tab, fg_color="#001100", border_color="#00FF00", border_width=1)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.f9_title = ctk.CTkLabel(left_frame, text="", font=("Courier", 15, "bold"), text_color="#00FF00")
        self.f9_title.pack(pady=5)

        self.f9_info = ctk.CTkLabel(left_frame, text="", font=("Courier", 12), text_color="#00AA00")
        self.f9_info.pack(pady=5)

        self.f9_status = ctk.CTkLabel(left_frame, text="", font=("Courier", 12, "italic"), text_color="#00FF00")
        self.f9_status.pack(pady=5)

        self.f9_coords_lbl = ctk.CTkLabel(left_frame, text="", font=("Courier", 13, "bold"), text_color="#00FF00")
        self.f9_coords_lbl.pack(pady=10)

        # Auto clicker configs
        self.click_title = ctk.CTkLabel(left_frame, text="", font=("Courier", 14, "bold"), text_color="#00FF00")
        self.click_title.pack(pady=10)

        self.lbl_interval = ctk.CTkLabel(left_frame, text="", font=("Courier", 12), text_color="#00AA00")
        self.lbl_interval.pack()
        self.click_interval_ent = ctk.CTkEntry(left_frame, placeholder_text="1.0", fg_color="#000000", text_color="#00FF00")
        self.click_interval_ent.insert(0, "1.0")
        self.click_interval_ent.pack(pady=5)

        self.lbl_click_type = ctk.CTkLabel(left_frame, text="", font=("Courier", 12), text_color="#00AA00")
        self.lbl_click_type.pack()
        self.click_type_combo = ctk.CTkComboBox(left_frame, values=["Left", "Right"], fg_color="#000000", text_color="#00FF00")
        self.click_type_combo.pack(pady=5)

        self.btn_clicker_start = CyberButton(left_frame, text="", command=self.start_auto_clicker)
        self.btn_clicker_start.pack(pady=5)

        self.btn_clicker_stop = CyberButton(left_frame, text="", command=self.stop_auto_clicker)
        self.btn_clicker_stop.pack(pady=5)

        # Right Panel (Macro and Utilities)
        right_frame = ctk.CTkFrame(tab, fg_color="#001100", border_color="#00FF00", border_width=1)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.macro_lbl = ctk.CTkLabel(right_frame, text="", font=("Courier", 15, "bold"), text_color="#00FF00")
        self.macro_lbl.pack(pady=5)

        self.macro_status_lbl = ctk.CTkLabel(right_frame, text="", font=("Courier", 12, "italic"), text_color="#00AA00")
        self.macro_status_lbl.pack(pady=5)

        self.btn_rec_macro = CyberButton(right_frame, text="", command=self.toggle_record_macro)
        self.btn_rec_macro.pack(pady=5)

        self.btn_play_macro = CyberButton(right_frame, text="", command=self.play_macro)
        self.btn_play_macro.pack(pady=5)

        self.btn_clear_macro = CyberButton(right_frame, text="", command=self.clear_macro)
        self.btn_clear_macro.pack(pady=5)

        # Smart Clipboard historical log
        self.clip_lbl = ctk.CTkLabel(right_frame, text="", font=("Courier", 14, "bold"), text_color="#00FF00")
        self.clip_lbl.pack(pady=10)

        self.clip_listbox = tk.Listbox(right_frame, bg="#000000", fg="#00FF00", selectbackground="#00FF00", selectforeground="#000000", highlightcolor="#00FF00", font=("Courier", 10))
        self.clip_listbox.pack(fill="both", expand=True, padx=10, pady=5)

        self.btn_copy_clip = CyberButton(right_frame, text="", command=self.copy_selected_clipboard)
        self.btn_copy_clip.pack(pady=5)

        # Color Picker / OCR Quick Tools
        self.color_title_lbl = ctk.CTkLabel(right_frame, text="", font=("Courier", 14, "bold"), text_color="#00FF00")
        self.color_title_lbl.pack(pady=5)
        self.btn_pick_color = CyberButton(right_frame, text="", command=self.trigger_color_picker)
        self.btn_pick_color.pack(pady=5)

        self.ocr_lbl_title = ctk.CTkLabel(right_frame, text="", font=("Courier", 14, "bold"), text_color="#00FF00")
        self.ocr_lbl_title.pack(pady=5)
        self.btn_run_ocr = CyberButton(right_frame, text="", command=self.trigger_quick_ocr)
        self.btn_run_ocr.pack(pady=5)

        # Periodically refresh clipboard log
        self.update_clipboard_view()

    def setup_vault_tab(self):
        tab = self.tab_view.tab("THE VAULT")

        # Left Panel (AES Secure message and archiving)
        v_left = ctk.CTkFrame(tab, fg_color="#001100", border_color="#00FF00", border_width=1)
        v_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.enc_title_lbl = ctk.CTkLabel(v_left, text="", font=("Courier", 15, "bold"), text_color="#00FF00")
        self.enc_title_lbl.pack(pady=5)

        self.key_lbl_title = ctk.CTkLabel(v_left, text="", font=("Courier", 12), text_color="#00AA00")
        self.key_lbl_title.pack()
        self.vault_key_ent = ctk.CTkEntry(v_left, show="*", fg_color="#000000", text_color="#00FF00")
        self.vault_key_ent.pack(pady=5)

        self.msg_input_lbl = ctk.CTkLabel(v_left, text="", font=("Courier", 12), text_color="#00AA00")
        self.msg_input_lbl.pack()
        self.vault_text_box = ctk.CTkTextbox(v_left, height=120, fg_color="#000000", text_color="#00FF00", font=("Courier", 11))
        self.vault_text_box.pack(fill="x", padx=10, pady=5)

        btn_frame = ctk.CTkFrame(v_left, fg_color="transparent")
        btn_frame.pack(pady=5)
        self.btn_encrypt = CyberButton(btn_frame, text="", command=self.vault_encrypt)
        self.btn_encrypt.pack(side="left", padx=5)
        self.btn_decrypt = CyberButton(btn_frame, text="", command=self.vault_decrypt)
        self.btn_decrypt.pack(side="right", padx=5)

        # Secure Archiving
        self.arch_title_lbl = ctk.CTkLabel(v_left, text="", font=("Courier", 14, "bold"), text_color="#00FF00")
        self.arch_title_lbl.pack(pady=10)

        self.arch_progress = ctk.CTkProgressBar(v_left, progress_color="#00FF00", fg_color="#002200")
        self.arch_progress.set(0)
        self.arch_progress.pack(fill="x", padx=10, pady=5)

        self.btn_create_arch = CyberButton(v_left, text="", command=self.vault_create_archive)
        self.btn_create_arch.pack(pady=5)
        self.btn_extract_arch = CyberButton(v_left, text="", command=self.vault_extract_archive)
        self.btn_extract_arch.pack(pady=5)

        # Right Panel (Converters and Cyber-ops)
        v_right = ctk.CTkFrame(tab, fg_color="#001100", border_color="#00FF00", border_width=1)
        v_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.conv_lbl_title = ctk.CTkLabel(v_right, text="", font=("Courier", 14, "bold"), text_color="#00FF00")
        self.conv_lbl_title.pack(pady=10)
        self.btn_convert_media = CyberButton(v_right, text="", command=self.vault_convert_media)
        self.btn_convert_media.pack(pady=5)

        # Cyber-Ops: Hash generator, EXIF, Stego
        self.cyber_ops_lbl = ctk.CTkLabel(v_right, text="", font=("Courier", 14, "bold"), text_color="#00FF00")
        self.cyber_ops_lbl.pack(pady=10)

        self.btn_gen_hash = CyberButton(v_right, text="", command=self.vault_generate_hash)
        self.btn_gen_hash.pack(pady=5)
        self.btn_exif_rm = CyberButton(v_right, text="", command=self.vault_remove_exif)
        self.btn_exif_rm.pack(pady=5)
        self.btn_stego = CyberButton(v_right, text="", command=self.vault_stego_dialog)
        self.btn_stego.pack(pady=5)

        # Futuristic Live Scanning animation feedback
        self.scanning_radar = ScanningEffect(v_right)
        self.scanning_radar.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_i18n_tab(self):
        tab = self.tab_view.tab("SYSTEM LOCALE")

        self.lang_title_lbl = ctk.CTkLabel(tab, text="", font=("Courier", 18, "bold"), text_color="#00FF00")
        self.lang_title_lbl.pack(pady=20)

        # Custom Matrix-Grid representing language selection
        grid_frame = ctk.CTkFrame(tab, fg_color="transparent")
        grid_frame.pack(pady=10)

        row = 0
        col = 0
        for code, name in I18N.LANGUAGES.items():
            btn = CyberButton(
                grid_frame,
                text=name,
                width=160,
                height=45,
                command=lambda c=code: self.i18n.set_language(c)
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def refresh_ui_text(self):
        """
        Updates every label and button text dynamically on localized state change
        """
        self.title(self.i18n.get("app_title"))
        self.title_label.configure(text=self.i18n.get("app_title"))

        # Automation strings
        self.f9_title.configure(text=self.i18n.get("hotkey_title"))
        self.f9_info.configure(text=self.i18n.get("hotkey_info"))
        self.f9_status.configure(text=self.i18n.get("hotkey_status"))
        self.f9_coords_lbl.configure(text=self.i18n.get("last_coords", self.last_coords[0], self.last_coords[1]))

        self.click_title.configure(text=self.i18n.get("clicker_title"))
        self.lbl_interval.configure(text=self.i18n.get("clicker_interval"))
        self.lbl_click_type.configure(text=self.i18n.get("click_button"))
        self.btn_clicker_start.configure(text=self.i18n.get("start_clicker"))
        self.btn_clicker_stop.configure(text=self.i18n.get("stop_clicker"))

        self.macro_lbl.configure(text=self.i18n.get("macro_title"))
        self.btn_rec_macro.configure(text=self.i18n.get("record_macro") if not self.macro_is_recording else "STOP MACRO")
        self.btn_play_macro.configure(text=self.i18n.get("play_macro"))
        self.btn_clear_macro.configure(text=self.i18n.get("clear_macro"))

        self.clip_lbl.configure(text=self.i18n.get("clipboard_mgr"))
        self.btn_copy_clip.configure(text=self.i18n.get("clipboard_copy"))

        self.color_title_lbl.configure(text=self.i18n.get("color_picker"))
        self.btn_pick_color.configure(text=self.i18n.get("pick_color_btn"))

        self.ocr_lbl_title.configure(text=self.i18n.get("ocr_title"))
        self.btn_run_ocr.configure(text=self.i18n.get("ocr_btn"))

        # Vault strings
        self.enc_title_lbl.configure(text=self.i18n.get("enc_dec_msg"))
        self.key_lbl_title.configure(text=self.i18n.get("key_label"))
        self.msg_input_lbl.configure(text=self.i18n.get("msg_input"))
        self.btn_encrypt.configure(text=self.i18n.get("encrypt_btn"))
        self.btn_decrypt.configure(text=self.i18n.get("decrypt_btn"))

        self.arch_title_lbl.configure(text=self.i18n.get("archive_title"))
        self.btn_create_arch.configure(text=self.i18n.get("archive_btn"))
        self.btn_extract_arch.configure(text=self.i18n.get("extract_btn"))

        self.conv_lbl_title.configure(text=self.i18n.get("universal_conv"))
        self.btn_convert_media.configure(text=self.i18n.get("conv_btn"))

        self.cyber_ops_lbl.configure(text=self.i18n.get("cyber_ops"))
        self.btn_gen_hash.configure(text=self.i18n.get("hash_btn"))
        self.btn_exif_rm.configure(text=self.i18n.get("exif_btn"))
        self.btn_stego.configure(text=self.i18n.get("stego_btn"))

        # Locale strings
        self.lang_title_lbl.configure(text=self.i18n.get("lang_select_title"))

    # Automation controller methods
    def on_f9_captured(self, x, y):
        self.last_coords = (x, y)
        self.f9_coords_lbl.configure(text=self.i18n.get("last_coords", x, y))

    def start_auto_clicker(self):
        try:
            interval = float(self.click_interval_ent.get())
        except ValueError:
            interval = 1.0
        click_type = self.click_type_combo.get().lower()
        self.auto_clicker.start(interval, click_type, self.last_coords)

    def stop_auto_clicker(self):
        self.auto_clicker.stop()

    def toggle_record_macro(self):
        if not self.macro_is_recording:
            self.macro_recorder.start_recording()
            self.macro_is_recording = True
            self.macro_status_lbl.configure(text="Macro Status: Recording...")
            self.btn_rec_macro.configure(text="STOP MACRO")
        else:
            self.macro_recorder.stop_recording()
            self.macro_is_recording = False
            self.macro_status_lbl.configure(text="Macro Status: Macro Saved")
            self.btn_rec_macro.configure(text=self.i18n.get("record_macro"))

    def play_macro(self):
        self.macro_recorder.play()

    def clear_macro(self):
        self.macro_recorder.clear()
        self.macro_status_lbl.configure(text="Macro Status: Cleared")

    def update_clipboard_view(self):
        history = self.clipboard.get_history()
        self.clip_listbox.delete(0, "end")
        for idx, item in enumerate(history[-20:]):  # Display top 20 items
            self.clip_listbox.insert("end", f"[{idx+1}] {item[:50]}...")
        self.after(2000, self.update_clipboard_view)

    def copy_selected_clipboard(self):
        try:
            sel = self.clip_listbox.curselection()
            if sel:
                history = self.clipboard.get_history()
                item = history[-20:][sel[0]]
                self.clipboard.copy_item(item)
        except Exception:
            pass

    def trigger_color_picker(self):
        """
        Global Color Picker using screen screenshot analysis.
        """
        try:
            # Capture target pixel under mouse dynamically
            mx, my = self.last_coords
            screenshot = ImageGrab.grab(bbox=(mx-1, my-1, mx+2, my+2))
            rgb = screenshot.getpixel((1, 1))
            hex_col = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            messagebox.showinfo("Color Picker Result", f"Coordinates: X:{mx} Y:{my}\nRGB: {rgb}\nHEX: {hex_col}")
            self.clipboard.copy_item(hex_col)
        except Exception as e:
            messagebox.showerror("Error", f"Could not pick color: {str(e)}")

    def trigger_quick_ocr(self):
        """
        Runs screen OCR analysis utilizing standard easyocr / pytesseract if available.
        Otherwise falls back cleanly to safe demo verification.
        """
        try:
            import pytesseract
            mx, my = self.last_coords
            screenshot = ImageGrab.grab(bbox=(mx-100, my-50, mx+100, my+50))
            text = pytesseract.image_to_string(screenshot)
            messagebox.showinfo("Quick OCR Result", f"Extracted Text:\n{text}")
        except Exception:
            # Safe clean fallback system when drivers not fully configured
            messagebox.showwarning("OCR Warn", self.i18n.get("unsupported_ocr"))

    # Vault Controller Methods
    def vault_encrypt(self):
        key = self.vault_key_ent.get()
        if not key:
            messagebox.showerror("Error", self.i18n.get("invalid_key"))
            return
        msg = self.vault_text_box.get("1.0", "end-1c")
        try:
            cipher = SecureVault.encrypt_message(msg, key)
            self.vault_text_box.delete("1.0", "end")
            self.vault_text_box.insert("1.0", cipher)
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))

    def vault_decrypt(self):
        key = self.vault_key_ent.get()
        if not key:
            messagebox.showerror("Error", self.i18n.get("invalid_key"))
            return
        cipher = self.vault_text_box.get("1.0", "end-1c").strip()
        try:
            plain = SecureVault.decrypt_message(cipher, key)
            self.vault_text_box.delete("1.0", "end")
            self.vault_text_box.insert("1.0", plain)
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))

    def vault_create_archive(self):
        files = filedialog.askopenfilenames(title="Select files to archive")
        if files:
            save_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
            if save_path:
                def update_progress(val):
                    self.arch_progress.set(val / 100)

                threading.Thread(target=lambda: [
                    SecureVault.create_secure_archive(files, save_path, update_progress),
                    messagebox.showinfo("Vault Success", f"Archived successfully to {save_path}")
                ], daemon=True).start()

    def vault_extract_archive(self):
        archive = filedialog.askopenfilename(title="Select archive to extract", filetypes=[("ZIP files", "*.zip")])
        if archive:
            out_dir = filedialog.askdirectory(title="Select output destination directory")
            if out_dir:
                def update_progress(val):
                    self.arch_progress.set(val / 100)

                threading.Thread(target=lambda: [
                    SecureVault.extract_secure_archive(archive, out_dir, update_progress),
                    messagebox.showinfo("Vault Success", "Extracted successfully")
                ], daemon=True).start()

    def vault_convert_media(self):
        src = filedialog.askopenfilename(title="Select file to convert")
        if src:
            dest = filedialog.asksaveasfilename(title="Save converted file as")
            if dest:
                try:
                    SecureVault.local_format_convert(src, dest)
                    messagebox.showinfo("Vault Success", f"Successfully converted and saved to {dest}")
                except Exception as e:
                    messagebox.showerror("Conversion Error", str(e))

    def vault_generate_hash(self):
        src = filedialog.askopenfilename(title="Select File to Hash")
        if src:
            sha256 = SecureVault.generate_file_hash(src, "sha256")
            md5 = SecureVault.generate_file_hash(src, "md5")
            messagebox.showinfo("Cyber Ops - Hash Checksum", f"SHA-256:\n{sha256}\n\nMD5:\n{md5}")

    def vault_remove_exif(self):
        src = filedialog.askopenfilename(title="Select Image File", filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp")])
        if src:
            dest = filedialog.asksaveasfilename(title="Save Cleared Image as", defaultextension=".png", filetypes=[("PNG", "*.png")])
            if dest:
                if SecureVault.remove_exif_metadata(src, dest):
                    messagebox.showinfo("Cyber Ops Success", "EXIF metadata metadata scrubbed successfully.")
                else:
                    messagebox.showerror("Error", "Could not scrub EXIF.")

    def vault_stego_dialog(self):
        steg_win = ctk.CTkToplevel(self)
        steg_win.title("Steganography Panel")
        steg_win.geometry("500x400")
        steg_win.configure(fg_color="#000000")

        # Bring to top
        steg_win.attributes("-topmost", True)

        lbl = ctk.CTkLabel(steg_win, text="STEGANOGRAPHY WORKSTATION", font=("Courier", 16, "bold"), text_color="#00FF00")
        lbl.pack(pady=10)

        txt_box = ctk.CTkTextbox(steg_win, height=100, fg_color="#111", text_color="#00FF00", font=("Courier", 11))
        txt_box.pack(fill="x", padx=10, pady=5)

        def handle_hide():
            src = filedialog.askopenfilename(title="Select Carrier Image", filetypes=[("Images", "*.png")])
            if src:
                dest = filedialog.asksaveasfilename(title="Save Carrier as", defaultextension=".png", filetypes=[("PNG", "*.png")])
                if dest:
                    text = txt_box.get("1.0", "end-1c")
                    if SecureVault.hide_secret_text_steg(src, text, dest):
                        messagebox.showinfo("Steg Success", f"Secret message hidden in {dest}")
                        steg_win.destroy()
                    else:
                        messagebox.showerror("Error", "Failed hiding secret.")

        def handle_extract():
            src = filedialog.askopenfilename(title="Select Stego Image", filetypes=[("Images", "*.png")])
            if src:
                text = SecureVault.extract_secret_text_steg(src)
                txt_box.delete("1.0", "end")
                txt_box.insert("1.0", text)
                messagebox.showinfo("Steg Extracted", "Message successfully extracted!")

        btn_hide = CyberButton(steg_win, text="HIDE MESSAGE IN IMAGE", command=handle_hide)
        btn_hide.pack(pady=10)
        btn_extr = CyberButton(steg_win, text="EXTRACT MESSAGE FROM IMAGE", command=handle_extract)
        btn_extr.pack(pady=10)

    def on_closing(self):
        # Stop background threads gracefully
        self.hotkey_tracker.stop()
        self.auto_clicker.stop()
        self.macro_recorder.stop_recording()
        self.clipboard.running = False
        self.bg_canvas.stop()
        self.scanning_radar.stop()
        self.destroy()

if __name__ == "__main__":
    app = NeoGenCyberToolbox()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
