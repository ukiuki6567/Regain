#レスポンス例一覧
from flask import Flask, jsonify

app = Flask(__name__)
#日本語設定
app.config["JSON_AS_ASCII"] = False

#プロジェクト一覧表示
@app.route('/')
def project_get():
    return jsonify([
    {
        "project_id": 1,
        "project_name": "プロジェクトA",
        "estimated_time": "20:00",
        "passed_time": "27:34"
    },
    {
        "project_id": 2,
        "project_name": "プロジェクトB",
        "estimated_time": "10:00",
        "passed_time": "3:10"
    },
    {
        "project_id": 3,
        "project_name": "プロジェクトC",
        "estimated_time": "5:00",
        "passed_time": "0:00"
    }
]
)

#新規プロジェクト作成
@app.route('/create', methods=['POST'])
def project_create():
    return jsonify()

#既存プロジェクト編集
@app.route('/edit', methods=['POST'])
def project_edit():
    return jsonify()

#既存プロジェクト削除
@app.route('/delete', methods=['DELETE'])
def project_delete():
    return jsonify()

#既存プロジェクト選択、プロセス一覧表示    
@app.route('/<int:project_id>')
def process_get(project_id):
    return jsonify([
    {
        "process_id": 1,
        "process_name": "要件定義",
        "estimated_time": "10:00",
        "predict_date": "0",
        "passed_time":"7:00",
        "status_name": "完了",
        "deadline": "1/15",
    },
    {
        "process_id": 2,
        "process_name": "基本設計",
        "estimated_time": "9:00",
        "predict_date": "4",
        "passed_time":"9:00",
        "status_name": "着手",
        "deadline": "1/20",
    },
    {
        "process_id": 3,
        "process_name": "詳細設計",
        "estimated_time": "5:00",
        "predict_date": "0",
        "passed_time":"0:00",
        "status_name": "未着手",
        "deadline": "1/25",
    },
    {
        "process_id": 4,
        "process_name": "開発",
        "estimated_time": "0:00",
        "predict_date": "0",
        "passed_time":"0:00",
        "status_name": "未着手",
        "deadline": "1/30",
    }
]
)

#新規プロセス作成
@app.route('/<int:project_id>/create', methods=['POST'])
def process_create(project_id):
    return jsonify()

#既存プロセス編集
@app.route('/<int:project_id>/edit', methods=['POST'])
def process_edit(project_id):
    return jsonify()
    
#既存プロセス削除                
@app.route('/<int:project_id>/delete', methods=['DELETE'])
def process_delete(project_id):
    return jsonify()

#既存プロセス選択
@app.route('/<int:project_id>/<int:process_id>')
def task_get(project_id, process_id):
    return jsonify([
                    {
                        "task_id": 1,
                        "task_name": "システム概要記述",
                        "estimated_time": "1:00",
                        "passed_time":"2:00",
                        "deadline": "1/15",
                        "status_name": "着手",
                        "priority_name": "低",
                        "running_days":2
                    },
                    {
                        "task_id": 2,
                        "task_name": "開発目的記述",
                        "estimated_time": "0:30",
                        "passed_time":"0:00",
                        "deadline": "1/16",
                        "status_name": "未着手",
                        "priority_name": "高",
                        "running_days":2
                    }
                    ]
            )

#新規タスク作成
@app.route('/<int:project_id>/<int:process_id>/create', methods=['POST'])
def task_create(project_id, process_id):
    return jsonify()

#既存タスク編集
@app.route('/<int:project_id>/<int:process_id>/edit', methods=['POST'])
def task_edit(project_id, process_id):
    return jsonify()

#既存タスク削除
@app.route('/<int:project_id>/<int:process_id>/delete', methods=['DELETE'])
def task_delete(project_id, process_id):
    return jsonify()

#既存タスク選択、タイマー情報表示
@app.route('/<int:project_id>/<int:process_id>/<int:task_id>', methods=['GET'])
def time_get(project_id, process_id, task_id):
    return jsonify({
                        "task_name": "開発目的記述",
                        "commit_time":"10:00",
                    })                  

#タイマー情報更新
@app.route('/<int:project_id>/<int:process_id>/<int:task_id>', methods=['POST'])
def time_post(project_id, process_id, task_id):
    return jsonify()

if __name__ == "__main__":
    app.run()