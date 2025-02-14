const express = require('express');
const cors = require('cors');
const axios = require('axios');
const path = require('path');

const app = express();

// Enable CORS
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '/')));

// Proxy endpoint for payment requests
app.post('/api/payment', async (req, res) => {
    try {
        const response = await axios({
            method: 'POST',
            url: 'https://payments.relworx.com/api/mobile-money/request-payment',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.relworx.v2',
                'Authorization': `Bearer ${process.env.RELWORX_API_KEY || '45ecb53c81fead.Rta8MNVQQhDS7s1J_hqIYw'}`
            },
            data: req.body
        });
        
        res.json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json({
            success: false,
            message: error.response?.data?.message || 'Payment request failed'
        });
    }
});

// Proxy endpoint for phone validation
app.post('/api/validate', async (req, res) => {
    try {
        const response = await axios({
            method: 'POST',
            url: 'https://payments.relworx.com/api/mobile-money/validate',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.relworx.v2',
                'Authorization': `Bearer ${process.env.RELWORX_API_KEY || '45ecb53c81fead.Rta8MNVQQhDS7s1J_hqIYw'}`
            },
            data: req.body
        });
        
        res.json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json({
            success: false,
            message: error.response?.data?.message || 'Validation failed'
        });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
}); 