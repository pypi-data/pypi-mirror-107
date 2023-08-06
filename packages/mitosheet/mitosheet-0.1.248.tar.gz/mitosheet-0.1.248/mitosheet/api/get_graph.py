import io
import json
import pandas as pd
from mitosheet.mito_analytics import log
from mitosheet.sheet_functions.types.utils import get_mito_type
import plotly.express as px
import sys # In order to print in this file use sys.stdout.flush() once after the print statements.

# We have a variety of heuristics to make sure that we never send too much data
# to the frontend to display to the user. See comments below in the file for 
# which heuristics we use. They use the following constants 

# Max number of unique non-number items to display in a graph
# NOTE: make sure to change both in unison so they make sense
MAX_UNIQUE_NON_NUMBER_VALUES = 10_000
MAX_UNIQUE_NON_NUMBER_VALUES_COMMENT = '(Top 10k)'

# Max number of rows to display in a graph, if a non number exists
# NOTE: keep comment in sync also
MAX_ROWS_NON_NUMBER_EXISTS = 100_000
MAX_ROWS_NON_NUMBER_EXISTS_COMMENT = '(First 100k)'

# Some, uh, constants that are nice
X = 'x'
Y = 'y'

def filter_series_to_top_unique_values(
        main_series: pd.Series,
        num_unique_values: int,
        other_series=None
    ) -> pd.Series: 
    """
    Helper function for filtering the main_series down to the top most common
    num_unique_values at most. Will not change the series if there are less
    values than that.

    If you pass an other_series, will filter this to the same indexes as well, 
    making sure the columns stay the same size (which is necessary if you want
    to graph them).
    """
    if len(main_series) < num_unique_values or main_series.nunique() < num_unique_values:
        if other_series is None:
            return main_series
        else:
            return main_series, other_series

    value_counts_series = main_series.value_counts()

    most_frequent_values_list = value_counts_series.head(n=num_unique_values).index.tolist()
    filtered_main_series = main_series[main_series.isin(most_frequent_values_list)]
    if other_series is None:
        return filtered_main_series
    else:
        return filtered_main_series, other_series.iloc[filtered_main_series.index]


def get_single_column_graph(axis, df, column_header):
    """
    One Axis Graphs heuristics:
    1. Number Column - we do not filtering. These graphs are pretty efficient up to 1M rows
    2. Non-number column. We filter to the top 10k values, as the graphs get pretty laggy 
       beyond that
    """
    series: pd.Series = df[column_header]
    mito_type = get_mito_type(series)

    title = f'{column_header} Frequencies'

    filtered = False
    if mito_type != 'number_series':
        if series.nunique() > MAX_UNIQUE_NON_NUMBER_VALUES:
            title = f'{title} {MAX_UNIQUE_NON_NUMBER_VALUES_COMMENT}'
            series = filter_series_to_top_unique_values(
                series, 
                MAX_UNIQUE_NON_NUMBER_VALUES
            )
            filtered = True

    labels = {axis: ''}

    kwargs = {
        axis: series,
        'title': title,
        'labels': labels
    }

    fig = px.histogram(
        **kwargs        
    )

    log(f'get_{axis}_axis_graph_figure', {
        f'param_is_number_series_{axis}': mito_type == 'number_series',
        'param_filtered': filtered
    })

    return fig



def get_both_axis_graph_figure(
        df_x: pd.DataFrame, column_header_x_axis: pd.Series, 
        df_y: pd.DataFrame, column_header_y_axis: pd.Series
    ):
    """
    Two Axis Graphs heuristics:
    1. Two numbers columns: do nothing, display a scatter plot. These scale well. 
    2. At least one non-number column:
        - For each non-number column, make sure there are at most MAX_UNIQUE_NON_NUMBER_VALUES in it
        - Limit the number of rows to MAX_ROWS_NON_NUMBER_EXISTS
    """
    series_x: pd.Series = df_x[column_header_x_axis]
    series_y: pd.Series = df_y[column_header_y_axis]

    is_number_series_x = get_mito_type(series_x) == 'number_series' 
    is_number_series_y = get_mito_type(series_y) == 'number_series'

    labels = {
        'x': '', 
        'y': ''
    }

    if is_number_series_x and is_number_series_y:
        # Both are number series
        fig = px.scatter(
            x=series_x, 
            y=series_y, 
            title=f'{column_header_x_axis} vs {column_header_y_axis}',
            labels=labels
        )

        log('get_both_axis_graph_figure', {
            'param_is_number_series_x': is_number_series_x,
            'param_is_number_series_y': is_number_series_y,
        })

    else:
        title_x = f'{column_header_x_axis}'
        title_y = f'{column_header_y_axis}'

        filtered_x = False
        filtered_y = False
        filtered_rows = False

        if not is_number_series_x:
            # Fitler the x series first
            old_size = len(series_x)
            series_x, series_y = filter_series_to_top_unique_values(
                series_x, 
                MAX_UNIQUE_NON_NUMBER_VALUES,
                other_series=series_y
            )

            # Reset indexes, so we can filter again, if we filtered once
            if old_size > len(series_x):
                filtered_x = True
                series_x = series_x.reset_index(drop=True)
                series_y = series_y.reset_index(drop=True)
                title_x = f'{column_header_x_axis} {MAX_UNIQUE_NON_NUMBER_VALUES_COMMENT}'
    
        
        if not is_number_series_y:
            # Then filter the y series
            old_size = len(series_y)
            series_y, series_x = filter_series_to_top_unique_values(
                series_y, 
                MAX_UNIQUE_NON_NUMBER_VALUES,
                other_series=series_x
            )
            if len(series_y) < old_size:
                filtered_y = True
                title_y = f'{column_header_y_axis} {MAX_UNIQUE_NON_NUMBER_VALUES_COMMENT}'
        
        # Build the almost full title
        title = f'{title_x} vs {title_y}'

        if len(series_x) > MAX_ROWS_NON_NUMBER_EXISTS:
            filtered_rows = True
            series_x = series_x.head(MAX_ROWS_NON_NUMBER_EXISTS)
            series_y = series_y.head(MAX_ROWS_NON_NUMBER_EXISTS)
            title = f'{title} {MAX_ROWS_NON_NUMBER_EXISTS_COMMENT}'

        fig = px.scatter(
            x=series_x, 
            y=series_y, 
            title=title,
            labels=labels
        )

        log('get_both_axis_graph_figure', {
            'param_is_number_series_x': is_number_series_x,
            'param_is_number_series_y': is_number_series_y,
            'param_filtered_x': filtered_x,
            'param_filtered_y': filtered_y,
            'param_filtered_rows': filtered_rows,
        })

    fig.update_xaxes(tickangle=45)

    return fig


