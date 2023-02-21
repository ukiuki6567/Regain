from flask import jsonify, Blueprint

bp = Blueprint('delete', __name__, url_prefix="/")

#既存プロジェクト削除
@bp.route('/delete', methods=['DELETE'])
def project_delete():
    #単純に現在地を返す
    return jsonify({"py":"delete.py",
                    "rooting":"/delete"})

#既存プロセス削除
@bp.route('/<int:project_id>/delete', methods=['DELETE'])
def process_delete(project_id):
    #単純に現在地を返す
    return jsonify({"py":"delete.py",
                    "rooting":"/<int:project_id>/delete",
                    "project_id":project_id})

#既存タスク削除
@bp.route('/<int:project_id>/<int:process_id>/delete', methods=['DELETE'])
def task_delete(project_id, process_id):
    #単純に現在地を返す
    return jsonify({"py":"delete.py",
                    "rooting":"/<int:project_id>/<int:process_id>/delete",
                    "project_id":project_id,
                    "process_id":process_id})