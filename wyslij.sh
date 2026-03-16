#!/bin/bash
echo "--- Rozpoczynam wysyłanie do GitHub ---"
git add .
echo "Co dzisiaj zrobiłeś?"
read opis
git commit -m "$opis"
git push
echo "--- Gotowe! ---"
