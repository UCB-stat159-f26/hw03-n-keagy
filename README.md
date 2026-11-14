# HW3: Tennis Career Package

This package extracts career match data from Tennis Abstract, and creates a scatterplot for a select player, mimicking the scatterplot of Serena Williams' career matches from the NYT. The x-axis shows the player's age, and the y-axis shows the difference between the player's and opponent's age. Blue points are wins, and purple points are losses.

## Install

From the project folder:

```sh
python -m pip install .
```

Or from GitHub (after package files are pushed):

```sh
python -m pip install git+https://github.com/UCB-stat159-f26/hw03-n-keagy.git
```

## Use

```python
import matplotlib.pyplot as plt
from tennis_career import get_matches, plot_matches

serena = get_matches("serena williams")
plot_matches(serena)
plt.show()

rafa = get_matches("Rafael Nadal")
plot_matches(rafa)
plt.show()
```

`get_matches()` returns a cleaned data frame.
`"Serena Williams"` and `"SerenaWilliams"` both work.
Invalid player names raise an error.
`plot_matches()` takes the data frame and returns the plot axes.
Ages are approximate, since they use tournament dates.

## Tests

From the project folder:

```sh
python -m unittest discover -s tests
```

Tests use the specified female and male sample data.