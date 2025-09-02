import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# ========== Caesar Cipher for Text ==========
def encrypt_text(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def decrypt_text(text, shift):
    return encrypt_text(text, -shift)

# ========== Caesar Cipher for Image ==========
def encrypt_image(img, shift):
    pixels = img.load()
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j][:3]  # ignore alpha if present
            pixels[i, j] = ((r + shift) % 256, (g + shift) % 256, (b + shift) % 256)
    return img

def decrypt_image(img, shift):
    return encrypt_image(img, -shift)

# ========== Core Functions for Text ==========
def process_text(mode):
    message = text_box.get("1.0", tk.END).strip()
    try:
        shift = int(entry_shift.get())
    except ValueError:
        messagebox.showerror("Error", "Shift must be an integer!")
        return
    
    result = encrypt_text(message, shift) if mode == "E" else decrypt_text(message, shift)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

# ========== Core Functions for Image ==========
def load_image():
    global current_image, original_image
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if filepath:
        img = Image.open(filepath).convert("RGB")
        original_image = img.copy()
        current_image = img
        display_image(img)

def display_image(img):
    img_resized = img.resize((250, 250))
    img_tk = ImageTk.PhotoImage(img_resized)
    label_img.config(image=img_tk)
    label_img.image = img_tk

def process_image(mode):
    global current_image
    if current_image is None:
        messagebox.showwarning("Warning", "Please upload an image first!")
        return
    try:
        shift = int(entry_shift.get())
    except ValueError:
        messagebox.showerror("Error", "Shift must be an integer!")
        return
    
    img = current_image.copy()
    img = encrypt_image(img, shift) if mode == "E" else decrypt_image(img, shift)
    current_image = img
    display_image(img)

def save_image():
    if current_image:
        filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")])
        if filepath:
            current_image.save(filepath)
            messagebox.showinfo("Saved", f"Image saved to {filepath}")

# ========== Tkinter UI ==========
root = tk.Tk()
root.title("🔐 Caesar Cipher Tool (Text + Image)")
root.geometry("850x700")
root.config(bg="#eaf4fc")

title = tk.Label(root, text="🔐 Caesar Cipher Tool", font=("Arial", 20, "bold"), bg="#eaf4fc", fg="navy")
title.pack(pady=10)

# Tabs
notebook = ttk.Notebook(root)
frame_text = tk.Frame(notebook, bg="#f9fbff")
frame_img = tk.Frame(notebook, bg="#f9fbff")
notebook.add(frame_text, text="Encrypt / Decrypt Text")
notebook.add(frame_img, text="Encrypt / Decrypt Image")
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# ===== TEXT TAB =====
tk.Label(frame_text, text="Enter Message:", font=("Arial", 12, "bold"), bg="#f9fbff").pack(anchor="w", padx=10)
text_box = tk.Text(frame_text, height=6, width=80)
text_box.pack(padx=10, pady=5)

tk.Label(frame_text, text="Shift Value:", font=("Arial", 12, "bold"), bg="#f9fbff").pack(anchor="w", padx=10)
entry_shift = tk.Entry(frame_text, width=10, font=("Arial", 12))
entry_shift.pack(pady=5)

btn_frame_text = tk.Frame(frame_text, bg="#f9fbff")
btn_frame_text.pack(pady=5)

tk.Button(btn_frame_text, text="Encrypt Text", command=lambda: process_text("E"), width=15, bg="green", fg="white").grid(row=0, column=0, padx=10)
tk.Button(btn_frame_text, text="Decrypt Text", command=lambda: process_text("D"), width=15, bg="red", fg="white").grid(row=0, column=1, padx=10)

tk.Label(frame_text, text="Result:", font=("Arial", 12, "bold"), bg="#f9fbff").pack(anchor="w", padx=10)
output_box = tk.Text(frame_text, height=6, width=80, fg="blue")
output_box.pack(padx=10, pady=5)

# ===== IMAGE TAB =====
btn_img = tk.Button(frame_img, text="Upload Image", command=load_image, bg="lightgray")
btn_img.pack(pady=5)

label_img = tk.Label(frame_img, bg="#f9fbff")
label_img.pack(pady=10)

btn_frame_img = tk.Frame(frame_img, bg="#f9fbff")
btn_frame_img.pack(pady=5)

tk.Button(btn_frame_img, text="Encrypt Image", command=lambda: process_image("E"), width=15, bg="green", fg="white").grid(row=0, column=0, padx=10)
tk.Button(btn_frame_img, text="Decrypt Image", command=lambda: process_image("D"), width=15, bg="red", fg="white").grid(row=0, column=1, padx=10)

tk.Button(frame_img, text="Save Image", command=save_image, bg="#9dc9fb").pack(pady=5)

# Track images
current_image = None
original_image = None

root.mainloop()
