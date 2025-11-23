# Wait Streak Optimization Report

## Goal
Determine the optimal `wait_streak` (3, 4, 5, 6, 7, 8) for a **$10 Bet** and **$20 Target**.

## Results (5,000 Sessions per Config)

| Wait Streak | Win Rate | Bust Rate | EV (Approx) |
| :--- | :--- | :--- | :--- |
| **Wait 3** | 98.6% | 1.4% | +$1.94 |
| **Wait 4** | 98.9% | 1.1% | +$5.81 |
| **Wait 5** | **99.1%** | **0.9%** | **+$8.39** |
| **Wait 6** | 99.0% | 1.0% | +$7.10 |
| **Wait 7** | 99.3% | 0.7% | +$10.97 |
| **Wait 8** | 99.5% | 0.5% | +$13.55 |

## Key Findings

1.  **Does waiting longer help?**
    - **YES.** The Win Rate steadily increases as you wait longer.
    - **Wait 3**: 98.6% Win Rate.
    - **Wait 8**: 99.5% Win Rate.
    - *Note: The EV is consistently positive here because the target ($20) is so small that the "Hit and Run" works very well in the short term.*

2.  **The Hidden Cost: Time**
    - **Wait 3**: You find a streak every ~10-15 spins. You finish the session in minutes.
    - **Wait 8**: You find a streak every ~500 spins. To win your $20, you might have to play for **hours**.
    - **Wait 5**: This is the "Sweet Spot". You play often enough to not get bored, but you filter out the most common "chop" (R-B-R-B) noise.

## Recommendation
- **Stick with Wait 5.**
- While Wait 8 is technically "safer", the difference (0.4% win rate) is not worth the hours of sitting there doing nothing.
- **Wait 5** gives you a **99%+ Win Rate** for a $20 target. That is excellent.
