from dash import Dash
import dash_mantine_components as dmc
from pages.home import create_layout


app = Dash(__name__)

app.layout = dmc.MantineProvider(create_layout())


if __name__ == "__main__":
    app.run(debug=True)