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
import { createRef } from "react";

const BASE_URL = "http://localhost:8000";
 

// Main React component for the application
class App extends React.Component {
  
  // Initialize component state
  constructor(props) {
    super(props);
    this.state = {
      textDetails: [], // Array to store text data retrieved from the server
      fileDetails: {id:[], name: [],prob: []}, // Array to store file data retrieved from the server
      inputText: "", // Input string from the user
      files: [], // File selected by the user for upload
      currentFileIndex: 0, // Track which file is being shown
      activeTab: 1, // Active tab
      displayedFile: "", // File to display, chosen by the user from the uploaded files
      uploadedFilesContent: [], // Array to store content of uploaded files
      currentAlgorithmIndices: {}, // Tracks the current algorithm index for each file
    };

    // Create refs for the left and right CodeDisplay components
    this.leftBoxRef = createRef();
    this.rightBoxRef = createRef();
  }

  scrollUp = () => {
    this.scrollBothBoxes(-50); // Scroll up by 50px
  };

  scrollDown = () => {
    this.scrollBothBoxes(50); // Scroll down by 50px
  };

  scrollBothBoxes = (scrollAmount) => {
    if (this.leftBoxRef.current) {
      this.leftBoxRef.current.scrollTop += scrollAmount;
    }
    if (this.rightBoxRef.current) {
      this.rightBoxRef.current.scrollTop += scrollAmount;
    }
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
    const selectedFiles = Array.from(e.target.files);
    
    // Filter to ensure only .txt, .py, and .c files are added
    const allowedExtensions = ['text/plain', 'application/x-python-code', 'text/x-csrc'];
    const allowedFiles = selectedFiles.filter(file => allowedExtensions.includes(file.type) || file.name.endsWith('.py') || file.name.endsWith('.c'));

    // Check if any files are selected
    if (allowedFiles.length === 0) {
      alert("Tylko pliki .txt, .py, i .c są dozwolone");
    }
  
    // Update the state with only allowed files
    this.setState(prevState => ({ files: [...prevState.files, ...allowedFiles] }));
  };

  handleFileRemove = (fileName) => {
    this.setState(prevState => ({files: prevState.files.filter((file) => file.name !== fileName)}))
  };

  handleNextFile = () => {
    this.setState((prevState) => {
      const fileNames = Object.keys(prevState.fileDetails);
      const nextFileIndex = (prevState.currentFileIndex + 1) % fileNames.length;
      const nextFileName = fileNames[nextFileIndex];
  
      return {
        currentFileIndex: nextFileIndex,
        displayedFile: nextFileName,
      };
    });
  };
  
  handlePreviousFile = () => {
    this.setState((prevState) => {
      const fileNames = Object.keys(prevState.fileDetails);
      const prevFileIndex = (prevState.currentFileIndex - 1 + fileNames.length) % fileNames.length;
      const prevFileName = fileNames[prevFileIndex];
  
      return {
        currentFileIndex: prevFileIndex,
        displayedFile: prevFileName,
      };
    });
  };

  handleNextAlgorithm = () => {
    this.setState((prevState) => {
      const { displayedFile, currentAlgorithmIndices, fileDetails } = prevState;
  
      const currentIndex = currentAlgorithmIndices[displayedFile] || 0;
      const algorithmCount = fileDetails[displayedFile]?.name?.length || 0;
      const nextIndex = (currentIndex + 1) % algorithmCount;
  
      return {
        currentAlgorithmIndices: {
          ...currentAlgorithmIndices,
          [displayedFile]: nextIndex,
        },
      };
    });
  };
  
  handlePreviousAlgorithm = () => {
    this.setState((prevState) => {
      const { displayedFile, currentAlgorithmIndices, fileDetails } = prevState;
  
      const currentIndex = currentAlgorithmIndices[displayedFile] || 0;
      const algorithmCount = fileDetails[displayedFile]?.name?.length || 0;
      const prevIndex = (currentIndex - 1 + algorithmCount) % algorithmCount;

      return {
        currentAlgorithmIndices: {
          ...currentAlgorithmIndices,
          [displayedFile]: prevIndex,
        },
      };
    });
  };

