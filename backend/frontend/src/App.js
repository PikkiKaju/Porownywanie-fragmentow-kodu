import React from "react";
import axios from "axios";

import "./App.css";
import Header from './Components/Header.js'
import FileUploader from './Components/FileUploader.js'
import SendFiles from './Components/SendFiles.js'
import CodeDisplay from './Components/CodeDisplay.js'
import ChangeFilesButton from "./Components/ChangeFilesButton.js";
import Scroll from "./Components/Scroll.js";
import DropDown from './Components/DropDown.js'

// Main React component for the application
class App extends React.Component {
  
  // Initialize component state
  state = {
    textDetails: [], // Array to store text data retrieved from the server
    fileDetails: [], // Array to store file data retrieved from the server
    inputText: "", // Input string from the user
    files: [], // File selected by the user for upload
    activeTab: 2, // Active tab
    displayedFile: "", // File to display, chosen by the user from the uploaded files
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

  //Lifecycle method called when the component mounts
  componentDidMount() {
    //Fetch initial data from the backend when the component mounts
    //this.getTextData();
    //this.getFileData();
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
    // Store the selected files in state
    this.setState(prevState => ({files: [...prevState.files, ...Array.from(e.target.files)]}));
  };

  handleFileRemove = (fileName) => {
    this.setState(prevState => ({files: prevState.files.filter((file) => file.name !== fileName)}))
  };

  // Handler function to upload the selected file to the server
  handleFileUpload = (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    const files = this.state.files; // Get the file from state
    // Check if a file is selected
    if (!files || files.length === 0) {
      alert("Wprowadź plik do wysłania");
      return;
    }

    // Create a new FormData object
    const formData = new FormData();

    files.forEach((file) => {
        formData.append("files", file); /// Append the files to the FormData
    });


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

        this.switchTab(2);
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

  // Function to switch tabs
  switchTab = (tabNumber) => {
    this.setState({ activeTab: tabNumber });
  };

  BackToHome = () => { // Returns to tab 1 
    this.setState({
      files: [],
    });
    // to do: Remove files
    this.switchTab(1);
  };

  HandleDisplayFile = (e) => { // Changes displayed file depending of the users choice in dropdown
    this.setState({ displayedFile: e.target.value });
  };

  getFileNames = () => {
    return this.state.files.map(file => file.name); // Returns files names
  };

  // Render method to display the component UI
  render() {

    const { activeTab } = this.state;

    return (
      <div className="container">
        {activeTab === 1 ? ( // tab1 --------------------------------------------------------------------------------------------------
          <div>
            <Header/>
            {/* Form for submitting text input 
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
            </form>*/}

            <br></br>
            <FileUploader files={this.state.files} onFileChange={this.handleFileChange} onFileRemove={this.handleFileRemove}/>
            {/* Form for uploading files */}
            <form onSubmit={this.handleFileUpload}>
              <SendFiles/>
            </form>            
          </div>



        ):( // tab2 ------------------------------------------------------------------------------------------------------------
          <div style={{height: '100vh', textAlign: 'center', }}>
            {/* Label with measure of similarity */}
            <div style={{display: 'flex', justifyContent: 'space-between', width: '100%', height: '20%'}}>
            <button style={{
                  background: 'none',
                  border: 'none',
                  fontSize: '40px',
                  cursor: 'pointer',
                  paddingLeft: '20px',
                  color: '#6a64ae',
                }} onClick={this.BackToHome}>
                ⮌
                </button>
              <h1 style={{margin: '40px 0px 10px 0px', color: 'white', position: 'absolute', left: '50%', transform: 'translateX(-50%)'}}>Podobieństwo 50%</h1>
            </div>
            
            <div style={{display: 'flex', height: '65%', justifyContent: 'center'}}>
              <CodeDisplay code={"rdyfguijop"}/>

              {/* Arrows in the middle to scroll both displays */}                
              <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '80%', marginTop: '20px' }}> 
                <Scroll icon = "⮝"/>
                <Scroll icon = "⮟"/>
              </div>
              <CodeDisplay  code={"import matplotlib python code abcd\
                                  m = 1\
                                  \
                                  for _ in range(5):\
                                  \
                                    if (m == 0 or m !=2):\
                                    \
                                      kjscd bLSJKHadsjkcnajkdc\
                                      import matplotlib python code abcd\
                                  m = 1\
                                  \
                                  for _ in range(5):\
                                  \
                                    if (m == 0 or m !=2):\
                                    \
                                      kjscd bLSJKHadsjkcnajkdc\
                                  isudbclasjkcb asikdck;sbdc;kjdc hcbsduj\
                                  import matplotlib python code abcd\
                                  m = 1\
                                  \
                                  for _ in range(5):\
                                  \
                                    if (m == 0 or m !=2):\
                                    \
                                      kjscd bLSJKHadsjkcnajkdc\
                                  isudbclasjkcb asikdck;sbdc;kjdc hcbsduj\
                                  import matplotlib python code abcd\
                                  m = 1\
                                  \
                                  for _ in range(5):\
                                  \
                                    if (m == 0 or m !=2):\
                                    \
                                      kjscd bLSJKHadsjkcnajkdc\
                                  isudbclasjkcb asikdck;sbdc;kjdc hcbsduj\
                                  isudbclasjkcb asikdck;sbdc;kjdc hcbsduj"}/>


              {/* Display text data retrieved from the server */}
              {/*{this.state.textDetails.map((detail) => (
                <div key={detail.id}>
                  <div className="card">
                    <p>Tekst z backendu nr {detail.id}</p>
                    <p> {detail.inputText} </p>*/}
                    {/* Form for deleting an item */}
                    {/*<form onSubmit={(e) => this.handleDeleteText(e, detail.id)}>
                      <button type="submit">Usuń tekst</button>
                    </form>
                  </div>
                </div>
              ))}*/}

              {/* Display file data retrieved from the server */}
              {/*{this.state.fileDetails.map((detail) => (
                <div key={detail.id}>
                  <div className="card">
                    <p>Plik z backendu nr {detail.id}</p>
                    <p> {detail.filename} </p>*/}
                    {/* Form for deleting a file */}
                    {/*<form onSubmit={(e) => this.handleDeleteFile(e, detail.id)}>
                      <button type="submit">Usuń plik</button>
                    </form>
                  </div>
                </div>
              ))} */}
            </div>
            <div style={{display: 'flex', justifyContent: 'center', }}>
            <div style={{
                  display: 'flex',
                  width: '40%',
                  justifyContent: 'center',
                  padding: '10px',
                  margin: '0px 40px 0px 0px',
              }}>
                <ChangeFilesButton/> {/* Buttons to change code to compare */}
              </div>
              <div style={{
                  display: 'flex',
                  width: '40%',
                  justifyContent: 'center',
                  padding: '10px',
                  margin: '0px 0px 0px 40px', 
              }}>
              <DropDown value={this.state.displayedFile}
                        onChange={(e) => this.HandleDisplayFile(e)}
                        options={this.getFileNames()}
              />
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }
}

export default App;
