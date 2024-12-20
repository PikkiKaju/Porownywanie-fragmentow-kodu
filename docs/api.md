# Dokumentacja API

To API jest zrobione poprzez django rest-framework i póki co składa się z end-pointów do przesyłania tekstu i plików.

**Adres Bazowy:** `http://localhost:8000/`

### 1. Zarządzanie Danymi Tekstowymi (/wel/)

**Model:** `Text`

| Metoda | Opis                                     | Parametry w żądaniu (JSON)              | Odpowiedź (JSON)                                                | Kody odpowiedzi |
| ------ | ---------------------------------------- | --------------------------------------- | --------------------------------------------------------------- | --------------- |
| GET    | Pobiera wszystkie wpisy tekstowe z bazy. | Brak                                    | `[{ "id": int, "inputText": string }]`                          | 200             |
| POST   | Tworzy nowy wpis.                        | `{ "inputText": string }`               | `{ "id": int, "inputText": string }`                            | 201             |
| DELETE | Usuwa wpis o podanym ID.                 | Brak, ale wymaga ID w URL: `/wel/{id}/` | 204 No Content (sukces) <br> lub 404 Not Found (nie znaleziono) | 204, 404        |

##### Przykład użycia w `javascript` poprzez `axios`:

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

### 2. Przesyłanie Plików (/file/)

**Model:** `File`

| Metoda | Opis                              | Parametry w żądaniu (Multipart/form-data) | Odpowiedź (JSON)                                                         | Kody odpowiedzi |
| ------ | --------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------ | --------------- |
| GET    | Pobiera listę przesłanych plików. | Brak                                      | `[{ "id": int, "file": string }]` (ścieżka pliku - **Należy poprawić!**) | 200             |
| POST   | Przesyła nowy plik.               | `file` (plik)                             | `{ "id": int, "file": string }` (ścieżka pliku - **Należy poprawić!**)   | 201             |
| DELETE | Usuwa plik o podanym ID.          | Brak, ale wymaga ID w URL: `/file/{id}/`  | 204 No Content (sukces) lub 404 Not Found                                | 204, 404        |

##### Przykład użycia w `javascript` poprzez `axios`:

```javascript
// Pobieranie plików z serwera
axios
  .get("http://localhost:8000/file/") // API endpoint URL
  .then((response) => {
    this.setState({ response: response.data });
  });

// Wysyłanie pliku na serwer
const formData = new FormData(); // Obiekt FormData
axios
  .post(
    "http://localhost:8000/file/", // API endpoint URL
    formData, // dane z formularza z plikiem
    { headers: { "Content-Type": "multipart/form-data" } } // Typ danych jako multipart/form-data wymagany przez parser API
  )
  .then((response) => {});

// Usuwanie pliku z bazy serwera
axios
  .delete(`http://localhost:8000/file/${id}/`) // API endpoint URL z id pliku do usunięcia
  .then((response) => {});
```

**Uwagi:**
Wszystkie dane tekstowe i pliki przesyłane na serwer zapisywane są lokalnie w bazie, która znajduje się w pliku `db.sqlite3` oraz pod ścieżką `media/uploads` i pliki te nie są śledzone przez gita.
