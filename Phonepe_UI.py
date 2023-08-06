import io
import pandas as pd
import streamlit as st
import ydata_profiling
import xlsxwriter
from streamlit_player import st_player
from streamlit_pandas_profiling import st_profile_report
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space

# Data Prep

# Reading from csv so as to make it work for everyone in streamlit cloud app...
# Otherwise there's another file named Home_with_SQL_Part.py in Miscellaneous directory in this same repo...

agg_trans_df = pd.read_csv(r'C:\Users\Jaya Prakash\Desktop\Phonepe_pulse\CSV files\agg_trans.csv')
agg_user_df = pd.read_csv(r'C:\Users\Jaya Prakash\Desktop\Phonepe_pulse\CSV files\agg_user.csv')
map_trans_df = pd.read_csv(r'C:\Users\Jaya Prakash\Desktop\Phonepe_pulse\CSV files\map_trans.csv')
map_user_df = pd.read_csv(r'C:\Users\Jaya Prakash\Desktop\Phonepe_pulse\CSV files\map_user.csv')
top_trans_dist_df = pd.read_csv(r'C:\Users\Jaya Prakash\Desktop\Phonepe_pulse\CSV files\top_trans_dist.csv')
top_trans_pin_df = pd.read_csv(r'C:\Users\Jaya Prakash\Desktop\Phonepe_pulse\CSV files\top_trans_pin.csv')
top_user_dist_df = pd.read_csv(r'C:\Users\Jaya Prakash\Desktop\Phonepe_pulse\CSV files\top_user_dist.csv')
top_user_pin_df = pd.read_csv(r'C:\Users\Jaya Prakash\Desktop\Phonepe_pulse\CSV files\top_user_pin.csv')

if 'options' not in st.session_state:
    st.session_state['options'] = {
        'Aggregate Transaction': 'agg_trans_df',
        'Aggregate User': 'agg_user_df',
        'Map Transaction': 'map_trans_df',
        'Map User': 'map_user_df',
        'Top Transaction Districtwise': 'top_trans_dist_df',
        'Top Transaction Pincodewise': 'top_trans_pin_df',
        'Top User Districtwise': 'top_user_dist_df',
        'Top User Pincodewise': 'top_user_pin_df'
    }

df_names = [
    var_name for var_name in globals()
    if isinstance(globals()[var_name], pd.core.frame.DataFrame) and var_name.endswith('_df')
]

if 'df_list' not in st.session_state:
    st.session_state['df_list'] = []

    for var_name in df_names:
        st.session_state[var_name] = globals()[var_name]
        st.session_state['df_list'].append(var_name)


def year_to_str(df):
    df['Year'] = df["Year"].astype(str)


for df_name in st.session_state['df_list']:
    df = globals()[df_name]
    year_to_str(df)
    globals()[df_name] = df

# App


st.set_page_config(
    page_title='PhonePe Data Visualization', layout='wide',
    page_icon='Related Images and Videos/Logo.png'
)

st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title(':blue[PhonePe Data Visualization]')

add_vertical_space(2)

phonepe_description = """PhonePe has launched PhonePe Pulse, a data analytics platform that provides insights into
                        how Indians are using digital payments. With over 30 crore registered users and 2000 crore
                        transactions, PhonePe, India's largest digital payments platform with 46% UPI market share,
                        has a unique ring-side view into the Indian digital payments story. Through this app, you
                        can now easily access and visualize the data provided by PhonePe Pulse, gaining deep
                        insights and interesting trends into how India transacts with digital payments."""

st.write(phonepe_description)

add_vertical_space(2)

st_player(url="https://www.youtube.com/watch?v=c_1H6vivsiA", height=480)

add_vertical_space(2)

# # Provide the correct file path for the image
# image_path = "C:/Users/Jaya Prakash/Downloads/phonepe.jpg"  # Use forward slashes or escape backslashes
#
# # Display the image
# st.image(image_path, caption="PhonePe Image", use_column_width=True)


add_vertical_space(2)

col1, col2, col3 = st.columns(3)

total_reg_users = top_user_dist_df['Registered_users'].sum()
col1.metric(
    label='Total Registered Users',
    value='{:.2f} Cr'.format(total_reg_users / 100000000),
    delta='Forward Trend'
)

total_app_opens = map_user_df['App_opens'].sum()
col2.metric(
    label='Total App Opens', value='{:.2f} Cr'.format(total_app_opens / 100000000),
    delta='Forward Trend'
)

col3.metric(label='Total Transaction Count', value='2000 Cr +', delta='Forward Trend')

style_metric_cards(background_color='200329')

add_vertical_space(2)

# st.image(r'C:\Users\Jaya Prakash\Desktop\Phonepe_pulse\Related Images and Videos\Pulse.gif', use_column_width=True)

add_vertical_space(2)

col, buff = st.columns([2, 4])

