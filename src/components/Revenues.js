import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Form, Button } from 'react-bootstrap';
import './Finance.css';

const Revenues = () => {
  const [revenues, setRevenues] = useState([]);
  const [newRevenue, setNewRevenue] = useState({
    description: '',
    amount: '',
    date: ''
  });

  useEffect(() => {
    axios.get('http://localhost:5000/revenues', { withCredentials: true })
      .then(response => {
        setRevenues(response.data.revenues);
      })
      .catch(error => {
        console.error('Failed to fetch revenues:', error);
      });
  }, []);

  const handleChange = (e) => {
    setNewRevenue({ ...newRevenue, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/revenues', newRevenue, { withCredentials: true })
      .then(response => {
        setRevenues([...revenues, response.data.revenue]);
        setNewRevenue({ description: '', amount: '', date: '' });
      })
      .catch(error => {
        console.error('Failed to add revenue:', error);
      });
  };

  return (
    <div className="finance-section">
      <h2>Revenues</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formDescription">
          <Form.Label>Description</Form.Label>
          <Form.Control type="text" name="description" value={newRevenue.description} onChange={handleChange} required />
        </Form.Group>
        <Form.Group controlId="formAmount">
          <Form.Label>Amount</Form.Label>
          <Form.Control type="number" name="amount" value={newRevenue.amount} onChange={handleChange} required />
        </Form.Group>
        <Form.Group controlId="formDate">
          <Form.Label>Date</Form.Label>
          <Form.Control type="date" name="date" value={newRevenue.date} onChange={handleChange} required />
        </Form.Group>
        <Button variant="primary" type="submit">Add Revenue</Button>
      </Form>

      <Table striped bordered hover className="finance-table">
        <thead>
          <tr>
            <th>Description</th>
            <th>Amount</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {revenues.map((revenue, index) => (
            <tr key={index}>
              <td>{revenue.description}</td>
              <td>{revenue.amount}</td>
              <td>{revenue.date}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Revenues;
