import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">Baessy Finance App</Link>
      </div>
      <ul className="nav-links">
        <li><Link to="/transactions">Transactions</Link></li>
        <li><Link to="/expenses">Expenses</Link></li>
        <li><Link to="/revenues">Revenues</Link></li>
      </ul>
      <div className="profile">
        <img src="./images/baessy.png" alt="Profile Avatar" />
        <span>Nicolas Mabeleng</span>
      </div>
    </nav>
  );
};

export default Navbar;
