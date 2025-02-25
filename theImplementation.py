import subprocess
import sys
import os

def install_package(package):
    """Check if a package is installed and install it if missing."""
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package],
            stdout=subprocess.DEVNULL,  # Suppress output
            stderr=subprocess.DEVNULL   # Suppress errors unless installation fails
        )
# Required packages
required_packages = {
    "nltk": "nltk",
    "matplotlib.pyplot": "matplotlib",
    "io" :None,
    "base64":None
}

# Check & install missing packages
for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
    except ImportError:
        install_package(package_name)

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt


analyzer=SentimentIntensityAnalyzer()

    
def get_sentiment_score(score, sentiment):
    if sentiment['neu'] > 0.7:  # If more than 70% neutral, force neutrality
        return 0
    elif score >= 0.05:
        return 1
    elif score <= -0.05:
        return -1
    else:
        return 0


def statistical_analyzer(reviews,details=False):
    posCount,negCount,neuCount=0,0,0
    responseList=[]
    for review in reviews:
        result=analyzer.polarity_scores(review)
        response=get_sentiment_score(result['compound'],result)
        responseList.append(response)
        if(details):
            print(result)
            print(f"Text: {review}\nVADER: {response}\nResult:{response}\n\n")

    for response in responseList:
        if response==1:
            posCount+=1
        elif response==-1:
            negCount+=1
        else:
            neuCount+=1

    return posCount,negCount,neuCount

#can work on local machine but not anywhere else
def graphical(pos,neg,neu):
    context=["Positive","Negative","Neutral"]
    percentage=[pos,neg,neu]
    colors = ['#4CAF50', '#F44336', '#9E9E9E']
    
    plt.title("Graphical Representation!")
    plt.pie(percentage,labels=context,autopct="%.1f%%",colors=colors)
    plt.show()

# Generate the Pie Chart for real website
def generate_pie_chart(pos, neg, neu):
    if pos + neg + neu == 0:
        print("No valid sentiment scores to plot.")
        return
    labels = ["Positive", "Negative", "Neutral"]
    sizes = [pos, neg, neu]
    colors = ["#4CAF50", "#F44336", "#FFC107"]
    fig, ax = plt.subplots(figsize=(5, 5))  # Create figure and axis
    ax.set_position([0.1, 0.2, 0.6, 0.6])  # [left, bottom, width, height]

    wedges, texts, autotexts = plt.pie(
        sizes, colors=colors, autopct="%1.1f%%", startangle=90, labeldistance=0.5,radius=0.7
    )
    plt.legend(wedges, labels, title="Sentiment", loc="upper right", bbox_to_anchor=(1.35, 1))
    plt.axis("equal")  # Keep the pie chart circular

    img_path = os.path.join('static', 'sentiment_pie_chart.png')
    plt.savefig(img_path)  # Save the image to static folder
    plt.close()  # Close the plot to free memory
