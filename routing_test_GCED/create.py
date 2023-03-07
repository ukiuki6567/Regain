from flask import jsonify, Blueprint

bp = Blueprint('create', __name__, url_prefix="/")

#新規プロジェクト作成
@bp.route('/create', methods=['POST'])
def project_create():
    #単純に現在地を返す
    return jsonify({"py":"create.py",
                    "rooting":"/create"})

#新規プロセス作成
@bp.route('/<int:project_id>/create', methods=['POST'])
def process_create(project_id):
    #単純に現在地を返す
    return jsonify({"py":"create.py",
                    "rooting":"/<int:project_id>/create",
                    "project_id":project_id})

#新規タスク作成
@bp.route('/<int:project_id>/<int:process_id>/create', methods=['POST'])
def task_create(project_id, process_id):
    #単純に現在地を返す
    return jsonify({"py":"create.py",
                    "rooting":"/<int:project_id>/<int:process_id>/create",
                    "project_id":project_id,
                    "process_id":process_id})