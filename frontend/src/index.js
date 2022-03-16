import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

const HomePage = () => {
  ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    document.getElementById('root')
  );
}

HomePage();

export default HomePage;  // unneeded;

