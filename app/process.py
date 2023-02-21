#プロセスに対するcreate,edit,delete,process選択処理の定義

from flask import jsonify, Blueprint
from db_driver import dbDriver
import task

#プロセスのルーティング/<int:project_id>
bp = Blueprint('process', __name__, url_prefix="/<int:project_id>")
#タスクへのルーティング情報
bp.register_blueprint(task.bp)

#新規プロセス作成
@bp.route('/create', methods=['POST'])
def process_create(project_id):
    return jsonify()

#既存プロセス編集
@bp.route('/edit', methods=['POST'])
def process_edit(project_id):
    return jsonify()

#既存プロセス削除
@bp.route('/delete', methods=['DELETE'])
def process_delete(project_id):
    return jsonify()

#既存プロセス選択、タスク一覧表示
@bp.route('/<int:process_id>')
def task_get(project_id, process_id):
    
    #dbDriverの生成とSQL実行
    regain_db_driver = dbDriver()

    
    #タスク一覧取得
    
    # JOIN元のSQLパーツ
    # rows = regain_db_driver.sql_run("select task_id from tasks where process_id = " + str(process_id))
    # print(rows)
    # rows = regain_db_driver.sql_run("select task_id, DATE_FORMAT(sec_to_time(sum(time_to_sec(commit_time))),'%k:%i') as passed_time from commits group by task_id ")
    # print(rows)

    rows = regain_db_driver.sql_run("select tasks.task_id," + 
                                    " task_name," + 
                                    " DATE_FORMAT(estimated_time,'%k:%i') as estimated_time,"
                                    " DATE_FORMAT(deadline,'%m/%e') as deadline," +
                                    " IFNULL(times.passed_time, '0:00') as passed_time," +
                                    " status_name," +
                                    " priority_name," +
                                    " IFNULL(running_days, 0) as running_days" +
                                    " from tasks" +
                                    " left join (select task_id, count(*) as running_days, DATE_FORMAT(sec_to_time(sum(time_to_sec(commit_time))),'%k:%i') as passed_time from commits group by task_id) as times" +
                                    " on tasks.task_id = times.task_id" +
                                    " left join task_statuses" +
                                    " on tasks.status_id = task_statuses.status_id" +
                                    " left join priorities" +
                                    " on tasks.priority_id = priorities.priority_id" +
                                    " where process_id = " + str(process_id))
    print(rows)

    #dbDriverのクローズと値返却
    regain_db_driver.db_close()
    return jsonify(rows)