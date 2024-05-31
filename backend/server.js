const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const app = express();
const PORT = process.env.PORT || 3000;
const SECRET_KEY = ''; // We'll use the secure secret key

const user = []; //In-memory user store

app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.post('signup.html', async (req, res) => {
    const { firstName, lastName, email, password } = req.body;
    const userExists = user.find(user => user.email == email);

    if (userExists) {
        return res.status(400).json({message: 'User already exists!'});
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    user.push({firstName, lastName, email, password:hashedPassword});

    res.status(201).json({message: 'User Created Successful!'});
});

app.post('signIn', async (req, res) => {
    const { username, password, } = req.body;
    const inuser = user.find(user => user.email == username);

    if (!inuser) {
        return res.status(400).json({message: 'Invalid username or password!'});
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
        return res.status(400).json({message: 'Invalid username or password!'});
    }

    const token = jwt.sign({username: user.email}, SECRET_KEY, {expiresIn:'1h'});
    res.status(200).json({message: 'Sign In Successful!', token});
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

