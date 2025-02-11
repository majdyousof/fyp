import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from GTFSfunctions import getRealTimePositions, getShapeCSV

# Set Streamlit page configuration to wide mode
st.set_page_config(page_title="Real-Time Train Positions", layout="wide")

# Function to plot data on a map
def plotRealTimePositions(GTFSVehiclePosition: pd.DataFrame, routeShapes: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    # Define colors for each shape_id
    colors = {
        'RED': '#E31837',
        'GREEN': '#00A94F',
        'YELLOW': '#FFD200',
        'BLUE': '#0076C0',
        'SILVER': '#A1A2A1',
        'ORANGE': '#F7941E'
    }

    # Plot route shapes
    for shape_id in routeShapes['shape_id'].unique():
        shape_data = routeShapes[routeShapes['shape_id'] == shape_id]
        fig.add_trace(go.Scattermap(
            lat=shape_data['shape_pt_lat'], 
            lon=shape_data['shape_pt_lon'], 
            mode='lines', 
            name=shape_id,
            line=dict(color=colors[shape_id], width=4)
        ))

    # Plot vehicle positions

    fig.add_trace(go.Scattermap(
        lat=GTFSVehiclePosition['latitude'],
        lon=GTFSVehiclePosition['longitude'],
        mode='markers',
        marker=dict(size=10, color='mintcream', opacity=0.8),
        name='Vehicle Positions'
    ))

    fig.update_layout(
        map=dict(
            style='carto-darkmatter',
            center=dict(lat=38.95, lon=-77.15),
            zoom=9.3,
        ),
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    
    return fig

# Main Streamlit app
def main():
    st.title("Real-Time Train Positions")
    
    # Load API key
    with open('key.txt') as f:
        apiKey = f.read().strip()
    
    headers = {'api_key': apiKey}
    url = 'https://api.wmata.com/gtfs/rail-gtfsrt-vehiclepositions.pb'

    # Load shapes data
    routeShapes = getShapeCSV()

    # Refresh button
    if st.button("Refresh Data"):
        GTFSVehiclePosition = getRealTimePositions(url, headers)
        
        # Plot data on map
        fig = plotRealTimePositions(GTFSVehiclePosition, routeShapes)
        
        # Display map in Streamlit
        st.plotly_chart(fig)

if __name__ == '__main__':
    main()


# # Main Streamlit app auto refresh
# def main():
#     st.title("Real-Time Train Positions")
    
#     # Load API key
#     with open('key.txt') as f:
#         apiKey = f.read().strip()
    
#     headers = {'api_key': apiKey}
#     url = 'https://api.wmata.com/gtfs/rail-gtfsrt-vehiclepositions.pb'

#     # Load shapes data
#     routeShapes = getShapeCSV()

#     # Create a placeholder for the plot
#     plot_placeholder = st.empty()

#     # Continuous update loop
#     while True:
#         # Fetch real-time data
#         GTFSVehiclePosition = getRealTimePositions(url, headers)
        
#         # Plot data on map
#         fig = plotRealTimePositions(GTFSVehiclePosition, routeShapes)
        
#         # Update the plot in the placeholder
#         plot_placeholder.plotly_chart(fig)
        
#         # Wait for 10 seconds before updating again
#         time.sleep(10)

# if __name__ == '__main__':
#     main()
