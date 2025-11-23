import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Analyzer:
    def __init__(self, history_df):
        self.history = history_df

    def calculate_metrics(self):
        """Calculates key performance metrics."""
        total_spins = len(self.history)
        final_bankroll = self.history['bankroll'].iloc[-1]
        min_bankroll = self.history['bankroll'].min()
        max_bankroll = self.history['bankroll'].max()
        
        total_bets = self.history[self.history['bet_amount'] > 0].shape[0]
        wins = self.history[self.history['outcome'] == 'Win'].shape[0]
        losses = self.history[self.history['outcome'] == 'Loss'].shape[0]
        busts = self.history[self.history['outcome'] == 'Bust'].shape[0]
        
        win_rate = (wins / total_bets * 100) if total_bets > 0 else 0
        
        return {
            'Total Spins': total_spins,
            'Final Bankroll': final_bankroll,
            'Max Drawdown': min_bankroll,
            'Peak Bankroll': max_bankroll,
            'Total Bets Placed': total_bets,
            'Win Rate': win_rate,
            'Busts (Table Limit Hits)': busts
        }

    def plot_bankroll(self, save_path=None, labels=None):
        """
        Plots the bankroll over time.
        If self.history is a list of DataFrames, plots multiple lines.
        """
        plt.figure(figsize=(12, 6))
        
        if isinstance(self.history, dict):
            # Comparative Plot
            for label, df in self.history.items():
                sns.lineplot(data=df, x='spin_index', y='bankroll', label=label)
        else:
            # Single Plot
            sns.lineplot(data=self.history, x='spin_index', y='bankroll')
            
        plt.title('Bankroll Over Time - Strategy Comparison')
        plt.xlabel('Spin Number')
        plt.ylabel('Bankroll ($)')
        plt.axhline(0, color='red', linestyle='--')
        plt.legend()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()
