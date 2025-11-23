import numpy as np

def count_streaks(n_spins=1_000_000):
    print(f"Simulating {n_spins:,} spins...")
    
    # 0: Red, 1: Black, 2: Green
    p_red = 18/38
    p_black = 18/38
    p_green = 2/38
    
    spins = np.random.choice([0, 1, 2], size=n_spins, p=[p_red, p_black, p_green])
    
    # Find streaks
    # We only care about Red (0) or Black (1) streaks. Green breaks them.
    
    current_streak = 0
    current_color = None
    
    streak_counts = {} # Length -> Count
    
    for spin in spins:
        if spin == 2: # Green
            current_streak = 0
            current_color = None
            continue
            
        if spin == current_color:
            current_streak += 1
        else:
            # Streak ended (or started)
            # Record the streak we just finished (if any)
            if current_streak > 0:
                streak_counts[current_streak] = streak_counts.get(current_streak, 0) + 1
            
            current_streak = 1
            current_color = spin
            
        # Also record "active" streaks? 
        # No, usually we count completed streaks. 
        # BUT, for the user, they want to know "Did it hit 12?".
        # If I have a streak of 15, that implies it WAS a streak of 12 at some point.
        # So we should count how many times we REACHED N.
    
    # Let's re-scan to count "Times we reached streak N"
    reached_counts = {}
    
    current_streak = 0
    current_color = None
    
    for spin in spins:
        if spin == 2:
            current_streak = 0
            current_color = None
        elif spin == current_color:
            current_streak += 1
        else:
            current_streak = 1
            current_color = spin
            
        if current_streak > 0:
            reached_counts[current_streak] = reached_counts.get(current_streak, 0) + 1

    print("\n--- Frequency of Streaks (in 1 Million Spins) ---")
    print(f"Streak of 5+:  {reached_counts.get(5, 0):,} times")
    print(f"Streak of 8+:  {reached_counts.get(8, 0):,} times")
    print(f"Streak of 10+: {reached_counts.get(10, 0):,} times")
    print(f"Streak of 12+: {reached_counts.get(12, 0):,} times (THIS BUSTS YOU)")
    print(f"Streak of 15+: {reached_counts.get(15, 0):,} times")
    print(f"Streak of 20+: {reached_counts.get(20, 0):,} times")

if __name__ == "__main__":
    count_streaks()
