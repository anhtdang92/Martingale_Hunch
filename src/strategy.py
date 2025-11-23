import pandas as pd

class MartingaleHunch:
    def __init__(self, min_bet=10, max_bet=1000, wait_streak=4):
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.wait_streak = wait_streak
        
    def run(self, spins_df):
        """
        Runs the strategy on a dataframe of spins.
        spins_df columns: ['number', 'color']
        """
        history = []
        bankroll = 0
        current_bet = 0
        bet_on = None # 'Red' or 'Black'
        streak_color = None
        streak_count = 0
        
        # Martingale state
        martingale_step = 0 # 0 means not betting
        
        for i, row in spins_df.iterrows():
            spin_color = row['color']
            
            # 1. Resolve existing bet if any
            step_profit = 0
            bet_amount = 0
            outcome = 'No Bet'
            
            if current_bet > 0:
                bet_amount = current_bet
                if spin_color == bet_on:
                    # Win
                    step_profit = current_bet
                    bankroll += step_profit
                    outcome = 'Win'
                    # Reset Martingale
                    current_bet = 0
                    bet_on = None
                    martingale_step = 0
                else:
                    # Loss (Opposite color or Green)
                    step_profit = -current_bet
                    bankroll += step_profit
                    outcome = 'Loss'
                    
                    # Martingale Progression
                    next_bet = current_bet * 2
                    if next_bet <= self.max_bet:
                        current_bet = next_bet
                        # Keep betting on the same color (Hunch: it HAS to flip eventually)
                        # Wait, user said: "wait for 4 blacks... bet it wont hit 5"
                        # So if 4 Blacks, bet Red.
                        # If Red wins, great.
                        # If Black hits (5 Blacks), we lost.
                        # Do we bet Red again? "so on and so forth until i win"
                        # Yes, standard Martingale is sticking to the bet until win.
                    else:
                        # Table limit hit - BUST
                        outcome = 'Bust'
                        current_bet = 0
                        bet_on = None
                        martingale_step = 0
            
            # 2. Update Streak (Only if not currently in a betting sequence? 
            # User said: "which i start over again by waiting for 4 red/blacks")
            # This implies we only look for a new streak AFTER the current betting sequence finishes.
            
            if current_bet == 0:
                if spin_color in ['Red', 'Black']:
                    if spin_color == streak_color:
                        streak_count += 1
                    else:
                        streak_color = spin_color
                        streak_count = 1
                else:
                    # Green resets streak
                    streak_color = None
                    streak_count = 0
                
                # 3. Check Trigger
                if streak_count >= self.wait_streak:
                    # Trigger Martingale
                    # Bet AGAINST the streak
                    bet_on = 'Black' if streak_color == 'Red' else 'Red'
                    current_bet = self.min_bet
                    martingale_step = 1
                    # Reset streak tracking so we don't trigger again immediately if we win/lose?
                    # Actually, if we enter betting mode, we ignore the streak counter until we reset.
            
            # Log state
            history.append({
                'spin_index': i,
                'spin_result': spin_color,
                'streak_count': streak_count if current_bet == 0 else 'Betting',
                'bet_amount': bet_amount,
                'bet_on': bet_on if bet_amount > 0 else None,
                'outcome': outcome,
                'profit': step_profit,
                'bankroll': bankroll
            })
            
        return pd.DataFrame(history)
