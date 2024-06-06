import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Form, Button, Card } from 'react-bootstrap';
import './Profile.css';

const Profile = () => {
  const [profile, setProfile] = useState({
    email: '',
    username: '',
    name: '',
    id: '',
    address: '',
    occupation: '',
    profilePicture: ''
  });

  const [profilePicture, setProfilePicture] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:5000/profile', { withCredentials: true })
      .then(response => {
        setProfile(response.data.user);
      })
      .catch(error => {
        console.error('Failed to fetch profile:', error);
      });
  }, []);

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    setProfilePicture(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('name', profile.name);
    formData.append('id', profile.id);
    formData.append('address', profile.address);
    formData.append('occupation', profile.occupation);

    if (profilePicture) {
      formData.append('profilePicture', profilePicture);
    }

    axios.post('http://localhost:5000/profile', formData, {
      withCredentials: true,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
      .then(response => {
        setProfile(response.data.user);
        setProfilePicture(null);
      })
      .catch(error => {
        console.error('Failed to update profile:', error);
      });
  };

  return (
    <div className="profile-section">
      <Card style={{ width: '18rem' }}>
        <Card.Img variant="top" src={profile.profilePicture ? `http://localhost:5000/${profile.profilePicture}` : '/default-avatar.png'} />
        <Card.Body>
          <Card.Title>{profile.username}</Card.Title>
          <Card.Text>
            Email: {profile.email}
          </Card.Text>
        </Card.Body>
      </Card>

      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formName">
          <Form.Label>Name</Form.Label>
          <Form.Control type="text" name="name" value={profile.name} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="formId">
          <Form.Label>ID</Form.Label>
          <Form.Control type="text" name="id" value={profile.id} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="formAddress">
          <Form.Label>Address</Form.Label>
          <Form.Control type="text" name="address" value={profile.address} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="formOccupation">
          <Form.Label>Occupation</Form.Label>
          <Form.Control type="text" name="occupation" value={profile.occupation} onChange={handleChange} />
        </Form.Group>
        <Form.Group controlId="formProfilePicture">
          <Form.Label>Profile Picture</Form.Label>
          <Form.Control type="file" name="profilePicture" onChange={handleFileChange} />
        </Form.Group>
        <Button variant="primary" type="submit">Update Profile</Button>
      </Form>
    </div>
  );
};

export default Profile;
