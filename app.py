import os
import pickle
import uuid

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import openai
from dash import Dash, Input, Output, State, callback, page_container
from flask import request

import utils
from constants import redis_instance

openai.api_key = os.getenv("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")

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_scripts=["https://cdn.plot.ly/plotly-2.18.2.min.js"],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="AI Data Insights",
    use_pages=True,
)


server = app.server


def layout():
    return dmc.MantineProvider(
        [
            utils.jumbotron(),
            page_container,
        ],
    )


app.layout = layout


@callback(
    Output("save-clip", "content"),
    Input("save-clip", "n_clicks"),
    State("current-charts", "children"),
    prevent_initial_call=True,
)
def copy_link_to_view(n, current):
    figure_id = str(uuid.uuid4())
    redis_instance.set(figure_id, pickle.dumps(current))
    return request.host_url[:-1] + app.get_relative_path(f"/view?layout={figure_id}")


if __name__ == "__main__":
    app.run(debug=True)
