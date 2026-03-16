#!/bin/bash
echo "--- Przygotowuję paczkę ---"

git add .
echo "Co dzisiaj zrobiłeś?"
read opis
git commit -m "$opis"

if [ $? -eq 0 ]; then
    echo "[OK] Zmiany zatwierdzone lokalnie."
    
    echo "--- Sprawdzam połączenie z GitHubem ---"
    if ping -c 1 google.com > /dev/null 2>&1; then
        git push
        if [ $? -eq 0 ]; then
            echo "[OK] Wszystko wysłane na GitHub!"
        else
            echo "[ERROR] Coś poszło nie tak z wysyłką."
        fi
    else
        echo "[INFO] Brak neta. Zmiany zostały tylko na laptopie."
    fi
else
    echo "[ERROR] Nie udało się zrobić commit (może brak zmian?)"
fi
