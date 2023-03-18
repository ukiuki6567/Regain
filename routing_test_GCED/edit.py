from flask import jsonify, Blueprint

bp = Blueprint('edit', __name__, url_prefix="/")

#既存プロジェクト編集
@bp.route('/edit', methods=['POST'])
def project_edit():
    #単純に現在地を返す
    return jsonify({"py":"edit.py",
                    "rooting":"/edit"})

#既存プロセス編集
@bp.route('/<int:project_id>/edit', methods=['POST'])
def process_edit(project_id):
    #単純に現在地を返す
    return jsonify({"py":"edit.py",
                    "rooting":"/<int:project_id>/edit",
                    "project_id":project_id})

#既存タスク編集
@bp.route('/<int:project_id>/<int:process_id>/edit', methods=['POST'])
def task_edit(project_id, process_id):
    #単純に現在地を返す
    return jsonify({"py":"edit.py",
                    "rooting":"/<int:project_id>/<int:process_id>/edit",
                    "project_id":project_id,
                    "process_id":process_id})

#タイマー情報更新
@bp.route('/<int:project_id>/<int:process_id>/<int:task_id>', methods=['POST'])
def time_get(project_id, process_id, task_id):
    #単純に現在地を返す
    return jsonify({"py":"edit.py",
                    "rooting":"/<int:project_id>/<int:process_id>/<int:task_id>",
                    "project_id":project_id,
                    "process_id":process_id,
                    "task_id":task_id})