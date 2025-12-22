

#SEBELUM MENJALANKAN PROGRAM, HARAP INSTALL RICH DI TERMINAL MENGGUNAKAN COMMAND "pip install rich" (library Rich)


import json
import os
from datetime import datetime
from UI import booting, shutdown
from rich.progress import track
import time

DB_FILE = "moodnote.json"

# =======================
# DATABASE
# =======================

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "moods": []}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

# =======================
# REGISTER
# =======================
def register():
    db = load_db()
    print("\n=== REGISTER ===")

    username = input("Username: ")
    if username in db["users"]:
        print("❌ Username sudah dipakai!")
        return

    password = input("Password: ")

    db["users"][username] = {"password": password}
    save_db(db)

    print("✅ Akun berhasil dibuat!")

# =======================
# LOGIN
# =======================
def login():
    db = load_db()
    print("\n=== LOGIN ===")

    username = input("Username: ")
    password = input("Password: ")

    if username in db["users"] and db["users"][username]["password"] == password:
        print("✔ Login berhasil!")
        return username

    print("❌ Username atau password salah!")
    return None 


# =======================
# DETAIL MOOD (Rating + Comment)
# =======================
def lihat_detail_mood(mood, current_user, idx):
    while True:
        
        #MENAMPILKAN DETAIL NOTES YANG DIPILIH
        os.system("cls")
        print(f'{" "*len(mood['text'])}|=========={"="*len(mood['user'])}=|')
        print(f'{"="*len(mood['text'])}| Notes By {mood['user']} |{"="*len(mood['text'])}')
        print(f'{" "*len(mood['text'])}|=========={"="*len(mood['user'])}=|')
        print(f'\n\n{" "*len(mood['text'])} {mood['text']} {" "*len(mood['text'])}\n\n') 
        print(f'{"="*len(mood['text'])}============={"="*len(mood['user'])}{"="*len(mood['text'])}')  #POSTINGAN
        print(f'\nWaktu : {mood['time']}\n')
        print(f'{"-"*len(mood['text'])}-------------{"-"*len(mood['user'])}{"-"*len(mood['text'])}')
  
        # tampilkan total suka dan total komen
        db = load_db()
        if db["moods"]:
                db = load_db()
                totalsuka = 0
                totalkomen = 0
                for idlike in range(1, len(db['moods'][idx]["likes"])):
                    totalsuka = totalsuka + (len(db['moods'][idx]["likes"][idlike]))

                for idkomen in range(len(db['moods'][idx]["comments"])):
                    totalkomen = totalkomen +  (len(db['moods'][idx]["comments"][idkomen]['komen'][0]))

                if totalsuka > 0:
                    print(f"🩷  Likes {totalsuka}")
                else:
                    print("🩷  Belum ada suka.")
                if totalkomen > 0:
                    print(f"🗨️  Comments {totalkomen}")
                else:
                    print("🗨️  Belum ada komentar.")
                save_db(db)
        print(f'{"-"*len(mood['text'])}-------------{"-"*len(mood['user'])}{"-"*len(mood['text'])}') #PENUTUP POSTINGAN
        


        # tampilkan isi komentar
        print("---- Komentar ----")
        db = load_db()
        print("")
        if db['moods']:
            if len(db['moods'][idx]['comments']) > 0:
                for c in db['moods'][idx]['comments']:
                    print(f"- {c['user']}: {c['komen']}")
            else:  
                print('''
            Belum ada komentar.
    Jadilah yang pertama berkomentar!!''')
        else:
            print('ERROR')  
        print(f'\n{"_"*len(mood['text'])}_____________{"_"*len(mood['user'])}{"_"*len(mood['text'])}') #PENUTUP KOMENTAR

        #TAMPILAN MENU UNTUK USER MEMILIH
        menupost = ["Suka", "Tambah Komentar", "Kembali"]
        for x in range(len(db['moods'][idx]["comments"])):
                if current_user == db["moods"][idx]['comments'][x]['user']: #JIKA DI POSTINGAN NOTES ADA KOMENTAR current_user, MAKA OPSI 3 AKAN MENJADI HAPUS KOMENTAR
                    menupost.insert(2, "Hapus Komentar")
                    break
        print("\n")
        for i in range(len(menupost)):
            print(f"{i+1}. {menupost[i]}") #MENAMPILKAN MENU



        pilih = input("Pilih sesuai opsi di atas menggunakan angka! : ") 
        db = load_db()

        if pilih == "1": #memberi suka jika currentuser != None alias harus login terlebih dahulu
            if current_user == None:
                print("HARAP LOGIN UNTUK MEMBERI SUKA!!")
            else:
                idlike = len(db['moods'][idx]["likes"])
                nilai = 1
                if nilai == 1:
                    db = load_db()
                    if db['moods'][idx]["likes"] == []  :
                        db['moods'][idx]["likes"].append({
                                    "user" : []
                                })
                        save_db(db)
                        if current_user in db['moods'][idx]["likes"][0]["user"]:
                            print('kamu telah menyukai postingan ini')
                        else:
                                db = load_db()
                                db['moods'][idx]["likes"][0]["user"].append(current_user)
                                db['moods'][idx]["likes"].append({
                                    "suka" : nilai
                                })
                                save_db(db)
                                print("✔ notes berhasil disukai!")
                        db = load_db()
                    else:   #SETIAP USER HANYA BISA MEMBERI 1 LIKE TIAP 1 NOTES, JIKA USER SUDAH MEMBERI LIKE PADA NOTES, MAKA DIBERIKAN OPSI UNTUK MENDISLIKE.
                        if current_user in db['moods'][idx]["likes"][0]["user"]:
                            print('kamu telah menyukai notes ini')
                            while True:
                                unlike = input("apakah kamu ingin batal suka notes ini (y/n)")
                                if unlike == "y":
                                    db = load_db()
                                    likes = db['moods'][idx]["likes"]
                                    for i, item in enumerate(likes):
                                        if "suka" in item:
                                            likes.pop()
                                            break
                                    if current_user in likes[0]["user"]:
                                        likes[0]["user"].remove(current_user)
                                    print("berhasil mebantalkan suka!")
                                    save_db(db)
                                    break
                                elif unlike == "n":
                                    break
                                elif unlike == "":
                                    print('masukan sesuai format')
                                    True
                        else:
                            db['moods'][idx]["likes"][0]["user"].append(current_user)
                            db['moods'][idx]["likes"].append({
                                    "suka" : nilai
                            })
                            save_db(db)
                            print("✔ notes berhasil disukai!")
        elif pilih == "2": #UNTUK MENAMBAHKAN KOMENTAR TERHADAP NOTES JIKA USER SUDAH LOGIN ALIAS current_user != None
            if current_user == None:
                print("HARAP LOGIN UNTUK MENAMBAHKAN KOMENTAR!!")
            else:
                t = 1
                while t == 1:
                    komentar = input("Masukkan komentar: ")
                    if komentar == "":
                        t = 1
                        print('KOMENTAR TIDAK BOLEH KOSONG!!')
                    else:
                        db = load_db()
                        db['moods'][idx]["comments"].append({
                            "user" : current_user,
                            "komen" : komentar
                        })
                        t = 0
                        save_db(db)
                        print("✔ Komentar ditambahkan!")

        elif pilih == "3": #JIKA USER SUDAH MENAMBAHKAN KOMENTAR DI POSTINGAN NOTES, MAKA AKAN MUNCUL OPSI KETIGA MENJADI HAPUS KOMENTAR
            db = load_db()
            user_komen = [m for m in db["moods"][idx]['comments'] if m["user"] == current_user] #jika True, maka ada komentar current_user di notes tersebut
            if current_user != None and user_komen: #user harus sudah login dan user_komen True untuk menghapus komentar
                for x in range(len(db['moods'][idx]["comments"])):
                    if current_user == db["moods"][idx]['comments'][x]['user']:
                        db = load_db()
                        print("\n=== HAPUS KOMENTAR ===")
                        for i, m in enumerate(user_komen):
                            print(f"{i+1}. {m['komen']}")

                        asik = input("Pilih komentar yang ingin dihapus: ")

                        if asik.isdigit():
                            opsi = int(asik) - 1
                            if 0 <= opsi < len(user_komen):
                                komen_to_delete = user_komen[opsi]
                                db["moods"][idx]["comments"].remove(komen_to_delete)
                                save_db(db)
                                print("✔ Komentar berhasil dihapus!")
                                break
                            else:
                                print("Pilihan tidak valid!")
                        else:
                            print("Input salah!")
            else:      #JIKA TIDAK ADA KOMENTAR current_user DI POSTINGAN NOTES, MAKA OPSI 3 AKAN MENJADI KEMBALI 
                break

        elif pilih == "4":
            break
            

        input("\nTekan Enter untuk lanjut...")




