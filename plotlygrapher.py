import plotly.graph_objects as go
import numpy as np
from PIL import Image
from sscws.sscws import SscWs

ssc = SscWs()

def genfig():
    global fig
    earth_radius = 6371
    u = np.linspace(0, 2 * np.pi, 1000)
    v = np.linspace(0, np.pi, 1000)
    x0 = earth_radius * np.outer(np.cos(u), np.sin(v))
    y0 = earth_radius * np.outer(np.sin(u), np.sin(v))
    z0 = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))

    earth_img = Image.open("earth_texture.jpg").resize(x0.shape)
    earth_texture = np.array(earth_img)
    if earth_texture.ndim == 3:
        earth_texture = earth_texture.mean(axis=2)
    earth_texture = (earth_texture - earth_texture.min()) / (earth_texture.max() - earth_texture.min())

    fig = go.Figure(
        data=[go.Surface(
            x=x0,
            y=y0,
            z=z0,
            surfacecolor=earth_texture,
            opacity=0.85,
            colorscale=[[0, "rgb(0,40,120)"], [1, "rgb(0,120,220)"]],
            showscale=False,
            name="Earth",
            hoverinfo="skip",
        )],
    )

def gentrajectory(cxc, cyc, czc, ctimes, name, showiss):
    global fig
    ctimelabels = np.array([actime.strftime("%B %d, %Y %I:%M:%S %p") for actime in ctimes])

    if showiss:
        starttime = ctimes[0]
        endtime = ctimes[-1]
        result = ssc.get_locations(["iss"], [starttime.strftime("%Y-%m-%dT%H:%M:%SZ"), endtime.strftime("%Y-%m-%dT%H:%M:%SZ")])
        data = result["Data"][0]
        times = np.array([onetime.strftime("%B %d, %Y %I:%M:%S %p") for onetime in data["Time"]])
        coords = data["Coordinates"][0]

        fig.add_trace(go.Scatter3d(
            x=coords["X"],
            y=coords["Y"],
            z=coords["Z"],
            mode="lines+markers",
            line=dict(color="orange", width=5),
            marker=dict(size=4, color="yellow", symbol="circle"),
            name="ISS Orbit",
            text=times,
            hovertemplate="Time: %{text}<br>X: %{x}<br>Y: %{y}<br>Z: %{z}"
        ))

    fig.add_trace(go.Scatter3d(
        x=cxc,
        y=cyc,
        z=czc,
        mode="lines+markers",
        line=dict(color="lime", width=3, dash="dash"),
        marker=dict(size=4, color="lime", symbol="circle"),
        name=name,
        text=ctimelabels,
        hovertemplate="Time: %{text}<br>X: %{x}<br>Y: %{y}<br>Z: %{z}"
    ))

def stars(randomseed, numstars, spread):
    global fig
    np.random.seed(randomseed)
    star_x = np.random.uniform(-spread, spread, numstars)
    star_y = np.random.uniform(-spread, spread, numstars)
    star_z = np.random.uniform(-spread, spread, numstars)
    fig.add_trace(go.Scatter3d(
        x=star_x,
        y=star_y,
        z=star_z,
        mode="markers",
        marker=dict(size=2, color="white", opacity=0.7),
        name="Stars",
        hoverinfo="skip",
        showlegend=False
    ))

def showorbit():
    global fig
    fig.update_layout(
        title="Custom Satelite Orbit Visualization",
        scene=dict(
            xaxis_title="X (km)",
            yaxis_title="Y (km)",
            zaxis_title="Z (km)",
            bgcolor="rgb(5,5,20)",
            xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
        ),
        paper_bgcolor="rgb(5,5,20)",
        plot_bgcolor="rgb(5,5,20)",
        showlegend=True,
        font=dict(family="Arial", size=16, color="white"),
    )

    fig.show()
