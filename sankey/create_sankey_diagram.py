import pandas as pd
import plotly.graph_objects as go

# Load the data
df_links = pd.read_csv("links.csv")
df_core_service = pd.read_csv("core_service2.csv")
df_law = pd.read_csv("law2.csv")

# Create mappings for labels and details
label_map = pd.concat([df_core_service, df_law]).set_index('key').to_dict()['label']
detail_map = pd.concat([df_core_service, df_law]).set_index('key').to_dict()['detail']

# Assign colors to core services
core_service_colors = {
    "cs-01": "#588b8b",
    "cs-02": "#f0ead2",
    "cs-03": "#ffd5c2",
    "cs-04": "#f28f3b",
    "cs-05": "#c8553d",
    "cs-06": "#2d3047",
    "cs-07": "#93b7be"
}

# Extract unique nodes
unique_nodes_df = pd.DataFrame({'key': list(set(df_links['source']).union(set(df_links['target'])))})
unique_nodes_df['label'] = unique_nodes_df['key'].map(label_map)
unique_nodes_df['detail'] = unique_nodes_df['key'].map(detail_map)
unique_nodes_df["color"] = unique_nodes_df["key"].map(lambda x: core_service_colors.get(x, "#531942"))

# Create a mapping from node name to index
node_map = {node: i for i, node in enumerate(unique_nodes_df['key'])}

# Convert source and target labels to indices
df_links['source_index'] = df_links['source'].map(node_map)
df_links['target_index'] = df_links['target'].map(node_map)

# Assign colors to links based on the target core service
df_links["color"] = df_links["target"].map(lambda x: core_service_colors.get(x, "gray"))

# Create Sankey diagram using Plotly
sankey_figure = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=unique_nodes_df['label'].tolist(),
        customdata=unique_nodes_df['detail'].tolist(),
        hovertemplate="%{label}<br>%{customdata}",
        color=unique_nodes_df["color"].tolist(),
    ),
    link=dict(
        source=df_links['source_index'].tolist(),
        target=df_links['target_index'].tolist(),
        value=[1] * len(df_links),  # Assume equal weight for all links
        color=df_links["color"].tolist(),  # Apply colors to links
    )
))

# Set layout
sankey_figure.update_layout(title_text="ความเชื่อมโยงเกี่ยวกับ ดำเนินการหลักด้านสารสนเทศของ สทนช." ,
                            font_size=14 ,
                            width=1000,  # กำหนดความกว้าง
                            height=1200   # กำหนดความสูง
                           )

# Show the diagram
sankey_figure.show()



# บันทึกเป็นไฟล์ HTML
html_file_path = "./network_graph.html"
sankey_figure.write_html(html_file_path)