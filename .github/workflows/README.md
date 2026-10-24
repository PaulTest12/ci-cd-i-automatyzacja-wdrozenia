# Pipeline

Główny workflow znajduje się w `pipeline.yml`. Testy i build obrazu są wykonywane przy Pull Requestach i pushach na `main`. Obraz GHCR jest publikowany tylko dla pushów do `main`. Zadanie `deploy` jest opcjonalne i wymaga zmiennej repozytorium `DEPLOY_ENABLED=true` oraz sekretów serwera opisanych w głównym README.
