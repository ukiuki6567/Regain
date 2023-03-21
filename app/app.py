# flaskのファイル

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    project_id=1
    process_id=2
    tasks = [{
        "task_id": "4",
        "task_name": "タスクA",
        "status_name": "着手",
        "priority_name": "高",
        "estimated_time": "3:24",
        "passed_time": "1:21",
        "deadline": "3/27"
    }, {
        "task_id": "3",
        "task_name": "タスクB",
        "status_name": "未着手",
        "priority_name": "高",
        "estimated_time": "1:44",
        "passed_time": "0:32",
        "deadline": "3/30"
    }, {
        "task_id": "2",
        "task_name": "タスクC",
        "status_name": "未着手",
        "priority_name": "高",
        "estimated_time": "1:00",
        "passed_time": "0:32",
        "deadline": "3/30"
    }]

    # templatesフォルダ内のindex.htmlを表示する,flask
    return render_template('tasks.html', project_id=project_id, process_id=process_id, tasks=tasks)


if __name__ == '__main__':
    app.run()
