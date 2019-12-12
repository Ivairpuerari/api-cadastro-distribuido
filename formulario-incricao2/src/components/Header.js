import React from 'react';
import './Header.css';
import {Link} from 'react-router-dom'

import logo from '../assets/logo_1.svg';


export default function Header() {
  return (
    <header id="main-header">
        <div className="header-content">
            <Link to="/">
              <img src={logo} alt="InstaRocket" />
            </Link>
        </div>
    </header>
  );
}
