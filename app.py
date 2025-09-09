import streamlit as st
import math
import pandas as pd

def calculate_monthly_payment(principal, annual_rate, years):
    """
    Calculate monthly lease payment using the standard loan payment formula
    
    Args:
        principal: Loan amount (in LKR)
        annual_rate: Annual interest rate (as decimal, e.g., 0.11 for 11%)
        years: Loan term in years
    
    Returns:
        Monthly payment amount
    """
    monthly_rate = annual_rate / 12
    total_months = years * 12
    
    if monthly_rate == 0:
        return principal / total_months
    
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**total_months) / ((1 + monthly_rate)**total_months - 1)
    return monthly_payment

def calculate_declining_balance_payments(principal, rate_per_lakh_per_month, years):
    """
    Calculate payments for declining balance lease (rate per lakh per month)
    
    This method calculates both:
    1. Principal payment (to reduce the balance)
    2. Interest/service charge based on outstanding balance
    
    Args:
        principal: Loan amount (in LKR)
        rate_per_lakh_per_month: Rate per lakh per month (e.g., 1080)
        years: Loan term in years
    
    Returns:
        Dictionary with payment details and schedule
    """
    total_months = years * 12
    remaining_balance = principal
    monthly_principal_payment = principal / total_months  # Equal principal payments
    total_payments = 0
    total_interest_paid = 0
    payment_schedule = []
    
    for month in range(1, total_months + 1):
        # Calculate interest/service charge based on current balance
        lakhs_remaining = remaining_balance / 100000  # Convert to lakhs
        interest_payment = lakhs_remaining * rate_per_lakh_per_month
        
        # Total monthly payment = principal payment + interest payment
        total_monthly_payment = monthly_principal_payment + interest_payment
        
        # Update balance (only principal payment reduces the balance)
        remaining_balance -= monthly_principal_payment
        total_payments += total_monthly_payment
        total_interest_paid += interest_payment
        
        payment_schedule.append({
            "Month": month,
            "Payment": f"LKR {total_monthly_payment:,.2f}",
            "Principal": f"LKR {monthly_principal_payment:,.2f}",
            "Interest": f"LKR {interest_payment:,.2f}",
            "Balance": f"LKR {remaining_balance:,.2f}",
            "Lakhs_Remaining": f"{lakhs_remaining:.2f}"
        })
        
        # If balance is paid off, break
        if remaining_balance <= 0:
            break
    
    return {
        "total_payments": total_payments,
        "total_interest": total_interest_paid,
        "payment_schedule": payment_schedule,
        "months_to_payoff": len(payment_schedule)
    }

