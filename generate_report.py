import pandas as pd
import re

try:
    # Read the raw output (it was printed to stdout, so it might be messy if we read the file directly)
    # Actually, let's just run the optimizer again and get the dataframe directly in this script
    from src.optimizer import Optimizer
    
    opt = Optimizer(wait_streak=5)
    df = opt.optimize(min_target=50, max_target=500, step=50, n_sessions=2000) # 2k sessions for speed/accuracy balance
    
    # Generate Markdown
    report = "# Session Optimization Report\n\n"
    report += "## Goal\n"
    report += "Find the optimal 'Take Profit' target for the Martingale Hunch strategy (Wait 5).\n"
    report += "Simulated **2,000 sessions** per target.\n\n"
    
    report += "## Results\n"
    report += "| Target Profit | Win Rate | Bust Rate | Expected Value (EV) |\n"
    report += "| :--- | :--- | :--- | :--- |\n"
    
    for i, row in df.iterrows():
        report += f"| ${row['Target Profit']:.0f} | {row['Win Rate']:.1%} | {row['Bust Rate']:.1%} | ${row['Expected Value']:.2f} |\n"
        
    report += "\n## Key Findings\n"
    best_ev = df.loc[df['Expected Value'].idxmax()]
    report += f"1. **Best EV**: The mathematically 'least bad' option is to aim for **${best_ev['Target Profit']:.0f}**.\n"
    report += f"   - Win Rate: **{best_ev['Win Rate']:.1%}**\n"
    report += f"   - Expected Value: **${best_ev['Expected Value']:.2f}** per session.\n"
    
    report += "2. **Risk/Reward**: As you increase the target profit, the Win Rate drops significantly.\n"
    report += "   - Aiming for $50 has a high win rate, but one bust wipes out ~25 wins.\n"
    report += "   - Aiming for $500 is nearly a coin flip (or worse) with a heavy penalty for failure.\n"
    
    report += "\n## Recommendation\n"
    report += "If you must play, **take small profits ($50-$100) and leave**. The longer you stay to reach a high target, the closer you get to the inevitable streak of 12 that busts you.\n"
    
    with open('OPTIMIZATION_REPORT.md', 'w') as f:
        f.write(report)
        
    print("Report generated successfully.")
    
except Exception as e:
    print(f"Error: {e}")