# =======================
# MENAMPILKAN POSTINGAN NOTES KETIKA USER BELUM LOGIN
# =======================
def show_all_moods_before_login():
    db = load_db()

    if not db["moods"]:
        print("Belum ada mood siapapun.\n")
        return

    for i, mood in enumerate(db["moods"]):
        print(f"{i+1}. {mood['user']} → {mood['text']} ({mood['time']})\n") #UI BUAT MOOD

    pilih = input("\nPilih mood untuk lihat detail (Enter untuk kembali): ")
    if pilih.isdigit():
        idx = int(pilih) - 1
        if 0 <= idx < len(db["moods"]):
            lihat_detail_mood(db["moods"][idx], None, idx) #current_user akan None

# =======================
# MENAMPILKAN POSTINGAN NOTES KETIKA USER SUDAH LOGIN
# =======================
def show_all_moods_after_login(current_user):
    db = load_db()

    print("--- 💌 Mood Terbaru Pengguna💌 ---\n")

    if not db["moods"]:
        print("Belum ada mood.")
        return

    for i, mood in enumerate(db["moods"]):
        print(f"{i+1}. {mood['user']} → {mood['text']} ({mood['time']})\n") #UI BUAT MOOD

    pilih = input("\nPilih nomor mood untuk lihat detail (Enter untuk lanjut): ")

    if pilih.isdigit():
        idx = int(pilih) - 1
        if 0 <= idx < len(db["moods"]):
            lihat_detail_mood(db["moods"][idx], current_user, idx)


