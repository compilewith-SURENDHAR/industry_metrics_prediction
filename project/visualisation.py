import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import matplotlib.animation as animation
import numpy as np

def plot_energy_usage_2(day, load_type, df=None):
    if df is None:  
        df = pd.read_csv("final_data.csv")
    # Filter based on user inputs
    load_mapping = {"Light": 0, "Medium": 1, "Heavy": 2}
    load_type_encoded = load_mapping.get(load_type)
    df = df[df[f"Day_Of_Week_{day}"] == 1]  
    if load_type != "Any":
        df = df[df["Load_Type"] == load_type_encoded]  

    # Plot line graph
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x="Hour", y="Usage_kWh", marker="o", ci=None)

    plt.xlabel("Hour of the Day")
    plt.ylabel("Energy Usage (kWh)")
    plt.title("Hourly Energy Usage Trend")
    plt.grid(False)

    # Display in Streamlit
    st.pyplot(plt)



def plot_energy_usage_1(day, df = None):
    if df is None:  
        df = pd.read_csv("final_data.csv")
    # Filter based on selected day
    if day != "Any":
        df = df[df[f"Day_Of_Week_{day}"] == 1]  

    # Plot line graph for all load types
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x="Hour", y="Usage_kWh", hue="Load_Type", marker="o", ci=None)

    plt.xlabel("Hour of the Day")
    plt.ylabel("Energy Usage (kWh)")
    plt.title(f"Hourly Energy Usage Trend for {day}")
    plt.legend(title="Load Type")
    plt.grid(False)

    # Display in Streamlit
    st.pyplot(plt)
    

def plot_energy_usage(df=None):
    if df is None:  
        df = pd.read_csv("final_data.csv")
    # Plot line graph for all days and load types
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="Hour", y="Usage_kWh",  style="WeekStatus", marker="o", ci=None)

    plt.xlabel("Hour of the Day")
    plt.ylabel("Energy Usage (kWh)")
    plt.title("Overall Hourly Energy Usage Trend")
    plt.legend(title="week status")
    plt.grid(False)

    # Display in Streamlit
    st.pyplot(plt)
    

def plot_energy_trend_for_load(load_type):
    # Load dataset
    data = pd.read_csv("final_data.csv")

    # Map Load Type
    load_mapping = {"Light": 0, "Medium": 1, "Heavy": 2}
    load_type_encoded = load_mapping.get(load_type)

    if load_type_encoded is None:
        st.write(f"Invalid load type: {load_type}")
        return  

    # Filter for selected Load Type
    load_data = data[data['Load_Type'] == load_type_encoded]

    # Check if filtering is correct
    if load_data.empty:
        st.write("No data found for the selected load type!")
        return

    # Aggregate energy usage by NSM
    load_data = load_data.groupby('NSM', as_index=False)['Usage_kWh'].mean()

    # Convert NSM to HH:MM
    load_data['Time'] = pd.to_datetime(load_data['NSM'], unit='s').dt.strftime('%H:%M')

    # Debugging: Print first few rows
    print(load_data.head())  

    # Plot
    plt.figure(figsize=(14, 6))
    plt.fill_between(load_data['NSM'], load_data['Usage_kWh'], color='skyblue', alpha=0.4)
    plt.plot(load_data['NSM'], load_data['Usage_kWh'], color='b', alpha=0.6)

    # Labels
    plt.title(f'Energy Consumption Trend for {load_type}')
    plt.xlabel('Time of Day (HH:MM)')
    plt.ylabel('Average Energy Consumption (kWh)')

    # Set X-axis ticks
    tick_interval = 3600  # 1-hour intervals
    tick_positions = load_data['NSM'][::4]  # Pick every 4th value for better readability
    tick_labels = load_data['Time'][::4]

    plt.xticks(tick_positions, tick_labels, rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Show in Streamlit
    st.pyplot(plt)


    
def plot_animated_energy_trend_by_load():
    
    data = pd.read_csv("final_data.csv")  

    # Aggregate energy usage
    load_data = data.groupby(['NSM', 'Load_Type'], as_index=False)['Usage_kWh'].mean()
    load_data['Time'] = pd.to_datetime(load_data['NSM'], unit='s').dt.strftime('%H:%M')
    
    # Unique loads
    unique_loads = load_data['Load_Type'].unique()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_loads)))
    color_dict = dict(zip(unique_loads, colors))
    lines = {load: ax.plot([], [], alpha=0.8, color=color_dict[load], label=f'Load: {load}')[0] for load in unique_loads}

    def init():
        ax.set_xlim(0, 86400)
        ax.set_ylim(0, load_data['Usage_kWh'].max() * 1.1)
        return lines.values()

    def animate(frame):
        current_nsm = sorted(load_data['NSM'].unique())[frame]
        data_to_plot = load_data[load_data['NSM'] <= current_nsm]
        
        for load in unique_loads:
            subset = data_to_plot[data_to_plot['Load_Type'] == load]
            lines[load].set_data(subset['NSM'], subset['Usage_kWh'])

        ax.set_title('Energy Consumption Trends by Load Type')
        ax.set_xlabel('Time of Day')
        ax.set_ylabel('Avg Energy Consumption (kWh)')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='upper right')
        return lines.values()

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(load_data['NSM'].unique()), interval=100, blit=False, repeat=True)

    return fig