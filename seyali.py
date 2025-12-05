import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('/content/youtube_shorts_performance_dataset.csv')

st.set_page_config(page_title='YouTube Shorts Performance Dashboard', layout='wide')
st.title('YouTube Shorts Performance Analysis')

# Sidebar for user inputs
st.sidebar.header('Filter Data and Select Plot Options')

# Define numerical columns for filtering
numerical_cols = ['views', 'likes', 'comments', 'shares', 'duration_sec', 'hashtags_count']
categorical_cols = ['category', 'upload_hour']

# Filtering section in sidebar
st.sidebar.subheader('Filter Numerical Columns')
filtered_df = df.copy()
for col in numerical_cols:
    min_val, max_val = float(df[col].min()), float(df[col].max())
    selected_min, selected_max = st.sidebar.slider(
        f'Select range for {col.replace("_", " ").title()}',
        min_val,
        max_val,
        (min_val, max_val)
    )
    filtered_df = filtered_df[(filtered_df[col] >= selected_min) & (filtered_df[col] <= selected_max)]

# Plot selection section in sidebar
st.sidebar.subheader('Plot Options')
x_axis_scatter = st.sidebar.selectbox('Select X-axis for Scatter Plot', numerical_cols)
y_axis_scatter = st.sidebar.selectbox('Select Y-axis for Scatter Plot', numerical_cols)

category_for_plots = st.sidebar.selectbox('Select Categorical Column for Count/Pie Plots', categorical_cols)

# Main content area for plots
st.header('Visualizations')

# --- Scatter Plot ---
st.subheader(f'Scatter Plot: {y_axis_scatter.replace("_", " ").title()} vs {x_axis_scatter.replace("_", " ").title()}')
fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
sns.scatterplot(x=x_axis_scatter, y=y_axis_scatter, data=filtered_df, ax=ax_scatter, hue=category_for_plots, palette='viridis')
ax_scatter.set_title(f'{y_axis_scatter.replace("_", " ").title()} vs {x_axis_scatter.replace("_", " ").title()}')
ax_scatter.set_xlabel(x_axis_scatter.replace("_", " ").title())
ax_scatter.set_ylabel(y_axis_scatter.replace("_", " ").title())
st.pyplot(fig_scatter)

# --- Count Plot and Pie Chart for Categorical Column ---
st.subheader(f'Analysis by {category_for_plots.replace("_", " ").title()}')

col1, col2 = st.columns(2)

with col1:
    st.write(f'**Count Plot for {category_for_plots.replace("_", " ").title()}**')
    fig_count, ax_count = plt.subplots(figsize=(10, 6))
    sns.countplot(x=category_for_plots, data=filtered_df, ax=ax_count, palette='magma', order=filtered_df[category_for_plots].value_counts().index)
    ax_count.set_title(f'Count of Shorts by {category_for_plots.replace("_", " ").title()}')
    ax_count.set_xlabel(category_for_plots.replace("_", " ").title())
    ax_count.set_ylabel('Number of Shorts')
    ax_count.tick_params(axis='x', rotation=45)
    st.pyplot(fig_count)

with col2:
    st.write(f'**Pie Chart for {category_for_plots.replace("_", " ").title()} Distribution**')
    fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
    counts = filtered_df[category_for_plots].value_counts()
    ax_pie.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('magma'))
    ax_pie.set_title(f'Distribution of {category_for_plots.replace("_", " ").title()}')
    ax_pie.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig_pie)

# --- Summary Report Button ---
st.header('Summary Report')
if st.button('Generate Summary Report'):
    st.subheader('Descriptive Statistics of Filtered Data')
    st.dataframe(filtered_df.describe())

    st.subheader('Top 5 most viewed shorts (filtered)')
    st.dataframe(filtered_df.nlargest(5, 'views')[['title', 'views', 'likes', 'comments', 'shares']])

    st.subheader('Average Metrics by Category (filtered)')
    st.dataframe(filtered_df.groupby('category')[numerical_cols].mean().sort_values('views', ascending=False))

    st.subheader('Average Metrics by Upload Hour (filtered)')
    st.dataframe(filtered_df.groupby('upload_hour')[numerical_cols].mean().sort_values('views', ascending=False))
