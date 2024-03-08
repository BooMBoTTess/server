import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, callback, Output, Input, ctx
from dash import html
import plotly.express as px
from plotly.graph_objs import YAxis

import src.data_reciever as get_data
from config import IP_ADDRESS

def create_dashboard_tables(df: pd.DataFrame, zamruk_id: int = -1, dep_id: int = -1):

    sort_order = ['Начальник отдела', 'Заместитель начальника отдела', 'Главный казначей', 'Консультант',
                  'Старший казначей', 'Главный специалист-эксперт', 'Казначей', 'Ведущий специалист-эксперт', 'Специалист 1 разряда']

    if zamruk_id == -1 and dep_id == -1:
        df_zamkruk_dash = df.groupby(by='Замрук', as_index=False, sort=False).sum().drop(['dep', 'post'], axis=1)

        df_deps_dash = df.groupby(by='dep', as_index=False, sort=False).sum().drop(['Замрук', 'post'], axis=1)

        df_post_dash = df.groupby(by='post', as_index=False, sort=False).sum().drop(['Замрук', 'dep'], axis=1)
    elif dep_id == -1:
        zamruk_target = df['Замрук'].drop_duplicates().reset_index(drop=True)[zamruk_id]
        df = df[df['Замрук'] == zamruk_target]

        df_zamkruk_dash = df.groupby(by='Замрук', as_index=False, sort=False).sum().drop(['dep', 'post'], axis=1)

        df_deps_dash = df.groupby(by='dep', as_index=False, sort=False).sum().drop(['Замрук', 'post'], axis=1)

        df_post_dash = df.groupby(by='post', as_index=False, sort=False).sum().drop(['Замрук', 'dep'], axis=1)
    else:
        dep_target = df['dep'].drop_duplicates().reset_index(drop=True)[dep_id]
        df = df[df['dep'] == dep_target]

        df_zamkruk_dash = df.groupby(by='Замрук', as_index=False, sort=False).sum().drop(['dep', 'post'], axis=1)

        df_deps_dash = df.groupby(by='dep', as_index=False, sort=False).sum().drop(['Замрук', 'post'], axis=1)

        df_post_dash = df.groupby(by='post', as_index=False, sort=False).sum().drop(['Замрук', 'dep'], axis=1)

    df_post_dash['post'] = df_post_dash['post'].astype("category")
    df_post_dash['post'] = df_post_dash['post'].cat.set_categories(sort_order)
    df_post_dash.sort_values(['post'], inplace=True)

    return df_zamkruk_dash, df_deps_dash, df_post_dash

def create_layout():

    app.layout = html.Div(
        children=[
            dcc.Location(id='url', refresh=False),
            html.Div(
                children=[
                    html.H1(children='Дашборд сотрудников отделов МБУ ФК'),
                    html.Div(children=[
                        html.Button('Сбросить фильтр', id='refresh-btn', n_clicks=0),
                        html.Div(children=[
                        html.H2(children=f'Количество штатных сотрудников: {staff_values[0]}', id='shtat_label'),
                        html.H2(children=f'Количество вакантных мест: {staff_values[1]}', id='vacant_label'),
                        html.H2(children=f'Всего сотрудников: {staff_values[2]}', id='full_label'),
                        ], className='data'
                        )
                    ], className='info'
                    )

                ], className='header'),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(
                                id='zamruk-graph',
                                figure=px.bar(df_zamruk_dash, y="Замрук", x=['Штат', 'Вакант'], orientation='h'),
                                config={
                                    'displayModeBar': False
                                }, className='up_graph_item'
                            ),
                            dcc.Graph(
                                id='post-graph',
                                figure=px.bar(df_post_dash.iloc[::-1], y="post", x=['Штат', 'Вакант'], orientation='h'),
                                config={
                                    'displayModeBar': False
                                }, className='up_graph_item'
                            )
                        ], className='up_wrap_graph'
                    ),
                    dcc.Graph(
                        id='dep-graph',
                        figure=px.bar(df_deps_dash, y="dep", x=['Штат', 'Вакант'], orientation='h'),
                        config={
                            'displayModeBar': False
                        },

                    ),
                ], className='wrap_graph'
            )
        ],

    )
    return app.layout

def error_layout():
    app.layout = html.Div(
        children=[
                dcc.Location(id='url', refresh=False),
                html.H1(children='Нет доступа к данным')
        ]
    )
    return app.layout

