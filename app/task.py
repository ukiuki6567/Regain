#タスクに対するcreate,edit,delete,task選択、タイマー更新処理の定義

from flask import jsonify, Blueprint, request, render_template
from db_driver import dbDriver
import datetime

from sql_template import SQLTemplates as sql_temp

#プロセスのルーティング/<int:project_id>
bp = Blueprint('task', __name__, url_prefix="/<int:process_id>")

#新規タスク作成
@bp.route('/create', methods=['POST'])
def task_create(project_id:int, process_id:int) -> int:
    """
    新規にタスクを作成する関数。
    ステータスは初期値となる。
    Method: POST
    jsonファイル例:
    {
        "task_name":"taskのなまえ",
        "priority_id":1,
        "estimated_time":"24:00",
        "deadline":"2023-02-05"
    }

    Args:
        project_id (int): 各プロジェクトに割り振られたID
        process_id (int): 各プロセスに割り振られたID

    Returns:
        int: 200(OK) or 500(NG)
    """
    params = request.get_json()
    print(params)
    task_name = params["task_name"]
    priority_id = params.get("priority_id")
    estimated_time = params.get("estimated_time","0:00")
    if estimated_time == "" :
        estimated_time = "0:00"
    estimated_time += ":00"
    deadline = params.get("deadline","0000-00-00")
    if deadline == "" :
        deadline = "0000-00-00"

    #dbDriverの生成
    regain_db_driver = dbDriver()
    
    try:
        #task生成SQL文
        task_insert_sql = sql_temp.TASK_INSERT_SQL.format(
            task_name = task_name,
            process_id = process_id,
            estimated_time = estimated_time,
            deadline = deadline,
            priority_id = priority_id
        )
        rows = regain_db_driver.sql_run(task_insert_sql)
        rows = regain_db_driver.sql_run("COMMIT")
        regain_db_driver.db_close()

        # 200 (OK)
        result_num = 200
        return f"Task with task_name: {task_name} created.", result_num

    except Exception as e:
        print(f"Error creating task: {e}") # 本当はここでLoggerを使いたい
        
        # 500 (NG)
        result_num = 500
        return f"Error creating task with task_name: {task_name}.\nError: {str(e)}", result_num

#既存タスク編集
@bp.route('/edit', methods=['POST'])
def task_edit(project_id:int, process_id:int) -> int: 
    """
    既存のプロジェクト情報を変更する関数。
    プロジェクト名の情報変更があった場合、その内容をDBに更新する。
    Method: POST
    jsonファイル例:
    {
        "task_id": 12345,
        "task_name": "ほげほげ",
        "status_id": 2,
        "priority_id": 3,
        "estimated_time":"24:00",
        "deadline": "2023-02-23"
    }

    Args:
        project_id (int): 各プロジェクトに割り振られたID
        process_id (int): 各プロセスに割り振られたID

    Returns:
        int: 200(OK) or 500(NG)
    """

    # 処理開始
    print(f"処理開始: /{project_id}/{process_id}/edit")
    
    # dbDriverの生成
    regain_db_driver = dbDriver()

    ### タスクの更新があった場合、これをDBに反映（Update）する。
    try:
        # requestにより情報取得
        params = request.get_json()

        task_name, task_id = params["task_name"], params["task_id"]
        priority_id = params["priority_id"]
        status_id = params["status_id"]
        estimated_time = params.get("estimated_time","0:00")
        if estimated_time == "" :
            estimated_time = "0:00"
        estimated_time += ":00"
        deadline = params.get("deadline","0000-00-00")
        if deadline == "" :
            deadline = "0000-00-00"

        print(f"task_name: {task_name}, task_id: {task_id}, proiroty_id: {priority_id}, estimated_time: {estimated_time}, deadline: {deadline}")

        # タスク更新SQL
        task_update_sql = sql_temp.TASK_UPDATE_SQL.format(
            task_name = task_name,
            task_id = task_id,
            status_id = status_id,
            priority_id = priority_id,
            estimated_time = estimated_time,
            deadline = deadline
        )

        rows = regain_db_driver.sql_run(task_update_sql)
        rows = regain_db_driver.sql_run("COMMIT")
        regain_db_driver.db_close()

        # 200 (OK)
        result_num = 200
        return f"Task with task_id: {task_id} edited.", result_num

    except Exception as e:
        print(f"Error editing task: {e}") # 本当はここでLoggerを使いたい

        # 500 (NG)
        result_num = 500
        return f"Error editing task with task_id: {task_id}.\nError: {str(e)}", result_num