# =======================
# ADD MOOD
# =======================
def add_mood(user):
    db = load_db()

    while True:
      print("\n=== TULIS MOOD ===")
      mood_text = input("Mood kamu hari ini: ")
      if mood_text.strip() == "":
          print('NOTES TIDAK BOLEH KOSONG!!')
          True
      else:
          break

    post_id = len(db["moods"])
    for i in range(len(db['moods'])):
        if post_id == db['moods'][i]['id']:
            post_id = post_id + 1    #UNTUK MENGATASI DUPLIKAT ID TIAP POSTINGAN NOTES.
    entry = {
        "id" : post_id,
        "user": user,
        "text": mood_text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "likes": [],
        "comments": []
    }

    db["moods"].append(entry)
    save_db(db)

    print("✔ Mood berhasil ditambahkan!")


#UNTUK MENGEDIT POSTINGAN NOTES SENDIRI YANG TELAH DI POSTING
def editmood(user):
    db = load_db()

    user_moods = [m for m in db["moods"] if m["user"] == user]

    if not user_moods:
        print("❌ Kamu belum punya mood!")
        return

    
    while True:
      print("\n=== EDIT MOOD ===")
      for i, m in enumerate(user_moods):
          print(f"{i+1}. {m['text']} ({m['time']})")

      pilih = input("Pilih mood yang ingin di edit: ")
      
      if pilih.strip() == "" :
          print('TIDAK BOLEH KOSONG')
          True
      else:
          break
      
    while True:
        print("\n=== EDIT MOOD ===")
        new = input("Masukan notes baru : ")
        if new.strip() == "":
          print('TIDAK BOLEH KOSONG')
          True
        else:
            break
    
        
    if pilih.isdigit():
        idx = int(pilih) - 1
        if 0 <= idx < len(user_moods):
            user_moods[idx]['text'] = new
            save_db(db)
            print("✔ Mood berhasil dihapus!")
        else:
            print("Pilihan tidak valid!")
    else:
        print("Input salah!")


# =======================
# DELETE MOOD SENDIRI
# =======================
def delete_mood(user):
    db = load_db()

    user_moods = [m for m in db["moods"] if m["user"] == user]

    if not user_moods:
        print("❌ Kamu belum punya mood!")
        return

    print("\n=== HAPUS MOOD ===")
    for i, m in enumerate(user_moods):
        print(f"{i+1}. {m['text']} ({m['time']})")

    pilih = input("Pilih mood yang ingin dihapus: ")

    if pilih.isdigit():
        idx = int(pilih) - 1
        if 0 <= idx < len(user_moods):
            mood_to_delete = user_moods[idx]
            db["moods"].remove(mood_to_delete)
            save_db(db)
            print("✔ Mood berhasil dihapus!")
        else:
            print("Pilihan tidak valid!")
    else:
        print("Input salah!")

# =======================
# USER MENU
# =======================
def user_menu(user):
    while True:
        os.system("cls")
        print("=== MOODNOTE ===")
        print(f"Login sebagai: {user}")

        # otomatis tampilkan mood semua user
        show_all_moods_after_login(user)

        print("\n=== MENU ===")
        print("1. Tambah Mood")
        print("2. Edit Mood Saya")
        print("3. Hapus Mood Saya")
        print("4. Logout/Keluar")

        pilih = input("Pilih: ")

        if pilih == "1":
            add_mood(user)
        elif pilih == "2":
            editmood(user)
        elif pilih == "3":
            delete_mood(user)
        elif pilih == "4":
            break
        else:
            print("Pilihan tidak valid!")

# =======================
# MAIN MENU
# =======================
def main():
    while True:
        os.system("cls")
        booting()
        # otomatis tampil mood sebelum login
        print('''--- 💌 Mood Terbaru Pengguna💌 ---\n''')
        show_all_moods_before_login()

        print("\n1. Register")
        print("2. Login")
        print("3. Exit MOODNOTES")

        pilih = input("Pilih: ")

        if pilih == "1":
            register()

        elif pilih == "2":
            user = login()
            if user:
                user_menu(user)

        elif pilih == "3":
            shutdown()
            break

        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
