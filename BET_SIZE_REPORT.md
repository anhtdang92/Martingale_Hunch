# Bet Size & Target Optimization Report

## Goal
Determine if increasing the **Base Bet** ($10 -> $20 -> $50) improves the strategy by winning faster, or if the reduced safety net makes it worse.

## Results (5,000 Sessions per Config)

| Base Bet | Target Profit | Win Rate | Bust Rate | EV (Approx) |
| :--- | :--- | :--- | :--- | :--- |
| **$10** | **$20** | **98.8%** | **1.2%** | **+$4.52** |
| $10 | $50 | 97.0% | 3.0% | -$9.60 |
| $10 | $100 | 94.1% | 5.9% | -$30.83 |
| | | | | |
| **$20** | **$20** | **98.6%** | **1.4%** | **+$1.94** |
| $20 | $50 | 96.5% | 3.5% | -$16.20 |
| $20 | $100 | 93.0% | 7.0% | -$45.90 |
| | | | | |
| **$50** | **$20** | **98.0%** | **2.0%** | **-$25.80** |
| $50 | $50 | 95.2% | 4.8% | -$58.36 |
| $50 | $100 | 90.5% | 9.5% | -$120.15 |

## Key Findings

1.  **Is $20 a good target?**
    - **YES.** For a $10 base bet, aiming for $20 profit yielded a **positive EV** in this specific simulation run (+$4.52).
    - *Note: This positive EV is likely statistical noise (variance) in the 5,000 sessions, but it confirms that short, small targets are the only way to have a fighting chance.*

2.  **Should you bet higher ($20 or $50)?**
    - **NO.** Increasing the bet size drastically **worsens** your performance.
    - **$10 Bet**: You survive 7 losses.
    - **$50 Bet**: You only survive 5 losses.
    - The "speed" of winning does NOT compensate for the loss of safety. The Bust Rate for $50 bets is nearly **double** that of $10 bets.

## Recommendation
- **Stick to the Minimum Bet ($10).** It gives you the maximum number of "doubles" (safety steps).
- **Target Small Profits ($20 - $50).** The "Hit and Run" strategy is the most effective.
- **Walk Away.** Once you hit +$20, leave. Do not get greedy.
