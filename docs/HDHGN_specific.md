# Dokumentacja wykorzystania modelu HDHGN

Ta część dokumentacji HDHGN opisuje wykorzystanie poszczególnych funkcji znajdujących się w plikach HDHGN. 

## Opisy skryptów

### PredictFile.py

**Cel:** Przewidywanie etykiety dla danego pliku źródłowego przy użyciu wstępnie wytrenowanego modelu HDHGN.

**Użycie:**

```
python PredictFile.py --file_path <ścieżka_do_pliku_źródłowego> --model_path <ścieżka_do_modelu> --vocab_path <ścieżka_do_słownika>
```

**Argumenty:**

- `file_path`: Ścieżka do pliku źródłowego, który ma być przewidziany.
- `model_path`: Ścieżka do wstępnie wytrenowanego modelu.
- `vocab_path`: Ścieżka do pliku słownika.

**Funkcje:**

- `predict(file_path, model_path, vocab_path)`: Główna funkcja do przewidywania etykiety dla danego pliku.

**Przykład:**

```bash
python PredictFile.py --file_path plik_do_klasyfikacji.py --model_path model.pth --vocab_path vocab.json
```

### ProcessData.py

**Cel:** Podział zbioru danych na zestawy treningowe, walidacyjne i testowe dla plików źródłowych Python i C.

**Użycie:**

```
python ProcessData.py [-p] [-c]

opcje:
  -p   czy przetworzyć pliki Python
  -c   czy przetworzyć pliki C
```

**Funkcje:**

- `splitdata(source_files_path)`: Podział plików źródłowych Python na zestawy treningowe, walidacyjne i testowe.
- `splitdata_c(source_files_path)`: Podział plików źródłowych C na zestawy treningowe, walidacyjne i testowe.

### vocab.py

**Cel:** Utworzenie słownika dla plików źródłowych Python i C.

**Użycie:**

```
python vocab.py [-p] [-c]

opcje:
  -p   czy stworzyć słownik dla plików Python
  -c   czy stworzyć słownik dla pliki C
```

### prepare_source_files.py

**Cel:** Przygotowanie plików źródłowych poprzez zmianę rozszerzeń plików i przenoszenie plików do odpowiednich katalogów.

**Użycie:**

```
python prepare_source_files.py --num_files <liczba_plików_do_wygenerowania> --directory_python <ścieżka_do_katalogu_z_plikami_python> --directory_c <ścieżka_do_katalogu_z_plikami_c>
```

**Funkcje:**

- `change_files_extensions(directory)`: Zmiana rozszerzeń plików z .txt na .py.
- `change_files_extensions_c(directory)`: Zmiana rozszerzeń plików z .txt na .c.
- `move_files(source_path, new_path, num_files)`: Przenoszenie plików Python do nowych katalogów.
- `move_files_c(source_path, new_path, num_files)`: Przenoszenie plików C do nowych katalogów.

### clear_train_directories.py

**Cel:** Czyszczenie katalogów treningowych i plików w celu przygotowania do nowej sesji treningowej.

**Użycie:**

```
python clear_train_directories.py
```

**Działanie:**

- Skrypt iteruje przez listę katalogów i plików, aby je usunąć, jeśli istnieją.

## Zależności

- Python 3.11
- PyTorch 2.5.1
- torch-geometric 2.6.1
- Dodatkowe zależności wymienione w requirements.txt
