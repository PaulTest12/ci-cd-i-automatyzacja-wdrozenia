# Scenariusze testowe

| ID | Scenariusz | Oczekiwany wynik |
|---|---|---|
| T1 | GET `/` | HTTP 200 i informacja o aplikacji |
| T2 | GET `/health` | HTTP 200 i `status: ok` |
| T3 | GET `/items` | HTTP 200 i lista dwóch elementów |
| T4 | GET nieistniejącej ścieżki | HTTP 404 i odpowiedź JSON |
| T5 | Lint Ruff | Brak błędów stylu / typowych usterek |
| T6 | Błąd w teście | Zadanie `test` kończy się niepowodzeniem; publikacja i deploy są blokowane |
| T7 | Push na `main` po przejściu testów | Obraz zostaje opublikowany w GHCR |
| T8 | Brak `DEPLOY_ENABLED=true` | Job `deploy` jest pomijany, CI i publikacja nadal mogą się zakończyć sukcesem |
| T9 | Poprawna konfiguracja serwera | Kontener zostaje uruchomiony, a `/health` odpowiada poprawnie |

## Dowód wykonania

Do dokumentacji końcowej należy dołączyć zrzuty z GitHub Actions po rzeczywistym uruchomieniu workflow. Nie należy wpisywać fikcyjnych wyników czasu ani statusu. Testy lokalne i testy wykonane w Actions należy oznaczać oddzielnie.
