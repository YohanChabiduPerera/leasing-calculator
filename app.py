import streamlit as st
import math

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

def main():
    st.set_page_config(
        page_title="Lease Calculator",
        page_icon="🏠",
        layout="wide"
    )
    
    st.title("🏠 Lease Calculator")
    st.markdown("Calculate monthly rental payments for your lease")
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input Parameters")
        
        # Input fields
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
        
        interest_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=50.0,
            value=11.0,
            step=0.1,
            help="Enter the annual interest rate as a percentage"
        )
    
    with col2:
        st.header("💰 Calculation Results")
        
        if st.button("Calculate Monthly Payment", type="primary"):
            # Convert interest rate from percentage to decimal
            annual_rate_decimal = interest_rate / 100
            
            # Calculate monthly payment
            monthly_payment = calculate_monthly_payment(lease_amount, annual_rate_decimal, lease_duration)
            
            # Display results
            st.success(f"**Monthly Payment: LKR {monthly_payment:,.2f}**")
            
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
    
    # Sidebar with additional information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This calculator uses the standard loan payment formula to calculate monthly lease payments.
        
        **Formula Used:**
        ```
        M = P × [r(1+r)^n] / [(1+r)^n - 1]
        ```
        Where:
        - M = Monthly payment
        - P = Principal amount
        - r = Monthly interest rate
        - n = Total number of payments
        """)
        
        st.header("📊 Quick Reference")
        st.markdown(f"""
        **Current Input:**
        - Amount: LKR {lease_amount:,}
        - Duration: {lease_duration} years
        - Interest: {interest_rate}%
        """)

if __name__ == "__main__":
    main()
