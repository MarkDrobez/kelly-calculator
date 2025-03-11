import streamlit as st

def kelly_criterion(edge, bankroll, kelly_fraction=25, max_bet_percent=2.5):
    """
    Calculate the optimal bet size using Kelly Criterion with a fractional approach and max bet cap.
    
    Parameters:
    edge (float): The expected value percentage as a decimal (e.g., 0.12 for 12%).
    bankroll (float): Total available bankroll.
    kelly_fraction (float, optional): Fraction of full Kelly to use as a percentage (default is 25 for 0.25 or 25% Kelly).
    max_bet_percent (float, optional): Maximum bet size as a percentage of bankroll (default is 2.5%).
    
    Returns:
    float: Suggested stake amount.
    """
    # Convert edge, kelly fraction, and max bet percentage to decimal
    edge = edge / 100
    kelly_fraction = kelly_fraction / 100
    max_bet_percent = max_bet_percent / 100
    
    # If edge is negative, no bet should be placed
    if edge <= 0:
        return 0.0
    
    # Kelly Criterion calculation
    bet_size = edge * bankroll * kelly_fraction
    
    # Apply max bet cap
    max_bet = bankroll * max_bet_percent
    return round(min(bet_size, max_bet))

# Streamlit UI
st.set_page_config(page_title="Kelly Stake Calculator", layout="wide")
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        .stButton button { width: 100%; border-radius: 5px; font-size: 14px; padding: 8px; }
        .stNumberInput input { border-radius: 5px; font-size: 14px; }
        .stContainer { padding: 1rem; }
        .stSuccess { background-color: #d4edda; padding: 10px; border-radius: 5px; }
        .stInfo { background-color: #cce5ff; padding: 10px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

st.title("Kelly Stake Calculator")

# Initialize session state for bankroll and log
if 'bankroll' not in st.session_state:
    st.session_state.bankroll = 5000.0
if 'log' not in st.session_state:
    st.session_state.log = []

bankroll = st.session_state.bankroll

col1, col2 = st.columns([1.5, 2])

with col2:
    st.subheader("Bet Settings")
    edge = st.number_input("Edge (as percentage, e.g., 4.5 for 4.5%):", min_value=0.0, value=14.18, step=0.1)
    kelly_fraction = st.number_input("Kelly Fraction (as percentage, e.g., 25 for 25%):", min_value=0.0, value=25, step=1)
    max_bet_percent = st.number_input("Max Bet % of Bankroll (e.g., 2.5 for 2.5%):", min_value=0.0, value=2.5, step=0.1)

    # Calculate suggested bet automatically
    suggested_bet = kelly_criterion(edge, bankroll, kelly_fraction, max_bet_percent)
    st.markdown(f"<div class='stSuccess'>💰 Suggested Bet: €{suggested_bet}</div>", unsafe_allow_html=True)
    
    if st.button("I Placed This Bet", key="place_bet"):
        if suggested_bet <= bankroll:
            st.session_state.bankroll -= suggested_bet
            st.session_state.log.append(f"- €{suggested_bet} (Bet Placed)")
            st.rerun()
        else:
            st.error("Insufficient funds to place the bet!")

    # Display updated bankroll
    st.markdown(f"<div class='stInfo'>📌 Updated Bankroll: €{st.session_state.bankroll}</div>", unsafe_allow_html=True)
    
    # Manual balance update below bankroll
    new_balance = st.number_input("Current Balance (€):", value=st.session_state.bankroll, step=10.0)
    if st.button("Set Balance", key="set_balance"):
        st.session_state.log.append(f"Balance changed to €{new_balance}")
        st.session_state.bankroll = new_balance
        st.rerun()

with col1:
    st.subheader("Balance Log")
    with st.container():
        for log_entry in reversed(st.session_state.log):
            st.write(log_entry)
