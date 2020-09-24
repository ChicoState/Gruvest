import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Systemvote from './components/systemvote.js';

class App extends Component {
  render() {
	console.log('Init App');
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Systemvote</h1>
        </header>
        <Systemvote />
      </div>
    );
  }
}

export default App;
