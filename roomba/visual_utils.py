import numpy as np

# For visualization
import plotly.graph_objects as go
import ipywidgets as widgets
from IPython.display import display


def visualize_grid(grid):
    """
    Visualizes the grid
    """
    # Create a meshgrid for the plot
    x = np.arange(grid.shape[0])
    y = np.arange(grid.shape[1])
    x, y = np.meshgrid(x, y)

    # Create a surface plot using Plotly
    fig = go.Figure(data=[go.Surface(z=grid, x=x, y=y)])

    # Set plot layout
    fig.update_layout(
        title="Random Heights Surface Plot",
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Height'
        )
    )

    # Show the plot
    fig.show()


def visualize_path(potential_grid: np.ndarray, path: list, fig_size: int = 600):
    """
    Visualizes the climber's path withs an interactive slider
    to move through the path points. The figure is sized to be square.
    """
    
    # Create the initial heatmap for the potential grid
    heatmap = go.Heatmap(z=potential_grid, colorscale='Viridis', showscale=True)

    # Create the initial figure with the heatmap
    fig = go.Figure(data=[heatmap])

    # Customize layout to ensure a square figure
    fig.update_layout(
        title="Climber's Path on Potential Grid",
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate",
        yaxis=dict(autorange='reversed'),  # Reverse y-axis to match grid orientation
        width=fig_size,  # Set the figure width
        height=fig_size  # Set the figure height to match width for square shape
    )

    # Create a scatter trace for the path (initially empty)
    path_trace = go.Scatter(
        x=[], 
        y=[], 
        mode='lines+markers',
        line=dict(color='red', width=2),
        marker=dict(size=8, color='red'),
        name="Climber's Path"
    )
    fig.add_trace(path_trace)

    # Display the figure
    fig_widget = go.FigureWidget(fig)

    # Define a function to update the path trace based on slider value
    def update_path(step):
        # Get the current path up to the slider's step
        if step > 0:
            current_path = path[:step]
            x_coords, y_coords = zip(*current_path)
            with fig_widget.batch_update():
                fig_widget.data[1].x = y_coords
                fig_widget.data[1].y = x_coords
        else:
            with fig_widget.batch_update():
                fig_widget.data[1].x = []
                fig_widget.data[1].y = []

    # Create a slider for selecting the step in the path
    slider = widgets.IntSlider(value=0, min=0, max=len(path), step=1, description="Step")

    # Update the figure when the slider value changes
    widgets.interactive(update_path, step=slider)

    # Display the slider and the figure
    display(slider, fig_widget)