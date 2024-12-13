import React from "react";
import axios from "axios";

import "./App.css";

class App extends React.Component {
  state = {
    details: [],
    inputText: "",
  };


  getData = () => {
    axios.get("http://localhost:8000/wel/")
    .then((res) => {
      this.setState({
        details: res.data,
      });
    })
    .catch((err) => { });
  }

  componentDidMount() {
    let data;

    this.getData();
  }

  handleInput = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  handleSubmit = (e) => {
    e.preventDefault();

    axios
      .post("http://localhost:8000/wel/", {
        inputText: this.state.inputText,
      })
      .then((res) => {
        this.getData();
        this.setState({
          inputText: "",
        });
      })
      .catch((err) => { });
  };

  handleRemove = (e, id) => {
    e.preventDefault();
    axios
      .delete(`http://localhost:8000/wel/${id}/`) //
      .then((res) => {
        this.getData();
      })
      .catch((err) => {
        console.error(err);
      });
  };

  render() {
    return (
      <div className="container jumbotron ">
        <form onSubmit={this.handleSubmit}>
          <div>
            <div>
              <span id="basic-addon1">Coś do backendu</span>
            </div>
            <input
              type="text"
              placeholder="Coś do backendu"
              value={this.state.inputText}
              name="inputText"
              onChange={this.handleInput}
            />
          </div>

          <button type="submit">Prześlij</button>
        </form>

        <hr />

        {this.state.details.map((detail, id) => (
          <div key={detail.id}>
            <div className="card">
              <p>Cos z backendu nr {detail.id}</p>
              <p> {detail.inputText} </p>
              <form onSubmit={(e) => this.handleRemove(e, detail.id)}>
                <button type="submit">Usuń</button>
              </form>
            </div>
          </div>
        ))}
      </div>
    );
  }
}

export default App;
