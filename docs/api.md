# Dokumentacja API

API jest zrobione z django rest-framework i póki co składa się z end-pointów do przesyłania tekstu i plików.

**Adres Bazowy:** `http://localhost:8000/`

### 1. Zarządzanie danymi tekstowymi (/wel/)

**Model:** `Text`

| Metoda | Opis                                     | Parametry w żądaniu (JSON)              | Odpowiedź (JSON)                                                | Kody odpowiedzi |
| ------ | ---------------------------------------- | --------------------------------------- | --------------------------------------------------------------- | --------------- |
| GET    | Pobiera wszystkie wpisy tekstowe z bazy. | Brak                                    | `[{ "id": int, "inputText": string }]`                          | 200             |
| POST   | Tworzy nowy wpis.                        | `{ "inputText": string }`               | `{ "id": int, "inputText": string }`                            | 201             |
| DELETE | Usuwa wpis o podanym ID.                 | Brak, ale wymaga ID w URL: `/wel/{id}/` | 204 No Content (sukces) <br> lub 404 Not Found (nie znaleziono) | 204, 404        |

##### Przykład użycia z `axios`:

```javascript
// Pobieranie wpisów tekstowych z serwera
axios
  .get("http://localhost:8000/wel/") // API endpoint URL
  .then((response) => {
    this.setState({ response: response.data });
  });

// Wysyłanie tekstu na serwer
axios
  .post("http://localhost:8000/wel/", // API endpoint URL
    { inputText: this.state.inputText } // tekst z inputu
  )
  .then((response) => {});

// Usuwanie wpisu z tekstem z bazy serwera
axios
  .delete(`http://localhost:8000/wel/${id}/`) // API endpoint URL z id wpisu do usunięcia
  .then((response) => {});
```

### 2. Zarządzanie plikami (/file/)

**Model:** `File`

| Metoda | Opis                              | Parametry w żądaniu (Multipart/form-data) | Odpowiedź (JSON)                                                         | Kody odpowiedzi |
| ------ | --------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------ | --------------- |
| GET    | Pobiera listę przesłanych plików. | Brak                                      | `[{ "id": int, "file_name": string, file_content": string }]`            | 200, 404        |
| GET    | Pobiera plik o podanym ID.        | Brak, ale wymaga ID w URL: `/file/{id}/`  | `{ "id": int, "file_name": string, file_content": string }`              | 200, 404        |
| POST   | Przesyła nowy plik.               | `FormData` (dane z formularza z plikiem)  | `{ "id": int, "file": string }`                                          | 201             |
| DELETE | Usuwa plik o podanym ID.          | Brak, ale wymaga ID w URL: `/file/{id}/`  | 204 No Content (sukces) lub 404 Not Found                                | 204, 404        |


##### Przykład użycia z `axios`:

```javascript
// Wysyłanie pliku na serwer
const formData = new FormData(); // Obiekt FormData
axios
  .post(
    "http://localhost:8000/file/", // API endpoint URL
    formData, // dane z formularza z plikiem
    { headers: { "Content-Type": "multipart/form-data" } } // Typ danych jako multipart/form-data wymagany przez parser API
  )
  .then((response) => {});

// Pobieranie plików z serwera
axios
  .get("http://localhost:8000/file/") // API endpoint URL
  .then((response) => {
    this.setState({ response: response.data });
  });

// Pobieranie plik o podanym ID z serwera
axios
  .get("http://localhost:8000/file/<ID_Pliku>") // API endpoint URL
  .then((response) => {
    this.setState({ response: response.data });
  });

// Usuwanie pliku z bazy serwera
axios
  .delete(`http://localhost:8000/file/<ID_Pliku>/`) // API endpoint URL z id pliku do usunięcia
  .then((response) => {});
```
### 3. Predykcja kodu w plikach (/predict/)

**Model:** `File`

| Metoda | Opis                              | Parametry w żądaniu (Multipart/form-data) | Odpowiedź (JSON)                                                         | Kody odpowiedzi |
| ------ | --------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------ | --------------- |
| POST   | Przesyła pliki do predykcji.      | `FormData` (dane z formularza z plikiem)  | `{ "file_name": string, "file_lang": string, "results": [[label: string, similarity_value: float, probability: float]], "files_contents": [[file_name: string, file_content: string]]}` | 201             |

```javascript
// Utworzenie obiektu FormData
const files = this.state.files;
const formData = new FormData();
  files.forEach((file, i) => formData.append(`files`, file, file.name));

// Wysyłanie pliku do predykcji przez model HDHGN
axios
  .post(
    "http://localhost:8000/predict/<liczba_podobnych_plików_w_odpowiedzi>", // API endpoint URL
    formData, // dane z formularza z plikiem
    { headers: { "Content-Type": "multipart/form-data" } } // Typ danych jako multipart/form-data wymagany przez parser API
  )
  .then((response) => {});
```


**Uwagi:**
Wszystkie dane tekstowe i pliki przesyłane na serwer zapisywane są lokalnie w bazie, która znajduje się w pliku `db.sqlite3` oraz pod ścieżką `media/uploads`.
