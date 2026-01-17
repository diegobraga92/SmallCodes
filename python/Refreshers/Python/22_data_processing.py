"""
COMPREHENSIVE PYTHON DATA PROCESSING & VISUALIZATION DEMONSTRATION
====================================================================

This module demonstrates key Python concepts including:
1. Networking & APIs (HTTP, REST, JSON, HTTP clients)
2. File operations & data processing (os, sys, pathlib, parsing, streaming)
3. Data Processing (pandas, numpy)
4. Data Visualization (matplotlib, seaborn)
"""

# ============================================================================
# SECTION 1: IMPORTS AND SETUP
# ============================================================================

import os
import sys
import json
import csv
import yaml
import time
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Generator, Tuple
import requests
import httpx

# Data Processing Libraries
import numpy as np
import pandas as pd

# Visualization Libraries
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.axes import Axes

# For demonstration purposes
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse

# Set visualization style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# SECTION 2: NUMPY ARRAYS DEMONSTRATION
# ============================================================================

class NumpyDemonstration:
    """Demonstrates numpy array operations and numerical computing."""
    
    def __init__(self):
        self.array_data = {}
        
    def demonstrate_array_creation(self):
        """Show various ways to create numpy arrays."""
        print("\n" + "="*60)
        print("NUMPY ARRAY CREATION")
        print("="*60)
        
        # 1. From Python lists
        print("\n1. Creating arrays from Python lists:")
        list_data = [1, 2, 3, 4, 5]
        array_from_list = np.array(list_data)
        print(f"   List: {list_data}")
        print(f"   Array: {array_from_list}")
        print(f"   Type: {type(array_from_list)}")
        print(f"   Shape: {array_from_list.shape}")
        print(f"   Dtype: {array_from_list.dtype}")
        
        # 2. Multi-dimensional arrays
        print("\n2. Multi-dimensional arrays:")
        matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        print(f"   2D Array:\n{matrix}")
        print(f"   Shape: {matrix.shape}")
        print(f"   Dimensions: {matrix.ndim}")
        
        # 3. Special arrays
        print("\n3. Special arrays:")
        
        # Zeros and ones
        zeros = np.zeros((3, 4))
        ones = np.ones((2, 3, 2))
        print(f"   Zeros (3x4):\n{zeros}")
        print(f"   Ones (2x3x2) shape: {ones.shape}")
        
        # Identity matrix
        identity = np.eye(4)
        print(f"   Identity matrix (4x4):\n{identity}")
        
        # Arange and linspace
        range_array = np.arange(0, 10, 2)  # Start, stop, step
        linspace_array = np.linspace(0, 1, 5)  # Start, stop, num_points
        print(f"   Arange (0 to 10 step 2): {range_array}")
        print(f"   Linspace (0 to 1, 5 points): {linspace_array}")
        
        # 4. Random arrays
        print("\n4. Random arrays:")
        np.random.seed(42)  # For reproducibility
        
        random_uniform = np.random.rand(3, 3)
        random_normal = np.random.randn(2, 4)
        random_integers = np.random.randint(0, 100, (5,))
        
        print(f"   Random uniform (3x3):\n{np.round(random_uniform, 2)}")
        print(f"   Random normal (2x4):\n{np.round(random_normal, 2)}")
        print(f"   Random integers (0-100, size 5): {random_integers}")
        
        # Save for later use
        self.array_data['matrix'] = matrix
        self.array_data['random_uniform'] = random_uniform
    
    def demonstrate_array_operations(self):
        """Show mathematical and logical operations on arrays."""
        print("\n" + "="*60)
        print("NUMPY ARRAY OPERATIONS")
        print("="*60)
        
        # Create sample arrays
        a = np.array([1, 2, 3, 4, 5])
        b = np.array([10, 20, 30, 40, 50])
        
        print("\n1. Element-wise operations:")
        print(f"   a = {a}")
        print(f"   b = {b}")
        print(f"   a + b = {a + b}")
        print(f"   a * b = {a * b}")
        print(f"   b / a = {b / a}")
        print(f"   a ** 2 = {a ** 2}")
        
        # Broadcasting
        print("\n2. Broadcasting:")
        print(f"   a + 10 = {a + 10}")
        print(f"   a * 2.5 = {a * 2.5}")
        
        # Aggregation operations
        print("\n3. Aggregation operations:")
        print(f"   Sum of a: {np.sum(a)}")
        print(f"   Mean of a: {np.mean(a)}")
        print(f"   Std of a: {np.std(a)}")
        print(f"   Min of a: {np.min(a)}")
        print(f"   Max of a: {np.max(a)}")
        
        # Matrix operations
        print("\n4. Matrix operations:")
        matrix_a = np.array([[1, 2], [3, 4]])
        matrix_b = np.array([[5, 6], [7, 8]])
        
        print(f"   Matrix A:\n{matrix_a}")
        print(f"   Matrix B:\n{matrix_b}")
        print(f"   Dot product:\n{np.dot(matrix_a, matrix_b)}")
        print(f"   Matrix A determinant: {np.linalg.det(matrix_a):.2f}")
        print(f"   Matrix A inverse:\n{np.linalg.inv(matrix_a)}")
        
        # Boolean operations and filtering
        print("\n5. Boolean operations and filtering:")
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        print(f"   Data: {data}")
        print(f"   Data > 5: {data > 5}")
        print(f"   Data[data > 5]: {data[data > 5]}")
        print(f"   Data[(data > 3) & (data < 8)]: {data[(data > 3) & (data < 8)]}")
        
        # Reshaping and transposing
        print("\n6. Reshaping and transposing:")
        arr = np.arange(12)
        print(f"   Original (1D): {arr}")
        reshaped = arr.reshape(3, 4)
        print(f"   Reshaped (3x4):\n{reshaped}")
        print(f"   Transposed:\n{reshaped.T}")
        
        # Save operations
        self.array_data['reshaped'] = reshaped
        
    def demonstrate_advanced_features(self):
        """Show advanced numpy features."""
        print("\n" + "="*60)
        print("ADVANCED NUMPY FEATURES")
        print("="*60)
        
        # Stacking arrays
        print("\n1. Stacking arrays:")
        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        
        print(f"   a = {a}, b = {b}")
        print(f"   vstack (vertical):\n{np.vstack([a, b])}")
        print(f"   hstack (horizontal): {np.hstack([a, b])}")
        
        # Splitting arrays
        print("\n2. Splitting arrays:")
        arr = np.arange(10)
        print(f"   Array: {arr}")
        splits = np.array_split(arr, 3)
        for i, split in enumerate(splits):
            print(f"   Split {i+1}: {split}")
        
        # Vectorized operations (much faster than loops)
        print("\n3. Vectorized operations:")
        x = np.linspace(0, 10, 1000)
        
        # Traditional Python way (slow)
        start_time = time.time()
        y_slow = [np.sin(val) for val in x]
        slow_time = time.time() - start_time
        
        # Vectorized numpy way (fast)
        start_time = time.time()
        y_fast = np.sin(x)
        fast_time = time.time() - start_time
        
        print(f"   Slow (list comprehension): {slow_time:.6f} seconds")
        print(f"   Fast (vectorized): {fast_time:.6f} seconds")
        print(f"   Speedup: {slow_time/fast_time:.1f}x faster!")
        
        # Universal functions (ufuncs)
        print("\n4. Universal functions (ufuncs):")
        angles = np.array([0, np.pi/2, np.pi])
        print(f"   Angles: {angles}")
        print(f"   Sin: {np.sin(angles)}")
        print(f"   Cos: {np.cos(angles)}")
        print(f"   Exp: {np.exp([0, 1, 2])}")
        
        # Save for visualization
        self.array_data['x'] = x
        self.array_data['y_fast'] = y_fast

