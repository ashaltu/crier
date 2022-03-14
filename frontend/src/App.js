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
      cookie: cookie,
      token: initToken,
      expiration: initExpiration,
    };
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
          
        </div>
      </div>
    )
  }

  


}