def get_html_and_script_from_figure(fig, height, width):
    """
    Given a plotly figure, generates HTML from it, and returns
    a dictonary with the div and script for the frontend.

    The plotly HTML generated by the write_html function call is a div with two children:
    1. a div that contains the id for the graph itself
    2. a script that actually builds the graph
    
    Because we have to dynamically execute the script, we split these into two 
    strings, to make them easier to do what we need on the frontend
    """
    # Send the graph back to the frontend
    buffer = io.StringIO()
    fig.write_html(
        buffer,
        full_html=False,
        include_plotlyjs=False,
        default_height=height,
        default_width=width,
    )
    
    original_html = buffer.getvalue()
    # First, we remove the main div, and the resulting whitespace, to just have the children
    original_html = original_html[5:]
    original_html = original_html[:-6]
    original_html = original_html.strip()

    # Then, we split the children into the div, and the script 
    # making sure to remove the script tag (so we can execute it)
    script_start = '<script type=\"text/javascript\">'
    script_end = '</script>'
    split_html = original_html.split(script_start)
    div = split_html[0]
    script = split_html[1][:-len(script_end)]

    return {
        'html': div,
        'script': script
    }


def get_graph(send, event, wsc):
    """
    Creates a graph of the passed parameters, and sends it back as a PNG
    string to the frontend for display.

    Params:
    - column_header_x_axis (optional)
    - sheet_index_x_axis (optional)
    - column_header_y_axis (optional)
    - sheet_index_y_axis (optional)
    - height (optional) - int representing the div width
    - width (optional) - int representing the div width

    If only an x axis is given, and if the series is a numeric series,
    will return a histogram. Otherwise, as long as there are less than 
    20 distinct items in the series, will return a bar chart of the 
    value count. Otherwise, will return nothing.
    """
    keys = event.keys()

    # Get the x axis params, if they were provided
    sheet_index_x_axis = event['sheet_index_x_axis'] if 'sheet_index_x_axis' in keys else None
    column_header_x_axis = event['column_header_x_axis'] if 'column_header_x_axis' in keys else None
    x_axis = sheet_index_x_axis is not None and column_header_x_axis is not None

    # Get the y axis params, if they were provided
    column_header_y_axis = event['column_header_y_axis'] if 'column_header_y_axis' in keys else None
    sheet_index_y_axis = event['sheet_index_y_axis'] if 'sheet_index_y_axis' in keys else None
    y_axis = sheet_index_y_axis is not None and column_header_y_axis is not None
    
    # Find the height and the width, defaulting to fill whatever container its in
    height = event["height"] if 'height' in keys else '100%'
    width = event["width"] if 'width' in keys else '100%'
    
    try:
        if not x_axis and not y_axis:
            # If no axes provided, return
            send({
                'event': 'api_response',
                'id': event['id'],
                'data': ''
            })
            return
        if x_axis and not y_axis:
            df_x = wsc.dfs[sheet_index_x_axis]
            fig = get_single_column_graph(
                X, df_x, column_header_x_axis
            )
        elif y_axis and not x_axis:
            df_y = wsc.dfs[sheet_index_y_axis]
            fig = get_single_column_graph(
                Y, df_y, column_header_y_axis
            )
        else:

            df_x: pd.DataFrame = wsc.dfs[sheet_index_x_axis]
            df_y: pd.DataFrame = wsc.dfs[sheet_index_y_axis]
            
            fig = get_both_axis_graph_figure(
                df_x, column_header_x_axis,
                df_y, column_header_y_axis
            )
        
        # Get rid of some of the default white space
        fig.update_layout(
            margin=dict(
                t=30, 
                b=0,
                r=10
            ),
        )

        html_and_script = get_html_and_script_from_figure(
            fig, height, width
        )

        send({
            'event': 'api_response',
            'id': event['id'],
            'data': json.dumps(html_and_script)
        })

    except Exception as e:
        # As not being able to make a graph is a non-critical error that doesn't
        # result from user interaction, we don't want to throw an error if something
        # weird happens, so we just return nothing in this case
        send({
            'event': 'api_response',
            'id': event['id'],
            'data': ''
        })