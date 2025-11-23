import numpy as np

class FastSimulator:
    def __init__(self, min_bet=10, max_bet=1000, wait_streak=5):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.wait_streak = wait_streak
        
        # American Roulette Probabilities
        self.p_red = 18/38
        self.p_black = 18/38
        self.p_green = 2/38
        
    def simulate_session(self, target_profit, max_spins=10000):
        """
        Simulates a single session until Target Profit or Bust.
        Returns: 'Win' or 'Bust', and final bankroll.
        """
        bankroll = 0
        current_bet = 0
        streak_count = 0
        streak_color = None # 0: Red, 1: Black, 2: Green
        
        # We can't easily vectorize the *entire* session logic because betting depends on state.
        # But we can generate a batch of spins and iterate fast using Numba or just optimized Python.
        # For "Millions of spins" in Python, a pure loop is slow.
        # However, for "Session Optimization", we need to run many *independent* sessions.
        # We can simulate the "Game Logic" efficiently.
        
        # Let's use a generator approach for infinite spins until stop condition
        
        spins = np.random.choice([0, 1, 2], size=max_spins, p=[self.p_red, self.p_black, self.p_green])
        # 0: Red, 1: Black, 2: Green
        
        for spin in spins:
            # 1. Resolve Bet
            if current_bet > 0:
                # We always bet AGAINST the streak.
                # If streak was Red (0), we bet Black (1).
                # Win if spin == 1.
                
                winning_color = 1 if streak_color == 0 else 0
                
                if spin == winning_color:
                    bankroll += current_bet
                    current_bet = 0
                    # Reset streak? Logic says "start over again by waiting for 4 red/blacks"
                    streak_count = 0 
                    streak_color = None
                else:
                    bankroll -= current_bet
                    next_bet = current_bet * 2
                    if next_bet <= self.max_bet:
                        current_bet = next_bet
                        # Streak continues effectively for betting purposes
                    else:
                        return 'Bust', bankroll # Hit table limit
            
            # 2. Check Stop Conditions
            if bankroll >= target_profit:
                return 'Win', bankroll
            if bankroll <= -self.max_bet: # Simplified bust check (if we lost 1000 total? No, table limit is max bet)
                # Actually, "Bust" usually means losing the bankroll. 
                # But here "Bust" is defined as "Hitting the Table Limit" which forces a loss realization.
                # If we hit table limit, we take the loss and stop? Or reset?
                # User said: "so on and so forth until i win". 
                # If we hit table limit, we CANNOT double. We lose the sequence.
                # That is a "Bust" for the session usually.
                pass

            # 3. Update Streak (if not betting)
            if current_bet == 0:
                if spin == 2: # Green
                    streak_count = 0
                    streak_color = None
                else:
                    if spin == streak_color:
                        streak_count += 1
                    else:
                        streak_count = 1
                        streak_color = spin
                
                if streak_count >= self.wait_streak:
                    current_bet = self.min_bet
                    # Bet is placed for NEXT spin
        
        return 'Incomplete', bankroll

    def run_monte_carlo(self, target_profit, n_sessions=1000):
        """
        Runs N sessions and returns statistics.
        """
        results = []
        for _ in range(n_sessions):
            res, val = self.simulate_session(target_profit)
            results.append(res)
            
        wins = results.count('Win')
        busts = results.count('Bust')
        
        return {
            'Target Profit': target_profit,
            'Win Rate': wins / n_sessions,
            'Bust Rate': busts / n_sessions,
            'EV': (wins * target_profit) - (busts * 1000) # Approx EV: Win Target vs Lose Max Bet (approx 1000 loss sequence)
            # Note: A bust sequence 10+20+40+80+160+320+640 = 1270 loss.
        }

# Optimized version using Numba would be better, but standard Python is fine for 10k sessions if logic is simple.