df, staff_values = get_data.main()
app = dash.Dash(__name__)
if type(df) != pd.DataFrame:
    print('data not found')
    app.layout = error_layout()
else:
    df_zamruk_dash, df_deps_dash, df_post_dash = create_dashboard_tables(df.copy())
    external_stylesheets = ['style.css']
    app.layout = create_layout()


@app.callback([Output('post-graph', 'figure'), Output('dep-graph', 'figure'), Output('zamruk-graph', 'figure'),
               Output('shtat_label', 'children'), Output('vacant_label', 'children'), Output('full_label', 'children')],

              [Input('url', 'pathname'), Input('refresh-btn', 'n_clicks'),
               Input('zamruk-graph', 'clickData'), Input('dep-graph', 'clickData')])
def display_page(pathname, refresh_button_click, zamruk_clickData, dep_ckickData):
    pathname = str(pathname)
    print("PATHNAME = ", pathname)
    print(zamruk_clickData, dep_ckickData)
    print(ctx.triggered_id)
    pathname = pathname.lstrip('/')
    df, staff_values = get_data.main()

    template = 'plotly_dark'
    if ctx.triggered_id == 'refresh-btn':
        zamruk_clickData, dep_ckickData = (None, None)

    if ctx.triggered_id == 'zamruk-graph':
        df = df[df['Замрук'] == zamruk_clickData['points'][0]['y']]

    if ctx.triggered_id == 'dep-graph':
        df = df[df['dep'] == dep_ckickData['points'][0]['y']]

    if not '.' in pathname:
        df_zamruk_dash, df_deps_dash, df_post_dash = create_dashboard_tables(df.copy())
    else:
        key, value = pathname.split('.')
        key = int(key)
        value = int(value)
        if key == 1:
            df_zamruk_dash, df_deps_dash, df_post_dash = create_dashboard_tables(df.copy(), zamruk_id=value)
        elif key == 3:
            df_zamruk_dash, df_deps_dash, df_post_dash = create_dashboard_tables(df.copy(), dep_id=value)



    fig_zamruk = px.bar(df_zamruk_dash.iloc[::-1].sort_values('Всего', ascending=False), y="Замрук", x=['Штат', 'Вакант'], orientation='h',
                        color_discrete_map={'Штат': '#397dd6', 'Вакант': '#00dbcd'}, template=template, text_auto=True,

                        )
    fig_dep = px.bar(df_deps_dash.iloc[::-1], y="dep", x=['Штат', 'Вакант'], orientation='h',
                     color_discrete_map={'Штат': '#397dd6', 'Вакант': '#00dbcd'}, template=template, text_auto=True)
    fig_post = px.bar(df_post_dash.iloc[::-1], y="post", x=['Штат', 'Вакант'], orientation='h',
                      color_discrete_map={'Штат': '#397dd6', 'Вакант': '#00dbcd'}, template=template, text_auto=True)


    fig_zamruk.update_traces(textfont_size=12, textangle=0, textposition="inside", hovertemplate = None,
                             hoverinfo='none', cliponaxis=False, marker_line_color='white', marker_line_width=1.5)
    fig_dep.update_traces(textfont_size=12, textangle=0, textposition="inside", hovertemplate = None,
                          hoverinfo='none', cliponaxis=False, marker_line_color='white', marker_line_width=1.5)
    fig_post.update_traces(textfont_size=12, textangle=0, textposition="inside", hovertemplate = None,
                           hoverinfo='none', cliponaxis=False, marker_line_color='white', marker_line_width=1.5)

    fig_zamruk.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1),
        legend_title_text='Количество сотрудников согласно списку заместителей должностей',
        xaxis_title='',
        yaxis_title='',
    )
    fig_dep.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1),
        legend_title_text='Количество сотрудников согласно отделам',
        xaxis_title='',
        yaxis_title='',
    )
    fig_post.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1),
        legend_title_text='Количество сотрудников согласно должностям',
        xaxis_title='',
        yaxis_title='',
    )


    return fig_post, fig_dep, fig_zamruk, f'Количество штатных сотрудников: {staff_values[0]}',\
        f'Количество вакантных мест: {staff_values[1]}', f'Всего сотрудников: {staff_values[2]}'


if __name__ == '__main__':
    app.run(debug=False, host=IP_ADDRESS, port=8050)
