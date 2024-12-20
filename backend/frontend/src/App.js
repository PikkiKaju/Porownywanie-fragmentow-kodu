import React from "react";
import axios from "axios";

import "./App.css";

// Main React component for the application
class App extends React.Component {
  // Initialize component state
  state = {
    textDetails: [], // Array to store text data retrieved from the server
    fileDetails: [], // Array to store file data retrieved from the server
    inputText: "", // Input string from the user
    file: null, // File selected by the user for upload
  };

  // Function to fetch text data from the backend API endpoint
  getTextData = () => {
    // Send a GET request to the server to retrieve text data
    axios
      .get("http://localhost:8000/wel/") // API endpoint URL
      .then((res) => {
        // Update the 'textDetails' state with the received data
        this.setState({
          textDetails: res.data,
        });
      })
      .catch((err) => {
        console.error("Could not retrieve data from server: " + err);
        alert("Nie udało się pobrać danych tekstowych");
      });
  };

  // Function to fetch file data from the backend API endpoint
  getFileData = () => {
    // Send a GET request to the server to retrieve file data
    axios
      .get("http://localhost:8000/file/") // API endpoint URL
      .then((res) => {
        // Update the 'fileDetails' state with the received data
        this.setState({
          fileDetails: res.data,
        });
      })
      .catch((err) => {
        console.error("Could not retrieve data from server: " + err);
        alert("Nie udało się pobrać plików");
      });
  };

  // Lifecycle method called when the component mounts
  componentDidMount() {
    // Fetch initial data from the backend when the component mounts
    this.getTextData();
    this.getFileData();
  }

  // Handler function to update the input text state
  handleInput = (e) => {
    // Dynamically update state based on input name
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  // Handler function to update the file state when a file is selected
  handleFileChange = (e) => {
    // Store the selected file in state
    this.setState({
      file: e.target.files[0],
    });
  };

  // Handler function to upload the selected file to the server
  handleFileUpload = (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    const file = this.state.file; // Get the file from state
    
    // Check if a file is selected
    if (file === null) {
      alert("Wprowadź plik do wysłania");
      return;
    }

    // Create a new FormData object
    const formData = new FormData(); 
    formData.append("file", file); // Append the file to the FormData
    formData.append("filename", file.name); // Append the filename to the FormData

    // Send a POST request to the server with the file data
    axios
      .post("http://localhost:8000/file/", formData, {
        // API endpoint for file upload
        headers: {
          "Content-Type": "multipart/form-data", // Set content type for file upload
        },
      })
      .then((res) => {
        // Fetch updated data from the backend after successful upload
        this.getFileData(); 
        // Clear the file state after successful upload
        this.setState({
          file: null,
        });
      })
      .catch((err) => {
        console.error("Error uploading file: ", err);
        alert("Nie udało się wysłać pliku");
      });
  };

  // Handler function to submit text data to the server
  handleTextSubmit = (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    // Check if input text is empty
    if (this.state.inputText === "") {
      alert("Wprowadź tekst do wysłania");
      return;
    }

    // Send a POST request to the server with the input text
    axios
      .post("http://localhost:8000/wel/", {
        // API endpoint URL
        inputText: this.state.inputText, // Send the input text to the backend
      })
      .then((res) => {
        // Fetch updated data from the backend after successful submission
        this.getTextData();
        // Clear the input text state
        this.setState({
          inputText: "",
        });
      })
      .catch((err) => {
        console.error("Error while submitting data: ", err);
        alert("Nie udało się wysłać danych");
      });
  };

  // Handler function to remove an item from the backend and update the UI
  handleDeleteText = (e, id) => {
    e.preventDefault(); // Prevent default form submission behavior

    // Send a DELETE request to the server to delete a text item by ID
    axios
      .delete(`http://localhost:8000/wel/${id}/`) // API endpoint for deleting an item by ID
      .then((res) => {
        // Fetch updated data after successful deletion
        this.getTextData();
      })
      .catch((err) => {
        console.error("Error while deleting data: ", err);
        alert("Nie udało się usunąć tekstu");
      });
  };

  // Handler function to remove an item from the backend and update the UI
  handleDeleteFile = (e, id) => {
    e.preventDefault(); // Prevent default form submission behavior

    // Send a delete request to the server to delete a file by ID
    axios
      .delete(`http://localhost:8000/file/${id}/`) // API endpoint for deleting an item by ID
      .then((res) => {
        // Fetch updated data after successful deletion
        this.getFileData();
      })
      .catch((err) => {
        console.error("Error while deleting data: ", err);
        alert("Nie udało się usunąć pliku");
      });
  };

  // Render method to display the component UI
  render() {
    return (
      <div className="container">
        {/* Form for submitting text input */}
        <form onSubmit={this.handleTextSubmit}>
          <div>
            <div>
              <span id="basic-addon1">Tekst do backendu</span>
            </div>
            <input
              type="text"
              placeholder="Wpisz tekst"
              value={this.state.inputText}
              name="inputText"
              onChange={this.handleInput}
            />
          </div>

          <button type="submit">Prześlij tekst</button>
        </form>

        <br></br>

        {/* Form for uploading files */}
        <form onSubmit={this.handleFileUpload}>
          <div>
            <div>
              <span>Plik do backendu</span>
            </div>
            <input type="file" name="file" onChange={this.handleFileChange} />
          </div>
          <button type="submit">Prześlij plik</button>
        </form>

        <hr />

        {/* Display text data retrieved from the server */}
        {this.state.textDetails.map((detail) => (
          <div key={detail.id}>
            <div className="card">
              <p>Tekst z backendu nr {detail.id}</p>
              <p> {detail.inputText} </p>
              {/* Form for deleting an item */}
              <form onSubmit={(e) => this.handleDeleteText(e, detail.id)}>
                <button type="submit">Usuń tekst</button>
              </form>
            </div>
          </div>
        ))}

        {/* Display file data retrieved from the server */}
        {this.state.fileDetails.map((detail) => (
          <div key={detail.id}>
            <div className="card">
              <p>Plik z backendu nr {detail.id}</p>
              <p> {detail.filename} </p>
              {/* Form for deleting a file */}
              <form onSubmit={(e) => this.handleDeleteFile(e, detail.id)}>
                <button type="submit">Usuń plik</button>
              </form>
            </div>
          </div>
        ))}
      </div>
    );
  }
}

export default App;
