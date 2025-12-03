import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# JSON dosya ismi
JSON_FILE = "icerikler.json"


#
# Fonksiyonlar
#
def load_data():
    """JSON dosyasından içerikleri yükler ve Treeview'e ekler."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                treeview.insert("", tk.END, values=(item["İçerik Adı"], item["Kategori"], item["İçerik Türü"],
                                                    item["İçerik Puanı"], item["İzlem Durumu"]))
    else:
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)


def save_data():
    """Treeview'deki içerikleri JSON dosyasına kaydeder."""
    data = []
    for row_id in treeview.get_children():
        row = treeview.item(row_id, "values")
        data.append({
            "İçerik Adı": row[0],
            "Kategori": row[1],
            "İçerik Türü": row[2],
            "İçerik Puanı": row[3],
            "İzlem Durumu": row[4],
        })
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def Ekle():
    if(moveName_entry.get()!="" and moveName_entry.get()!="İçerik ismi giriniz"):

        icerik_adi = moveName_entry.get()
        icerik_turu = default.get()
        izlenme_durumu = "İzlenmiş" if var.get() else "İzlenmemiş"

        # Eğer izlenmemişse yıldız puanı "--" olarak ayarla
        icerik_puani = "--" if izlenme_durumu == "İzlenmemiş" else canvas.itemcget(value_tag, "text")

        kategori = kategori_var.get()

        # Treeview'e ekle
        treeview.insert("", tk.END, values=(icerik_adi, kategori, icerik_turu, icerik_puani, izlenme_durumu))

        # JSON dosyasına kaydet
        save_data()

        print(f"Eklendi: {icerik_adi}, {kategori}, {icerik_turu}, Puan: {icerik_puani}, Durum: {izlenme_durumu}")
    else:messagebox.showerror("Hata Başlık", "Hatalı Giriş !")


def Sil():
    """Seçilen içeriği siler."""
    selected_item = treeview.selection()
    if selected_item:
        treeview.delete(selected_item)
        save_data()  # Silindikten sonra JSON dosyasını güncelle
    else:
        messagebox.showerror("Hata Başlık", "Lütfen Silinecek İçeriği Seçiniz!")


