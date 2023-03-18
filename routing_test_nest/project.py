#プロジェクトに対するcreate,edit,delete,project選択処理の定義

from flask import jsonify, Blueprint
import process

#プロジェクトのルーティング/
bp = Blueprint('project', __name__, url_prefix="/")
#プロセスへのルーティング情報
bp.register_blueprint(process.bp)

#新規プロジェクト作成
@bp.route('/create', methods=['POST'])
def project_create():
    #単純に現在地を返す
    return jsonify({"py":"project.py",
                    "rooting":"/create"})

#既存プロジェクト編集
@bp.route('/edit', methods=['POST'])
def project_edit():
    #単純に現在地を返す
    return jsonify({"py":"project.py",
                    "rooting":"/edit"})

#既存プロジェクト削除
@bp.route('/delete', methods=['DELETE'])
def project_delete():
    #単純に現在地を返す
    return jsonify({"py":"project.py",
                    "rooting":"/delete"})

#既存プロジェクト選択、プロセス一覧表示
@bp.route('/<int:project_id>')
def process_get(project_id):
    #単純に現在地を返す
    return jsonify({"py":"project.py",
                    "rooting":"/<int:project_id>",
                    "project_id":project_id})