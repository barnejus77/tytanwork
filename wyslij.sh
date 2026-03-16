#!/bin/bash
echo "--- Rozpoczynam wysyłanie do GitHub ---"
git add .
git commit -m "Aktualizacja z dnia: $(date)"
git push
echo "--- Gotowe! ---"