option = col.selectbox(
    label='Select Dataset',
    options=list(st.session_state['options'].keys()),
    key='df'
)

tab1, tab2 = st.tabs(['Report and Dataset', 'Download Dataset'])

with tab1:
    column1, column2, buffer = st.columns([2, 2, 4])

    show_profile = column1.button(label='Show Detailed Report', key='show')
    show_df = column2.button(label='Show Dataset', key='show_df')

    if show_profile:
        df_name = st.session_state['options'][option]
        df = globals()[df_name]
        pr = df.profile_report()
        st_profile_report(pr)

    if show_df:
        st.data_editor(
            data=globals()[st.session_state['options'][option]],
            use_container_width=True
        )

with tab2:
    col1, col2, col3 = st.columns(3)

    df_name = st.session_state['options'][option]
    df = globals()[df_name]

    csv = df.to_csv()
    json = df.to_json(orient='records')
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, engine='xlsxwriter', index=False)
    excel_bytes = excel_buffer.getvalue()

    col1.download_button(
        "Download CSV file", data=csv,
        file_name=f'{option}.csv',
        mime='text/csv', key='csv'
    )
    col2.download_button(
        "Download JSON file", data=json,
        file_name=f'{option}.json',
        mime='application/json', key='json'
    )
    col3.download_button("Download Excel file", data=excel_bytes,
                         file_name=f'{option}.xlsx',
                         mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         key='excel'
                         )



import streamlit as st
import plotly.express as px
import json
from streamlit_extras.add_vertical_space import add_vertical_space


# Data Prep


agg_trans = st.session_state["agg_trans_df"]
map_trans = st.session_state["map_trans_df"]
map_user = st.session_state["map_user_df"]


#1

trans_type_count = agg_trans.groupby('Transaction_type')['Transaction_count'].sum()

total_trans_count = agg_trans['Transaction_count'].sum()

trans_type_perc = round(trans_type_count / total_trans_count * 100, 2).reset_index()

trans_type_fig = px.pie(
                        trans_type_perc, names='Transaction_type',
                        values='Transaction_count', hole=.65,
                        hover_data={'Transaction_count': False}
                        )

trans_type_fig.update_layout(width = 900, height = 500)


#2


trans_state = agg_trans.groupby('State')['Transaction_count'].sum().reset_index()
trans_state_sorted = trans_state.sort_values(by='Transaction_count', ascending=False).head(15)

trans_state_fig = px.bar(
                         trans_state_sorted, x='Transaction_count',
                         y='State', orientation='h',
                         text='Transaction_count', text_auto='.2s',
                         labels = {'Transaction_count': "Transaction Count"}
                         )

trans_state_fig.update_layout(
                                yaxis=dict(autorange="reversed"),
                                width = 900, height = 500
                                )


#3


trans_district = map_trans.groupby(['State', 'District'])[['Transaction_count']].sum().reset_index()

trans_district_sorted = trans_district.sort_values(by='Transaction_count', ascending=False).head(15)

trans_district_fig = px.bar(
                            trans_district_sorted, x='Transaction_count',
                            y='District', orientation='h',
                            text='Transaction_count', text_auto='.2s',
                            labels = {'Transaction_count': "Transaction Count"},
                            hover_name='State',
                            hover_data={'State': False, 'District': True}
                            )

trans_district_fig.update_layout(
                                 yaxis = dict(autorange="reversed"),
                                 width = 900, height = 500
                                 )


#4


user_state = map_user.groupby('State')['Registered_users'].sum().reset_index()

with open(r"C:/Users/Jaya Prakash/Desktop/Phonepe_pulse/CSV files/india_states.json") as f:
    geojson = json.load(f)

if 'geojson' not in st.session_state:
    st.session_state["geojson"] = geojson

user_state_fig = px.choropleth(
                                user_state, geojson = geojson,
                                locations = 'State',
                                featureidkey = 'properties.ST_NM',
                                color='Registered_users', projection = 'orthographic',
                                labels = {'Registered_users': "Registered Users"},
                                color_continuous_scale = 'reds'
                                )

user_state_fig.update_geos(fitbounds='locations', visible=False)
user_state_fig.update_layout(height=600, width=900)


# App


# st.set_page_config(page_title = 'Overview', layout = 'wide', page_icon = 'C:/Users/Jaya Prakash/Desktop/Phonepe_pulse/CSV files/Logo.png')

st.title(':blue[Overview]')

add_vertical_space(3)

#1

st.subheader(":blue[Transaction Breakdown by Type]")

st.plotly_chart(trans_type_fig)

#2

st.subheader(":blue[Transaction Count by State]")

st.plotly_chart(trans_state_fig)

#3

st.subheader(":blue[Transaction Count by District]")

st.plotly_chart(trans_district_fig)

#4

st.subheader(':blue[Registered User Count by State]')

st.plotly_chart(user_state_fig, use_container_width = True)


