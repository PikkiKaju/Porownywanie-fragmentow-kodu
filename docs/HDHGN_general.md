# Heterogeneous Directed Hypergraph Neural Network (HDHGN)

## Wstęp

Jest to implementacja modelu Heterogenicznej Skierowanej Sieci Neuronowej Hipergrafów (HDHGN) z artykułu [Heterogeneous Directed Hypergraph Neural Network over abstract syntax tree (AST) for Code Classification](https://doi.org/10.18293/SEKE2023-136).

Pliki zawarte tutaj służą do przeprocesowania plikow z kodem źródłowym z naszej bazy i utworzeniu sieci HDHGN.

## Wymagania

Oryginalnie w artykule wszystko zostało przeprowadzone na Ubuntu 18.04.6 LTS i Pythonie 3.8.
Nasz projekt korzysta jednak z Pythona 3.13 (najnowszego na obecny czas), aczkolwiek niestety ta wersja nie jest kompatybilna z PyTorchem i innymi wymaganymi bibliotekami, więc tutaj zastosowany został najnowszy możliwy Python 3.11.

Model zaimplementowany jest za pomocą [PyTorch](https://pytorch.org/docs/2.5/) 2.5.1 i [torch geometric 2.6.1](https://pytorch-geometric.readthedocs.io/en/2.6.1/index.html). Model trenuje się albo poprzez CPU albo poprzez rdzenie CUDA w GPU NVIDIA. W moim przypadku było to robione za pomocą CUDA na karcie GTX 1660.
Aby korzystać z rdzeni CUDA potrzebny jest CUDA toolkit, który trzeba zainstalować w odpowiedniej wersji i dobrany do swojego systemu. W moim przypadku był to toolkit CUDA w wersji 12.4 (najnowsza wersja, którą obsługuje PyTorch)

Wymagane biblioteki są wymienione w pliku requirements.txt, z tym że całość PyTorch'a najlepiej zainstalować ręcznie, (te biblioteki są w requirements.txt zakomentowane). Poniżej jak to zrobić:
`pip install torch==2.5.1+cu124`
`pip install torch-geometric==2.6.1`
`pip install torch-scatter -f https://pytorch-geometric.com/whl/torch-2.5.1+cu124.html`

## Zbiory danych

Nasze zbiory danych pochodzą z [naszego folderu z algorytmami](https://drive.google.com/drive/folders/1xPyS70uPEFWSz7teoBGzQTof4sTWfsff). Trzeba je pobrać i pliki odpowiednio z Pythonem i z C wrzucić do folderów /data/txt_python_files i /data/txt_c_files.

## Użycie ogólne

Będąc w katalogu `/HDHGN` możemy bezpośrednio korzystać z:
`.\run.ps1`

run.sh wykonuje następujące czynności:

1. Przetwarza pliki źródłowe.
2. Uruchamia `ProcessData.py`, żeby losowo podzielić dane na zestawy treningowe, walidacyjne i testowe w proporcji 6:2:2. Nie dzieli bezpośrednio danych, zapisuje tylko odpowiadające im ścieżki.
3. Uruchamia `vocab.py`, żeby wygenerować pliki słownika.
4. Uruchamia `trainHDHGN.py` i `trainHDHGN_c.py`, żeby wytrenować model na plikach Python i C, po czym testuje i waliduje model po treningu.

Jeśli nie chcesz używać run.sh do wykonania wszystkich operacji naraz, można również wykonać je krok po kroku.

Model zostanie zapisany w katalogu `work_dir`, a wyniki w `work_dir/results`.xlsx. Wygenerowane też będą rysunki zmian funkcji strat i wyników dla zestawu walidacyjnego i testowego zapisane w `work_dir/HDHGN/XXX-loss.png` i `work_dir/HDHGN/XXX-accuracy.png`.

**Na moim sprzęcie udało się wytrenować sieć na plikach Python, lecz z plikami C miałem problemy, więc możecie napotkać błędy w terminalu.**
