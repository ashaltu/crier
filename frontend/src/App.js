import React, { Component } from 'react'

import ImageEmbed from './components/ImageEmbed';
import Writeup from './components/Writeup';
import Header from "./components/Header";
import ImagesBody from "./components/ImagesBody";
import Nav from "./components/Nav";

import writeupmd from "./components/writeup.md"

const parseCookie = str =>
  str
    .split(';')
    .map(v => v.split('='))
    .reduce((acc, v) => {
      acc[decodeURIComponent(v[0].trim())] = decodeURIComponent(v[1].trim());
      return acc;
    }, {});

let cookie = (document.cookie) ? parseCookie(document.cookie) : '';
let initToken = (cookie && cookie['token']) ? cookie['token'] : '';
let initExpiration = (cookie && cookie['expiration']) ? cookie['expiration'] : '';

const debug = true;

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      token: initToken,
      expiration: initExpiration,
      image_paths: [],
      distances: [],
      showDemo: true, // temporary!
      markdown: '',
      errorLabel: ''
    };

    this.backendURL = "http://40.122.200.108:5001/";
  }

  componentDidMount() {
    fetch(writeupmd).then(res => res.text()).then(text => this.setState({markdown: text}));
    if (!this.state.token) this.createCookie();
  }

  createCookie = async () => {
    let response = await fetch(this.backendURL + "createtoken");
    let data = await response.json();

    let results = data;
    if (debug) console.log('Success:', data);
    let expireDate = new Date( Date.parse(results['expiration']) );
    let new_cookie = "token=" + results['new_token'] + "; expires=" + expireDate.toUTCString() + ";";
    this.setState({
        token: results['new_token'],
        expiration: results['expiration'],
        errorLabel: ''
    });
    
    document.cookie = new_cookie;
  };

  uploadImages = () => {
    if (!this.state.token) {
      this.setErrorLabel("No token created for some reason. Sorry, this is a backend issue.");
      return;
    }
    const formData = new FormData();
    const photos = document.querySelector('input[id="uploadimages"][multiple]');

    if (!photos.files.length) {
      this.setErrorLabel("Please select images on your device to upload");
      return;
    }
    formData.append('token', this.state.token);
    for (let i = 0; i < photos.files.length; i++) {
      formData.append(`photos_${i}`, photos.files[i]);
    }

    fetch(this.backendURL + "addimages", {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(result => {
      if (debug) console.log('Success:', result);
      this.setErrorLabel('');
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  deleteImages = () => {
    if (!this.state.token) {
      this.setErrorLabel("No token created for some reason. Sorry, this is a backend issue.");
      return;
    }
    fetch(this.backendURL + "removeimages", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'token': this.state.token }),
    })
    .then(response => response.json())
    .then(result => {
      if (debug) console.log('Success:', result);
      this.setErrorLabel("Image database successfully deleted.");
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  searchImage = (useExamples) => {
    if (!useExamples && !this.state.token) {
      this.setErrorLabel("No token created for some reason. Sorry, this is a backend issue.");
      return;
    }

    const formData = new FormData();
    const photos = document.querySelector((useExamples) ? 'input[id="searchexamples"]' : 'input[id="searchimages"]');

    if (!photos.files.length) {
      this.setErrorLabel("Please select an image to search with");
      return;
    }

    formData.append('token', (useExamples) ? 'example_image_corpus' : this.state.token);
    for (let i = 0; i < photos.files.length; i++) {
      formData.append(`photos_${i}`, photos.files[i]);
    }

    fetch(this.backendURL + "search", {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(result => {
      if (result['success'] === true) {
        this.setState({
          image_paths: result['image_paths'],
          distances: result['distances'],
          errorLabel: ''
        });
        if (debug) console.log('Success:', result);
      } else if (result['reason'].startsWith("Search request not fulfilled since engine still indexing")) {
        this.setState({
          errorLabel: 'Engine is still indexing added images, please wait 15-30s and try again.'
        })
        if (debug) console.log('Still indexing:', result);
      } else if (result['reason'].startsWith("No image database uploaded")) {
        this.setState({
          errorLabel: 'Please upload your image database to begin searching'
        })
        if (debug) console.log('No image database found:', result);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  insertImages = () => {
    if (!this.state.image_paths || !this.state.image_paths.length) return;

    const zip = (a, b) => a.map((k, i) => [k, b[i]]);
    return (
      <>
        {this.state.image_paths && this.state.distances &&
        zip(this.state.image_paths, this.state.distances).map(
          function(path_dist_blob, idx) {
            return <ImageEmbed imgPath={path_dist_blob[0]} distance={path_dist_blob[1]} rank={idx+1}/>;
          }
        )}
      </>
    );
  };

  showDemoButtonLabel = () => {
    return (this.state.showDemo) ? "Show Writeup" : "Show Demo";
  };

  setErrorLabel = (errorMsg) => {
    this.setState({
      errorLabel: errorMsg
    });
  };

  showDemoButtonStyle = {
    width: '100%',
    backgroundColor: '#ff4931',
    color: 'white',
    border: 'none',
    fontSize: '1.25em',
    margin: 0,
    cursor: 'pointer'
  };

  render () {

    return (
      <div style={{display:"block"}}>
        <Header />
        <button className="demoButton" style={this.showDemoButtonStyle} onClick={() => this.setState({showDemo: !this.state.showDemo, errorLabel: ''})}>
          <b>{this.showDemoButtonLabel()}</b>
        </button>

        <div style={{display:'flex'}}>
            {
              this.state.showDemo && 
              <>
                {Nav(this.createCookie, this.uploadImages, this.deleteImages, this.searchImage, this.setErrorLabel)}
                {ImagesBody(this.insertImages, this.state.errorLabel)}
              </>
            }

            { 
              !this.state.showDemo && 
              <>
                {Writeup(this.state.markdown)}
              </>
            }

        </div>

      </div>
    )
  };

};