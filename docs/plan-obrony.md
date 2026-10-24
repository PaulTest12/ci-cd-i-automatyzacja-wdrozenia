# Plan prezentacji i obrony

1. Przedstawić problem: ręczne testowanie i wdrażanie zwiększa ryzyko błędów.
2. Pokazać repozytorium i podział na aplikację, testy, kontenery oraz pipeline.
3. Omówić przepływ: push → lint/test → build obrazu → publikacja → opcjonalny deploy.
4. Otworzyć GitHub Actions i pokazać rzeczywiste logi przejścia testów.
5. Zademonstrować błąd testu, który blokuje publikację.
6. Po skonfigurowaniu VPS pokazać wdrożenie oraz endpoint `/health`.
7. Omówić ograniczenia i możliwe rozszerzenia: rollback, HTTPS, monitoring, środowiska staging/production.

## Pytania, które mogą paść

**Dlaczego CI i CD?** CI automatycznie integruje zmiany i weryfikuje kod; CD automatyzuje przygotowanie wydania i jego dostarczenie/wdrożenie.

**Dlaczego Docker?** Ujednolica środowisko uruchomieniowe pomiędzy komputerem programisty i serwerem.

**Po co tag SHA?** Pozwala wskazać dokładną wersję kodu odpowiadającą wdrożonemu obrazowi.

**Co się dzieje, jeśli test nie przejdzie?** Publikacja zależy od zakończenia testów sukcesem, więc nie zostanie uruchomiona.

**Czy aplikacja automatycznie wdraża się na serwerze od razu?** Tylko po skonfigurowaniu `DEPLOY_ENABLED=true`, sekretów SSH i działającego serwera z Dockerem. Bez tego workflow testuje kod i publikuje obraz, a job deploy jest pomijany.
