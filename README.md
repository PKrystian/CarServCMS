# CarServCMS

Projekt demonstracyjny FastAPI z bazą danych PostgreSQL uruchamiany za pomocą Docker Compose.

### Database Access

The application uses a PostgreSQL database. You can manage it using the included pgAdmin instance.

-   **pgAdmin URL:** [http://localhost:5050/pgadmin](http://localhost:5050/pgadmin)
-   **pgAdmin Login:**
    -   Email: `admin@admin.com`
    -   Password: `admin`

**Database Credentials:**

-   **Host:** `postgres`
-   **Port:** `5432`
-   **Database Name:** `carserv`
-   **Application User:** `user` / `password`
-   **Admin User:** `admin` / `admin`

The database connection in pgAdmin is automatically configured as "CarServ DB".

## API Usage

The API is accessible at [http://localhost:8000](http://localhost:8000). Documentation (Swagger UI) is available at [http://localhost:8000/docs](http://localhost:8000/docs).

**Available Key Endpoints:**

-   `GET /users`: List all users.
-   `GET /pages`: List all pages.
-   `GET /content`: List all content items.

**Authentication:**
-   Username: `admin`
-   Password: `admin`

### Resetting the Database

If you need to reset the database (e.g., to apply a new schema from `init.sql`), use the `clean_start` command. **WARNING: This will delete all data in the database.**

```bash
./run.bat clean_start
```

This command removes the Docker volumes associated with the project and then rebuilds and starts the containers.

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
1. `run.bat build_start` - budowanie i startowanie kontenerów
3. `run.bat stop` - zatrzymanie aplikacji

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