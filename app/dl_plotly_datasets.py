import pandas as pd
from dash import Dash, html, Input, Output, dash_table, dcc
from dash.exceptions import PreventUpdate
from df_manage import DfManage
import plotly_datasets_info
import pyperclip

# Create the actual state (instance) of the application
app = Dash(__name__)

# Create an instance of a class that processes DataFrame Object
df_manage = DfManage()

# DataFrame object to be displayed in the data_table component at startup
data_list = [['data1',1],['data2',2]] 
df_base = pd.DataFrame(data_list,columns=['culumn1','culumn2'])

# Set plotly datasets information
table_name_list = plotly_datasets_info.datasets_list

# Number of rows per page linking Data_table and DataFrame
ROW_PER_PAGE = 20

# Layout definition processing
title_div = html.Div(html.H3('Download Plotly Dataset'))

# Dropdown
drop_down_div = html.Div([
    html.Div('Select Dataset:',style={'font-weight': 'bold'}),
    dcc.Dropdown(
        id='drop_down_div',
        options=[dict(label=x,value=x) for x in table_name_list],
        value=None,
        style={'margin-top': '10px','margin-bottom': '10px','width': '500px'}
    )
])

# Change the style of the export button
# https://community.plotly.com/t/styling-the-export-button-in-datatable/38798/9
export_button = html.Button(
    'CSV Download', 
    id='export_table',
    style={'backgroundColor': 'paleturquoise','margin-top': '10px'}, 
    **{'data-text': ''}
)

# div tag to display data in the output table
table_out_div = html.Div(id='data_table_out',style={'margin-bottom': '10px'})

# DataTable
dash_data_table = dash_table.DataTable(
    id='data_table',
    columns=[dict(name=str(i),id=str(i)) for i in df_base.columns],
    data=df_base.to_dict('records'),
    fixed_rows=dict(headers=True,data=0),
    # all three widths are needed
    style_cell=dict(
        textAlign='left',
        minWidth='50px',
        width='100px',
        maxWidth='200px',
        overflow='hidden',
        textOverflow='ellipsis',
    ),
    style_header=dict(backgroundColor='paleturquoise',textAlign='center'),
    style_data=dict(backgroundColor='lavender'),
    sort_action='none',
    export_format='csv',
    page_size = 10,
    style_table=dict(height='375px',overflowY='auto')
)

# DataTable Layout Definition
table_div = html.Div(
    [
        dash_data_table,
        export_button
    ],
    id='table_div',style={'display':'none'}
)

# Application Layout Definition
app.layout = html.Div(
    [
        title_div,
        drop_down_div, 
        table_out_div, 
        table_div
    ]
)

# Callback function to update and display data_table triggered by Dropdown
@app.callback(
        Output('data_table', 'data'),
        Output('data_table', 'columns'),
        Output('data_table', 'page_size'),
        Output('data_table', 'page_current'),
        Output('data_table', 'selected_cells'),
        Output('data_table', 'active_cell'),
        Output('table_div', 'style'),
        Input('drop_down_div', 'value')
        )
def update_table(value):
    if value in table_name_list:
        # copy filename
        filename = value.replace('.csv', '')
        pyperclip.copy(filename)
        # Replace spaces with %20
        if ' ' in value:
            value = value.replace(' ', '%20')
        data_url = 'https://raw.githubusercontent.com/plotly/datasets/master/' + value
        df = pd.read_csv(data_url)
        df_manage.df_data = df
        data = df.to_dict('records')
        columns = [dict(name=str(i),id=str(i),deletable=False,renamable=False) for i in df.columns]
        page_size = ROW_PER_PAGE
        page_current = 0
        selected_cells = []
        active_cell = None
        return data, columns, page_size, page_current, selected_cells, active_cell, {'display':'inline'}
    # https://dash.plotly.com/advanced-callbacks
    # https://community.plotly.com/t/expected-the-output-type-to-be-a-list-or-tuple-but-got-none/50634
    raise PreventUpdate

# JS callback to call click() on the default export button
# https://community.plotly.com/t/moving-datatable-export-button-and-changing-text/39115/2
app.clientside_callback(
    '''
    function(n_clicks) {
        if (n_clicks > 0)
            document.querySelector('#data_table button.export').click()
        return ''
    }
    ''',
    # Specify custom data attributes as component_property
    Output('export_table', 'data-text'),
    Input('export_table', 'n_clicks')
)

# Callback function to update data_table_out triggered by cell selection and page switching
@app.callback(
    Output('data_table_out', 'children'),
    Input('data_table', 'active_cell'),
    Input('data_table', 'page_current')
    )
def get_active_cell(active_cell,page_current):
    df = df_manage.df_data
    if page_current is None:
        page_num = 0
    else:
        page_num = page_current
    df_manage.df_page_num = page_num

    if active_cell:
        page_num = df_manage.df_page_num
        row = active_cell['row'] + page_num * ROW_PER_PAGE
        column = active_cell['column']
        column_id = active_cell['column_id']
        cell_data = df.iloc[row][active_cell['column_id']]
        text = f'\'{cell_data}\' from table row: {row} culumn: {column} column_id: {column_id}'
    else:
        text = 'No data selection'
    return html.Div([
        html.Div('Select Table Data: ',style={'font-weight': 'bold'}),
        html.Div(children=text,style={'margin-left': '5px'})
    ],
    style={'display':'inline-flex'}
    )

if __name__ == '__main__':
    app.run(debug=True)