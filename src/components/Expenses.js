import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Form, Button } from 'react-bootstrap';
import './Finance.css';

const Expenses = () => {
  const [expenses, setExpenses] = useState([]);
  const [newExpense, setNewExpense] = useState({
    description: '',
    amount: '',
    date: ''
  });

  useEffect(() => {
    axios.get('http://localhost:5000/expenses', { withCredentials: true })
      .then(response => {
        setExpenses(response.data.expenses);
      })
      .catch(error => {
        console.error('Failed to fetch expenses:', error);
      });
  }, []);

  const handleChange = (e) => {
    setNewExpense({ ...newExpense, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/expenses', newExpense, { withCredentials: true })
      .then(response => {
        setExpenses([...expenses, response.data.expense]);
        setNewExpense({ description: '', amount: '', date: '' });
      })
      .catch(error => {
        console.error('Failed to add expense:', error);
      });
  };

  return (
    <div className="finance-section">
      <h2>Expenses</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formDescription">
          <Form.Label>Description</Form.Label>
          <Form.Control type="text" name="description" value={newExpense.description} onChange={handleChange} required />
        </Form.Group>
        <Form.Group controlId="formAmount">
          <Form.Label>Amount</Form.Label>
          <Form.Control type="number" name="amount" value={newExpense.amount} onChange={handleChange} required />
        </Form.Group>
        <Form.Group controlId="formDate">
          <Form.Label>Date</Form.Label>
          <Form.Control type="date" name="date" value={newExpense.date} onChange={handleChange} required />
        </Form.Group>
        <Button variant="primary" type="submit">Add Expense</Button>
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
          {expenses.map((expense, index) => (
            <tr key={index}>
              <td>{expense.description}</td>
              <td>{expense.amount}</td>
              <td>{expense.date}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default Expenses;
