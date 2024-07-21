import base64
import io
import json
import flask
import pandas as pd

from dash import Dash, dash_table, html, dcc, Input, Output, State
import plotly.graph_objects as go


df = pd.DataFrame(columns=["status"])


app = Dash(__name__)

def make_link_message_url(row):
    content = row['message']
    filename = str(row['message_id'])
    encoded_content = base64.urlsafe_b64encode(json.dumps(content).encode()).decode()
    return f'[Download](download/{filename}/{encoded_content})'



@app.server.route('/download/<msg_id>/<path:path>')
def serve_static(msg_id, path):
    content = json.loads(base64.urlsafe_b64decode(path.encode()).decode())
    buffer = io.BytesIO()
    buffer.write(content.encode())
    buffer.seek(0)
    return flask.send_file(buffer, as_attachment=True, download_name=f'message_{msg_id}.json', mimetype='application/json')


def generate_table():
    ignored = ["date", "download", "message"]

    return dash_table.DataTable(
        id='status-table',
        columns=[{"name": i, "id": i} for i in df.columns if i not in ignored] + [
            {'name': 'message', 'id': 'download', 'presentation': 'markdown'}
        ],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        page_action="native",
        page_current=0,
        page_size=25,

        style_cell={'textAlign': 'left'},
        style_cell_conditional=[
            {
                'if': {'column_id': column_id},
                'textAlign': 'center'
            }
            for column_id in ["message_id", "publication_id", "documentum_id", "status"]
        ],
        style_header={
            'backgroundColor': 'blue',
            'fontWeight': 'bold',
            'color': 'red',
            'textAlign': 'center',
            'font-family':'sans-serif',
        },
        style_filter={
            'backgroundColor': 'blue',
            'fontWeight': 'bold',
            'color': 'red',
            'textAlign': 'center',
            'font-family':'sans-serif',
        },
        style_data={
            'width': '150px', 
            'minWidth': '150px', 
            'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'backgroundColor': 'yellow',
            'font-family':'consolas',
        },
        style_data_conditional=[
            {
                'if': {'column_id': 'download'},
                'width': '50px',
                'minWidth': '50px', 
                'maxWidth': '50px',
            },
        ]
    )

def serve_layout():
    global df
    df = pd.read_pickle('data.pkl')

    df["download"] = df.apply(make_link_message_url, axis=1)

    df['date'] = df['created_at'].dt.date
    # df["created_at"] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # df["updated_at"] = df['updated_at'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Group by date and status and count occurrences
    pivot_table = (
        df
        .groupby(['date', 'status'])
        .size()
        .reset_index(name='count')
        .pivot(index='status', columns='date', values='count')
        .fillna(0)
    )

    selected_status = json.dumps([
        {'status': status, 'visible': True}
        for status in sorted(df['status'].unique())
    ])

    

    return html.Div([
        dcc.Store(id='selected-statuses', data=selected_status),
        dcc.Store(id='pivot-status', data=pivot_table.to_json(orient="index", date_format='iso')),
        html.Div([
            html.H1('Fricadel Dashboard', className="centered"),
        ], className="container"),
        html.Div([
            dcc.Graph(id='status-graph'),
        ], className="container"),
        html.Div([
            generate_table()
        ]),
    ])


@app.callback(
    Output('status-table', 'data'),
    Input('selected-statuses', 'data')
)
def build_table(selected_statuses) -> dash_table.DataTable:
    print("\nFiltering the data table")

    selected_statuses = json.loads(selected_statuses)
    visible_status = [status["status"] for status in selected_statuses if status["visible"] is True]

    return df[df["status"].isin(visible_status)].to_dict(orient='records')


@app.callback(
    Output('status-graph', 'figure'),
    Input('selected-statuses', 'data'),
    State('pivot-status', 'data'),
)
def daily_barplot(selected_statuses, pivot_status) -> go.Figure:
    print("\nUpdating status graph")
    selected_statuses = json.loads(selected_statuses)
    pivot_status = json.loads(pivot_status)

    fig = go.Figure()

    # Add bars for each status
    for status_data in selected_statuses:
        status = status_data['status']
        visible = status_data["visible"]

        x, y = list(pivot_status[status].keys()), list(pivot_status[status].values())
        fig.add_trace(go.Bar(
            x=x,
            y=y,
            name=status,
            visible=visible
        ))

    # Update layout for better readability
    fig.update_layout(
        barmode='stack',
        title='Count of status per day',
        xaxis_title='Date',
        yaxis_title='Count',
        legend_title='Status',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    
    return fig


@app.callback(
    Output('selected-statuses', 'data'),
    Input('status-graph', 'restyleData'),
    State('selected-statuses', 'data')
)
def update_selected_statuses(restyleData, selected_statuses):
    print("\nUpdate selected statuses")
    if restyleData is None:
        return selected_statuses
    
    selected_statuses = json.loads(selected_statuses)

    idx_status = restyleData[1][0]
    visibility = restyleData[0]["visible"][0]
    selected_statuses[idx_status]["visible"] = visibility

    return json.dumps(selected_statuses)




app.layout = serve_layout()

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)