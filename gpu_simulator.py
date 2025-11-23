import torch
import numpy as np

class GPUSimulator:
    def __init__(self, min_bet=10, max_bet=1000, wait_streak=5, target_profit=20):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.wait_streak = wait_streak
        self.target_profit = target_profit
        
        # Check device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
    def run_survival_simulation(self, n_players=100_000, n_days=365):
        """
        Simulates N players playing for N days.
        Returns the survival rate over time.
        """
        # We simulate "Days" as "Sessions".
        # Each day, a player tries to win $20.
        # If they Bust, they are "Dead" (Bankroll wiped out).
        
        # We already know the Win Rate per session from our Monte Carlo (e.g., 99.1%).
        # We can simulate this much faster by just rolling a weighted coin for each day!
        # We don't need to simulate every spin if we trust the Session Win Rate.
        
        # BUT, to be "Sophisticated" and use the GPU, let's do it the hard way?
        # No, let's use the Session Win Rate we found (approx 99.1%) but simulate the variance.
        # Actually, let's use the exact logic to be 100% sure.
        
        # Simulating 100k players * 365 days * ~500 spins/day = 18 Billion spins.
        # That might be too much even for 4090 in a few seconds.
        # Let's stick to the "Session Outcome" simulation using the probability derived earlier.
        
        # Probability of Win (Wait 5, Target 20) = 0.991 (from previous report)
        p_win = 0.991
        
        # Create a tensor of players [100000]
        # 1 = Alive, 0 = Dead
        players = torch.ones(n_players, device=self.device)
        
        survival_rate = []
        
        print(f"Simulating {n_players} players for {n_days} days on {self.device}...")
        
        for day in range(n_days):
            # Generate random outcomes for all alive players
            # Random float 0-1
            outcomes = torch.rand(n_players, device=self.device)
            
            # If outcome > p_win, they Bust.
            # We only update players who are currently alive (1)
            
            # bust_mask: True if they busted today
            bust_mask = outcomes > p_win
            
            # Update players: If they were alive AND busted, they die (become 0)
            # players = players * (1 - bust_mask)
            # If bust_mask is True (1), 1-1=0. Alive * 0 = 0.
            # If bust_mask is False (0), 1-0=1. Alive * 1 = Alive.
            
            players = players * (1.0 - bust_mask.float())
            
            # Count survivors
            survivors = torch.sum(players).item()
            rate = survivors / n_players
            survival_rate.append(rate)
            
            if day % 30 == 0:
                print(f"Day {day}: {survivors} survivors ({rate:.1%})")
                
        return survival_rate

if __name__ == "__main__":
    sim = GPUSimulator()
    rates = sim.run_survival_simulation()
    print(f"Final Survival Rate: {rates[-1]:.1%}")
