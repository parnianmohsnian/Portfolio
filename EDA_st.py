import streamlit as st
import pandas as pd
import plotly.express as px
import json
import matplotlib.pyplot as plt
import seaborn as sns

# Load the GeoJSON data
india_states = json.load(open("/home/parnian/digipay/states_india.geojson", "r"))

# Create a mapping of state names to IDs
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]

# Load your dataframe 'df' here
def load_data():
    # Load your data into a DataFrame (Replace this with your actual data loading code)
    # Example:
    df = pd.read_csv('/home/parnian/digipay/Training Data.csv')
    return df

def explore_data(df):
    st.subheader('Exploratory Data Analysis')

    st.write("### Data Overview")
    if st.checkbox('Show Data'):
        st.write(df)

    st.write("### Age Distribution based on Risk_Flag")
    Age = df.groupby(by=["Risk_Flag", "Age"])["Id"].count()
    Age_df = pd.DataFrame(Age).reset_index()
    fig_age = plt.figure()
    sns.barplot(data=Age_df, x="Age", y="Id", hue="Risk_Flag")
    st.pyplot(fig_age)

    st.write("### Car Ownership Distribution based on Risk_Flag")
    Car_Ownership = df.groupby(by=["Risk_Flag", "Car_Ownership"])["Id"].count()
    Car_Ownership_df = pd.DataFrame(Car_Ownership).reset_index()
    fig_car_ownership = plt.figure()
    sns.barplot(data=Car_Ownership_df, x="Car_Ownership", y="Id", hue="Risk_Flag")
    st.pyplot(fig_car_ownership)

    st.write("### STATE Distribution based on Risk_Flag")
    STATE = df.groupby(by=["Risk_Flag", "STATE"])["Id"].count()
    STATE_df = pd.DataFrame(STATE).reset_index()
    fig_STATE = plt.figure()
    sns.barplot(data=STATE_df, x="STATE", y="Id", hue="Risk_Flag")
    st.pyplot(fig_STATE)

    st.write("### Married/Single Distribution based on Risk_Flag")
    Married_Single = df.groupby(by=["Risk_Flag", "Married/Single"])["Id"].count()
    Married_Single_df = pd.DataFrame(Married_Single).reset_index()
    fig_ms = plt.figure()
    sns.barplot(data=Married_Single_df, x="Married/Single", y="Id", hue="Risk_Flag")
    st.pyplot(fig_ms)

    st.write("### Car ownership and Age based on Risk_Flag")
    fig_box_car_age = plt.figure()
    sns.boxplot(data=df, x="Car_Ownership", y="Age", hue="Risk_Flag")
    st.pyplot(fig_box_car_age)

    st.write("### House ownership and Age based on Risk_Flag")
    fig_box_house_age = plt.figure()
    sns.boxplot(data=df, x="House_Ownership", y="Age", hue="Risk_Flag")
    st.pyplot(fig_box_house_age)

    st.write("### Car ownership and Income based on Risk_Flag")
    fig_box_car_income = plt.figure()
    sns.boxplot(data=df, x="Car_Ownership", y="Income", hue="Risk_Flag")
    st.pyplot(fig_box_car_income)


    st.write("### House ownership and Income based on Risk_Flag")
    fig_box_house_income = plt.figure()
    sns.boxplot(data=df, x="House_Ownership", y="Income", hue="Risk_Flag")
    st.pyplot(fig_box_house_income)




    st.write("### House ownership based on Risk_Flag")
    fig_bar_house = plt.figure()
    sns.countplot(df, x="House_Ownership", hue="Risk_Flag")
    st.pyplot(fig_bar_house)



   

    
    fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(18, 15))
    plt.subplots_adjust(hspace=1)
    fig.suptitle("Top 15 Countsplots", fontsize=18, y=0.95)

    for col, ax in zip(['CITY', 'STATE', 'Profession'], axs.ravel()):
        countplot = sns.countplot(data=df, x=col, order=df[col].value_counts().iloc[:15].index, ax=ax)
        countplot.set_title("Top 15 " + col)
        countplot.set_xticklabels(countplot.get_xticklabels(), rotation=45, horizontalalignment='right')
        for p in countplot.patches:
            countplot.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    st.pyplot(fig)

    st.write("### Age Distribution based on Risk_Flag")
    fig_profession = plt.figure()
    sns.countplot(y="Profession", data=df, palette="Set3",
                   order=df['Profession'].value_counts().index,
                   dodge=False)
    st.pyplot(fig_profession)


    
# Create a Streamlit app
def main():
    st.title('Credit Risk Analysis')

    # Load data
    df = load_data()
    df['STATE'] = df['STATE'].str.replace('_', " ")
    df["Id_state"] = df["STATE"].map(state_id_map)

    # Group by 'Risk_Flag' and 'Id_state' and calculate median income
    df1 = df.groupby(['Risk_Flag', 'Id_state'])['Income'].median().reset_index()

    # Group by 'Risk_Flag' and 'Id_state' and calculate median car ownership
    df['Car_Ownership'] = pd.to_numeric(df['Car_Ownership'], errors='coerce')
    df_car = df.groupby(['Risk_Flag', 'Id_state'])['Car_Ownership'].median().reset_index()


    # Display choropleth map for income median per state when Risk_Flag is True
    fig_income_true = px.choropleth_mapbox(
        df1[df1['Risk_Flag'] == True],
        locations="Id_state",
        geojson=india_states,
        color="Income",
        hover_name="Id_state",
        title="Risk flag true & income median per state",
        mapbox_style="stamen-watercolor",
        center={"lat": 24, "lon": 78},
        zoom=3,
        opacity=0.5
    )
    st.plotly_chart(fig_income_true)

    # Display choropleth map for income median per state when Risk_Flag is False
    fig_income_false = px.choropleth_mapbox(
        df1[df1['Risk_Flag'] == False],
        locations="Id_state",
        geojson=india_states,
        color="Income",
        hover_name="Id_state",
        title="Risk flag false & income median per state",
        mapbox_style="stamen-watercolor",
        center={"lat": 24, "lon": 78},
        zoom=3,
        opacity=0.5
    )
    st.plotly_chart(fig_income_false)

    # Display choropleth map for car ownership median per state when Risk_Flag is False
    fig_car_ownership = px.choropleth_mapbox(
        df_car[df_car['Risk_Flag'] == False],
        locations="Id_state",
        geojson=india_states,
        color="Car_Ownership",
        hover_name="Id_state",
        title="Risk flag false & car ownership median per state",
        mapbox_style="stamen-watercolor",
        center={"lat": 24, "lon": 78},
        zoom=3,
        opacity=0.5
    )
    st.plotly_chart(fig_car_ownership)
    
    st.title('Credit Risk Analysis')
    df = load_data()
    explore_data(df)



if __name__ == "__main__":
    main()
