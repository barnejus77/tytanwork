#!/bin/bash
echo "--- Rozpoczynam wysyłanie do GitHub jak nie zabraknie neta :-) ---"
if ping -c 1 google.com; then
	git add .
	echo "Co dzisiaj zrobiłeś?"
	read opis
	git commit -m "$opis"
	git push
	if [$? eq 0]; then 
		echo "[OK]" Gotowe!
	else 
		echo "[ERROR] niestety brak netu"
	fi
else 
	echo "Brak internetu zapis lokalny"
	git add .
	echo "co dzisaj zrobiles"
	read opis
	git commit -m "$opis"
	if [$? eq 0]; then 
                echo "[OK] Gotowe! Zmiany zapisane tylko lokalnie"
        else
                echo "[ERROR] masz dzisaj pecha nic nie dziala"
        fi

fi

