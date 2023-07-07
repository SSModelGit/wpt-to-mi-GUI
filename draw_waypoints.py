from flask import Flask, render_template_string

import folium
from folium.plugins import Draw

app = Flask(__name__)

@app.route("/")
def iframe():
    """Embed a map as an iframe on a page."""
#     m = folium.Map(location=[41.759775, -70.621177],
#                    zoom_start=14,
#                    tiles='Stamen Terrain')
    m = folium.Map(location=[41.759775, -70.621177],
                   zoom_start=13)
    Draw(export=True,
         filename="my_plan.geojson",
         position="topleft",
         draw_options={"polyline": {"allowIntersection": False}},
         edit_options={"poly": {"allowIntersection": False}}).add_to(m)

    # set the iframe width and height
    m.get_root().width = "1024px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()

    return render_template_string(
        """
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                    <h1>Draw Markers In Desired Order</h1>
                    {{ iframe|safe }}
                </body>
            </html>
        """,
        iframe=iframe,
    )


if __name__ == "__main__":
    app.run(debug=True)