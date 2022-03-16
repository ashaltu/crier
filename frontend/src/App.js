import React, { Component } from 'react'

import ImageEmbed from './components/ImageEmbed';
import Writeup from './components/Writeup';
import Header from "./components/Header";
import Demo from "./components/Demo";

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

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      token: initToken,
      expiration: initExpiration,
      image_paths: [],
      distances: [],
      showDemo: true, // temporary!
      markdown: ''
    };

    this.backendURL = "http://40.122.200.108:5001/";
  }

  componentDidMount() {
    fetch(writeupmd).then(res => res.text()).then(text => this.setState({markdown: text}));
  }

  createCookie = async () => {
    let response = await fetch(this.backendURL + "createtoken");
    let data = await response.json();

    let results = data;
    console.log(data);
    let expireDate = new Date( Date.parse(results['expiration']) );
    let new_cookie = "token=" + results['new_token'] + "; expires=" + expireDate.toUTCString() + ";";
    this.setState({
        token: results['new_token'],
        expiration: results['expiration']
    });
    
    document.cookie = new_cookie;
  };

  uploadImages = () => {
    const formData = new FormData();
    const photos = document.querySelector('input[id="uploadimages"][multiple]');

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
      console.log('Success:', result);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  deleteImages = () => {
    fetch(this.backendURL + "removeimages", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 'token': this.state.token }),
    })
    .then(response => response.json())
    .then(result => {
      console.log('Success:', result);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  searchImage = () => {
    const formData = new FormData();
    const photos = document.querySelector('input[id="searchimages"][multiple]');

    formData.append('token', this.state.token);
    for (let i = 0; i < photos.files.length; i++) {
      formData.append(`photos_${i}`, photos.files[i]);
    }

    fetch(this.backendURL + "search", {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(result => {
      //let requireImgs = result['image_paths'].map((v, i) => require(v));
      this.setState({
        image_paths: result['image_paths'],
        distances: result['distances']
      });
      console.log('Success:', result);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  insertImages = () => {
    const zip = (a, b) => a.map((k, i) => [k, b[i]]);

    return (
      <>
        {zip(this.state.image_paths, this.state.distances).map(
          function(path_dist_blob, idx) {
            return <ImageEmbed imgPath={path_dist_blob[0]} distance={path_dist_blob[1]}/>;
          }
        )}
      </>
    );
  };

  render () {

    return (
      <div>
        <Header />

        {
          this.state.showDemo && 
          <>
            <button onClick={() => this.setState({showDemo: false})}>
              Show Writeup
            </button>
            {Demo(this.createCookie, this.uploadImages, this.deleteImages, this.searchImage, this.insertImages)}
          </>
        }

        { 
          !this.state.showDemo && 
          <>
            <button onClick={() => this.setState({showDemo: true})}>
              Show Demo
            </button>
            {Writeup(this.state.markdown)}
          </>
        }
      </div>
    )
  };

};