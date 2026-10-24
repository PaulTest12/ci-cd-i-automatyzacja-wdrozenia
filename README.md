# Platforma automatycznego wdrażania aplikacji internetowych

Prosty demonstrator CI/CD: zmiana kodu w GitHub uruchamia testy i kontrolę jakości, sprawdza możliwość zbudowania obrazu Docker, a po wypchnięciu zmian do `main` publikuje obraz w GitHub Container Registry (GHCR). Opcjonalnie workflow może wdrożyć obraz na serwerze Linux przez SSH.

## 1. Architektura

1. Programista wypycha zmianę do repozytorium GitHub lub otwiera Pull Request.
2. GitHub Actions instaluje zależności, uruchamia Ruff i testy pytest.
3. Pipeline buduje obraz Docker, aby wykryć błędy konteneryzacji.
4. Po zmianie na `main` obraz jest publikowany w GHCR pod tagiem SHA commita i `latest`.
5. Jeśli skonfigurowano serwer i zmienną repozytorium `DEPLOY_ENABLED=true`, nowy obraz jest pobierany przez serwer, uruchamiany przez Docker Compose i sprawdzany endpointem `/health`.

## 2. Uruchomienie lokalne

Wymagane: Python 3.12+ oraz opcjonalnie Docker Desktop.

PowerShell, z głównego katalogu repozytorium:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r apps/web-app/requirements.txt -r apps/web-app/requirements-dev.txt
py -m ruff check apps/web-app
py -m pytest -q apps/web-app/tests
```

Uruchom aplikację bez Dockera:

```powershell
Set-Location apps/web-app
py -m flask --app apps/web-app/app.py run --host 127.0.0.1 --port 8000
```

Następnie otwórz `http://127.0.0.1:8000/` lub `http://127.0.0.1:8000/health`.

Alternatywnie uruchom przez Docker Compose:

```powershell
docker compose up --build -d
```

Aby zatrzymać kontener:

```powershell
docker compose down
```

## 3. Wgranie projektu na GitHub

1. Rozpakuj archiwum ZIP.
2. Na https://github.com/new utwórz repozytorium `web-deployment-platform`. Na początek nie dodawaj README, licencji ani `.gitignore` przez formularz.
3. Otwórz PowerShell w rozpakowanym folderze projektu.
4. Wykonaj polecenia (zastąp `TWOJ_LOGIN` swoją nazwą użytkownika GitHub):

```powershell
git init
git add .
git commit -m "Initial commit: web deployment platform"
git branch -M main
git remote add origin https://github.com/TWOJ_LOGIN/web-deployment-platform.git
git push -u origin main
```

Jeśli Git nie zna tożsamości autora, ustaw lokalnie swoje dane:

```powershell
git config user.name "Twoje Imię"
git config user.email "adres-uzywany-na-githubie@example.com"
```

Po ustawieniu danych ponów `git commit` i `git push`.

## 4. Co sprawdzić w GitHub Actions

1. Otwórz repozytorium w przeglądarce.
2. Wybierz zakładkę **Actions**.
3. Otwórz workflow **Build, test and deploy**.
4. Wejdź w najnowsze wykonanie i sprawdź zadania `test` oraz `publish-image`.
5. `test` powinien przejść dla Pull Requestów oraz pushy. `publish-image` publikuje obraz tylko po pushu na `main`.
6. Bez serwera zadanie `deploy` ma status **skipped** — to oczekiwane zachowanie. Publikacja obrazu w GHCR jest osobnym krokiem od wdrożenia na serwer.

## 5. Opcjonalne wdrożenie na serwer Linux

Potrzebujesz dostępnego przez SSH serwera Linux z Docker Engine i wtyczką Docker Compose. Użytkownik SSH musi móc uruchamiać polecenia `docker` bez interaktywnego wpisywania hasła. Przykładowy port aplikacji to `8080`.

### 5.1. Przygotuj dostęp SSH

Na swoim komputerze wygeneruj oddzielny klucz wdrożeniowy (nie używaj klucza prywatnego, którego nie chcesz udostępniać w CI):

```powershell
New-Item -ItemType Directory -Force "$HOME/.ssh" | Out-Null
ssh-keygen -t ed25519 -C "github-actions-deploy" -f "$HOME/.ssh/web-deploy-key"
```

Dodaj zawartość `web-deploy-key.pub` do `~/.ssh/authorized_keys` użytkownika na serwerze. Klucz prywatny `web-deploy-key` nigdy nie trafia do repozytorium.

W ustawieniach repozytorium otwórz **Settings → Secrets and variables → Actions** i dodaj sekrety:

- `DEPLOY_HOST` — adres IP lub domena serwera.
- `DEPLOY_USER` — nazwa użytkownika SSH.
- `DEPLOY_SSH_KEY` — cała zawartość prywatnego klucza `web-deploy-key`.
- `DEPLOY_HOST_FINGERPRINT` — odcisk klucza SSH serwera; dodaj go przed włączeniem wdrażania, aby zweryfikować tożsamość hosta. Można go odczytać na serwerze poleceniem `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` (wartość SHA256).

Jeśli obraz GHCR ma być prywatny, dodaj również `GHCR_USER` oraz `GHCR_TOKEN` (PAT z minimalnym zakresem `read:packages`). Jeśli obraz jest publiczny, te dwa sekrety nie są potrzebne. Nigdy nie zapisuj sekretów w plikach repozytorium. Dla publicznego obrazu GHCR nie trzeba definiować `GHCR_USER` i `GHCR_TOKEN`; dla prywatnego obrazu trzeba ustawić oba sekrety.

### 5.2. Włącz wdrażanie

W sekcji **Settings → Secrets and variables → Actions → Variables** utwórz zmienną repozytorium:

- `DEPLOY_ENABLED` = `true`
- opcjonalnie `APP_PORT` = `8080`

Na serwerze upewnij się, że port 8080 jest dozwolony w firewallu, jeśli aplikacja ma być dostępna z internetu. Domyślnie proces deploy sprawdza aplikację lokalnie na serwerze przez `curl`.

Przy kolejnym pushu do `main` workflow wykona testy, opublikuje obraz i uruchomi go na serwerze. W zakładce Actions obejrzyj logi zadania `deploy`.

### Uwaga o GHCR

Po pierwszym opublikowaniu obrazu można zarządzać jego widocznością w ustawieniach pakietu GitHub Container Registry. Jeżeli pakiet pozostaje prywatny, serwer potrzebuje tokenu z uprawnieniem `read:packages`, przechowywanego jako sekret `GHCR_TOKEN`.

## 6. Test błędnego wdrożenia

W pliku `apps/web-app/tests/test_app.py` tymczasowo zmień oczekiwany status zdrowia z `ok` na `broken`, zapisz plik i wypchnij zmianę na gałąź roboczą / utwórz Pull Request. Test ma się nie powieść, a publikacja i wdrożenie nie powinny się uruchomić. Cofnij zmianę po demonstracji.

## 7. Co zawiera demonstrator

- aplikację Flask z endpointami `/`, `/health` i `/items`;
- testy automatyczne;
- kontrolę stylu Ruff;
- Dockerfile i Docker Compose;
- GitHub Actions do testowania, budowania i publikacji obrazu;
- opcjonalny etap zdalnego wdrażania przez SSH;
- dokumentację architektury i scenariuszy testowych.

To demonstrator edukacyjny, a nie gotowy system produkcyjny. Przed rzeczywistym użyciem należy dodatkowo skonfigurować HTTPS/reverse proxy, monitoring, kopie zapasowe i politykę aktualizacji zależności.
