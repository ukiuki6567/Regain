#タスクに対するcreate,edit,delete,task選択、タイマー更新処理の定義

from flask import jsonify, Blueprint, request, render_template
from db_driver import dbDriver
import datetime

#プロセスのルーティング/<int:project_id>
bp = Blueprint('task', __name__, url_prefix="/<int:process_id>")

#新規タスク作成
@bp.route('/create', methods=['POST'])
def task_create(project_id, process_id):
    return jsonify()

#既存タスク編集
@bp.route('/edit', methods=['POST'])
def task_edit(project_id, process_id):
    return jsonify()

#既存タスク削除
@bp.route('/delete', methods=['DELETE'])
def task_delete(project_id, process_id):
    return jsonify()

#既存タスク選択、タイマー情報表示
@bp.route('/<int:task_id>', methods=['GET'])
def timer_get(project_id, process_id, task_id):
    #本日の日付取得
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d")
    
    #dbDriverの生成とSQL実行
    regain_db_driver = dbDriver()
    
    #task_name取得
    rows = regain_db_driver.sql_run("select task_name from tasks where task_id = " + str(task_id))
    task_name = rows[0]["task_name"]
    
    #本日のcommit_time取得
    rows = regain_db_driver.sql_run("select DATE_FORMAT(commit_time,'%k:%i') as commit_time from commits where task_id = " + str(task_id)
                                    + " and commit_date = '" + now_str + "'")
    commit_time = "0:00"                                
    if(len(rows) != 0) :
        commit_time = rows[0]["commit_time"]

    #dbDriverのクローズと値返却
    regain_db_driver.db_close()
    return render_template('timer.html', title='timer', task_name = task_name, commit_time = commit_time)
    return jsonify({
                        "task_name": task_name,
                        "commit_time": commit_time,
                    })

#タイマー情報更新
@bp.route('/<int:task_id>', methods=['POST'])
def timer_post(project_id, process_id, task_id):
    return jsonify()