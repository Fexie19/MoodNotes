from rich.progress import track
import time
import os


def booting():
  os.system('cls')

  for step in track(range(10), description=f"Menjalankan MOODNOTES..."):
      t = 1
      time.sleep(0.2)
      if step == 9:
          t = 0

  if t == 0:
    os.system('cls')
    for step in track(range(1), description="MOODNOTES berhasil dijalankan..."):
                time.sleep(0.1)
                t = 2
      
  if t  == 2:
      print('''

      SELAMAT DATANG DI MOODNOTES

  ''')
      
      
def shutdown():
  os.system('cls')
  for step in track(range(10), description="Menghentikan MOODNOTES..."):
      t = 1
      time.sleep(0.1)
      if step == 9:
          t = 0

  if t == 0:
    os.system('cls')
    for step in track(range(1), description="MOODNOTES berhasil dihentikan..."):
                time.sleep(0)
                t = 2
      
  if t  == 2:
      print('''

            SAMPAI JUMPA
        JANGAN LUPA KEMBALI :)

  ''')