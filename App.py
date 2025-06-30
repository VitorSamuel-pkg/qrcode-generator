import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import os

def generate_qr():
    data = entry_url.get()
    output_path = entry_save.get()
    logo_path = entry_logo.get()

    if not data or not output_path:
        messagebox.showerror("Erro", "URL e local de salvamento são obrigatórios!")
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

        img.save(output_path)
        messagebox.showinfo("Sucesso", f"QR Code salvo em:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao gerar QR Code:\n{e}")

def browse_logo():
    file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
    if file_path:
        entry_logo.delete(0, tk.END)
        entry_logo.insert(0, file_path)

def browse_save():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
    if file_path:
        entry_save.delete(0, tk.END)
        entry_save.insert(0, file_path)

# Configuração da janela
root = tk.Tk()
root.title("Gerador de QR Code")
root.geometry("500x300")

# Widgets
tk.Label(root, text="URL:", font=("Arial", 12)).pack(pady=5)
entry_url = tk.Entry(root, width=50)
entry_url.pack()

tk.Label(root, text="Logo (opcional):", font=("Arial", 12)).pack(pady=5)
frame_logo = tk.Frame(root)
frame_logo.pack()
entry_logo = tk.Entry(frame_logo, width=40)
entry_logo.pack(side=tk.LEFT)
tk.Button(frame_logo, text="Procurar", command=browse_logo).pack(side=tk.LEFT, padx=5)

tk.Label(root, text="Salvar como:", font=("Arial", 12)).pack(pady=5)
frame_save = tk.Frame(root)
frame_save.pack()
entry_save = tk.Entry(frame_save, width=40)
entry_save.pack(side=tk.LEFT)
tk.Button(frame_save, text="Procurar", command=browse_save).pack(side=tk.LEFT, padx=5)

tk.Button(root, text="Gerar QR Code", command=generate_qr, bg="green", fg="white", font=("Arial", 12)).pack(pady=20)

root.mainloop()