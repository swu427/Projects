import pandas as pd
from flask import Flask, request, jsonify
import time
import flask
import re
import matplotlib.pyplot as plt
import io
import requests
import matplotlib
import io
matplotlib.use('Agg')
check_ip_dict = {}
count = 0
count_a = 0
count_b = 0 
num_subscribed = 0
# project: p4
# submitter: swu427
# partner: none
# hours: 20


app = Flask(__name__)
df = pd.read_csv("main.csv")




@app.route('/')
def home():
    global count 
    if count < 10:
        if count % 2 == 0: #even is A
            with open("index.html") as f:
                html = f.read()
                count += 1
                return html
        else :#odd is B
            with open("indexB.html") as f:
                html = f.read()
                count += 1
                return html
    else:
        if count_a > count_b:
            with open("index.html") as f:
                html = f.read()
                
                
        else:
            with open("indexB.html") as f:
                html = f.read()
    return html


@app.route("/dashboard_1.svg")
def plot1():
    global df
    fig, ax = plt.subplots(figsize=(5, 5))
    plt.scatter(df['Tuition'], df['Enrollment Numbers'], c=df['Adjusted Rank'], cmap='viridis')
    plt.xlabel('Tuition ($)')
    plt.ylabel('Enrollment Numbers')
    plt.title('Enrollment vs. Tuition')
    plt.colorbar(label='Adjusted Rank')
    
    f = io.StringIO() 
    fig.savefig(f, format="svg")
    plt.close()
    
    return flask.Response(f.getvalue(), headers={"Content-Type": "image/svg+xml"})

@app.route("/dashboard_2.svg")
def plot2():
    global df
    
    
    y = request.args.get('y')
    if y == "Tuition":
        fig, ax = plt.subplots(figsize=(7, 7))
        top_10_tuition = df.nlargest(10, 'Tuition')
        plt.bar(top_10_tuition['College Name'], top_10_tuition['Tuition'])
        plt.xlabel('University')
        plt.ylabel('Adjusted Rank')
        plt.title('Top 10 Expensive Universities by Tuition Cost')
        plt.xticks(rotation=90)
        f = io.StringIO() 
        fig.savefig(f, format="svg")
        plt.close(fig)
    else: 
        fig, ax = plt.subplots(figsize=(7, 7))
        top_10 = df.nsmallest(10, 'Adjusted Rank')
        plt.bar(top_10['College Name'], top_10['Adjusted Rank'])
        plt.xlabel('University')
        plt.ylabel('Adjusted Rank')
        plt.title('Top 10 Universities by Adjusted Rank')
        plt.xticks(rotation=90)

        f = io.StringIO() 
        fig.savefig(f, format="svg")
        plt.close(fig)
    
    return flask.Response(f.getvalue(), headers={"Content-Type": "image/svg+xml"})
    
@app.route('/donate.html')
def donate():
    global count_a
    global count_b
    from_value = flask.request.args.get('from')
   
    if from_value == "A":
        count_a += 1
    else:
        count_b += 1
    with open("donate.html") as f:
        html = f.read()
    return html
    
@app.route('/browse.html')
def browse():
    global df
    
    return "<html><head><meta charset = 'UTF-8'><title>browse</title></head><body><h1>Browse</h1>{}</body><html>".format(df.to_html())

@app.route('/browse.json')
def browse_json():
    global check_ip_dict
    check_ip = request.remote_addr
    
    list_of_dict = df.to_dict()
        
    if check_ip not in check_ip_dict or time.time() - check_ip_dict[check_ip] > 60:
        check_ip_dict[check_ip] = time.time()
        return jsonify(list_of_dict)
    else:
        return flask.Response("go away", status = 429, headers = {"Retry-After": "60"})
        
@app.route('/visitors.json')
def visitors_json():
    my_list = []
    for key, value in check_ip_dict.items():
        my_list.append(key) 
    return my_list

@app.route('/email', methods=["POST"])
def email():
    global num_subscribed
    email = str(request.data, "utf-8")
    if len(re.findall(r"^\w+@\w+\.\w{3}$", email)) > 0: # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
            num_subscribed += 1
        return jsonify(f"thanks, your subscriber number is {num_subscribed}!")
    return jsonify(f"please try again, your email, {email} was invalid") # 3

    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.