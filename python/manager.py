
import datetime
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import time
class NetworkManager:
    def __init__(self):
        self.devices = []
    
    def __len__(self):
        return len(self.devices)
    def __getitem__(self, index):
        return self.devices[index]
    def load_from_json(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for item in data:
                    if item["type"] == "antenna":
                        device = Antena(item["ip"], item["brand"], item["gain"])
                    elif item["type"] == "router":
                        device = Router(item["ip"], item["brand"], item["port"])
                
                    self.add_device(device)
            print(f"Pomyślnie wczytano {len(data)} urządzeń z pliku {filename}.")
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {filename}")
        except Exception as e:
            print(f"Wystąpił błąd podczas wczytywania: {e}")
    
    def send_telegram_alert(self,message):
        token = "**************************"
        chat_id = "7165931128"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
    
        payload = {
            "chat_id": chat_id,
            "text": message
        }
    
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"Błąd wysyłania powiadomienia: {e}")

    def add_device(self, device):
        self.devices.append(device)

    def show_all_active(self):
        for device in self.devices:
            if device.is_active:
                device.get_status()
   
    def count_by_brand(self, brand_name):
        count = 0
        for device in self.devices:
            if brand_name == device.brand:
                count += 1
        return count
    def health_check(self):
        online = 0
        offline = 0
        print(f"\n--- Skanowanie sieci: {datetime.datetime.now().strftime('%H:%M:%S')} ---")
        with ThreadPoolExecutor(max_workers=10) as executor:
            # executor.map zwraca iterator z wynikami funkcji check_device
            results = list(executor.map(self.check_device, self.devices))
            
        # Teraz po prostu liczymy True i False w liście wyników
        online = results.count(True)
        offline = results.count(False)
        total = len(self.devices)

        print("\n=== PODSUMOWANIE STATUSU ===")
        print(f"✅ Online:  {online}")
        print(f"❌ Offline: {offline}")
        print(f"📊 Łącznie: {total}")

           
           
    def check_device(self,device):     
        
        try:
            device.ping()
            print(f"[OK] {device.brand} ({device.ip}) jest online.")
            return True
            
        except ConnectionError as e:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[ALARM] {e}")
            self.send_telegram_alert(f" ALARM SIECIOWY!\n{e}")
            with open("network_errors.txt", "a") as file:
                file.write(f"[{timestamp}] BŁĄD: {e}\n")
            return False
        
    def remove_device(self, ip):
        self.devices = [d for d in self.devices if d.ip != ip]
    def save_to_json(self):
        lista=[]    
        for device in self.devices: 
            if isinstance(device, Antena):              
                dane = {"type":"antenna", "ip":device.ip, "brand": device.brand, "gain": device.gain}
            else:
                dane = {"type":"router", "ip":device.ip, "brand": device.brand, "port": device.port}
            lista.append(dane)
        with open('devices.json', 'w', encoding='utf-8') as f:
            json.dump(lista, f, ensure_ascii=False, indent=4)
    def start_monitoring(self, interval=30):
        print(f"\n Uruchomiono monitoring ciągły (interwał: {interval}s)")
        print("Naciśnij Ctrl+C, aby wrócić do menu głównego.")
        try:
            while True:
                self.health_check()
                print(f"--- Czekam {interval} sekund na kolejny skan... ---")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n Monitoring przerwany przez użytkownika.")

from abc import ABC, abstractmethod
import random
import os
import ipaddress
class NetworkDevice(ABC):  
    def __init__(self, ip, brand, is_active=True):
        self.ip = ip
        self.brand = brand
        self.is_active = is_active
    
    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        try:
            ipaddress.ip_address(value)
            self._ip = value
        except ValueError:
            raise ValueError(f"Niepoprawny adres IP: {value}")

    @abstractmethod  
    def get_status(self):
        pass

    def __str__(self):
        return f"Urządzenie {self.brand} IP {self.ip}"
    def ping(self):
        
        # -c 1 oznacza 1 pakiet, -W 1 to timeout (1 sekunda czekania)
        # > /dev/null 2>&1 to magia Linuxa, która ucisza konsolę (nie śmieci nam w terminalu)
        response = os.system(f"ping -c 1 -W 1 {self.ip} > /dev/null 2>&1")
        if response == 0:
            return True 
        else:
            raise ConnectionError(f"Host {self.ip} nie odpowiada na PING")
    
        
         

        
class Antena(NetworkDevice):
    def __init__(self, ip, brand, gain):
        super().__init__(ip, brand)
        self.gain = gain
    def get_status(self):
        print(f"Antena {self.brand} (IP: {self.ip}) ma zysk {self.gain} dBi.")

class Router(NetworkDevice):
    def __init__(self, ip, brand, port):
        super().__init__(ip, brand)
        self.port = port
    def get_status(self):
        print(f"Router {self.brand} (IP: {self.ip}) ma  {self.port} portów .")
def main():
    manager = NetworkManager()
    manager.load_from_json("devices.json")
    
    while True:
        print("\n=== SYSTEM MONITORINGU SIECI ===")
        print("1. Pokaż wszystkie urządzenia")
        print("2. Uruchom skanowanie (Health Check)")
        print("3. Statystyki marek")
        print("4. Dodaj urządzenie")
        print("5. Monitoring ciągły (Auto-Skan)")
        print("6. Wyjście")
        
        wybor = input("Wybierz opcję (1-6): ")

        if wybor == "1":
            manager.show_all_active()
        elif wybor == "2":
            manager.health_check()
        elif wybor == "3":
            marka = input("Podaj nazwę marki: ")
            print(f"Liczba urządzeń {marka}: {manager.count_by_brand(marka)}")
        elif wybor == "4":
             while True:
                 print("1. Antena")
                 print("2. Router")
                 print("3. Powrót do menu")
                 choice = input("Wybierz opcje ")
                 try:
                    if choice == "1":
                        device = Antena(input("podaj IP \n"),input("podaj Brand \n"),input("podaj Gain \n"))
                        manager.add_device(device)
                        print(f"{device} dodano")
                    elif choice == "2":
                        device = Router(input("podaj IP \n"),input("podaj Brand \n"),input("podaj ilosc portow \n"))
                        manager.add_device(device)
                        print(f"{device} dodano")
                    elif choice == "3":
                        break
                 except ValueError as e:
                     print(f" Błąd: {e}. Spróbuj ponownie.")
        elif wybor == "5":
            sekundy = input("Co ile sekund skanować? (domyślnie 30): ")
            interwal = int(sekundy) if sekundy.isdigit() else 30
            manager.start_monitoring(interwal)
        elif wybor == "6":
            print("Zamykanie systemu... Do zobaczenia!")
            manager.save_to_json()
            break
        else: 
            print("Niepoprawny wybór, spróbuj ponownie.")

if __name__ == "__main__":
    main()    








