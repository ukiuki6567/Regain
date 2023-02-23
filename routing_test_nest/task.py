#タスクに対するcreate,edit,delete,task選択、タイマー更新処理の定義

from flask import jsonify, Blueprint
import task

#プロセスのルーティング/<int:project_id>
bp = Blueprint('task', __name__, url_prefix="/<int:process_id>")

#新規タスク作成
@bp.route('/create', methods=['POST'])
def task_create(project_id, process_id):
    #単純に現在地を返す
    return jsonify({"py":"task.py",
                    "rooting":"/<int:project_id>/<int:process_id>/create",
                    "project_id":project_id,
                    "process_id":process_id})

#既存タスク編集
@bp.route('/edit', methods=['POST'])
def task_edit(project_id, process_id):
    #単純に現在地を返す
    return jsonify({"py":"task.py",
                    "rooting":"/<int:project_id>/<int:process_id>/edit",
                    "project_id":project_id,
                    "process_id":process_id})

#既存タスク削除
@bp.route('/delete', methods=['DELETE'])
def task_delete(project_id, process_id):
    #単純に現在地を返す
    return jsonify({"py":"task.py",
                    "rooting":"/<int:project_id>/<int:process_id>/delete",
                    "project_id":project_id,
                    "process_id":process_id})

#既存タスク選択、タイマー情報表示
@bp.route('/<int:task_id>', methods=['GET'])
def timer_get(project_id, process_id, task_id):
    #単純に現在地を返す
    return jsonify({"py":"task.py", 
                    "rooting":"/<int:project_id>/<int:process_id>/<int:task_id>",
                    "project_id":project_id,
                    "process_id":process_id,
                    "task_id":task_id})

#タイマー情報更新
@bp.route('/<int:task_id>', methods=['POST'])
def timer_post(project_id, process_id, task_id):
    #単純に現在地を返す
    return jsonify({"py":"task.py",
                    "rooting":"/<int:project_id>/<int:process_id>/<int:task_id>",
                    "project_id":project_id,
                    "process_id":process_id,
                    "task_id":task_id})