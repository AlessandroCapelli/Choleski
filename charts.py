import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Global variables
INPUT_DIRECTORY = '/Users/'

def chart_os(os):
    df_python = pd.read_csv(INPUT_DIRECTORY + 'data_python_' + os.lower() + '.csv')
    df_matlab = pd.read_csv(INPUT_DIRECTORY + 'data_matlab_' + os.lower() + '.csv')

    fig = go.Figure()

    config = {'toImageButtonOptions': {'format': 'png', 'filename': 'chart', 'height': 1000, 'width': 2000, 'scale': 2}}

    fig.add_trace(go.Scatter(x=df_python['Matrix name'], y=df_python['Elapsed time (s)'], name='Python: Elapsed time (s)'))
    fig.add_trace(go.Scatter(x=df_python['Matrix name'], y=df_python['Memory (MB)'], name='Python: Memory (MB)'))
    fig.add_trace(go.Scatter(x=df_python['Matrix name'], y=df_python['Relative error'], name='Python: Relative error'))

    fig.add_trace(go.Scatter(x=df_matlab['Matrix name'], y=df_matlab['Elapsed time (s)'], name='Matlab: Elapsed time (s)', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=df_matlab['Matrix name'], y=df_matlab['Memory (MB)'], name='Matlab: Memory (MB)', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=df_matlab['Matrix name'], y=df_matlab['Relative error'], name='Matlab: Relative error', line=dict(dash='dash')))

    fig.update_layout(title=os, showlegend=True, yaxis_type='log', yaxis=dict(showexponent='all', exponentformat='e'), template='plotly_dark', legend=dict(x=0.2, y=1.075), legend_orientation='h')
    fig.show(config=config)

def chart_env(env):
    df_linux = pd.read_csv(INPUT_DIRECTORY + 'data_' + env.lower() + '_linux.csv')
    df_windows = pd.read_csv(INPUT_DIRECTORY + 'data_' + env.lower() + '_windows.csv')

    fig = go.Figure()

    config = {'toImageButtonOptions': {'format': 'png', 'filename': 'chart', 'height': 1000, 'width': 2000, 'scale': 2}}

    fig.add_trace(go.Scatter(x=df_linux['Matrix name'], y=df_linux['Elapsed time (s)'], name='Linux: Elapsed time (s)'))
    fig.add_trace(go.Scatter(x=df_linux['Matrix name'], y=df_linux['Memory (MB)'], name='Linux: Memory (MB)'))
    fig.add_trace(go.Scatter(x=df_linux['Matrix name'], y=df_linux['Relative error'], name='Linux: Relative error'))

    fig.add_trace(go.Scatter(x=df_windows['Matrix name'], y=df_windows['Elapsed time (s)'], name='Windows: Elapsed time (s)', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=df_windows['Matrix name'], y=df_windows['Memory (MB)'], name='Windows: Memory (MB)', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=df_windows['Matrix name'], y=df_windows['Relative error'], name='Windows: Relative error', line=dict(dash='dash')))

    fig.update_layout(title=env, showlegend=True, yaxis_type='log', yaxis=dict(showexponent='all', exponentformat='e'), template='plotly_dark', legend=dict(x=0.2, y=1.075), legend_orientation='h')
    fig.show(config=config)

def chart_mem(mat, os):
    dt_mem = np.loadtxt(INPUT_DIRECTORY + mat + '_' + os.lower() + '.txt', delimiter=',')

    fig = go.Figure()

    config = {'toImageButtonOptions': {'format': 'png', 'filename': 'chart', 'height': 1000, 'width': 2000, 'scale': 2}}

    fig.add_trace(go.Scatter(x=list(range(1, 10*(len(dt_mem)), 10)), y=dt_mem, name=mat))

    fig.update_layout(title=mat, showlegend=True, yaxis=dict(showexponent='all', exponentformat='e'), template='plotly_dark', legend=dict(x=0.2, y=1.075), legend_orientation='h')
    fig.show(config=config)

if __name__ == '__main__':
    chart_os('Darwin')
    chart_os('VM_Linux')
    chart_os('VM_Windows')
    chart_os('Linux')
    chart_os('Windows')

    chart_env('Python')
    chart_env('Matlab')

    chart_mem('StocF-1465', 'Darwin')
    chart_mem('Flan_1565', 'Darwin')
    chart_mem('StocF-1465', 'Linux')
    chart_mem('Flan_1565', 'Linux')
    chart_mem('StocF-1465', 'Windows')
    chart_mem('Flan_1565', 'Windows')