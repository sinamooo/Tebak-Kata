import random
import requests

def main(kategori_user="Semua"):
    # URL Google Docs untuk mengambil daftar kata
    url = "https://docs.google.com/document/d/1sCm3fZd2LGzLLa5ygtmeVfX-2BRPMKdK2Ni087-NzU0/export?format=txt"
    
    try:
        response = requests.get(url)
        response.encoding = 'utf-8' 
        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        
        # --- LOGIKA FILTER KATEGORI ---
        if kategori_user != "Semua":
            # Mencari baris yang formatnya "Kategori: Kata" dan cocok dengan pilihan user
            filtered_lines = [l for l in lines if l.lower().startswith(kategori_user.lower() + ":")]
            
            if filtered_lines:
                pilihan = random.choice(filtered_lines)
            else:
                # Jika kategori yang dipilih tidak ditemukan di file, ambil random dari semua
                pilihan = random.choice(lines)
        else:
            # Jika user pilih "Semua", ambil random dari seluruh daftar
            pilihan = random.choice(lines)
        
        # Memisahkan Kategori dan Kata
        if ":" in pilihan:
            kategori, word = pilihan.split(":", 1)
        else:
            kategori, word = "Umum", pilihan
            
        word = word.lower().strip()
        kategori = kategori.strip()
        
    except Exception as e:
        # Cadangan jika koneksi internet atau proses download bermasalah
        kategori, word = "Hewan", "kucing"

    # --- PENANGANAN NAMA FILE GAMBAR ---
    image_name = word.replace(" ", "").replace("-", "") 

    # Pilih satu huruf bantuan pertama secara otomatis
    huruf_untuk_hint = word.replace(" ", "").replace("-", "")
    hint_letter = random.choice(huruf_untuk_hint) if huruf_untuk_hint else ""
    
    # Membuat tampilan awal (Contoh: "k _ _ _ _ g")
    display = ""
    for char in word:
        if char == " ":
            display += " " 
        elif char == "-":
            display += "-" 
        elif char == hint_letter:
            display += char 
        else:
            display += "_"
            
    # Mengembalikan 5 nilai ke app.py
    return word, hint_letter, display, kategori, image_name