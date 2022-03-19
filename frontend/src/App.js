import React, { Component } from 'react'

import ImageEmbed from './components/ImageEmbed';
import Writeup from './components/Writeup';
import Header from "./components/Header";
import ImagesBody from "./components/ImagesBody";
import Nav from "./components/Nav";

import writeupmd from "../public/assets/docs/writeup.md"

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
let initExpiration = (cookie && cookie['tokenExpiration']) ? cookie['tokenExpiration'] : '';

const debug = false;

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
      errorLabel: 'Start searching by uploading up to 50 images.'
    };

    this.backendURL = "https://crierapi.ashaltu.com/";
  }

  componentDidMount() {
    fetch(writeupmd).then(res => res.text()).then(text => this.setState({markdown: text}));
    if (!this.state.expiration && this.cookieExpired()) this.createCookie();
  }

  cookieExpired = () => {
    const currentTime = new Date().toISOString();
    const tokenExpiration = new Date(this.state.expiration);
    const isExpired = !this.state.token || (tokenExpiration > currentTime) || (this.state.token && !document.cookie);
    if (isExpired) this.setErrorLabel("Session expired, please refresh the page to continue.");
    return isExpired;
  }

  createCookie = async () => {
    let response = await fetch(this.backendURL + "createtoken");
    let data = await response.json();

    let results = data;
    if (debug) console.log('Success:', data);
    let expireDate = new Date( Date.parse(results['expiration']) );
    let new_cookie = "token=" + results['new_token'] + "; expires=" + expireDate.toUTCString() + ";";
    let new_cookie_expiration = "tokenExpiration=" + expireDate.toUTCString() + "; expires=" + expireDate.toUTCString() + ";";
    this.setState({
        token: results['new_token'],
        expiration: results['expiration'],
        errorLabel: ''
    });
    
    document.cookie = new_cookie;
    document.cookie = new_cookie_expiration;
  };

  uploadImages = () => {
    if (this.cookieExpired()) return;

    const formData = new FormData();
    const photos = document.querySelector('input[id="uploadimages"][multiple]');

    if (!photos.files.length) {
      this.setErrorLabel("Please select images on your device to upload");
      return;
    }

    if (photos.files.length > 50) {
      this.setErrorLabel("Please select 50 or fewer images to index. This is a demo :(");
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
    if (this.cookieExpired()) return;

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
    if (!useExamples && this.cookieExpired()) return;

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
        this.setErrorLabel('Engine is still indexing added images, please wait 15-30s and try again.');
        if (debug) console.log('Still indexing:', result);
      } else if (result['reason'].startsWith("No image database uploaded")) {
        this.setErrorLabel('Please upload your image database to begin searching');
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
    return (this.state.showDemo) ? "Go to Project Info" : "Go to Demo";
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
        
        <div style={{position: 'sticky', top: 0}}>
          <Header />
          <button className="demoButton" style={this.showDemoButtonStyle} onClick={() => this.setState({showDemo: !this.state.showDemo, errorLabel: ''})}>
            <u><b>{this.showDemoButtonLabel()}</b></u>
          </button>
        </div>

        <div style={{display:'flex', justifyContent: 'center'}}>
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