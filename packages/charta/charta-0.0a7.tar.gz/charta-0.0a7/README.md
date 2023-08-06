# charta

A package for building realtime dashboards. Originally designed for monitoring the progress of optimization problems.

## Installation
charta is available on PyPi. You can

```
pip install charta
```

## Quickstart
Run the server in the terminal with:
```
charta-server
```

Then open your browser to [localhost:8889](http://localhost:8889/).
The following code should draw a sine wave to the dashboard.

```python
import numpy as np
from charta import Dashboard, Series, Chart

# Create some data.
x = np.linspace(0, np.pi)
y = np.sin(x)

# Get a reference to the dashboard.
dash = Dashboard.default()

# Add data to the dashboard.
dash.add_series(Series("x", x))
dash.add_series(Series("y", y))
dash.add_chart(Chart("chart", ["x", "y"]))
```
