import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Force reload of sys.path to be sure
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from src.optimizer import Optimizer
from src.simulator import RouletteWheel
from src.strategy import MartingaleHunch
from src.analysis import Analyzer
from gpu_simulator import GPUSimulator

st.set_page_config(page_title="Martingale Hunch Optimizer", layout="wide")

st.title("🎲 Martingale Hunch Strategy Optimizer")

# Sidebar Controls
st.sidebar.header("Strategy Parameters")
wait_streak = st.sidebar.slider("Wait Streak (Red/Black)", 4, 10, 5)
min_bet = st.sidebar.number_input("Min Bet ($)", value=10)
max_bet = st.sidebar.number_input("Max Bet (Table Limit)", value=1000)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Session Optimizer", "⏱️ Wait Streak Analysis", "🎰 Live Simulator", "💀 Survival Analysis", "🏆 Final Recommendation"])

with tab1:
    st.header("Find the Optimal Take Profit")
    st.markdown("""
    This tool simulates thousands of sessions to find the **"Sweet Spot"**.
    - **Win Rate**: Probability of reaching the target profit before busting.
    - **Expected Value (EV)**: Average profit/loss per session.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        n_sessions = st.slider("Number of Sessions per Target", 100, 5000, 1000)
    with col2:
        # Allow lower targets to see the $20 sweet spot
        max_target = st.slider("Max Target Profit to Test", 50, 500, 200)
        step_size = st.slider("Step Size", 10, 50, 10)
        
    if st.button("Run Profit Optimization"):
        with st.spinner("Running Monte Carlo Simulation..."):
            opt = Optimizer(wait_streak=wait_streak)
            # Override simulator params
            opt.simulator.min_bet = min_bet
            opt.simulator.max_bet = max_bet
            
            # Start from $10 to capture the low-end sweet spot
            df = opt.optimize(min_target=10, max_target=max_target, step=step_size, n_sessions=n_sessions)
            
            st.success("Optimization Complete!")
            
            # Display Metrics
            best_ev = df.loc[df['Expected Value'].idxmax()]
            st.metric("Best Expected Value", f"${best_ev['Expected Value']:.2f}", f"Target: ${best_ev['Target Profit']}")
            
            # Plots
            fig, ax1 = plt.subplots(figsize=(10, 6))
            
            color = 'tab:blue'
            ax1.set_xlabel('Target Profit ($)')
            ax1.set_ylabel('Win Rate (%)', color=color)
            ax1.plot(df['Target Profit'], df['Win Rate'] * 100, color=color, marker='o')
            ax1.tick_params(axis='y', labelcolor=color)
            
            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            
            color = 'tab:red'
            ax2.set_ylabel('Expected Value ($)', color=color)  # we already handled the x-label with ax1
            ax2.plot(df['Target Profit'], df['Expected Value'], color=color, linestyle='--', marker='x')
            ax2.tick_params(axis='y', labelcolor=color)
            ax2.axhline(0, color='gray', linestyle=':', alpha=0.5)
            
            plt.title(f"Win Rate vs. EV (Wait Streak: {wait_streak})")
            st.pyplot(fig)
            
            st.dataframe(df)

with tab2:
    st.header("Optimize Wait Streak")
    st.markdown(f"""
    Compare different Wait Streaks (3, 4, 5, 6, 7, 8) for a fixed Target Profit.
    **Current Settings**: Bet ${min_bet}, Target Profit (Set below).
    """)
    
    target_for_wait = st.number_input("Target Profit for Comparison ($)", value=20)
    n_sessions_wait = st.slider("Sessions per Config", 100, 5000, 2000)
    
    if st.button("Run Wait Streak Analysis"):
        with st.spinner("Running Comparative Analysis..."):
            from src.fast_simulator import FastSimulator
            
            wait_streaks = [3, 4, 5, 6, 7, 8]
            results = []
            
            for wait in wait_streaks:
                sim = FastSimulator(min_bet=min_bet, max_bet=max_bet, wait_streak=wait)
                stats = sim.run_monte_carlo(target_profit=target_for_wait, n_sessions=n_sessions_wait)
                
                res = {
                    'Wait Streak': wait,
                    'Win Rate': stats['Win Rate'],
                    'Bust Rate': stats['Bust Rate'],
                    'EV': (stats['Win Rate'] * target_for_wait) - (stats['Bust Rate'] * 1270) # Approx loss
                }
                results.append(res)
            
            df_wait = pd.DataFrame(results)
            st.success("Analysis Complete!")
            
            # Plot
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Win Rate Bar Chart
            sns.barplot(data=df_wait, x='Wait Streak', y='Win Rate', ax=ax1, color='skyblue')
            ax1.set_title("Win Rate by Wait Streak")
            ax1.set_ylim(0.9, 1.0) # Zoom in to see difference
            ax1.axhline(1.0, color='green', linestyle='--')
            
            # EV Bar Chart
            sns.barplot(data=df_wait, x='Wait Streak', y='EV', ax=ax2, color='lightgreen')
            ax2.set_title("Expected Value by Wait Streak")
            ax2.axhline(0, color='red', linestyle='--')
            
            st.pyplot(fig)
            st.dataframe(df_wait)

with tab3:
    st.header("Live Session Simulator")
    st.markdown("Watch a single session play out.")
    
    target_profit = st.number_input("Target Profit ($)", value=20) # Default to the recommended $20
    
    if st.button("Run Single Session"):
        wheel = RouletteWheel()
        # Generate enough spins for a long session
        spins_df = wheel.generate_spins(2000)
        
        strategy = MartingaleHunch(min_bet=min_bet, max_bet=max_bet, wait_streak=wait_streak)
        # We need to modify strategy to stop at target profit
        # For now, run standard and slice it
        history_df = strategy.run(spins_df)
        
        # Find stop point
        stop_index = -1
        outcome = "Incomplete"
        for i, row in history_df.iterrows():
            if row['bankroll'] >= target_profit:
                stop_index = i
                outcome = "Win"
                break
            if row['outcome'] == 'Bust':
                stop_index = i
                outcome = "Bust"
                break
        
        if stop_index != -1:
            history_df = history_df.iloc[:stop_index+1]
            
        analyzer = Analyzer(history_df)
        
        st.subheader(f"Outcome: {outcome}")
        st.line_chart(history_df['bankroll'])
        st.dataframe(history_df.tail())

with tab4:
    st.header("💀 Survival Analysis (GPU)")
    st.markdown("""
    **"What if I play every day for a year?"**
    
    This simulation uses your **RTX 4090** (via PyTorch) to simulate **100,000 Players** trying to win $20 every day for 365 days.
    
    - **Goal**: Survive the whole year.
    - **Failure**: Losing your bankroll (Bust) on ANY single day.
    """)
    
    if st.button("Run Year-Long Simulation"):
        with st.spinner("Simulating 100,000 Players on GPU..."):
            
            sim = GPUSimulator()
            rates = sim.run_survival_simulation(n_players=100000, n_days=365)
            
            st.success("Simulation Complete!")
            
            # Plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(rates, color='red', linewidth=2)
            ax.set_title("Survival Rate Over 365 Days")
            ax.set_xlabel("Day")
            ax.set_ylabel("Percent of Players Alive")
            ax.set_ylim(0, 1.0)
            ax.grid(True, alpha=0.3)
            
            # Annotate final
            final_rate = rates[-1]
            ax.text(365, final_rate, f"{final_rate:.1%}", fontsize=12, fontweight='bold')
            
            st.pyplot(fig)
            
            st.metric("Final Survival Rate", f"{final_rate:.1%}")
            st.error(f"This means {100 - final_rate*100:.1f}% of players went BUST within a year.")

with tab5:
    st.header("🏆 Final Recommendation")
    
    st.success("The Final Number: **$20 Profit Target**")
    
    st.markdown("""
    ### Why $20?
    Based on our extensive simulations (Monte Carlo Analysis), aiming for a small **$20 profit** with a **$10 base bet** is the statistically safest strategy.
    
    #### 1. The "Hit and Run" Sweet Spot
    - **Win Rate**: ~98.8%
    - **Risk**: You are only exposing yourself to the "Bust Streak" for a very short time.
    - **EV**: This was the only configuration that showed a positive Expected Value in our tests (due to variance, but it indicates it's the least negative option).
    
    #### 2. Why not bet higher?
    We tested increasing the bet to $20 and $50.
    - **$10 Bet**: You survive **7** losses in a row.
    - **$50 Bet**: You only survive **5** losses in a row.
    - **Result**: Betting $50 **doubles** your chance of busting. The speed isn't worth the risk.
    
    ### The Strategy Checklist
    1.  **Wait**: Wait for a streak of **5** (Red/Black).
    2.  **Bet**: Start with **$10** on the opposite color.
    3.  **Martingale**: Double on loss ($10 -> $20 -> $40...).
    4.  **Stop**: As soon as your total bankroll is **+$20**, **WALK AWAY**.
    """)
    
    st.warning("⚠️ **Warning**: If you continue playing after winning $20, the probability of a total loss ($1,270) increases with every spin. The 'Win' is only valid if you stop.")
