# Opis architektury

## Cel

Platforma automatyzuje powtarzalne czynności potrzebne do dostarczenia nowej wersji aplikacji internetowej. Zmiana kodu uruchamia pipeline, który sprawdza jakość i testy przed publikacją obrazu. Opcjonalny etap deploy uruchamia ten obraz na serwerze Linux.

## Komponenty

- **GitHub repository** — przechowuje kod, Dockerfile, testy i definicje pipeline'u.
- **GitHub Actions** — wykonuje kroki automatyzacji po `push`, Pull Request lub ręcznym wywołaniu.
- **Ruff** — statyczna kontrola kodu Python.
- **pytest** — testy endpointów aplikacji.
- **Docker Buildx / GHCR** — budowanie i publikowanie wersjonowanego obrazu kontenera.
- **Linux + Docker Compose** — opcjonalne środowisko docelowe.
- **SSH secrets** — bezpieczne przekazanie parametrów dostępu do serwera przez ustawienia repozytorium, a nie przez kod.

## Przepływ CI/CD

1. Push lub Pull Request.
2. Instalacja zależności.
3. Lint i testy.
4. Budowanie obrazu w trybie kontrolnym.
5. Po udanym pushu na `main`: publikacja obrazu z tagiem SHA i `latest`.
6. Jeśli zmienna `DEPLOY_ENABLED` ma wartość `true`: połączenie SSH, pobranie obrazu, uruchomienie kontenera i sprawdzenie `/health`.

## Dlaczego tag SHA?

Tag zawierający identyfikator commita jednoznacznie wiąże wdrożony obraz z wersją źródła. Tag `latest` ułatwia podgląd najnowszej publikacji, ale do wdrażania używany jest konkretny SHA.

## Ograniczenia

Przykład nie implementuje automatycznego rollbacku ani HTTPS. W środowisku produkcyjnym należy dodać reverse proxy (np. Caddy lub Nginx), certyfikat TLS, monitoring, kontrolę dostępu do GHCR, kopie zapasowe i procedurę rollbacku.
