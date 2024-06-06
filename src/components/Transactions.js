import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Form, Button } from 'react-bootstrap';
import './Finance.css';

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [newTransaction, setNewTransaction] = useState({
    description: '',
    amount: '',
    date: ''
  });

  useEffect(() => {
    axios.get('http://localhost:5000/transactions', { withCredentials: true })
      .then(response => {
        setTransactions(response.data.transactions);
      })
      .catch(error => {
        console.error('Failed to fetch transactions:', error);
      });
  }, []);

  const handleChange = (e) => {
    setNewTransaction({ ...newTransaction, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/transactions', newTransaction, { withCredentials: true })
      .then(response => {
        setTransactions([...transactions, response.data.transaction]);
        setNewTransaction({ description: '', amount: '', date: '' });
      })
      .catch(error => {
        console.error('Failed to add transaction:', error);
      });
  };

  return (
    <div className="finance-section">
      <h2>Transactions</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formDescription">
          <Form.Label>Description</Form.Label>
          <Form.Control type="text" name="description" value={newTransaction.description} onChange={handleChange} required />
        </Form.Group>
        <Form.Group controlId="formAmount">
          <Form.Label>Amount</Form.Label>
          <Form.Control type="number" name="amount" value={newTransaction.amount} onChange={handleChange} required />
        </Form.Group>
        <Form.Group controlId="formDate">
          <Form.Label>Date</Form.Label>
          <Form.Control type="date" name="date" value={newTransaction.date} onChange={handleChange} required />
        </Form.Group>
        <Button variant="primary" type="submit">Add Transaction</Button>
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
          {transactions.map((transaction, index) => (
            <tr key={index}>
              <td>{transaction.description}</td>
              <td>{transaction.amount}</td>
              <td>{transaction.date}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Transactions;