# ============================================================================
# SECTION 3: PANDAS BASICS DEMONSTRATION
# ============================================================================

class PandasDemonstration:
    """Demonstrates pandas for data manipulation and analysis."""
    
    def __init__(self, data_dir="demo_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def demonstrate_dataframe_creation(self):
        """Show various ways to create pandas DataFrames."""
        print("\n" + "="*60)
        print("PANDAS DATAFRAME CREATION")
        print("="*60)
        
        # 1. From dictionary
        print("\n1. Creating DataFrame from dictionary:")
        data = {
            'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'Age': [25, 30, 35, 28, 32],
            'Department': ['Engineering', 'Sales', 'Engineering', 'Marketing', 'Sales'],
            'Salary': [70000, 65000, 80000, 60000, 75000],
            'Join_Date': pd.date_range('2022-01-01', periods=5, freq='M')
        }
        
        df = pd.DataFrame(data)
        print(f"   DataFrame shape: {df.shape}")
        print(f"   DataFrame columns: {list(df.columns)}")
        print(f"\n   First 3 rows:")
        print(df.head(3))
        
        # 2. From CSV (creating sample CSV first)
        print("\n2. Creating and reading from CSV:")
        csv_file = self.data_dir / "employees.csv"
        df.to_csv(csv_file, index=False)
        
        df_from_csv = pd.read_csv(csv_file, parse_dates=['Join_Date'])
        print(f"   Read {len(df_from_csv)} rows from CSV")
        print(f"   CSV info:")
        print(df_from_csv.info())
        
        # 3. From numpy arrays
        print("\n3. Creating DataFrame from numpy arrays:")
        np_data = {
            'Temperature': np.random.normal(20, 5, 100),
            'Humidity': np.random.uniform(30, 90, 100),
            'Pressure': np.random.normal(1013, 10, 100)
        }
        np_df = pd.DataFrame(np_data)
        print(f"   Random weather data DataFrame:")
        print(np_df.head())
        
        # Save DataFrames for later use
        self.df = df
        self.np_df = np_df
        
    def demonstrate_data_manipulation(self):
        """Show data manipulation techniques."""
        print("\n" + "="*60)
        print("PANDAS DATA MANIPULATION")
        print("="*60)
        
        df = self.df.copy()
        
        # Selecting data
        print("\n1. Selecting data:")
        print(f"   Single column:\n{df['Name'].head()}")
        print(f"\n   Multiple columns:\n{df[['Name', 'Salary']].head()}")
        print(f"\n   By position (iloc):\n{df.iloc[1:4, 0:3]}")
        print(f"\n   By label (loc):\n{df.loc[0:2, ['Name', 'Department']]}")
        
        # Filtering
        print("\n2. Filtering data:")
        high_salary = df[df['Salary'] > 70000]
        print(f"   Employees with salary > 70,000:\n{high_salary}")
        
        engineering = df[df['Department'] == 'Engineering']
        print(f"\n   Engineering department:\n{engineering}")
        
        # Sorting
        print("\n3. Sorting data:")
        sorted_by_salary = df.sort_values('Salary', ascending=False)
        print(f"   Sorted by salary (descending):\n{sorted_by_salary}")
        
        # Adding/Modifying columns
        print("\n4. Adding and modifying columns:")
        df['Salary_in_K'] = df['Salary'] / 1000
        df['Bonus'] = df['Salary'] * 0.1
        df['Experience'] = [3, 5, 10, 4, 6]
        
        print(f"   Updated DataFrame:\n{df}")
        
        # Grouping and aggregation
        print("\n5. Grouping and aggregation:")
        dept_stats = df.groupby('Department').agg({
            'Salary': ['mean', 'min', 'max', 'count'],
            'Age': 'mean',
            'Experience': 'sum'
        }).round(2)
        
        print(f"   Department statistics:\n{dept_stats}")
        
        # Pivot tables
        print("\n6. Pivot tables:")
        # Create sample sales data
        sales_data = {
            'Date': pd.date_range('2024-01-01', periods=30, freq='D'),
            'Product': np.random.choice(['Widget', 'Gadget', 'Thingy'], 30),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], 30),
            'Sales': np.random.randint(100, 1000, 30)
        }
        sales_df = pd.DataFrame(sales_data)
        
        pivot = pd.pivot_table(sales_df, 
                              values='Sales', 
                              index='Region', 
                              columns='Product', 
                              aggfunc='sum',
                              fill_value=0)
        
        print(f"   Sales pivot table:\n{pivot}")
        
        self.sales_df = sales_df
        
    def demonstrate_data_cleaning(self):
        """Show data cleaning techniques."""
        print("\n" + "="*60)
        print("PANDAS DATA CLEANING")
        print("="*60)
        
        # Create a messy dataframe
        print("\n1. Creating messy data for cleaning:")
        messy_data = {
            'Name': ['Alice', 'Bob', None, 'Diana', 'Eve', 'Frank', None],
            'Age': [25, 30, 35, 28, 32, None, 40],
            'Salary': [70000, None, 80000, 60000, 75000, 68000, 90000],
            'Department': ['Engineering', 'Sales', 'Engineering', None, 'Sales', 'HR', 'Engineering']
        }
        
        messy_df = pd.DataFrame(messy_data)
        print(f"   Original messy data:\n{messy_df}")
        print(f"\n   Info:")
        print(messy_df.info())
        
        # Handling missing values
        print("\n2. Handling missing values:")
        print(f"   Missing values count:\n{messy_df.isnull().sum()}")
        
        # Fill missing values
        filled_df = messy_df.copy()
        filled_df['Age'].fillna(filled_df['Age'].mean(), inplace=True)
        filled_df['Salary'].fillna(filled_df['Salary'].median(), inplace=True)
        filled_df['Department'].fillna('Unknown', inplace=True)
        filled_df['Name'].fillna('Unknown', inplace=True)
        
        print(f"\n   After filling missing values:\n{filled_df}")
        
        # Drop rows/columns
        print("\n3. Dropping missing values:")
        dropped_df = messy_df.dropna()  # Drop rows with any NaN
        print(f"   After dropping rows with NaN: {len(dropped_df)} rows")
        
        # Remove duplicates
        print("\n4. Handling duplicates:")
        dup_data = pd.DataFrame({
            'A': [1, 1, 2, 2, 3, 3, 3],
            'B': ['a', 'a', 'b', 'b', 'c', 'c', 'd']
        })
        
        print(f"   Data with duplicates:\n{dup_data}")
        print(f"   Duplicate rows:\n{dup_data.duplicated()}")
        unique_df = dup_data.drop_duplicates()
        print(f"   After removing duplicates:\n{unique_df}")
        
        # Data type conversion
        print("\n5. Data type conversion:")
        df_types = filled_df.copy()
        print(f"   Original dtypes:\n{df_types.dtypes}")
        df_types['Age'] = df_types['Age'].astype(int)
        print(f"   After converting Age to int:\n{df_types.dtypes}")
        
        # String operations
        print("\n6. String operations:")
        df_types['Name_Upper'] = df_types['Name'].str.upper()
        df_types['Dept_Short'] = df_types['Department'].str[:3]
        print(f"   String operations:\n{df_types[['Name', 'Name_Upper', 'Department', 'Dept_Short']]}")
        
        self.messy_df = messy_df
        self.cleaned_df = filled_df
        
    def demonstrate_time_series(self):
        """Show time series operations."""
        print("\n" + "="*60)
        print("PANDAS TIME SERIES")
        print("="*60)
        
        # Create time series data
        print("\n1. Creating time series data:")
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        ts_data = pd.DataFrame({
            'Date': dates,
            'Temperature': np.random.normal(20, 5, 100).cumsum(),
            'Humidity': np.random.normal(60, 10, 100),
            'Sales': np.random.randint(100, 500, 100).cumsum()
        })
        
        ts_data.set_index('Date', inplace=True)
        print(f"   Time series data (first 5 rows):\n{ts_data.head()}")
        print(f"\n   Data info:")
        print(ts_data.info())
        
        # Resampling
        print("\n2. Resampling time series:")
        weekly_mean = ts_data.resample('W').mean()
        print(f"   Weekly averages:\n{weekly_mean.head()}")
        
        monthly_sum = ts_data.resample('M').sum()
        print(f"\n   Monthly totals:\n{monthly_sum}")
        
        # Rolling windows
        print("\n3. Rolling window operations:")
        ts_data['Temp_7day_avg'] = ts_data['Temperature'].rolling(window=7).mean()
        ts_data['Sales_30day_sum'] = ts_data['Sales'].rolling(window=30).sum()
        
        print(f"   With rolling averages (last 5 rows):\n{ts_data.tail()}")
        
        # Shifting for time lag
        print("\n4. Time shifting:")
        ts_data['Sales_lag1'] = ts_data['Sales'].shift(1)
        ts_data['Sales_diff'] = ts_data['Sales'].diff()
        print(f"   With lag and difference:\n{ts_data[['Sales', 'Sales_lag1', 'Sales_diff']].head(10)}")
        
        self.ts_data = ts_data

