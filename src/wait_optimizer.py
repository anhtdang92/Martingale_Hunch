import pandas as pd
from src.fast_simulator import FastSimulator

def optimize_wait():
    wait_streaks = [3, 4, 5, 6, 7, 8]
    target = 20
    bet = 10
    n_sessions = 5000
    
    results = []
    
    print(f"Running Wait Streak Optimization (Target ${target}, Bet ${bet})...")
    
    for wait in wait_streaks:
        # Note: FastSimulator doesn't currently track "Total Spins" to finish.
        # We might need to infer it or accept we only get Win Rate/EV.
        # For "Patience", Win Rate is the proxy for safety.
        
        sim = FastSimulator(min_bet=bet, max_bet=1000, wait_streak=wait)
        stats = sim.run_monte_carlo(target_profit=target, n_sessions=n_sessions)
        
        res = {
            'Wait Streak': wait,
            'Win Rate': stats['Win Rate'],
            'Bust Rate': stats['Bust Rate'],
            'EV (Approx)': (stats['Win Rate'] * target) - (stats['Bust Rate'] * 1270)
        }
        results.append(res)
        print(f"Wait {wait} -> Win {stats['Win Rate']:.1%}")

    df = pd.DataFrame(results)
    
    print("\n--- Wait Optimization Results ---")
    print(df.to_markdown(index=False))
    
    df.to_csv('output/wait_optimization.csv', index=False)

if __name__ == "__main__":
    optimize_wait()
