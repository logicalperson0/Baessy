import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import './AuthForm.css';

const Login = () => {
  const [formData, setFormData] = useState({
    username_or_email: '',
    password: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Send login request using Axios
    axios.post('http://localhost:5000/login', formData, { withCredentials: true })
      .then(response => {
        console.log(response.data);
        // Handle successful login
      })
      .catch(error => {
        console.error('Login failed:', error);
        // Handle login failure
      });
  };

  return (
    <div className="auth-form">
      <h2>Login</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formUsernameOrEmail">
          <Form.Label>Username or Email</Form.Label>
          <Form.Control type="text" name="username_or_email" placeholder="Enter username or email" value={formData.username_or_email} onChange={handleChange} required />
        </Form.Group>
        <Form.Group controlId="formPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
        </Form.Group>
        <Button variant="primary" type="submit">Login</Button>
      </Form>
    </div>
  );
};

export default Login;
