# Martingale Hunch Strategy - Simulation Report

## Strategy Overview
- **Strategy**: Martingale Hunch
- **Logic**: Wait for a streak of 4 (Red/Black), then bet against it.
- **Progression**: Martingale (Double bet after loss).
- **Parameters**:
    - Min Bet: $10
    - Max Bet: $1000
    - Wait Streak: 4

## Simulation Results (10,000 Spins)
The simulation was run over 10,000 spins of American Roulette (0, 00).

| Metric | Value |
| :--- | :--- |
| **Total Spins** | 10,000 |
| **Final Bankroll** | -$1,050 |
| **Peak Bankroll** | +$90 |
| **Max Drawdown** | -$3,220 |
| **Total Busts** | 5 |

> [!WARNING]
> **Analysis**: The strategy failed to generate a profit over the long run.
> The "Bust" event (hitting the $1000 table limit) occurred **5 times**.
> Each bust represents a significant loss that wipes out many small wins.
>
> The "Hunch" (waiting for 4) reduces the frequency of betting, but it does not change the statistical probability of the next spin. The wheel has no memory.

## Visualizations
### Bankroll Over Time
![Bankroll Chart](output/bankroll_chart.png)

## Conclusion
While the strategy can generate small profits in the short term (as seen by the Peak Bankroll of $90), the risk of hitting the table limit (Bust) is statistically significant and catastrophic for the bankroll when it happens. The presence of 0 and 00 ensures the house always has an edge.