def Edit():
    """Seçilen içeriği düzenler."""
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Hata Başlık", "Lütfen Düzenlenecek İçeriği Seçiniz!")
        return

    # Seçilen öğenin mevcut değerlerini al
    item = treeview.item(selected_item, "values")

    # Düzenleme penceresi oluştur
    edit_window = tk.Toplevel(general_screen)
    edit_window.title("Düzenle")
    edit_window.geometry("400x400")

    # İçerik Adı
    tk.Label(edit_window, text="İçerik Adı:").grid(row=0, column=0, padx=10, pady=10)
    content_name_entry = tk.Entry(edit_window)
    content_name_entry.insert(0, item[0])
    content_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Kategori (Film/Dizi)
    tk.Label(edit_window, text="Kategori:").grid(row=1, column=0, padx=10, pady=10)
    category_var = tk.StringVar(value=item[1])
    film_radio = tk.Radiobutton(edit_window, text="Film", variable=category_var, value="Film")
    film_radio.grid(row=1, column=1, sticky="w")
    dizi_radio = tk.Radiobutton(edit_window, text="Dizi", variable=category_var, value="Dizi")
    dizi_radio.grid(row=1, column=2, sticky="w")

    # İçerik Türü
    tk.Label(edit_window, text="İçerik Türü:").grid(row=2, column=0, padx=10, pady=10)
    content_type_var = tk.StringVar(value=item[2])
    content_type_menu = tk.OptionMenu(edit_window, content_type_var, *icerik_types)
    content_type_menu.grid(row=2, column=1, padx=10, pady=10)

    # Yıldız Değerlendirme
    tk.Label(edit_window, text="İçerik Puanı:").grid(row=3, column=0, padx=10, pady=10)

    canvas = tk.Canvas(edit_window, width=240, height=55, bg="white", highlightthickness=0)
    canvas.grid(row=3, column=1, columnspan=2, pady=10)

    bar_x1, bar_y1 = 25, 35
    bar_x2, bar_y2 = bar_x1 + 200, bar_y1 + 10

    bar = canvas.create_rectangle(bar_x1 + 5, bar_y1, bar_x2 - 5, bar_y2, fill="lightgray", outline="")

    gradient_lines = {}
    for i in range(bar_x1, bar_x2, 2):
        gradient_lines[i] = canvas.create_line(i, bar_x1, i, bar_y2, fill="lightgray", width=2)

    def start_drag(event):
        canvas.drag_data["x"] = event.x

    def drag(event):
        new_x = event.x
        if bar_x1 <= new_x <= bar_x2:
            delta_x = new_x - canvas.drag_data["x"]
            canvas.move(star, delta_x, 0)
            canvas.drag_data["x"] = new_x

            current_value = float((new_x - bar_x1) / (bar_x2 - bar_x1) * 5)
            update_bar_gradient(new_x)
            canvas.itemconfig(value_tag, text=f"{current_value:.1f}")
            canvas.coords(value_tag, new_x, bar_y1 - 20)

    def update_bar_gradient(x_position):
        for i in range(bar_x1, bar_x2, 2):
            ratio = (i - bar_x1) / (bar_x2 - bar_x1)
            distance_to_star = abs(x_position - i) / (bar_x2 - bar_x1)
            adjusted_ratio = max(0, 1 - distance_to_star * 2)
            color = f"#00{int(255 * adjusted_ratio):02x}{int(200 * (1 - adjusted_ratio)):02x}"
            canvas.itemconfig(gradient_lines[i], fill=color)

    def create_star(canvas, x, y, size=13, fill="gold"):
        points = [
            x, y - size,
               x + size * 0.4, y - size * 0.3,
               x + size, y - size * 0.3,
               x + size * 0.5, y + size * 0.1,
               x + size * 0.6, y + size,
            x, y + size * 0.4,
               x - size * 0.6, y + size,
               x - size * 0.5, y + size * 0.2,
               x - size, y - size * 0.3,
               x - size * 0.4, y - size * 0.3,
        ]
        return canvas.create_polygon(points, fill=fill, outline="black", width=1)

    star = create_star(canvas, bar_x1, (bar_y1 + bar_y2) // 2)

    value_tag = canvas.create_text(bar_x1, bar_y1 - 20, text=item[3], font=("Arial", 12), fill="black")

    canvas.drag_data = {"x": 0}
    canvas.tag_bind(star, "<Button-1>", start_drag)
    canvas.tag_bind(star, "<B1-Motion>", drag)

    # İzleme Durumu
    tk.Label(edit_window, text="İzleme Durumu:").grid(row=4, column=0, padx=10, pady=10)
    watch_status_var = tk.StringVar(value=item[4])
    watch_status_menu = tk.OptionMenu(edit_window, watch_status_var, "İzlenmiş", "İzlenmemiş")
    watch_status_menu.grid(row=4, column=1, padx=10, pady=10)

    def save_changes():
        """Değişiklikleri kaydeder."""
        updated_values = (
            content_name_entry.get(),
            category_var.get(),
            content_type_var.get(),
            canvas.itemcget(value_tag, "text"),
            watch_status_var.get(),
        )

        # Treeview'de güncelle
        treeview.item(selected_item, values=updated_values)

        # JSON dosyasını güncelle
        save_data()

        print(f"Güncellendi: {updated_values}")
        edit_window.destroy()

    # Kaydet butonu
    save_button = tk.Button(edit_window, text="Kaydet", command=save_changes)
    save_button.grid(row=5, column=0, columnspan=2, pady=20)

#
# Arayüz Tasarımı
#

bg_clr ='black'
general_screen = tk.Tk()
general_screen.title("İçerik Kayıt Sistemi")
general_screen.geometry("720x460")
general_screen.config(bg=bg_clr)
general_screen.resizable(False, False)

# İçerik Adı Girişi
m_text = "İçerik ismi giriniz"


def on_focus_in(event):
    if moveName_entry.get() == m_text:
        moveName_entry.delete(0, tk.END)
        moveName_entry.config(fg="white")


def on_focus_out(event):
    if moveName_entry.get() == "":
        moveName_entry.insert(0, m_text)
        moveName_entry.config(fg="gray")


move_x, move_y = 30, 30
moveName_label = tk.Label(text="İÇERİK İSMİ", bg=bg_clr)
moveName_label.place(x=move_x, y=move_y - 20)

moveName_entry = tk.Entry(general_screen, fg="gray")
moveName_entry.place(x=move_x, y=move_y, width=200)
moveName_entry.insert(0, m_text)
moveName_entry.bind("<FocusIn>", on_focus_in)
moveName_entry.bind("<FocusOut>", on_focus_out)

# Tür Girişi
icerik_types = ["KOMEDİ", "AKSİYON", "DRAM", "MACERA", "BİLİM KURGU", "GERİLİM", "KORKU"]
default = tk.StringVar(value="TÜR SEÇİNİZ")

moveType_label = tk.Label(text='İÇERİK TÜRLERİ', bg=bg_clr)
moveType_label.place(x=move_x, y=move_y + 35)

moveType_bar = tk.OptionMenu(general_screen, default, *icerik_types)
moveType_bar.place(x=move_x, y=move_y + 55)

# Film/Dizi Seçimi
kategori_var = tk.StringVar(value="Film")

kategori_label = tk.Label(text="KATEGORİ SEÇİMİ", bg=bg_clr)
kategori_label.place(x=move_x + 450, y=move_y - 20)

film_radio = tk.Radiobutton(general_screen, text="Film", variable=kategori_var, value="Film", bg=bg_clr)
film_radio.place(x=move_x + 450, y=move_y)
film_radio.select()

dizi_radio = tk.Radiobutton(general_screen, text="Dizi", variable=kategori_var, value="Dizi", bg=bg_clr)
dizi_radio.place(x=move_x + 450, y=move_y + 30)


# Yıldız Değerlendirme
def start_drag(event):
    canvas.drag_data["x"] = event.x


def drag(event):
    new_x = event.x
    if bar_x1 <= new_x <= bar_x2:
        delta_x = new_x - canvas.drag_data["x"]
        canvas.move(star, delta_x, 0)
        canvas.drag_data["x"] = new_x

        current_value = float((new_x - bar_x1) / (bar_x2 - bar_x1) * 5)
        update_bar_gradient(new_x)
        canvas.itemconfig(value_tag, text=f"{current_value:.1f}")
        canvas.coords(value_tag, new_x, bar_y1 - 20)


def update_bar_gradient(x_position):
    for i in range(bar_x1, bar_x2, 2):
        ratio = (i - bar_x1) / (bar_x2 - bar_x1)
        distance_to_star = abs(x_position - i) / (bar_x2 - bar_x1)
        adjusted_ratio = max(0, 1 - distance_to_star * 2)
        color = f"#00{int(255 * adjusted_ratio):02x}{int(200 * (1 - adjusted_ratio)):02x}"
        canvas.itemconfig(gradient_lines[i], fill=color)


def create_star(canvas, x, y, size=13, fill="gold"):
    points = [
        x, y - size,
           x + size * 0.4, y - size * 0.3,
           x + size, y - size * 0.3,
           x + size * 0.5, y + size * 0.1,
           x + size * 0.6, y + size,
        x, y + size * 0.4,
           x - size * 0.6, y + size,
           x - size * 0.5, y + size * 0.2,
           x - size, y - size * 0.3,
           x - size * 0.4, y - size * 0.3,
    ]
    return canvas.create_polygon(points, fill=fill, outline="black", width=1)


canvas = tk.Canvas(general_screen, width=240, height=55, bg=bg_clr, highlightthickness=0)
canvas.place(x=230, y=50)

bar_x1, bar_y1 = 25, 35
bar_x2, bar_y2 = bar_x1 + 200, bar_y1 + 10

bar = canvas.create_rectangle(bar_x1 + 5, bar_y1, bar_x2 - 5, bar_y2, fill="lightgray", outline="")

gradient_lines = {}
for i in range(bar_x1, bar_x2, 2):
    gradient_lines[i] = canvas.create_line(i, bar_x1, i, bar_y2, fill="lightgray", width=2)

star = create_star(canvas, bar_x1, (bar_y1 + bar_y2) // 2)

value_tag = canvas.create_text(bar_x1, bar_y1 - 20, text="0.0", font=("Arial", 12), fill="gold")

canvas.drag_data = {"x": 0}
canvas.tag_bind(star, "<Button-1>", start_drag)
canvas.tag_bind(star, "<B1-Motion>", drag)

# İzleme Durumu Checkbox
var = tk.IntVar()
checkbox = tk.Checkbutton(general_screen, text="İzledim", variable=var, bg=bg_clr)
checkbox.place(x=move_x + 220, y=move_y - 5)

# Butonlar
add_button = tk.Button(text="EKLE", command=Ekle,bg=bg_clr)
add_button.place(x=move_x + 600, y=move_y)

delete_button = tk.Button(text="SİL", command=Sil,bg=bg_clr)
delete_button.place(x=move_x + 600, y=move_y + 45)

edit_button = tk.Button(text="DÜZENLE", command=Edit,bg=bg_clr)
edit_button.place(x=move_x + 300, y=move_y + 350)

# Treeview
treeview = ttk.Treeview(general_screen,
                        columns=("İçerik Adı", "Kategori", "İçerik Türü", "İçerik Puanı", "İzlem Durumu"),
                        show="headings")

treeview.heading("İçerik Adı", text="İçerik Adı")
treeview.heading("Kategori", text="Kategori")
treeview.heading("İçerik Türü", text="İçerik Türü")
treeview.heading("İçerik Puanı", text="İçerik Puanı")
treeview.heading("İzlem Durumu", text="İzlem Durumu")

treeview.column("İçerik Adı", width=200)
treeview.column("Kategori", width=100)
treeview.column("İçerik Türü", width=150)
treeview.column("İçerik Puanı", width=100)
treeview.column("İzlem Durumu", width=100)

treeview.place(x=move_x, y=move_y + 100)

# JSON'dan verileri yükleme
load_data()

general_screen.mainloop()
