from flask import Flask, render_template, jsonify
import requests
from datetime import datetime, timedelta
import pytz
import json
import plotly
import plotly.graph_objs as go

user = 'cdeardon@axonify.com'
api_key = 'FbOZzOWDyP94zUCNA8gkesdHi0aKVaIgkIzniVEX7t6fKSJAaiuJ4Q==-EBBFCE2E7C74B6D85F24C847E4A8F16F11BCF2B6&Key=FbOZzOWDyP94zUCNA8gkesdHi0aKVaIgkIzniVEX7t6fKSJAaiuJ4Q==-EBBFCE2E7C74B6D85F24C847E4A8F16F11BCF2B6'
app = Flask(__name__)

@app.route('/')
def index():
    trace = go.Scatter(x=[1, 2, 3], y=[4, 5, 6])
    data = [trace]
    layout = go.Layout(title='My Scatter Plot')
    figure = go.Figure(data=data, layout=layout)
    figure_json = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)

    knowledge_map = f"https://demo-cdeardon.axonify.com/axonify/api/v2/users/{user}/knowledgemap?api_token=FbOZzOWDyP94zUCNA8gkesdHi0aKVaIgkIzniVEX7t6fKSJAaiuJ4Q==-EBBFCE2E7C74B6D85F24C847E4A8F16F11BCF2B6&Key=FbOZzOWDyP94zUCNA8gkesdHi0aKVaIgkIzniVEX7t6fKSJAaiuJ4Q==-EBBFCE2E7C74B6D85F24C847E4A8F16F11BCF2B6"
    knowledge_map_data = requests.get(knowledge_map).json()
    tz = pytz.timezone("US/Eastern")
    seven_days_ago = datetime.now(tz) - timedelta(days=30)
    training_details = f"https://demo-cdeardon.axonify.com/axonify/api/v2/users/{user}/trainingDetails?api_token=FbOZzOWDyP94zUCNA8gkesdHi0aKVaIgkIzniVEX7t6fKSJAaiuJ4Q==-EBBFCE2E7C74B6D85F24C847E4A8F16F11BCF2B6&Key=FbOZzOWDyP94zUCNA8gkesdHi0aKVaIgkIzniVEX7t6fKSJAaiuJ4Q==-EBBFCE2E7C74B6D85F24C847E4A8F16F11BCF2B6"
    training_details = requests.get(training_details).json()
    completed = [record for record in knowledge_map_data["knowledgeRecords"] if record["trainingModuleCompleted"] == "Y"]
    completed = len(completed)
    not_completed_count = [record for record in knowledge_map_data["knowledgeRecords"] if record["trainingModuleCompleted"] != "Y"]
    not_completed_count = len(not_completed_count)
    print(completed)
    for record in knowledge_map_data["knowledgeRecords"]:
        if record["topicGraduationTimestamp"]:
            record["topicGraduationTimestamp"] = datetime.strptime(record["topicGraduationTimestamp"], "%Y%m%dT%H:%M%z").replace(tzinfo=pytz.UTC)
    
    return render_template('index2.html', data=knowledge_map_data,seven_days_ago=seven_days_ago,figure = figure_json,training_details = training_details,completed =completed,not_completed_count=not_completed_count)

if __name__ == '__main__':
    app.run(debug=True)

