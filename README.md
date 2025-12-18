# CarServCMS

Projekt demonstracyjny FastAPI z bazą danych PostgreSQL uruchamiany za pomocą Docker Compose.

## Stos Technologiczny i Wersje

**Środowisko:**
- **Python**: 3.10 (obraz `python:3.10-slim`)
- **Baza danych**: PostgreSQL 15 (obraz `postgres:15`)

**Główne Biblioteki (zainstalowane w kontenerze):**
- **FastAPI**: (najnowsza wersja) - framework webowy
- **Uvicorn**: (najnowsza wersja) - serwer ASGI
- **SQLAlchemy**: (najnowsza wersja) - ORM do bazy danych
- **Psycopg2-binary**: (najnowsza wersja) - sterownik PostgreSQL

## Baza Danych

Baza danych jest dostępna lokalnie na porcie `5432`.

**URL połączenia (Connection String):**
```
postgresql://user:password@localhost:5432/carserv
```

- **Host**: `localhost`
- **Port**: `5432`
- **Użytkownik**: `user`
- **Hasło**: `password`
- **Nazwa bazy**: `carserv`

## Uruchomienie

Użyj skryptu `run.bat`:
1. `run.bat build_project` - budowanie kontenerów
2. `run.bat start_project` - uruchomienie aplikacji
3. `run.bat stop_project` - zatrzymanie aplikacji

Aplikacja będzie dostępna pod adresem: http://localhost:8000
Dokumentacja Swagger UI: http://localhost:8000/docs

## Przykładowe Requesty (Curl)

Aplikacja wykorzystuje Basic Auth.
**Login**: `admin`
**Hasło**: `admin`

### 1. Pobranie listy użytkowników
Ten endpoint zwraca listę wszystkich użytkowników z tabeli `users`.
```bash
curl -u admin:admin http://localhost:8000/users
```
*Działanie: FastAPI weryfikuje poświadczenia, następnie zapytuje bazę danych przez SQLAlchemy i zwraca listę obiektów JSON.*

### 2. Pobranie szczegółów użytkownika
Pobiera dane konkretnego użytkownika po ID (np. ID=1).
```bash
curl -u admin:admin http://localhost:8000/users/1
```
*Działanie: Szuka rekordu o danym ID. Jeśli nie znajdzie, zwraca błąd 404.*

### 3. Statystyki
Zwraca liczbę użytkowników w bazie.
```bash
curl -u admin:admin http://localhost:8000/stats
```