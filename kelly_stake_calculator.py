import streamlit as st

def kelly_criterion(edge, bankroll, kelly_fraction=0.25, max_bet_percent=0.025):
    """
    Calculate the optimal bet size using Kelly Criterion with a fractional approach and max bet cap.
    
    Parameters:
    edge (float): The expected value percentage as a decimal (e.g., 0.12 for 12%).
    bankroll (float): Total available bankroll.
    kelly_fraction (float, optional): Fraction of full Kelly to use (default is 0.25 or 25% Kelly).
    max_bet_percent (float, optional): Maximum bet size as a percentage of bankroll (default is 2.5%).
    
    Returns:
    float: Suggested stake amount.
    """
    # If edge is negative, no bet should be placed
    if edge <= 0:
        return 0.0
    
    # Kelly Criterion calculation
    bet_size = edge * bankroll * kelly_fraction
    
    # Apply max bet cap
    max_bet = bankroll * max_bet_percent
    return min(bet_size, max_bet)

# Streamlit UI
st.title("Kelly Stake Calculator")

# User inputs
bankroll = st.number_input("Bankroll (€):", min_value=0.0, value=5000.0, step=100.0)
edge = st.number_input("Edge (as decimal, e.g., 0.12 for 12%):", min_value=0.0, max_value=1.0, value=0.1418, step=0.01)
kelly_fraction = st.slider("Kelly Fraction (0-1):", min_value=0.0, max_value=1.0, value=0.25, step=0.01)
max_bet_percent = st.slider("Max Bet % of Bankroll (0-1):", min_value=0.0, max_value=1.0, value=0.025, step=0.001)

# Calculate suggested bet
if st.button("Calculate Suggested Bet"):
    suggested_bet = kelly_criterion(edge, bankroll, kelly_fraction, max_bet_percent)
    st.success(f"Suggested Bet: €{suggested_bet:.2f}")
