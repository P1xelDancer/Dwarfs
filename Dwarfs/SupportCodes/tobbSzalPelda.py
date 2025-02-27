import time
import threading

# Játékos állapotok (elérhető vagy éppen számol)
players = {1: True, 2: True}

def count_for_player(player, seconds):
    """ Játékos számolási funkciója """
    global players
    print(f"Játékos {player} számolni kezd {seconds} másodpercig...")
    players[player] = False  # Játékos blokkolása
    time.sleep(seconds)  # Várakozás
    players[player] = True  # Játékos újra elérhető
    print(f"🔔 Játékos {player} befejezte a számolást!")

def start_counting(player):
    """ Felhasználótól bekérjük a számolási időt és elindítjuk a folyamatot """
    if not players[player]:
        print(f"⏳ Játékos {player} épp számol, várj...")
        return

    try:
        seconds = int(input(f"Játékos {player}, meddig számoljunk? (másodperc): "))
        if seconds <= 0:
            print("Hibás idő! Próbáld újra.")
            return

        # Új szál indítása a számolásra
        thread = threading.Thread(target=count_for_player, args=(player, seconds))
        thread.start()
    except ValueError:
        print("Hibás bemenet! Kérlek számot adj meg.")

def menu():
    """ Menü a játékos kiválasztásához """
    while True:
        print("\n--- Válassz játékost ---")
        print("1 - Játékos 1")
        print("2 - Játékos 2")
        print("0 - Kilépés")
        
        choice = input("Választásod: ")
        
        if choice == "1":
            start_counting(1)
        elif choice == "2":
            start_counting(2)
        elif choice == "0":
            print("Kilépés...")
            break
        else:
            print("❌ Érvénytelen választás!")

# Menü indítása
menu()
