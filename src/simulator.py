import random
import pandas as pd

class RouletteWheel:
    def __init__(self):
        # American Roulette Setup
        # 0, 00 are Green
        # 1-36 are Red/Black
        self.numbers = ['0', '00'] + [str(i) for i in range(1, 37)]
        self.colors = self._initialize_colors()

    def _initialize_colors(self):
        # Standard American Roulette Colors
        # Red numbers: 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
        # Black numbers: 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35
        red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        
        colors = {}
        for num in self.numbers:
            if num in ['0', '00']:
                colors[num] = 'Green'
            elif int(num) in red_numbers:
                colors[num] = 'Red'
            else:
                colors[num] = 'Black'
        return colors

    def spin(self):
        """Simulates a single spin."""
        result = random.choice(self.numbers)
        return {
            'number': result,
            'color': self.colors[result]
        }

    def generate_spins(self, n_spins):
        """Generates a list of n spins."""
        spins = [self.spin() for _ in range(n_spins)]
        return pd.DataFrame(spins)

if __name__ == "__main__":
    # Quick test
    wheel = RouletteWheel()
    print(wheel.generate_spins(10))
