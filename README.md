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

## Reflection

This assignment came with a lot of challenges, as the last few homeworks were very specific and targeted. This assignment took the work from previous assignments and generalized it so any inputted player name, which was much more complicated than I initially thought it would be. It was helpful to distinctly separate downloading, cleaning, and plotting functions, to keep every part of the pipeline distinct and organized. An added issue was the difference in male and female data files, so there had to be separate code for extracting age from birthdays, versus just given age. I really wanted to keep all the code as simple and short as possible, and it took a lot of iterations to simplify the code. My first few attempts ended up with really complex, convoluted code, and it took a few attempts to find cleaner, more direct ways to organize my code. Overall, the assingment was difficult and took a lot of effort, but I feel much more confident in my general repo organization, and my coding approach. I also tried to improve on previous assingments, where I've lost points for not including enough commits.  