
# render template for template
import io
from ytcomment import get_youtube_comments,extract_video_id
from theImplementation import statistical_analyzer,generate_pie_chart
from emotion import sentence_generator
import base64
from flask import Flask, render_template,request,jsonify


app=Flask(__name__)

global_input_text=[]
global_option=""



@app.route("/")
def hello():
    return render_template("index.html") # calling index.html from render template

@app.route("/process",methods=["POST"])
def process():
    global global_input_text,global_option

    data=request.get_json() # to recieve json
    input_text=data.get("text","").strip()
    global_option=data.get("option","")
    max_results = int(data.get("max_results", 10)) 

    print(f"Received Data: {data}")  # Debug print
    print(f"Text:{global_input_text},Option: {global_option}")

    global_input_text.clear()
    global_input_text = [line.strip() for line in input_text.split(";") if line.strip()]

    response={}

    if global_option.lower()=="youtube":
        video_id=extract_video_id(global_input_text[0])
        if video_id:
            comments=get_youtube_comments(video_id,max_results)
            pos,neg,neu=statistical_analyzer(comments)
            
        else:
            response={"error": "Invalid Youtube Link","text":global_input_text}
    
    
    elif global_option.lower() == "random":
        # global_input_text=sentence_generator(max_results)
        pos, neg, neu = statistical_analyzer(global_input_text)

    else:
        response = {"error": "Invalid option"}

   # Generate and save the pie chart
    generate_pie_chart(pos, neg, neu)
    chart_url = "/static/sentiment_pie_chart.png" 

    response.update({
        "positive": pos,
        "negative": neg,
        "neutral": neu,
        "chart": chart_url
    })

    print(response)
    return jsonify(response)


# Function to access stored input & selected option anytime
@app.route("/get_latest", methods=["GET"])
def get_latest():
    global global_input_text, global_option
    print(f"Latest stored values - Input: {global_input_text}, Option: {global_option}")  # Prints to terminal
    return jsonify({"latest_input": global_input_text, "selected_option": global_option})


if __name__=="__main__":
    app.run(debug=True)
