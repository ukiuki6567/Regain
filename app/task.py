#タスクに対するcreate,edit,delete,task選択、タイマー更新処理の定義

from flask import jsonify, Blueprint, request, render_template
from db_driver import dbDriver
import datetime

from sql_template import SQLTemplates as sql_temp

#プロセスのルーティング/<int:project_id>
bp = Blueprint('task', __name__, url_prefix="/<int:process_id>")

#新規タスク作成
#受信JSON例
# {
#   "task_name":"taskのなまえ",
#   "priority_name":"低",
#   "estimated_time":"24:00",
#   "deadline":"2023-02-05"
# }
@bp.route('/create', methods=['POST'])
def task_create(project_id, process_id):
    params = request.get_json()
    task_name = params["task_name"]
    priority_name = params.get("priority_name")
    estimated_time = params.get("estimated_time","0:00")
    estimated_time += ":00"
    deadline = params.get("deadline","0000-00-00")

    #dbDriverの生成
    regain_db_driver = dbDriver()
    
    #task生成SQL文
    process_insert_sql = f"""
                        INSERT INTO
                            tasks (task_name, process_id, priority_id, estimated_time, deadline)
                        SELECT
                            '{task_name}', {process_id}, priority_id, CAST('{estimated_time}' as TIME), CAST('{deadline}' as DATE)
                        FROM
                            priorities
                        WHERE
                            priority_name = '{priority_name}'
                        """
    rows = regain_db_driver.sql_run(process_insert_sql)
    rows = regain_db_driver.sql_run("COMMIT")

    #dbDriverのクローズと200OK返却
    regain_db_driver.db_close()
    return jsonify()






#既存タスク編集
@bp.route('/edit', methods=['POST'])
def task_edit(project_id, process_id):
    """
    既存のプロジェクト情報を変更する関数。
    プロジェクト名の情報変更があった場合、その内容をDBに更新する。
    Method: POST
    jsonファイル例:
    {
        "task_id": 12345,
        "task_name": "ほげほげ",
        "priority_id": 3,
        "deadline": "2023-02-23"
    }
    """

    # 処理開始
    print(f"処理開始: /{project_id}/{process_id}/edit")
    
    # dbDriverの生成
    regain_db_driver = dbDriver()

    ### タスクの更新があった場合、これをDBに反映（Update）する。
    try:
        # requestにより情報取得
        params = request.get_json()
        print("hoge")

        task_name, task_id = params["task_name"], params["task_id"]
        priority_id = params["priority_id"]
        print("hoge")
        deadline = params.get("deadline","0000-00-00")

        print(f"task_name: {task_name}, task_id: {task_id}, proiroty_id: {priority_id}, deadline: {deadline}")
        
        # HTTP200OKなどの結果を格納する数字
        result_num = 0

        # プロジェクト一覧更新SQL
        task_update_sql = sql_temp.TASK_UPDATE_SQL.format(
            task_name = task_name,
            task_id = task_id,
            priority_id = priority_id,
            deadline = deadline
        )
        # print(task_update_sql)

        rows = regain_db_driver.sql_run(task_update_sql)
        rows = regain_db_driver.sql_run("COMMIT")
        result_num = regain_db_driver.db_close()
        
    except:
        print("Something Failed...") # 本当はここでLoggerを使いたい

    # 処理終了
    print(f"処理終了: /{project_id}/{process_id}/edit")

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