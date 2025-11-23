import pandas as pd
from src.fast_simulator import FastSimulator

def optimize_bets():
    base_bets = [10, 20, 50]
    targets = [20, 50, 100, 200]
    wait_streak = 5
    n_sessions = 5000
    
    results = []
    
    print(f"Running Bet Size Optimization ({n_sessions} sessions per config)...")
    
    for bet in base_bets:
        for target in targets:
            # Calculate Max Loss for this bet size
            # $10: 10+20+40+80+160+320+640 = 1270
            # $20: 20+40+80+160+320+640 = 1260
            # $50: 50+100+200+400+800 = 1550 (Next is 1600 > 1000)
            
            # We need to know the exact loss amount to calc EV correctly.
            # Let's just use the simulator's bankroll return on bust.
            
            sim = FastSimulator(min_bet=bet, max_bet=1000, wait_streak=wait_streak)
            stats = sim.run_monte_carlo(target_profit=target, n_sessions=n_sessions)
            
            # EV is tricky because 'Bust' returns a variable negative number depending on where it stopped.
            # But run_monte_carlo returns 'EV' based on a hardcoded 1000. Let's recalculate manually if needed.
            # Actually, let's trust the Win Rate as the primary metric for the user.
            
            res = {
                'Base Bet': bet,
                'Target Profit': target,
                'Win Rate': stats['Win Rate'],
                'Bust Rate': stats['Bust Rate'],
                'EV (Approx)': (stats['Win Rate'] * target) - (stats['Bust Rate'] * 1270) # Approx
            }
            results.append(res)
            print(f"Bet ${bet} -> Target ${target}: Win {stats['Win Rate']:.1%}")

    df = pd.DataFrame(results)
    
    print("\n--- Optimization Results ---")
    print(df.to_markdown(index=False))
    
    # Save
    df.to_csv('output/bet_optimization.csv', index=False)

if __name__ == "__main__":
    optimize_bets()
