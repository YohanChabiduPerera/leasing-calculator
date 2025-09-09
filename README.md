# Lease Calculator

A Streamlit web application for calculating monthly lease payments.

## Features

- Calculate monthly lease payments based on principal amount, interest rate, and lease duration
- Interactive input fields with default values (20 lakhs LKR, 5 years, 11% interest)
- Payment summary showing total amount paid and interest
- Payment schedule preview for the first 12 months
- Clean, responsive UI with sidebar information

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

3. Adjust the input parameters:
   - **Lease Amount**: Enter the total lease amount in LKR
   - **Lease Duration**: Enter the lease duration in years
   - **Annual Interest Rate**: Enter the interest rate as a percentage

4. Click "Calculate Monthly Payment" to see the results

## Default Values

The app comes pre-configured with your specified values:
- Lease Amount: 20,000,000 LKR (20 lakhs)
- Lease Duration: 5 years
- Annual Interest Rate: 11%

## Formula

The calculator uses the standard loan payment formula:
```
M = P × [r(1+r)^n] / [(1+r)^n - 1]
```

Where:
- M = Monthly payment
- P = Principal amount
- r = Monthly interest rate (annual rate ÷ 12)
- n = Total number of payments (years × 12)
