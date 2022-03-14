import React, { Component } from 'react'
import axios from "axios"
import {saveAs} from 'file-saver';
import ImageEmbed from './components/ImageEmbed';
import Header from "./components/Header";

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
    };
  }

  createCookie = async () => {
    let response = await fetch("http://40.122.200.108:5001/createtoken");
    let data = await response.json();

    let results = data;
    console.log(data);
    let expireDate = new Date( Date.parse(results['expiration']) );
    let new_cookie = "token=" + results['new_token'] + "; expires=" + expireDate.toUTCString() + ";";
    this.setState({
        cookie: new_cookie,
        token: results['new_token'],
        expiration: results['expiration']
    });
    
    document.cookie = new_cookie;
  };

  uploadImages = () => {
    return;
  }

  deleteImages = () => {
    return;
  }

  searchImage = () => {
    return;
  }


  render () {

    return (
      <div>
        <Header />

        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            minHeight: '70vh'
          }}
        >

          <button onClick={this.createCookie}>Create Cookie</button>

        </div>
      </div>
    )
  };

  


}