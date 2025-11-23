import pandas as pd
from src.fast_simulator import FastSimulator

class Optimizer:
    def __init__(self, wait_streak=5):
        self.simulator = FastSimulator(wait_streak=wait_streak)
        
    def optimize(self, min_target=50, max_target=500, step=50, n_sessions=1000):
        """
        Runs the simulator for a range of target profits.
        """
        targets = range(min_target, max_target + step, step)
        results = []
        
        print(f"Optimizing for Wait Streak {self.simulator.wait_streak}...")
        
        for target in targets:
            # We need to account for the actual cost of a bust.
            # Martingale 10-1000 sequence: 10, 20, 40, 80, 160, 320, 640.
            # Total Loss = 1270.
            # If we bust, we lose ~1270.
            
            stats = self.simulator.run_monte_carlo(target, n_sessions)
            
            # Refine EV calculation
            # EV = (Win Rate * Target) - (Bust Rate * 1270)
            ev = (stats['Win Rate'] * target) - (stats['Bust Rate'] * 1270)
            stats['Expected Value'] = ev
            
            results.append(stats)
            print(f"Target: ${target} -> Win Rate: {stats['Win Rate']:.1%}, EV: ${ev:.2f}")
            
        return pd.DataFrame(results)

if __name__ == "__main__":
    opt = Optimizer(wait_streak=5)
    df = opt.optimize()
    print(df)
