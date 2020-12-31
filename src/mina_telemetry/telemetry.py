import json
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import requests


def load_telemetry() -> list:
    with open("/Users/Francesco/mina-telemetry.json", "r") as f:
        return [json.loads(line) for line in f]

def get_node_data(ip: str) -> dict:
    ip_data = json.loads(requests.get(f"http://api.ipstack.com/{ip}?access_key={os.getenv('ACCESS_KEY')}&format=1").text)
    return {"lat": ip_data["latitude"], "lon": ip_data["longitude"]}

def construct_geo_fig(unique_edges: list, node_data: dict) -> go.Figure:
    edges_lon = [coord for coords in
                 [[node_data[src]["lon"], None, node_data[dst]["lon"]] for (src, dst) in unique_edges] for coord in
                 coords]
    edges_lat = [coord for coords in
                 [[node_data[src]["lat"], None, node_data[dst]["lat"]] for (src, dst) in unique_edges] for coord in
                 coords]

    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            locationmode='ISO-3',
            lon=edges_lon,
            lat=edges_lat,
            mode='lines',
            line=dict(width=0.5, color='red'),
            opacity=0.1
        )
    )
    fig.add_trace(go.Scattergeo(
        locationmode='ISO-3',
        lon=[node["lon"] for node in node_data.values()],
        lat=[node["lat"] for node in node_data.values()],
        hoverinfo='text',
        text=[node for node in node_data],
        mode='markers',
        marker=dict(
            size=5,
            color='rgb(255, 0, 0)',
            line=dict(
                width=3,
                color='rgba(68, 68, 68, 0)'
            )
        )))
    fig.update_layout(
        title_text='Mina Network',
        showlegend=False,
        geo=go.layout.Geo(
            showland=True,
            showcountries=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
        ),
        mapbox_style="stamen-terrain",
        height=1400,
    )
    return fig

def create_dash_app(fig: go.Figure) -> dash.Dash:
    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])
    return app

def run() -> dash.Dash:
    telemetry = load_telemetry()
    raw_edges = list(set([(node["node_ip_addr"], peer["host"]) for node in telemetry for peer in node["peers"]]))
    raw_nodes = list(set([node for edge in raw_edges for node in edge]))
    node_data = {node: get_node_data(node) for node in raw_nodes}
    unique_edges = [(x, y) for (x, y) in [(x, y) for (x, y) in raw_edges] + [(y, x) for (x, y) in raw_edges] if x < y]
    geo_fig =  construct_geo_fig(unique_edges, node_data)
    dash_app = create_dash_app(geo_fig)
    return dash_app

server = run().server

# Run ACCESS_KEY="your access key" python telemetry.py
if __name__ == "__main__":
    app = run()
    app.run_server()