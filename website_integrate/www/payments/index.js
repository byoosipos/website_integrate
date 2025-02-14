const express = require('express');
const cors = require('cors');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Relworx API configuration
const RELWORX_CONFIG = {
    BASE_URL: 'https://payments.relworx.com/api',
    API_KEY: '45ecb53c81fead.Rta8MNVQQhDS7s1J_hqIYw',
    ACCOUNT_NO: 'RELC23A5AB148'
};

// Middleware
app.use(cors({
    origin: ['https://dev.byoosi.com', 'http://localhost:3000'],
    methods: ['GET', 'POST'],
    credentials: true
}));
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Create router for Relworx API endpoints
const relworxRouter = express.Router();

// Proxy endpoint for payment request
relworxRouter.post('/mobile-money/request-payment', async (req, res) => {
    try {
        console.log('Received payment request:', req.body);
        const response = await axios.post(
            `${RELWORX_CONFIG.BASE_URL}/mobile-money/request-payment`,
            req.body,
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/vnd.relworx.v2',
                    'Authorization': `Bearer ${RELWORX_CONFIG.API_KEY}`
                }
            }
        );
        console.log('Relworx response:', response.data);
        res.json(response.data);
    } catch (error) {
        console.error('Payment request error:', error.response?.data || error.message);
        res.status(error.response?.status || 500).json({
            success: false,
            message: error.response?.data?.message || 'Payment request failed'
        });
    }
});

// Proxy endpoint for transaction status
relworxRouter.get('/mobile-money/transaction-status/:reference', async (req, res) => {
    try {
        console.log('Checking status for reference:', req.params.reference);
        const response = await axios.get(
            `${RELWORX_CONFIG.BASE_URL}/mobile-money/transaction-status/${req.params.reference}`,
            {
                headers: {
                    'Accept': 'application/vnd.relworx.v2',
                    'Authorization': `Bearer ${RELWORX_CONFIG.API_KEY}`
                }
            }
        );
        console.log('Status response:', response.data);
        res.json(response.data);
    } catch (error) {
        console.error('Status check error:', error.response?.data || error.message);
        res.status(error.response?.status || 500).json({
            success: false,
            message: error.response?.data?.message || 'Failed to check payment status'
        });
    }
});

// Mount the Relworx router
app.use('/api/relworx', relworxRouter);

// Webhook endpoint for payment notifications
app.post('/webhook', (req, res) => {
    console.log('Received webhook:', req.body);
    // Handle webhook notification
    // Verify signature and process payment update
    res.json({ success: true });
});

// Serve the payment page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('Server error:', err);
    res.status(500).json({
        success: false,
        message: 'Internal server error'
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`API endpoints:`);
    console.log(`- Payment request: POST /api/relworx/mobile-money/request-payment`);
    console.log(`- Status check: GET /api/relworx/mobile-money/transaction-status/:reference`);
    console.log(`- Webhook: POST /webhook`);
}); 