# ============================================================================
# SECTION 4: DATA VISUALIZATION DEMONSTRATION
# ============================================================================

class VisualizationDemonstration:
    """Demonstrates data visualization with matplotlib and seaborn."""
    
    def __init__(self, output_dir="demo_data/visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def demonstrate_matplotlib_basics(self):
        """Show basic matplotlib visualizations."""
        print("\n" + "="*60)
        print("MATPLOTLIB BASICS")
        print("="*60)
        
        # Generate sample data
        np.random.seed(42)
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        y3 = np.exp(x/10)
        
        # 1. Basic line plot
        print("\n1. Creating basic line plots...")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Single line plot
        ax1.plot(x, y1, label='sin(x)', color='blue', linewidth=2)
        ax1.set_title('Sine Wave')
        ax1.set_xlabel('X values')
        ax1.set_ylabel('sin(x)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Multiple lines plot
        ax2.plot(x, y1, label='sin(x)', color='blue')
        ax2.plot(x, y2, label='cos(x)', color='red', linestyle='--')
        ax2.plot(x, y3, label='exp(x/10)', color='green', linewidth=2)
        ax2.set_title('Multiple Functions')
        ax2.set_xlabel('X values')
        ax2.set_ylabel('Y values')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'line_plots.png', dpi=100)
        print(f"   Saved: {self.output_dir / 'line_plots.png'}")
        
        # 2. Scatter plot
        print("\n2. Creating scatter plots...")
        plt.figure(figsize=(10, 6))
        
        # Generate random data
        x_scatter = np.random.randn(100)
        y_scatter = x_scatter + np.random.randn(100) * 0.5
        sizes = np.random.rand(100) * 100
        colors = np.random.rand(100)
        
        scatter = plt.scatter(x_scatter, y_scatter, 
                             s=sizes, 
                             c=colors, 
                             alpha=0.6,
                             cmap='viridis')
        plt.colorbar(scatter, label='Color intensity')
        plt.title('Random Scatter Plot with Size and Color Encoding')
        plt.xlabel('X values')
        plt.ylabel('Y values')
        plt.grid(True, alpha=0.3)
        
        plt.savefig(self.output_dir / 'scatter_plot.png', dpi=100)
        print(f"   Saved: {self.output_dir / 'scatter_plot.png'}")
        
        # 3. Bar chart
        print("\n3. Creating bar charts...")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Vertical bar chart
        categories = ['A', 'B', 'C', 'D', 'E']
        values = [23, 45, 56, 78, 33]
        ax1.bar(categories, values, color=['red', 'blue', 'green', 'orange', 'purple'])
        ax1.set_title('Vertical Bar Chart')
        ax1.set_xlabel('Categories')
        ax1.set_ylabel('Values')
        
        # Horizontal bar chart
        ax2.barh(categories, values, color='skyblue')
        ax2.set_title('Horizontal Bar Chart')
        ax2.set_xlabel('Values')
        ax2.set_ylabel('Categories')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'bar_charts.png', dpi=100)
        print(f"   Saved: {self.output_dir / 'bar_charts.png'}")
        
        # 4. Histogram
        print("\n4. Creating histograms...")
        plt.figure(figsize=(10, 6))
        
        # Generate normally distributed data
        data_normal = np.random.normal(0, 1, 1000)
        data_uniform = np.random.uniform(-3, 3, 1000)
        
        plt.hist(data_normal, bins=30, alpha=0.7, label='Normal Distribution', density=True)
        plt.hist(data_uniform, bins=30, alpha=0.7, label='Uniform Distribution', density=True)
        plt.title('Histogram Comparison')
        plt.xlabel('Value')
        plt.ylabel('Density')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.savefig(self.output_dir / 'histograms.png', dpi=100)
        print(f"   Saved: {self.output_dir / 'histograms.png'}")
        
        plt.close('all')
        
    def demonstrate_seaborn_visualizations(self):
        """Show seaborn visualizations."""
        print("\n" + "="*60)
        print("SEABORN VISUALIZATIONS")
        print("="*60)
        
        # Create sample dataset
        print("\n1. Creating sample dataset for seaborn...")
        np.random.seed(42)
        n_samples = 200
        
        df = pd.DataFrame({
            'Feature_A': np.random.normal(0, 1, n_samples),
            'Feature_B': np.random.normal(5, 2, n_samples),
            'Feature_C': np.random.exponential(1, n_samples),
            'Category': np.random.choice(['Cat1', 'Cat2', 'Cat3'], n_samples),
            'Value': np.random.randn(n_samples),
            'Size': np.random.rand(n_samples) * 100
        })
        
        # Add correlation between features
        df['Feature_D'] = df['Feature_A'] * 0.7 + np.random.randn(n_samples) * 0.3
        
        print(f"   Sample dataset created with {len(df)} rows")
        print(df.head())
        
        # 2. Pair plot
        print("\n2. Creating pair plot...")
        pair_plot = sns.pairplot(df[['Feature_A', 'Feature_B', 'Feature_C', 'Category']], 
                                hue='Category',
                                diag_kind='kde',
                                palette='Set2')
        pair_plot.fig.suptitle('Pair Plot of Features by Category', y=1.02)
        pair_plot.savefig(self.output_dir / 'pair_plot.png', dpi=100, bbox_inches='tight')
        print(f"   Saved: {self.output_dir / 'pair_plot.png'}")
        
        # 3. Heatmap (correlation matrix)
        print("\n3. Creating correlation heatmap...")
        plt.figure(figsize=(10, 8))
        
        # Calculate correlation matrix
        corr_matrix = df[['Feature_A', 'Feature_B', 'Feature_C', 'Feature_D', 'Value']].corr()
        
        # Create heatmap
        sns.heatmap(corr_matrix, 
                   annot=True, 
                   cmap='coolwarm', 
                   center=0,
                   square=True,
                   linewidths=1,
                   cbar_kws={'label': 'Correlation Coefficient'})
        
        plt.title('Feature Correlation Heatmap')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'correlation_heatmap.png', dpi=100)
        print(f"   Saved: {self.output_dir / 'correlation_heatmap.png'}")
        
        # 4. Box plot and violin plot
        print("\n4. Creating box and violin plots...")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Box plot
        sns.boxplot(data=df, x='Category', y='Value', ax=ax1, palette='Set3')
        ax1.set_title('Box Plot by Category')
        ax1.set_xlabel('Category')
        ax1.set_ylabel('Value')
        
        # Violin plot
        sns.violinplot(data=df, x='Category', y='Value', ax=ax2, palette='Set3', inner='quartile')
        ax2.set_title('Violin Plot by Category')
        ax2.set_xlabel('Category')
        ax2.set_ylabel('Value')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'box_violin_plots.png', dpi=100)
        print(f"   Saved: {self.output_dir / 'box_violin_plots.png'}")
        
        # 5. KDE plot (Density plot)
        print("\n5. Creating KDE plots...")
        plt.figure(figsize=(10, 6))
        
        for category in df['Category'].unique():
            subset = df[df['Category'] == category]
            sns.kdeplot(data=subset['Feature_A'], label=category, fill=True, alpha=0.3)
        
        plt.title('Kernel Density Estimation by Category')
        plt.xlabel('Feature_A Value')
        plt.ylabel('Density')
        plt.legend(title='Category')
        plt.grid(True, alpha=0.3)
        
        plt.savefig(self.output_dir / 'kde_plot.png', dpi=100)
        print(f"   Saved: {self.output_dir / 'kde_plot.png'}")
        
        # 6. Joint plot
        print("\n6. Creating joint plot...")
        joint = sns.jointplot(data=df, x='Feature_A', y='Feature_D', 
                             kind='reg',  # Can be 'scatter', 'kde', 'hex', 'reg', 'resid'
                             color='purple',
                             height=8)
        
        joint.fig.suptitle('Joint Plot with Regression', y=1.02)
        joint.savefig(self.output_dir / 'joint_plot.png', dpi=100, bbox_inches='tight')
        print(f"   Saved: {self.output_dir / 'joint_plot.png'}")
        
        plt.close('all')
        
        # Save the dataframe for later use
        self.df = df
        
    def demonstrate_advanced_visualizations(self):
        """Show advanced and combined visualizations."""
        print("\n" + "="*60)
        print("ADVANCED VISUALIZATIONS")
        print("="*60)
        
        # Create time series data
        print("\n1. Creating time series visualizations...")
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        ts_df = pd.DataFrame({
            'Date': dates,
            'Temperature': np.random.normal(20, 5, 100).cumsum(),
            'Humidity': np.random.normal(60, 10, 100),
            'Sales': np.random.randint(100, 500, 100).cumsum(),
            'Category': np.random.choice(['A', 'B', 'C'], 100)
        })
        ts_df.set_index('Date', inplace=True)
        
        # Time series plot with multiple y-axes
        print("\n2. Creating multi-axis time series plot...")
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # First axis
        color = 'tab:red'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Temperature', color=color)
        ax1.plot(ts_df.index, ts_df['Temperature'], color=color, linewidth=2)
        ax1.tick_params(axis='y', labelcolor=color)
        
        # Second axis
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Humidity', color=color)
        ax2.plot(ts_df.index, ts_df['Humidity'], color=color, linestyle='--')
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title('Temperature and Humidity Over Time')
        fig.tight_layout()
        plt.savefig(self.output_dir / 'multi_axis_plot.png', dpi=100)
        print(f"   Saved: {self.output_dir / 'multi_axis_plot.png'}")
        
        # 3. Subplot grid
        print("\n3. Creating subplot grid...")
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Line plot
        axes[0, 0].plot(ts_df.index, ts_df['Sales'])
        axes[0, 0].set_title('Sales Over Time')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Sales')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Histogram
        axes[0, 1].hist(ts_df['Temperature'], bins=20, edgecolor='black', alpha=0.7)
        axes[0, 1].set_title('Temperature Distribution')
        axes[0, 1].set_xlabel('Temperature')
        axes[0, 1].set_ylabel('Frequency')
        
        # Plot 3: Scatter plot
        axes[1, 0].scatter(ts_df['Temperature'], ts_df['Humidity'], 
                          alpha=0.6, c=ts_df['Sales'], cmap='viridis')
        axes[1, 0].set_title('Temperature vs Humidity')
        axes[1, 0].set_xlabel('Temperature')
        axes[1, 0].set_ylabel('Humidity')
        plt.colorbar(axes[1, 0].collections[0], ax=axes[1, 0], label='Sales')
        
        # Plot 4: Bar plot
        sales_by_category = ts_df.groupby('Category')['Sales'].sum()
        axes[1, 1].bar(sales_by_category.index, sales_by_category.values, 
                      color=['red', 'blue', 'green'])
        axes[1, 1].set_title('Total Sales by Category')
        axes[1, 1].set_xlabel('Category')
        axes[1, 1].set_ylabel('Total Sales')
        
        plt.suptitle('Comprehensive Data Analysis Dashboard', fontsize=16)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'subplot_grid.png', dpi=100)
        print(f"   Saved: {self.output_dir / 'subplot_grid.png'}")
        
        # 4. 3D Plot (if matplotlib 3D is available)
        print("\n4. Creating 3D visualization...")
        try:
            from mpl_toolkits.mplot3d import Axes3D
            
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            # Generate 3D data
            x = np.random.randn(100)
            y = np.random.randn(100)
            z = x**2 + y**2 + np.random.randn(100)*0.5
            colors = np.random.rand(100)
            
            scatter = ax.scatter(x, y, z, c=colors, cmap='viridis', s=50, alpha=0.7)
            ax.set_xlabel('X Axis')
            ax.set_ylabel('Y Axis')
            ax.set_zlabel('Z Axis')
            ax.set_title('3D Scatter Plot')
            plt.colorbar(scatter, ax=ax, label='Color Value')
            
            plt.savefig(self.output_dir / '3d_plot.png', dpi=100)
            print(f"   Saved: {self.output_dir / '3d_plot.png'}")
        except ImportError:
            print("   3D plotting not available in this environment")
        
        plt.close('all')
        
        print(f"\nAll visualizations saved to: {self.output_dir}")

