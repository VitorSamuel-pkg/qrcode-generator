import customtkinter as ctk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Janela
root = ctk.CTk()
root.title("Gerador de QR Code com Preview")
root.geometry("700x400")
root.resizable(False, False)

# Frame Principal
main_frame = ctk.CTkFrame(root)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Frame Esquerdo (Inputs)
left_frame = ctk.CTkFrame(main_frame)
left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

# Frame Direito (Preview)
right_frame = ctk.CTkFrame(main_frame)
right_frame.grid(row=0, column=1, sticky="nsew")

main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

# === INPUTS ===
ctk.CTkLabel(left_frame, text="URL:", font=("Arial", 14)).pack(anchor="w", pady=(10, 5))
entry_url = ctk.CTkEntry(left_frame, width=300)
entry_url.pack(pady=5)

ctk.CTkLabel(left_frame, text="Logo (opcional):", font=("Arial", 14)).pack(anchor="w", pady=(15, 5))
frame_logo = ctk.CTkFrame(left_frame, fg_color="transparent")
frame_logo.pack(pady=5)
entry_logo = ctk.CTkEntry(frame_logo, width=200)
entry_logo.pack(side="left", padx=(0, 10))
ctk.CTkButton(frame_logo, text="Procurar", command=lambda: browse_file(entry_logo)).pack(side="left")

ctk.CTkLabel(left_frame, text="Salvar como:", font=("Arial", 14)).pack(anchor="w", pady=(15, 5))
frame_save = ctk.CTkFrame(left_frame, fg_color="transparent")
frame_save.pack(pady=5)
entry_save = ctk.CTkEntry(frame_save, width=200)
entry_save.pack(side="left", padx=(0, 10))
ctk.CTkButton(frame_save, text="Procurar", command=lambda: save_file(entry_save)).pack(side="left")

# === PREVIEW ===
preview_label = ctk.CTkLabel(right_frame, text="Prévia do QR Code aparecerá aqui")
preview_label.pack(pady=20)

# Botão principal
btn_gerar = ctk.CTkButton(root, text="Gerar e Salvar QR Code", command=lambda: generate_qr(preview=True), font=("Arial", 14))
btn_gerar.pack(pady=(10, 20))

# === FUNÇÕES ===

def browse_file(entry):
    path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
    if path:
        entry.delete(0, ctk.END)
        entry.insert(0, path)

def save_file(entry):
    path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
    if path:
        entry.delete(0, ctk.END)
        entry.insert(0, path)

def generate_qr(preview=False):
    data = entry_url.get()
    output_path = entry_save.get()
    logo_path = entry_logo.get()

    if not data:
        messagebox.showerror("Erro", "A URL é obrigatória!")
        return

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        if logo_path and os.path.exists(logo_path):
            logo = Image.open(logo_path)
            logo_size = 60
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
            img.paste(logo, pos)

        # Mostrar preview redimensionado
        img_preview = img.resize((200, 200), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_preview)
        preview_label.configure(image=img_tk, text="")
        preview_label.image = img_tk

        # Se for salvar:
        if output_path:
            img.save(output_path)
            messagebox.showinfo("Sucesso", f"QR Code salvo em:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao gerar QR Code:\n{e}")

root.mainloop()