  // Handler function to upload the selected file to the server
  handleFileUpload = (e) => {
    e.preventDefault();
    const { files } = this.state;
  
    if (!files || files.length === 0) {
      alert("Wprowadź plik do wysłania");
      return;
    }
  
    const formData = new FormData();
    files.forEach((file, i) => formData.append(`files`, file));
  
    axios
      .post(`${BASE_URL}/file/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((res) => {
        // Read the file content after upload and save it to uploadedFilesContent
        this.readFileContent(files);
        this.switchTab(2);  // Switch to tab 2
      })
      .catch((err) => {
        console.error("Error uploading file: ", err);
        alert("Nie udało się wysłać pliku");
      });
  };
  
  // Handler function to upload the selected file to the server for the HDHGN to analyze
  handleFileUploadForHDHGN = (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    const files = this.state.files; // Get the file from state
    
    // Check if a file is selected
    if (!files || files.length === 0) {
      alert("Wprowadź plik do wysłania");
      return;
    }

    // Create a new FormData object and append the uploaded files to it
    const formData = new FormData();
    files.forEach((file, i) => formData.append(`files`, file, file.name));
  
    // Send a POST request to the server with the file data
    axios
      .post(`${BASE_URL}/predict/5/`, formData, { // request a response with 5 results per sent file
        headers: {
          "Content-Type": "multipart/form-data", // Set content type for file upload
        },
      })
      .then((res) => {        
        this.readFileContent(files); // Read the file content after upload and save it to uploadedFilesContent
        this.switchTab(2);  // Switch to tab 2
        this.ProcessModelResults(res); // Process the model results from the server
      })
      .catch((err) => {
        console.error("Error uploading file: ", err);
        alert("Nie udało się wysłać pliku");
      });
  };

  readFileContent = (files) => {
    const fileContents = [];
    files.forEach((file) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        fileContents.push({ name: file.name, content: e.target.result });
        // Update the state once all files are read
        if (fileContents.length === files.length) {
          this.setState(
            {
              uploadedFilesContent: fileContents,
              displayedFile: fileContents[0]?.name || "", // Set the first file as default
            },
            () => {
              console.log('Updated uploadedFilesContent:', this.state.uploadedFilesContent);
            }
          );
        }
      };
      reader.readAsText(file);
    });
  };

  // Function handling the HDHGN prediction results received from the server 
  ProcessModelResults = (response) => {
    console.log("Full response:", response.data);
  
    let data;
    try {
      data = JSON.parse(response.data);
      console.log(data);
    } catch (error) {
      console.error("Error parsing response data:", error);
      return;
    }
  
    if (data && Array.isArray(data)) {
      const updatedFileDetails = { ...this.state.fileDetails };
      const updatedAlgorithmIndices = { ...this.state.currentAlgorithmIndices };
  
      data.forEach((fileData) => {
        if (fileData.results && Array.isArray(fileData.results) && fileData.results.length > 0) {
          const topFiveNames = fileData.results.slice(0, 5).map((item) => item[0]); // Algorithm names
          const topFiveProbs = fileData.results.slice(0, 5).map((item) => item[2]); // Probabilities
  
          // Store file_lang along with algorithm names and probabilities
          updatedFileDetails[fileData.file_name] = {
            name: topFiveNames,
            prob: topFiveProbs,
            file_lang: fileData.file_lang, // Add file_lang to the fileDetails object
          };
  
          // Initialize the algorithm index for this file
          updatedAlgorithmIndices[fileData.file_name] = 0;
        }
      });
  
      this.setState({
        fileDetails: updatedFileDetails,
        currentAlgorithmIndices: updatedAlgorithmIndices,
      });
  
      console.log("Updated fileDetails:", updatedFileDetails);
      console.log("Updated currentAlgorithmIndices:", updatedAlgorithmIndices);
    } else {
      console.error("Response data is empty, invalid, or missing results.");
    }
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
      .post(`${BASE_URL}/wel/`, {
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
      .delete(`${BASE_URL}/wel/${id}/`) // API endpoint for deleting an item by ID
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
      .delete(`${BASE_URL}/file/${id}/`) // API endpoint for deleting an item by ID
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

  HandleDisplayFile = (event) => {
    this.setState({ displayedFile: event.target.value });
  };

  // Returns files names
  getFileNames = () => {
    return this.state.fileDetails.map(file => file.name); 
  };

  // Returns user files names
  getUserFileNames = () => {
    return this.state.files.map(file => file.name); 
  };

  // Render method to display the component UI
  render() {
    const { activeTab, files, displayedFile, fileDetails, uploadedFilesContent, currentAlgorithmIndices} = this.state;
    // Get the content of the currently selected file for the right box
    const fileContentToDisplay = uploadedFilesContent.find(
      (file) => file.name === displayedFile
    )?.content || uploadedFilesContent[0]?.content || "No content available";
    console.log("filedetails:",fileDetails);

    const currentAlgorithmIndex = currentAlgorithmIndices[displayedFile] || 0;

    const selectedFileDetails = fileDetails[displayedFile] || {};
    const algorithmNames = selectedFileDetails.name || [];
    const probabilities = selectedFileDetails.prob || [];

    const currentAlgorithmName = algorithmNames[currentAlgorithmIndex] || "No algorithm selected";
    const currentProbability = probabilities[currentAlgorithmIndex] || "No probability available";
    const formattedProb = (currentProbability * 100).toFixed(2)

    return (
      <div className="container">
        {activeTab === 1 ? ( // tab1
          <div>
            <Header />
            <FileUploader
              files={files}
              onFileChange={this.handleFileChange}
              onFileRemove={this.handleFileRemove}
            />
            <form onSubmit={this.handleFileUploadForHDHGN}>
              <SendFiles />
            </form>
          </div>
        ) : ( // tab2
          <div style={{ height: '100vh', textAlign: 'center' }}>
          {/* Label with measure of similarity */}
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                width: '100%',
                height: '20%',
              }}
            >
              <button
                style={{
                  background: 'none',
                  border: 'none',
                  fontSize: '40px',
                  cursor: 'pointer',
                  paddingLeft: '20px',
                  color: '#6a64ae',
                }}
                onClick={this.BackToHome}
              >
                ⮌
              </button>
              <h1
                style={{
                  margin: '40px 0px 10px 0px',
                  color: 'white',
                  position: 'absolute',
                  left: '50%',
                  transform: 'translateX(-50%)',
                }}
              >
                {`Podobieństwo: ${formattedProb}%`} {/* Displaying prob */}
              </h1>
            </div>
            <div style={{ display: 'flex', marginTop: '40px', flexDirection: 'column' }}>
            <div style={{ display: 'flex' }}>
              <div style={{ display: 'flex', width: '50%', justifyContent: 'center', color: '#6a64ae' }}>
                ORYGINALNY KOD
              </div>
              <div style={{ display: 'flex', width: '50%', justifyContent: 'center', color: '#6a64ae' }}>
                KOD Z WYKRYTYM PODOBIEŃSTWEM
              </div>
            </div>
            <div style={{ display: 'flex', width: '50%', justifyContent: 'center', color: '#6a64ae', marginTop: '5px', marginLeft: '50%' }}>
            {currentAlgorithmName}
            </div>
          </div>
            <div style={{ display: 'flex', height: '65%', justifyContent: 'center' }}>
              {/* Right Box (Content from fileDetails) */}
              <CodeDisplay ref={this.rightBoxRef} code={fileContentToDisplay} />
              
              <div
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  height: '80%',
                  marginTop: '20px',
                }}
              >
                <Scroll icon="⮝" onClick={this.scrollUp} />
                <Scroll icon="⮟" onClick={this.scrollDown} />
              </div>
  
              {/* Left Box (Content from user selected file) */}
              <CodeDisplay ref={this.leftBoxRef} code={currentAlgorithmName} />
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'center' }}>
              <div
                style={{
                  display: 'flex',
                  width: '40%',
                  justifyContent: 'center',
                  padding: '10px',
                  margin: '0px 40px 0px 0px',
                }}
              >
                <DropDown
                value={this.state.displayedFile} // Selected file name
                onChange={this.HandleDisplayFile} // Updates displayedFile
                options={this.state.uploadedFilesContent.map(file => file.name)} // File names as options
                />
              </div>
              <div
                style={{
                  display: 'flex',
                  width: '40%',
                  justifyContent: 'center',
                  padding: '10px',
                  margin: '0px 0px 0px 40px',
                }}
              >
                <ChangeFilesButton
                  onPreviousFile={this.handlePreviousAlgorithm}
                  onNextFile={this.handleNextAlgorithm}
                  currentFileIndex={this.state.currentAlgorithmIndices[this.state.displayedFile]}
                  totalFiles={this.state.fileDetails[this.state.displayedFile]?.name?.length || 0}
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
