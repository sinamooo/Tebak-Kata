from flask import Flask, render_template, request, url_for, redirect
from hangman import main
import random

app = Flask(__name__)

# DATABASE SKOR SEDERHANA (Disimpan di memori server)
user_scores = {}

# Menyimpan status game agar data tidak hilang saat refresh
data_game = {
    "kata_asli": "",
    "sudah_ditebak": [],
    "nama": "",
    "sisa_nyawa": 5,
    "pesan": "",
    "kategori": "",
    "sisa_hint": 3,
    "image_name": "",
    "skor_saat_ini": 0 
}

@app.route('/')
def index():
    return render_template('index.html', 
                            game_start=False, 
                            nyawa=5, 
                            kategori="", 
                            sisa_hint=3,
                            skor=0)

# Route tambahan untuk memudahkan tombol "Main Lagi" di Pop-up
@app.route('/game')
def game():
    if not data_game["nama"]:
        return redirect(url_for('index'))
    
    # Ambil kata baru tapi tetap gunakan nama yang sama
    kata, hint, tampilan, kategori, image_name = main(data_game["kategori"] or "Semua")
    
    data_game["kata_asli"] = kata
    data_game["sudah_ditebak"] = [hint] 
    data_game["sisa_nyawa"] = 5
    data_game["sisa_hint"] = 3
    data_game["image_name"] = image_name
    data_game["pesan"] = "Ayo main lagi!"
    
    return render_template('index.html', 
                            game_start=True, 
                            user_name=data_game["nama"], 
                            display_word=tampilan,
                            nyawa=data_game["sisa_nyawa"],
                            notif=data_game["pesan"],
                            kategori=data_game["kategori"],
                            sisa_hint=data_game["sisa_hint"],
                            image_name=data_game["image_name"],
                            skor=data_game["skor_saat_ini"],
                            secret_word=data_game["kata_asli"])

@app.route('/start', methods=['POST'])
def start_game():
    nama_input = request.form.get('input_nama').strip().lower()
    kategori_pilihan = request.form.get('kategori_pilihan', 'Semua')
    
    data_game["nama"] = nama_input
    data_game["kategori"] = kategori_pilihan
    
    if nama_input in user_scores:
        data_game["skor_saat_ini"] = user_scores[nama_input]
    else:
        data_game["skor_saat_ini"] = 0
        user_scores[nama_input] = 0

    kata, hint, tampilan, kategori, image_name = main(kategori_pilihan) 
    
    data_game["kata_asli"] = kata
    data_game["sudah_ditebak"] = [hint] 
    data_game["sisa_nyawa"] = 5
    data_game["sisa_hint"] = 3
    data_game["image_name"] = image_name
    data_game["pesan"] = "Selamat bermain!"
    
    return render_template('index.html', 
                            game_start=True, 
                            user_name=data_game["nama"], 
                            display_word=tampilan,
                            nyawa=data_game["sisa_nyawa"],
                            notif=data_game["pesan"],
                            kategori=kategori,
                            sisa_hint=data_game["sisa_hint"],
                            image_name=data_game["image_name"],
                            skor=data_game["skor_saat_ini"],
                            secret_word=data_game["kata_asli"])

@app.route('/guess', methods=['POST'])
def guess_letter():
    guess = request.form.get('tebakan').lower().strip()
    word = data_game["kata_asli"]
    
    if not guess or len(guess) != 1 or not guess.isalpha():
        data_game["pesan"] = "Input tidak valid."
    elif guess in data_game["sudah_ditebak"]:
        data_game["pesan"] = f"Huruf '{guess}' sudah ditebak!"
    else:
        data_game["sudah_ditebak"].append(guess)
        if guess in word:
            data_game["pesan"] = f"Bagus! Huruf '{guess}' benar."
        else:
            data_game["sisa_nyawa"] -= 1
            data_game["pesan"] = f"Salah! Huruf '{guess}' tidak ada."

    display = "".join([char if char in data_game["sudah_ditebak"] or char == " " or char == "-" else "_" for char in word])

    if "_" not in display.replace(" ", "").replace("-", ""):
        data_game["skor_saat_ini"] += 100
        user_scores[data_game["nama"]] = data_game["skor_saat_ini"]
        
    return render_template('index.html', 
                            game_start=True, 
                            user_name=data_game["nama"], 
                            display_word=display,
                            nyawa=data_game["sisa_nyawa"],
                            notif=data_game["pesan"],
                            kategori=data_game["kategori"],
                            sisa_hint=data_game["sisa_hint"],
                            image_name=data_game["image_name"],
                            skor=data_game["skor_saat_ini"],
                            secret_word=data_game["kata_asli"])

@app.route('/get_hint', methods=['POST'])
def get_hint():
    if data_game["sisa_hint"] > 0:
        data_game["sisa_hint"] -= 1
        
        if data_game["sisa_hint"] >= 1:
            huruf_tersisa = [h for h in data_game["kata_asli"] if h not in data_game["sudah_ditebak"] and h not in [" ", "-"]]
            if huruf_tersisa:
                hint_baru = random.choice(huruf_tersisa)
                data_game["sudah_ditebak"].append(hint_baru)
        
    display = "".join([c if c in data_game["sudah_ditebak"] or c == " " or c == "-" else "_" for c in data_game["kata_asli"]])

    return render_template('index.html', 
                            game_start=True, 
                            user_name=data_game["nama"], 
                            display_word=display,
                            nyawa=data_game["sisa_nyawa"],
                            notif=data_game["pesan"],
                            kategori=data_game["kategori"],
                            sisa_hint=data_game["sisa_hint"],
                            image_name=data_game["image_name"],
                            skor=data_game["skor_saat_ini"],
                            secret_word=data_game["kata_asli"])

if __name__ == '__main__':
    app.run(debug=True)