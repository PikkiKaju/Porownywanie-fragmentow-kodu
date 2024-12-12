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

- instalujemy gita na swojej maszynie
- pobieramy i instalujemy Pythona 3.13.1 na swojej maszynie <br>
  _tu warto zaznaczyć, żeby dodał environment variables do path w systemie_
- tworzymy nowy pusty folder
- klonujemy repo z githuba: <br>
  `git clone https://github.com/PikkiKaju/Projekt_Inzynieria_Oprogramowania` <br>
- tworzymy wirtualne środowisko (venv) Pythona w tym folderze poprzez pobranego Python'a: <br>
  `python -m venv "pełna ścieżka do folderu"` <br>
  ew. korzystamy z IDE (jak np. VS Code), żeby nam to zrobiło z odpowiednią wersją Pythona jesli mamy ich kilka
- aktywujemy venv: <br>
  `.venv\Scripts\activate`
- instalujemy Django i wymagane biblioteki <br>
  `pip install -r backend/requirements.txt`

Teraz powinniśmy mieć aktywne venv i doinstalowane wszystko co potrzebne, żeby Python działał w naszym projekcie.

### Jak wlączyć serwer backendowy:

Żeby odpalić lokalny serwer backendowy zrobiony za pomocą Django:

- włączamy serwer: <br>
  `py backend/manage.py runserver`
- wchodzimy w przeglądarce na `localhost:8000` (domyślny port to 8000, ale może u was uruchomi się na innym, jeśli ten jest zajęty)

### Jak wlączyć aplikację frontendową:

Żeby włączyć frontend zriobiony w React'cie, to musimy włączyć lokalny runtime Node'a:

- przechodzimy do folderu z Reactem: <br>
  `cd /backend/frontend`
- instalujemy biblioteki Node'a:
  `npm install`
- włączamy aplikację React'ową: <br>
  `npm start`
- wchodzimy w przeglądarce na `localhost:3000` (domyślny port to 3000, ale może u was uruchomi się na innym, jeśli ten jest zajęty)