# ============================================================================
# SECTION 5: INTEGRATED DATA PIPELINE EXAMPLE
# ============================================================================

class IntegratedDataPipeline:
    """Integrated example showing complete data processing pipeline."""
    
    def __init__(self):
        self.data_dir = Path("demo_data/pipeline")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_sample_data(self):
        """Generate comprehensive sample dataset."""
        print("\n" + "="*60)
        print("GENERATING SAMPLE DATASET")
        print("="*60)
        
        np.random.seed(42)
        
        # Create e-commerce dataset
        n_customers = 1000
        n_products = 50
        n_transactions = 5000
        
        # Customer data
        print("1. Generating customer data...")
        customers = pd.DataFrame({
            'customer_id': range(1, n_customers + 1),
            'age': np.random.randint(18, 70, n_customers),
            'gender': np.random.choice(['M', 'F'], n_customers, p=[0.48, 0.52]),
            'income': np.random.lognormal(10.5, 0.5, n_customers).astype(int),
            'region': np.random.choice(['North', 'South', 'East', 'West'], n_customers),
            'signup_date': pd.date_range('2023-01-01', periods=n_customers, freq='H')
        })
        
        # Product data
        print("2. Generating product data...")
        categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
        products = pd.DataFrame({
            'product_id': range(1, n_products + 1),
            'product_name': [f'Product_{i:03d}' for i in range(1, n_products + 1)],
            'category': np.random.choice(categories, n_products, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
            'price': np.random.uniform(10, 1000, n_products).round(2),
            'cost': np.random.uniform(5, 500, n_products).round(2),
            'stock': np.random.randint(0, 1000, n_products)
        })
        
        # Transaction data
        print("3. Generating transaction data...")
        transactions = pd.DataFrame({
            'transaction_id': range(1, n_transactions + 1),
            'customer_id': np.random.choice(customers['customer_id'], n_transactions),
            'product_id': np.random.choice(products['product_id'], n_transactions),
            'quantity': np.random.randint(1, 5, n_transactions),
            'transaction_date': pd.date_range('2024-01-01', periods=n_transactions, freq='H')
        })
        
        # Calculate transaction value
        transactions = transactions.merge(products[['product_id', 'price']], on='product_id')
        transactions['total_value'] = transactions['quantity'] * transactions['price']
        
        # Reviews data
        print("4. Generating review data...")
        n_reviews = 3000
        reviews = pd.DataFrame({
            'review_id': range(1, n_reviews + 1),
            'customer_id': np.random.choice(customers['customer_id'], n_reviews),
            'product_id': np.random.choice(products['product_id'], n_reviews),
            'rating': np.random.randint(1, 6, n_reviews),
            'review_date': pd.date_range('2024-01-01', periods=n_reviews, freq='H'),
            'review_text': ['Good product' if i % 2 == 0 else 'Excellent quality' for i in range(n_reviews)]
        })
        
        # Save datasets
        print("\n5. Saving datasets...")
        customers.to_csv(self.data_dir / 'customers.csv', index=False)
        products.to_csv(self.data_dir / 'products.csv', index=False)
        transactions.to_csv(self.data_dir / 'transactions.csv', index=False)
        reviews.to_csv(self.data_dir / 'reviews.csv', index=False)
        
        print(f"   Generated {len(customers)} customers")
        print(f"   Generated {len(products)} products")
        print(f"   Generated {len(transactions)} transactions")
        print(f"   Generated {len(reviews)} reviews")
        
        self.customers = customers
        self.products = products
        self.transactions = transactions
        self.reviews = reviews
        
    def run_analysis_pipeline(self):
        """Run complete data analysis pipeline."""
        print("\n" + "="*60)
        print("DATA ANALYSIS PIPELINE")
        print("="*60)
        
        # Load data (or use already loaded)
        print("\n1. Loading and exploring data...")
        print(f"   Customers: {self.customers.shape}")
        print(f"   Products: {self.products.shape}")
        print(f"   Transactions: {self.transactions.shape}")
        print(f"   Reviews: {self.reviews.shape}")
        
        # Merge datasets
        print("\n2. Merging datasets for analysis...")
        # Merge transactions with product and customer info
        merged_data = self.transactions.merge(
            self.products[['product_id', 'category', 'price']], 
            on='product_id'
        ).merge(
            self.customers[['customer_id', 'age', 'gender', 'region', 'income']],
            on='customer_id'
        )
        
        print(f"   Merged dataset shape: {merged_data.shape}")
        print(f"   Merged columns: {list(merged_data.columns)}")
        
        # Basic statistics
        print("\n3. Calculating basic statistics...")
        stats = {
            'total_revenue': merged_data['total_value'].sum(),
            'avg_transaction_value': merged_data['total_value'].mean(),
            'total_transactions': len(merged_data),
            'unique_customers': merged_data['customer_id'].nunique(),
            'unique_products': merged_data['product_id'].nunique()
        }
        
        for key, value in stats.items():
            print(f"   {key}: {value:,.2f}" if isinstance(value, float) else f"   {key}: {value:,}")
        
        # Time-based analysis
        print("\n4. Time series analysis...")
        merged_data['transaction_date'] = pd.to_datetime(merged_data['transaction_date'])
        merged_data['month'] = merged_data['transaction_date'].dt.month
        merged_data['day_of_week'] = merged_data['transaction_date'].dt.day_name()
        
        # Monthly revenue
        monthly_revenue = merged_data.groupby('month')['total_value'].agg(['sum', 'count', 'mean'])
        print(f"\n   Monthly Revenue:")
        print(monthly_revenue.round(2))
        
        # Customer segmentation
        print("\n5. Customer segmentation analysis...")
        customer_stats = merged_data.groupby('customer_id').agg({
            'total_value': 'sum',
            'transaction_id': 'count',
            'product_id': pd.Series.nunique
        }).rename(columns={
            'total_value': 'total_spent',
            'transaction_id': 'transaction_count',
            'product_id': 'unique_products'
        })
        
        # Add customer demographics
        customer_stats = customer_stats.merge(
            self.customers[['customer_id', 'age', 'gender', 'income']].set_index('customer_id'),
            left_index=True, right_index=True
        )
        
        # Create customer segments based on spending
        customer_stats['segment'] = pd.qcut(customer_stats['total_spent'], 
                                          q=4, 
                                          labels=['Low', 'Medium', 'High', 'VIP'])
        
        print(f"   Customer segments distribution:")
        print(customer_stats['segment'].value_counts())
        
        # Product analysis
        print("\n6. Product performance analysis...")
        product_performance = merged_data.groupby(['product_id', 'category']).agg({
            'total_value': 'sum',
            'quantity': 'sum',
            'transaction_id': 'count'
        }).rename(columns={
            'total_value': 'revenue',
            'quantity': 'units_sold',
            'transaction_id': 'transaction_count'
        }).sort_values('revenue', ascending=False)
        
        print(f"\n   Top 5 products by revenue:")
        print(product_performance.head())
        
        # Save analysis results
        print("\n7. Saving analysis results...")
        monthly_revenue.to_csv(self.data_dir / 'monthly_revenue.csv')
        customer_stats.to_csv(self.data_dir / 'customer_segments.csv')
        product_performance.to_csv(self.data_dir / 'product_performance.csv')
        
        print(f"   Analysis results saved to {self.data_dir}")
        
        self.merged_data = merged_data
        self.customer_stats = customer_stats
        self.product_performance = product_performance
        
    def create_dashboard(self):
        """Create comprehensive visualization dashboard."""
        print("\n" + "="*60)
        print("CREATING ANALYSIS DASHBOARD")
        print("="*60)
        
        viz_dir = self.data_dir / 'dashboard'
        viz_dir.mkdir(exist_ok=True)
        
        # 1. Revenue trends
        print("\n1. Creating revenue trend visualizations...")
        plt.figure(figsize=(12, 8))
        
        # Daily revenue
        daily_revenue = self.merged_data.set_index('transaction_date')['total_value'].resample('D').sum()
        
        plt.subplot(2, 2, 1)
        daily_revenue.plot(color='green', linewidth=2)
        plt.title('Daily Revenue Trend')
        plt.xlabel('Date')
        plt.ylabel('Revenue ($)')
        plt.grid(True, alpha=0.3)
        
        # Revenue by category
        plt.subplot(2, 2, 2)
        category_revenue = self.merged_data.groupby('category')['total_value'].sum().sort_values()
        category_revenue.plot(kind='barh', color='skyblue')
        plt.title('Revenue by Product Category')
        plt.xlabel('Revenue ($)')
        plt.tight_layout()
        
        # Customer segment distribution
        plt.subplot(2, 2, 3)
        segment_dist = self.customer_stats['segment'].value_counts()
        colors = ['lightcoral', 'gold', 'lightgreen', 'cornflowerblue']
        segment_dist.plot(kind='pie', autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Customer Segment Distribution')
        plt.ylabel('')
        
        # Age vs Spending
        plt.subplot(2, 2, 4)
        age_spending = self.customer_stats.groupby(pd.cut(self.customer_stats['age'], bins=10))['total_spent'].mean()
        age_spending.plot(kind='bar', color='purple', alpha=0.7)
        plt.title('Average Spending by Age Group')
        plt.xlabel('Age Group')
        plt.ylabel('Average Spending ($)')
        plt.xticks(rotation=45)
        
        plt.suptitle('E-commerce Analytics Dashboard', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(viz_dir / 'dashboard_overview.png', dpi=120, bbox_inches='tight')
        print(f"   Saved: {viz_dir / 'dashboard_overview.png'}")
        
        # 2. Advanced visualizations
        print("\n2. Creating advanced visualizations...")
        
        # Correlation heatmap
        plt.figure(figsize=(10, 8))
        numeric_cols = self.customer_stats.select_dtypes(include=[np.number]).columns
        corr_matrix = self.customer_stats[numeric_cols].corr()
        
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, square=True)
        plt.title('Customer Metrics Correlation Heatmap')
        plt.tight_layout()
        plt.savefig(viz_dir / 'correlation_heatmap.png', dpi=100)
        print(f"   Saved: {viz_dir / 'correlation_heatmap.png'}")
        
        # Box plot by segment
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=self.customer_stats, x='segment', y='total_spent', palette='Set2')
        plt.title('Spending Distribution by Customer Segment')
        plt.xlabel('Customer Segment')
        plt.ylabel('Total Spending ($)')
        plt.grid(True, alpha=0.3)
        plt.savefig(viz_dir / 'spending_by_segment.png', dpi=100)
        print(f"   Saved: {viz_dir / 'spending_by_segment.png'}")
        
        # Time series decomposition (simplified)
        print("\n3. Creating time series analysis...")
        plt.figure(figsize=(12, 8))
        
        # Resample to weekly
        weekly_revenue = self.merged_data.set_index('transaction_date')['total_value'].resample('W').sum()
        
        # Plot with rolling average
        plt.subplot(2, 1, 1)
        weekly_revenue.plot(label='Weekly Revenue', alpha=0.7)
        weekly_revenue.rolling(window=4).mean().plot(label='4-Week Moving Average', linewidth=2)
        plt.title('Weekly Revenue with Moving Average')
        plt.xlabel('Date')
        plt.ylabel('Revenue ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Day of week analysis
        plt.subplot(2, 1, 2)
        dow_revenue = self.merged_data.groupby('day_of_week')['total_value'].sum()
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_revenue = dow_revenue.reindex(dow_order)
        dow_revenue.plot(kind='bar', color='teal', alpha=0.7)
        plt.title('Revenue by Day of Week')
        plt.xlabel('Day of Week')
        plt.ylabel('Revenue ($)')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(viz_dir / 'time_series_analysis.png', dpi=100)
        print(f"   Saved: {viz_dir / 'time_series_analysis.png'}")
        
        # 4. Generate report
        print("\n4. Generating analysis report...")
        report_file = self.data_dir / 'analysis_report.txt'
        
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("E-COMMERCE DATA ANALYSIS REPORT\n")
            f.write("="*60 + "\n\n")
            
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-"*40 + "\n")
            f.write(f"Total Revenue: ${self.merged_data['total_value'].sum():,.2f}\n")
            f.write(f"Total Transactions: {len(self.merged_data):,}\n")
            f.write(f"Unique Customers: {self.merged_data['customer_id'].nunique():,}\n")
            f.write(f"Average Transaction Value: ${self.merged_data['total_value'].mean():,.2f}\n\n")
            
            f.write("TOP PERFORMING CATEGORIES\n")
            f.write("-"*40 + "\n")
            top_categories = self.merged_data.groupby('category')['total_value'].sum().nlargest(3)
            for category, revenue in top_categories.items():
                f.write(f"{category}: ${revenue:,.2f}\n")
            
            f.write("\nCUSTOMER SEGMENT INSIGHTS\n")
            f.write("-"*40 + "\n")
            for segment in ['VIP', 'High', 'Medium', 'Low']:
                segment_data = self.customer_stats[self.customer_stats['segment'] == segment]
                if not segment_data.empty:
                    avg_spending = segment_data['total_spent'].mean()
                    f.write(f"{segment} Customers: {len(segment_data):,} "
                           f"(Avg Spending: ${avg_spending:,.2f})\n")
            
            f.write("\nTIME ANALYSIS\n")
            f.write("-"*40 + "\n")
            best_month = self.merged_data.groupby('month')['total_value'].sum().idxmax()
            f.write(f"Best Performing Month: {best_month}\n")
            best_day = self.merged_data.groupby('day_of_week')['total_value'].sum().idxmax()
            f.write(f"Best Performing Day: {best_day}\n")
        
        print(f"   Report saved: {report_file}")
        print(f"\nDashboard visualizations saved to: {viz_dir}")
        
        plt.close('all')

# ============================================================================
# SECTION 6: MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all demonstrations."""
    
    print("\n" + "="*80)
    print("PYTHON DATA PROCESSING & VISUALIZATION COMPREHENSIVE DEMONSTRATION")
    print("="*80)
    
    # Check for required packages
    required_packages = ['numpy', 'pandas', 'matplotlib', 'seaborn']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing required packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        if 'seaborn' in missing_packages:
            print("Note: seaborn requires matplotlib")
        sys.exit(1)
    
    # Clean up previous runs
    demo_dir = Path("demo_data")
    if demo_dir.exists():
        import shutil
        try:
            shutil.rmtree(demo_dir)
            print("Cleaned up previous demo directory")
        except:
            print("Could not clean up demo directory (might be in use)")
    
    try:
        # SECTION 2: Numpy Arrays
        print("\n" + "="*80)
        print("PART 1: NUMPY ARRAYS")
        print("="*80)
        
        numpy_demo = NumpyDemonstration()
        numpy_demo.demonstrate_array_creation()
        numpy_demo.demonstrate_array_operations()
        numpy_demo.demonstrate_advanced_features()
        
        # SECTION 3: Pandas Basics
        print("\n" + "="*80)
        print("PART 2: PANDAS DATA PROCESSING")
        print("="*80)
        
        pandas_demo = PandasDemonstration()
        pandas_demo.demonstrate_dataframe_creation()
        pandas_demo.demonstrate_data_manipulation()
        pandas_demo.demonstrate_data_cleaning()
        pandas_demo.demonstrate_time_series()
        
        # SECTION 4: Data Visualization
        print("\n" + "="*80)
        print("PART 3: DATA VISUALIZATION")
        print("="*80)
        
        viz_demo = VisualizationDemonstration()
        viz_demo.demonstrate_matplotlib_basics()
        viz_demo.demonstrate_seaborn_visualizations()
        viz_demo.demonstrate_advanced_visualizations()
        
        # SECTION 5: Integrated Pipeline
        print("\n" + "="*80)
        print("PART 4: INTEGRATED DATA PIPELINE")
        print("="*80)
        
        pipeline = IntegratedDataPipeline()
        pipeline.generate_sample_data()
        pipeline.run_analysis_pipeline()
        pipeline.create_dashboard()
        
        print("\n" + "="*80)
        print("DEMONSTRATION COMPLETE!")
        print("="*80)
        
        # Show generated files
        print("\nGenerated files and directories:")
        for root, dirs, files in os.walk("demo_data"):
            level = root.replace("demo_data", "").count(os.sep)
            indent = " " * 2 * level
            rel_path = os.path.relpath(root, "demo_data")
            if rel_path == ".":
                print("demo_data/")
            else:
                print(f"{indent}{os.path.basename(root)}/")
            
            subindent = " " * 2 * (level + 1)
            for file in sorted(files)[:5]:
                size = os.path.getsize(os.path.join(root, file))
                print(f"{subindent}{file} ({size:,} bytes)")
            if len(files) > 5:
                print(f"{subindent}... and {len(files) - 5} more files")
        
        print("\n" + "-"*80)
        print("KEY CONCEPTS DEMONSTRATED:")
        print("-"*80)
        print("1. NUMPY: Arrays, vectorized operations, broadcasting, linear algebra")
        print("2. PANDAS: DataFrames, data cleaning, grouping, time series, merging")
        print("3. VISUALIZATION: Matplotlib plots, Seaborn statistical graphics")
        print("4. INTEGRATION: Complete data pipeline from generation to dashboard")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n" + "="*80)
        print("Files are saved in 'demo_data' directory.")
        print("You can explore the generated files and visualizations.")
        
        # Show how to view visualizations
        viz_path = "demo_data/visualizations"
        if os.path.exists(viz_path):
            print(f"\nVisualizations are in: {viz_path}")
            print("To view them, you can:")
            print("1. Open the PNG files in any image viewer")
            print("2. Use Jupyter Notebook to display them inline")
            print("3. Open the dashboard images in the dashboard/ subdirectory")

if __name__ == "__main__":
    main()