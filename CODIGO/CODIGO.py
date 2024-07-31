import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import io
from rembg import remove
import os

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(title="SELECIONE UMA IMAGEM", filetypes=[("Imagens", "*.*")])
    if image_path:
        image_label.config(text="CAMINHO: " + image_path)
        image_label.pack()
        update_save_button_state()

def update_save_button_state():
    if format_var.get() == "PADRÃO" and remove_bg_var.get() == "NÃO":
        save_button.config(state=tk.DISABLED)
    else:
        save_button.config(state=tk.NORMAL)

def remove_background_and_save():
    if image_path:
        with open(image_path, "rb") as f:
            image_data = f.read()

        if remove_bg_var.get() == "SIM":
            output = remove(image_data)
            img = Image.open(io.BytesIO(output))
        else:
            img = Image.open(image_path)
        
        format_mapping = {
            "PADRÃO": os.path.splitext(image_path)[1][1:].upper(),
            "ICO": "ICO",
            "PNG": "PNG",
            "JPG": "JPEG",
            "JPEG": "JPEG"
        }

        selected_format = format_var.get()
        if selected_format in format_mapping:
            if selected_format in ["JPG", "JPEG"]:
                if img.mode in ["RGBA", "LA"]:
                    img = img.convert("RGB")
            
            file_extension = format_mapping[selected_format].lower()
            output_image_path = os.path.splitext(image_path)[0] + f"_CONVERTIDO.{file_extension}"
            img.save(output_image_path, format=format_mapping[selected_format])
            messagebox.showinfo("SUCESSO!", f"A imagem foi salva como {selected_format} com sucesso!")
        else:
            messagebox.showerror("ERRO", "Formato de imagem inválido.")

        update_save_button_state()

root = tk.Tk()
root.title("IMAGEM PARA CONVERSÃO")
root.geometry("400x400")

image_path = ""

select_button = tk.Button(root, text="SELECIONAR", command=select_image)
select_button.pack(pady=10)

image_label = tk.Label(root, text="CAMINHO: ")
image_label.pack()

format_label = tk.Label(root, text="CONVERTER PARA:")
format_label.pack(pady=5)

format_var = tk.StringVar(value="PADRÃO")

format_frame = tk.Frame(root)
format_frame.pack(pady=5)

tk.Radiobutton(format_frame, text="PADRÃO", variable=format_var, value="PADRÃO", command=update_save_button_state).pack(anchor=tk.W)
formats = ["ICO", "PNG", "JPG", "JPEG"]
for format_option in formats:
    tk.Radiobutton(format_frame, text=format_option, variable=format_var, value=format_option, command=update_save_button_state).pack(anchor=tk.W)

remove_bg_label = tk.Label(root, text="REMOVER FUNDO:")
remove_bg_label.pack(pady=5)

remove_bg_var = tk.StringVar(value="NÃO")

remove_bg_frame = tk.Frame(root)
remove_bg_frame.pack(pady=5)

tk.Radiobutton(remove_bg_frame, text="SIM", variable=remove_bg_var, value="SIM", command=update_save_button_state).pack(anchor=tk.W)
tk.Radiobutton(remove_bg_frame, text="NÃO", variable=remove_bg_var, value="NÃO", command=update_save_button_state).pack(anchor=tk.W)

save_button = tk.Button(root, text="SALVAR", command=remove_background_and_save, state=tk.DISABLED)
save_button.pack(pady=10)

footer_label = tk.Label(root, text="APP CRIADO PELO VILHALVA\nGITHUB: @VILHALVA", bg="gray", fg="white", height=2)
footer_label.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
