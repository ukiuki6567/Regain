from flask import jsonify, Blueprint

bp = Blueprint('get', __name__, url_prefix="/")

#既存プロジェクト選択、プロセス一覧表示
@bp.route('/<int:project_id>')
def process_get(project_id):
    #単純に現在地を返す
    return jsonify({"py":"get.py",
                    "rooting":"/<int:project_id>",
                    "project_id":project_id})

#既存プロセス選択
@bp.route('/<int:project_id>/<int:process_id>')
def task_get(project_id, process_id):
    #単純に現在地を返す
    return jsonify({"py":"get.py",
                    "rooting":"/<int:project_id>/<int:process_id>",
                    "project_id":project_id,
                    "process_id":process_id})

#既存タスク選択、タイマー情報表示
@bp.route('/<int:project_id>/<int:process_id>/<int:task_id>', methods=['GET'])
def time_get(project_id, process_id, task_id):
    #単純に現在地を返す
    return jsonify({"py":"get.py", 
                    "rooting":"/<int:project_id>/<int:process_id>/<int:task_id>",
                    "project_id":project_id,
                    "process_id":process_id,
                    "task_id":task_id})