import os
import pandas as pd
from src.simulator import RouletteWheel
from src.strategy import MartingaleHunch
from src.analysis import Analyzer

def main():
    # Configuration
    N_SPINS = 50000
    MIN_BET = 10
    MAX_BET = 1000
    WAIT_STREAKS = [4, 5, 6, 7, 8]
    
    print(f"Running Martingale Hunch Comparative Simulation...")
    print(f"Spins: {N_SPINS}, Wait Streaks: {WAIT_STREAKS}")
    
    # 1. Generate Data (Same spins for all strategies for fair comparison)
    wheel = RouletteWheel()
    spins_df = wheel.generate_spins(N_SPINS)
    
    results = {}
    histories = {}
    
    # 2. Run Strategies
    for wait in WAIT_STREAKS:
        print(f"Testing Wait Streak: {wait}...")
        strategy = MartingaleHunch(min_bet=MIN_BET, max_bet=MAX_BET, wait_streak=wait)
        history_df = strategy.run(spins_df)
        histories[f"Wait {wait}"] = history_df
        
        analyzer = Analyzer(history_df)
        results[f"Wait {wait}"] = analyzer.calculate_metrics()

    # 3. Analyze Results
    print("\n--- Comparative Results ---")
    summary_data = []
    for label, metrics in results.items():
        metrics['Strategy'] = label
        summary_data.append(metrics)
        
    summary_df = pd.DataFrame(summary_data)
    # Reorder columns
    cols = ['Strategy', 'Total Spins', 'Final Bankroll', 'Max Drawdown', 'Busts (Table Limit Hits)', 'Win Rate', 'Total Bets Placed']
    print(summary_df[cols])
        
    # 4. Save Outputs
    os.makedirs('output', exist_ok=True)
    summary_df[cols].to_csv('output/comparative_summary.csv', index=False)
    
    # Plot combined bankroll
    multi_analyzer = Analyzer(histories)
    multi_analyzer.plot_bankroll(save_path='output/comparative_bankroll_chart.png')
    print("\nResults saved to 'output/' directory.")

if __name__ == "__main__":
    main()