def main():
    st.set_page_config(
        page_title="Lease Calculator",
        page_icon="🏠",
        layout="wide"
    )
    
    st.title("🏠 Lease Calculator")
    st.markdown("Calculate monthly rental payments for your lease")
    
    # Scenario selection
    st.header("📋 Select Lease Type")
    scenario = st.radio(
        "Choose your lease calculation method:",
        ["Fixed Interest Rate Lease", "Declining Balance Lease (Rate per Lakh)"],
        help="Fixed Interest Rate: Traditional loan with fixed monthly payments\nDeclining Balance: Pay based on outstanding amount per lakh per month"
    )
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input Parameters")
        
        # Common input fields
        lease_amount = st.number_input(
            "Lease Amount (LKR)",
            min_value=0,
            value=2000000,  # Default 20 lakhs
            step=100000,
            help="Enter the total lease amount in Sri Lankan Rupees"
        )
        
        lease_duration = st.number_input(
            "Lease Duration (Years)",
            min_value=1,
            max_value=30,
            value=5,
            step=1,
            help="Enter the lease duration in years"
        )
        
        # Conditional input based on scenario
        if scenario == "Fixed Interest Rate Lease":
            interest_rate = st.number_input(
                "Annual Interest Rate (%)",
                min_value=0.0,
                max_value=50.0,
                value=11.0,
                step=0.1,
                help="Enter the annual interest rate as a percentage"
            )
        else:  # Declining Balance Lease
            rate_per_lakh = st.number_input(
                "Rate per Lakh per Month (LKR)",
                min_value=0,
                value=1080,
                step=10,
                help="Enter the rate per lakh per month (e.g., Commercial Bank: 1080)"
            )
    
    with col2:
        st.header("💰 Calculation Results")
        
        if st.button("Calculate Payments", type="primary"):
            if scenario == "Fixed Interest Rate Lease":
                # Convert interest rate from percentage to decimal
                annual_rate_decimal = interest_rate / 100
                
                # Calculate monthly payment
                monthly_payment = calculate_monthly_payment(lease_amount, annual_rate_decimal, lease_duration)
                
                # Display results
                st.success(f"**Fixed Monthly Payment: LKR {monthly_payment:,.2f}**")
                
                # Additional calculations
                total_payments = monthly_payment * lease_duration * 12
                total_interest = total_payments - lease_amount
                
                st.info(f"""
                **Payment Summary:**
                - Total Amount Paid: LKR {total_payments:,.2f}
                - Total Interest: LKR {total_interest:,.2f}
                - Interest as % of Principal: {(total_interest/lease_amount)*100:.2f}%
                """)
                
                # Payment schedule preview (first 12 months)
                st.subheader("📅 Payment Schedule Preview (First 12 Months)")
                
                remaining_balance = lease_amount
                monthly_rate = annual_rate_decimal / 12
                
                schedule_data = []
                for month in range(1, 13):
                    interest_payment = remaining_balance * monthly_rate
                    principal_payment = monthly_payment - interest_payment
                    remaining_balance -= principal_payment
                    
                    schedule_data.append({
                        "Month": month,
                        "Payment": f"LKR {monthly_payment:,.2f}",
                        "Principal": f"LKR {principal_payment:,.2f}",
                        "Interest": f"LKR {interest_payment:,.2f}",
                        "Balance": f"LKR {remaining_balance:,.2f}"
                    })
                
                st.dataframe(schedule_data, use_container_width=True)
                
            else:  # Declining Balance Lease
                # Calculate declining balance payments
                result = calculate_declining_balance_payments(lease_amount, rate_per_lakh, lease_duration)
                
                # Display results
                first_payment = result['payment_schedule'][0]['Payment'] if result['payment_schedule'] else "LKR 0.00"
                st.success(f"**First Month Payment: {first_payment}**")
                st.info(f"**Payments decrease each month as balance reduces**")
                
                st.info(f"""
                **Payment Summary:**
                - Total Amount Paid: LKR {result['total_payments']:,.2f}
                - Total Interest: LKR {result['total_interest']:,.2f}
                - Interest as % of Principal: {(result['total_interest']/lease_amount)*100:.2f}%
                - Months to Payoff: {result['months_to_payoff']}
                """)
                
                # Payment schedule preview (first 12 months or until payoff)
                st.subheader("📅 Payment Schedule Preview")
                
                preview_months = min(12, len(result['payment_schedule']))
                schedule_data = result['payment_schedule'][:preview_months]
                
                st.dataframe(schedule_data, use_container_width=True)
                
                if len(result['payment_schedule']) > 12:
                    st.caption(f"Showing first 12 months. Complete payoff in {result['months_to_payoff']} months.")
    
    # Sidebar with additional information
    with st.sidebar:
        st.header("ℹ️ About")
        
        if scenario == "Fixed Interest Rate Lease":
            st.markdown("""
            **Fixed Interest Rate Lease:**
            Uses the standard loan payment formula with fixed monthly payments.
            
            **Formula:**
            ```
            M = P × [r(1+r)^n] / [(1+r)^n - 1]
            ```
            Where:
            - M = Monthly payment
            - P = Principal amount
            - r = Monthly interest rate
            - n = Total number of payments
            """)
        else:
            st.markdown("""
            **Declining Balance Lease:**
            Payment amount decreases each month as the outstanding balance reduces.
            
            **Calculation:**
            ```
            Monthly Payment = (Outstanding Balance ÷ 100,000) × Rate per Lakh
            ```
            - Outstanding balance recalculated each month
            - Payment amount decreases over time
            - Common in Sri Lankan banking
            """)
        
        st.header("📊 Quick Reference")
        if scenario == "Fixed Interest Rate Lease":
            st.markdown(f"""
            **Current Input:**
            - Amount: LKR {lease_amount:,}
            - Duration: {lease_duration} years
            - Interest: {interest_rate}%
            """)
        else:
            st.markdown(f"""
            **Current Input:**
            - Amount: LKR {lease_amount:,}
            - Duration: {lease_duration} years
            - Rate per Lakh: LKR {rate_per_lakh}
            """)
        
        st.header("🏦 Bank Examples")
        st.markdown("""
        **Commercial Bank Sri Lanka:**
        - Rate per lakh per month: ~LKR 1,080
        
        **Other Banks:**
        - Rates vary by bank and loan type
        - Check with your bank for current rates
        """)

if __name__ == "__main__":
    main()
