import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def process_pdf():
    # Výběr vstupního souboru
    input_path = filedialog.askopenfilename(
        title="Výběr zdrojového PDF",
        filetypes=[("PDF files", "*.pdf")]
    )
    if not input_path:
        return
        
    # Získání původního jména souboru a vytvoření návrhu pro nový název
    base_name = os.path.basename(input_path)
    name_without_ext, ext = os.path.splitext(base_name) 
    suggested_name = f"{name_without_ext}_locked{ext}"  

    # Výběr, kam se má uložit výsledek
    output_path = filedialog.asksaveasfilename(
        title="Uložit rasterované PDF jako",
        initialfile=suggested_name,
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )
    if not output_path:
        return
        
    status_label.config(text="Probíhá rasterizace. Čekejte.", fg="orange")
    root.update()
    
    try:
        # Otevření původního PDF
        doc = fitz.open(input_path)
        # Vytvoření nového prázdného PDF
        new_doc = fitz.open()

        # Projití všech stránek
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Vyrenderování stránky jako obrázku
            pix = page.get_pixmap(dpi=200) 
            
            # Vytvoření nové prázdné stránky se stejnými rozměry
            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            
            # Vložení vyrenderovaného obrázku přes celou stránku
            new_page.insert_image(page.rect, pixmap=pix)

        # Uložení nového PDF s kompresí
        new_doc.save(output_path, garbage=4, deflate=True)
        new_doc.close()
        doc.close()
        
        # Aktualizace statusu bez vyskakovacího okna
        status_label.config(text="Hotovo! Raterizace se povedla a soubor byl uložen.", fg="green")
        
    except Exception as e:
        status_label.config(text="Nastala nečekaná chyba", fg="red")
        messagebox.showerror("Chyba", f"Chyba:\n{str(e)}")

# GUI
root = tk.Tk()
root.title("PDF rasterizér")
root.geometry("450x200")
root.resizable(False, False)

# UI Elementy
title_label = tk.Label(root, text="Převod PDF na rasterované PDF", font=("Arial", 11, "bold"), pady=35)
title_label.pack()

btn = tk.Button(root, text="Vybrat PDF pro rasterizaci", command=process_pdf, padx=20, pady=5, bg="#0078D7", fg="white", font=("Arial", 10, "bold"))
btn.pack()

status_label = tk.Label(root, text="", pady=10, font=("Arial", 9))
status_label.pack()

# Spuštění aplikace
root.mainloop()