#既存タスク削除
@bp.route('/delete', methods=['DELETE'])
def task_delete(project_id:int, process_id:int) -> int:
    """
    既存タスク削除処理。
    受け取ったtask_idに対応するプロジェクトを削除する。

    jsonファイル例:
    {
        "task_id": 12345
    }

    Args:
        project_id (int): 各プロジェクトに割り振られたID
        process_id (int): 各プロセスに割り振られたID

    Returns:
        int: 200(OK) or 500(NG)
    """
    # 処理開始
    print(f"処理開始: /{project_id}/{process_id}/delete")
    
    # dbDriverの生成
    regain_db_driver = dbDriver()

    ### プロジェクト名の更新があった場合、これをDBに反映（Update）する。
    try:
        # requestにより情報取得
        params = request.get_json()
        task_id = params["task_id"]
        print(f"task_id: {task_id}")

        # プロジェクト一覧更新SQL
        task_delete_sql = sql_temp.TASK_DELETE_SQL.format(task_id=task_id)
        rows = regain_db_driver.sql_run(task_delete_sql)
        rows = regain_db_driver.sql_run("COMMIT")

        regain_db_driver.db_close()

        # 200 (OK)
        result_num = 200
        return f"Task with task_id: {task_id} deleted.", result_num

    except Exception as e:
        print("Error deleting task: {e}") # 本当はここでLoggerを使いたい

        # 500 (NG)
        result_num = 500
        return f"Error deleting task with task_id: {task_id}.\nError: {str(e)}", result_num


#既存タスク選択、タイマー情報表示
@bp.route('/<int:task_id>', methods=['GET'])
def timer_get(project_id:int, process_id:int, task_id:int) -> str:
    """
    タイマー情報表示。
    Method: GET

    Args:
        project_id (int): 各プロジェクトに割り振られたID
        process_id (int): 各プロセスに割り振られたID
        task_id (int): 各タスクに割り振られたID

    Returns:
        str: htmlテンプレート (timer.html)
    """
    #本日の日付取得
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d")
    
    #dbDriverの生成とSQL実行
    regain_db_driver = dbDriver()
    
    try:
        #task_name取得
        task_name_sql = sql_temp.TIMAR_NAME_SELECT_SQL.format(task_id = task_id)
        rows = regain_db_driver.sql_run(task_name_sql)
        task_name = rows[0]["task_name"]
        
        #本日のcommit_time取得
        commit_time_sql = sql_temp.TIMER_TIME_SUM_SELECT_SQL.format(
            task_id = task_id,
            commit_date = now_str
        )
        rows = regain_db_driver.sql_run(commit_time_sql)
        commit_time = "0:00"                                
        if(len(rows) != 0) :
            commit_time = rows[0]["commit_time"]

        #dbDriverのクローズと値返却
        regain_db_driver.db_close()
        return render_template('timer.html', title='timer', task_name = task_name, commit_time = commit_time, project_id = project_id, process_id = process_id, task_i= task_id)


    except Exception as e:
        # 500 (NG)
        result_num = 500
        return f"Error displaing timer with project_id: {project_id}, process_id: {process_id}, task_id: {task_id}.\nError: {str(e)}", result_num


#タイマー情報更新
@bp.route('/<int:task_id>', methods=['POST'])
def timer_post(project_id:int, process_id:int, task_id:int) -> int:
    """
    対象タスクのcommit時間を更新する関数。
    Method: POST
    jsonファイル例:
    {
        "commit_time": "00:12"
    }
    """
    
    # dbDriverの生成
    regain_db_driver = dbDriver()

    ### タスクの更新があった場合、これをDBに反映（Update）する。
    try:
        # requestにより情報取得
        params = request.get_json()
        commit_time = params.get("commit_time","0:00")
        commit_time += ":00"
        #本日の日付取得
        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d")
        print(f"commit_date: {now_str}, commit_time: {commit_time}, task_id: {task_id}")

        # プロジェクト一覧更新SQL
        timer_update_sql = sql_temp.TIMER_UPDATE_SQL.format(
            commit_date = now_str,
            commit_time = commit_time,
            task_id = task_id
        )
        # print(task_update_sql)

        rows = regain_db_driver.sql_run(timer_update_sql)
        rows = regain_db_driver.sql_run("COMMIT")
        result_num = regain_db_driver.db_close()

        # 200 (OK)
        result_num = 200
        return f"Updateing commit time updated.", result_num
        
    except Exception as e:
        print("Error deleting process: {e}") # 本当はここでLoggerを使いたい

        # 500 (NG)
        result_num = 500
        return f"Error updating commit time with project_id: {project_id}, process_id: {process_id}, task_id: {task_id}.\nError: {str(e)}", result_num