# Projekt inżynieria oprogramowania

## Temat: “Czyj to kod?”

### Treść zadania <br>

System wykrywający plagiaty w kodzie źródłowym:

- analiza potencjalnych metod plagiatowania kodu źródłowego,
- opracowanie systemu wykrywającego plagiaty za pomocą konfigurowalnych miar podobieństwa, repozytorium lokalnego oraz dostępu do repozytoriów zdalnych (GIT i inne),
- dostosowanie do cech szczególnych danego języka programowania (lista słów kluczowych, komentarze, separatory itp.),
- raportowanie online,
- budowa bazy testowej (min. 50 fragmentów kodu po 30 wierszy).

**Efekt wow!**: opracowanie detekcji dia więcej niż jednego języka programowania.

## Informacje do kodu:

Jesli chcemy, żeby środowisko dobrze nam śmigało, to:

- Instalujemy gita na swojej maszynie,
- Pobieramy i instalujemy Python 3.13.1 na swojej maszynie, <br>
  _tu warto zaznaczyć, żeby dodał environment variables do path w systemie_
- Pobieramy i instalujemy Node.js v20.15.0 bądż wyższą na swojej maszynie, <br>
- Tworzymy nowy pusty folder,
- Klonujemy repo z githuba: <br>
  `git clone https://github.com/PikkiKaju/Projekt_Inzynieria_Oprogramowania` <br>
- Tworzymy wirtualne środowisko (venv) Pythona w tym folderze poprzez pobranego Python'a: <br>
  `python -m venv "pełna ścieżka do folderu"` <br>
  ew. korzystamy z IDE (jak np. VS Code), żeby nam to zrobiło z odpowiednią wersją Pythona jesli mamy ich kilka,
- Aktywujemy venv: <br>
  `.venv\Scripts\activate`
- Instalujemy Django i wymagane biblioteki <br>
  `pip install -r backend/requirements.txt`
- Tworzymy migracje w django, które utworzą nam baze danych i inne struktury: <br>
  `python manage.py backend/makemigrations`
  `python manage.py backend/migrate`
- Instalujemy Reacta i wymagane biblioteki node'a <br>
  `npm install`

Teraz powinniśmy mieć aktywne venv i doinstalowane wszystko co potrzebne, żeby Python i React działały w naszym projekcie.

### Jak wlączyć serwer backendowy:

Żeby włączyć lokalny serwer backendowy zrobiony za pomocą Django:

- Włączamy serwer: <br>
  `py backend/manage.py runserver`
- Wchodzimy w przeglądarce na `localhost:8000` (domyślny port to 8000, ale może u was uruchomi się na innym, jeśli ten jest zajęty)

### Jak wlączyć aplikację frontendową:

Żeby włączyć frontend zriobiony w React'cie, to musimy włączyć lokalny serwer Reacta:

- Włączamy aplikację Reactową: <br>
  `npm start`
- Wchodzimy w przeglądarce na `localhost:3000` (domyślny port to 3000, ale może u was uruchomi się na innym, jeśli ten jest zajęty)

##### Więcej informacji np. odnośnie API w django rest framework jest w docs/api
