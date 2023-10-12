import pandas as pd
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

insights_dict = {
    "Equipment Monitoring" : "Accessibility",
    "Investment Returns" : "Budgets",
    "Energy Efficiency" : "Energy Usage",
    "Maintenance Schedules" : "Safety Incidents",
    "Client Satisfaction" : "Tenant Satisfaction",
    "New Leases" : "Leases, Renewal Rate",
    "Lease Expirations" : "Leases, Expiring",
    "Occupancy Rate" : "Leases, Occupancy",
    "Preventative Maintenance" : "Work Orders, Preventative",
    "Work Order Completion" : "Work Orders",
    "Asset Valuation" : ""
}

@app.route("/insights", methods=['GET'])
def get_insights():
    name = request.args.get('name', type=str)
    df_users = pd.read_csv("recommendation_engine_users.csv")
    df_property = pd.read_csv("property_insights_extended.csv")
    df_roles = pd.read_csv("roles_duties_and_insights.csv")

    df_property[['Property Address', 'City']] = df_property['Property Address'].str.split(', ', expand=True)

    df_filtered = get_filtered_df(df_property, df_users, name)
    print(df_filtered)

    relevant_insights = getRelevantInsights(name, df_users, df_roles)

    relevant_array = relevant_insights.split(", ")
    insights1 = insights_dict[relevant_array[0]]
    insights2 = insights_dict[relevant_array[1]]

    insights1_array = insights1.split(", ")
    insights2_array = insights2.split(", ")

    if len(insights1_array) == 1:
        df1_insights = df_filtered.loc[df_filtered['Insight 1'] == insights1_array[0]]
        print(df1_insights)
    elif len(insights1_array) == 2:
        df1_insights1 = df_filtered.loc[df_filtered['Insight 1'] == insights1_array[0]]
        df1_insights = df1_insights1.loc[df1_insights1['Insight 2'] == insights1_array[1]]

    
    if len(insights2_array) == 1:
        df2_insights = df_filtered.loc[df_filtered['Insight 1'] == insights2_array[0]]
    elif len(insights2_array) == 2:
        df2_insights1 = df_filtered.loc[df_filtered['Insight 1'] == insights2_array[0]]
        df2_insights = df1_insights1.loc[df1_insights1['Insight 2'] == insights2_array[1]]

    final_df = pd.concat([df1_insights, df2_insights])

    selected_columns = ['Property Address', 'Driver', 'Criticality']

    final_df1 = final_df.loc[final_df['Criticality'] == 'Critical']
    final_df2 = final_df.loc[final_df['Criticality'] == 'High']
    final_df3 = final_df.loc[final_df['Criticality'] == 'Medium']
    final_df4 = final_df.loc[final_df['Criticality'] == 'Low']

    
    out_df = pd.concat([final_df1, final_df2, final_df3, final_df4])

    array_of_objects = [row[selected_columns].to_dict() for _, row in out_df.head(5).iterrows()]
    print(array_of_objects)
    return jsonify(array_of_objects)

def getRelevantInsights(name, df, df_roles):
    role = df.loc[df['Name'] == name, 'Role'].iloc[0]
    insights = df_roles.loc[df_roles['Role'] == role, 'Relevant Insights'].iloc[0]
    return insights

def get_filtered_df(df_property, df_users, name):
    client = df_users.loc[df_users['Name'] == name, 'Client'].iloc[0]
    location = df_users.loc[df_users['Name'] == name, 'Location'].iloc[0]
    
    df_client = df_property.loc[df_property['Account'] == client]
    df_city = df_client.loc[df_client['City'] == location]
    return df_city

if (__name__ == '__main__'):
    app.run()