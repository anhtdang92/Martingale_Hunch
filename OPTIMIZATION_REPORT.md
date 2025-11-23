# Session Optimization Report

## Goal
Find the optimal 'Take Profit' target for the Martingale Hunch strategy (Wait 5).
Simulated **2,000 sessions** per target.

## Results
| Target Profit | Win Rate | Bust Rate | Expected Value (EV) |
| :--- | :--- | :--- | :--- |
| $50 | 93.8% | 6.2% | $-32.50 |
| $100 | 89.5% | 10.4% | $-43.17 |
| $150 | 84.5% | 15.5% | $-70.10 |
| $200 | 78.1% | 21.9% | $-121.20 |
| $250 | 75.9% | 24.1% | $-115.56 |
| $300 | 70.2% | 29.8% | $-167.07 |
| $350 | 68.2% | 31.8% | $-165.16 |
| $400 | 63.8% | 36.1% | $-203.70 |
| $450 | 58.9% | 41.1% | $-257.78 |
| $500 | 54.8% | 45.2% | $-300.04 |

## Key Findings
1. **Best EV**: The mathematically 'least bad' option is to aim for **$50**.
   - Win Rate: **93.8%**
   - Expected Value: **$-32.50** per session.
2. **Risk/Reward**: As you increase the target profit, the Win Rate drops significantly.
   - Aiming for $50 has a high win rate, but one bust wipes out ~25 wins.
   - Aiming for $500 is nearly a coin flip (or worse) with a heavy penalty for failure.

## Recommendation
If you must play, **take small profits ($50-$100) and leave**. The longer you stay to reach a high target, the closer you get to the inevitable streak of 12 that busts you.
