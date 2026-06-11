"""App.py is the entry point for our project. It wires the page layout from pages.home.create_layout and registeres callbacks through callbacks.register_callback."""

import warnings
warnings.filterwarnings("ignore", module=r"pyagrum\.lib\.notebook") # Ignore Ipython warning
from dash import Dash
import dash_mantine_components as dmc
from pages.home import create_layout
from callbacks import register_callbacks

# manually select rendering
import matplotlib
matplotlib.use("Agg")

app = Dash(__name__)

# register all callbacks
register_callbacks(app)
app.layout = dmc.MantineProvider(create_layout())

if __name__ == "__main__":
    app.run(debug=True) # Before submitting it to the client or when the app is hosted this should be set to false.