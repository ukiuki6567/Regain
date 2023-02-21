#プロジェクトに対するcreate,edit,delete,project選択処理の定義

from flask import jsonify, Blueprint
from db_driver import dbDriver
import process

#プロジェクトのルーティング/
bp = Blueprint('project', __name__, url_prefix="/")
#プロセスへのルーティング情報
bp.register_blueprint(process.bp)

#新規プロジェクト作成
@bp.route('/create', methods=['POST'])
def project_create():
    return jsonify()

#既存プロジェクト編集
@bp.route('/edit', methods=['POST'])
def project_edit():
    return jsonify()

#既存プロジェクト削除
@bp.route('/delete', methods=['DELETE'])
def project_delete():
    return jsonify()

#既存プロジェクト選択、プロセス一覧表示
@bp.route('/<int:project_id>')
def process_get(project_id):
    return jsonify([
            {
                "process_id": 1,
                "process_name": "要件定義",
                "estimated_time": "10:00",
                "predict_date": "0",
                "passed_time":"7:00",
                "status_id": "完了",
                "deadline": "1/15",
            },
            {
                "process_id": 2,
                "process_name": "基本設計",
                "estimated_time": "9:00",
                "predict_date": "4",
                "passed_time":"9:00",
                "status_id": "着手",
                "deadline": "1/20",
            },
            {
                "process_id": 3,
                "process_name": "詳細設計",
                "estimated_time": "5:00",
                "predict_date": "0",
                "passed_time":"0:00",
                "status_id": "未着手",
                "deadline": "1/25",
            },
            {
                "process_id": 4,
                "process_name": "開発",
                "estimated_time": "0:00",
                "predict_date": "0",
                "passed_time":"0:00",
                "status_id": "未着手",
                "deadline": "1/30",
            }
        ]
    )