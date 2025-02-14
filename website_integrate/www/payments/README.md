# Relworx Payment Integration

This project implements Relworx payment integration for receiving payments.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Relworx credentials:
```
RELWORX_API_KEY=your_api_key
RELWORX_MERCHANT_ID=your_merchant_id
```

3. Run the application:
```bash
python app.py
```

## Features
- Payment processing using Relworx
- Payment status verification
- Transaction history

## Security Note
Never commit your `.env` file or expose your API credentials. 