#プロセスに対するcreate,edit,delete,process選択処理の定義

from flask import jsonify, Blueprint
import task

#プロセスのルーティング/<int:project_id>
bp = Blueprint('process', __name__, url_prefix="/<int:project_id>")
#タスクへのルーティング情報
bp.register_blueprint(task.bp)

#新規プロセス作成
@bp.route('/create', methods=['POST'])
def process_create(project_id):
    #単純に現在地を返す
    return jsonify({"py":"process.py",
                    "rooting":"/<int:project_id>/create",
                    "project_id":project_id})

#既存プロセス編集
@bp.route('/edit', methods=['POST'])
def process_edit(project_id):
    #単純に現在地を返す
    return jsonify({"py":"process.py",
                    "rooting":"/<int:project_id>/edit",
                    "project_id":project_id})

#既存プロセス削除
@bp.route('/delete', methods=['DELETE'])
def process_delete(project_id):
    #単純に現在地を返す
    return jsonify({"py":"process.py",
                    "rooting":"/<int:project_id>/delete",
                    "project_id":project_id})

#既存プロセス選択
@bp.route('/<int:process_id>')
def task_get(project_id, process_id):
    #単純に現在地を返す
    return jsonify({"py":"process.py",
                    "rooting":"/<int:project_id>/<int:process_id>",
                    "project_id":project_id,
                    "process_id":process_id})