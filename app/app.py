# flaskのファイル

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tasks.html', task_name="jinja2のお勉強", status_name="完了" , priority_name="高", estimated_time="5:00" ,passed_time="3:00", deadline="2/28") # templatesフォルダ内のindex.htmlを表示する

if __name__ == '__main__':
    app.run()