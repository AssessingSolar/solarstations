import folium

LEGEND_TEMPLATE = """
<div style="position:fixed;
     top: 10px; 
     left: 10px; 
     width: 120px; 
     height: {height}px; 
     border:2px solid grey; 
     z-index: 9999;
     background-color:#f2efe9;
     font-size:14px;">
     &nbsp;<b>Station markers</b><br>
     {entries}
</div>"""

# this uses the same kind of SVG symbol as folium's CircleMarker in the maps
MARKER_TEMPLATE = """
&nbsp;<svg style="width: 1.2em; height: 1.2em; vertical-align: middle"><g><path stroke="{color}" stroke-opacity="1" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="{color}" fill-opacity="0.2" fill-rule="evenodd" d="M2,7a5,5 0 1,0 10,0 a5,5 0 1,0 -10,0 " aria-describedby="leaflet-tooltip-1781"></path></g></svg>&nbsp;{label}<br>
"""

def make_legend(labels, colors):
    """
    Make a folium Element for a map legend.

    Parameters
    ----------
    labels : list
        The text to display for each legend entry
    colors : list
        Marker colors for each legend entry
    """
    n_entries = len(labels)
    height = 25 + 20 * n_entries  # 25 px for header, 20 for each entry
    entries = "\n".join([
        MARKER_TEMPLATE.format(label=label, color=color)
        for label, color in zip(labels, colors)
    ])
    legend_html = LEGEND_TEMPLATE.format(height=height, entries=entries)
    return folium.Element(legend_html)
