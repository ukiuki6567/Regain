#プロセスに対するcreate,edit,delete,process選択処理の定義

from flask import jsonify, Blueprint, request, render_template
from db_driver import dbDriver
import task

from sql_template import SQLTemplates as sql_temp

#プロセスのルーティング/<int:project_id>
bp = Blueprint('process', __name__, url_prefix="/<int:project_id>")
#タスクへのルーティング情報
bp.register_blueprint(task.bp)

#新規プロセス作成
@bp.route('/create', methods=['POST'])
def process_create(project_id:int) -> int:
    """
    新規にプロセスを作成する関数。
    ステータスは初期値となる。
    Method: POST
    jsonファイル例:
    {
        "process_name": "processのなまえ",
        "deadline":"2023-02-05"
    }

    Args:
        project_id (int): 各プロジェクトに割り振られたID

    Returns:
        int: 200 (OK) or 500 (NG)
    """
    params = request.get_json()
    process_name = params["process_name"]
    deadline = params.get("deadline","0000-00-00")

    #dbDriverの生成
    regain_db_driver = dbDriver()
    
    try:
        #process生成SQL文
        process_insert_sql = sql_temp.PROCESS_INSERT_SQL.format(
            process_name = process_name,
            project_id = project_id,
            deadline = deadline
        )
        rows = regain_db_driver.sql_run(process_insert_sql)
        rows = regain_db_driver.sql_run("COMMIT")
        regain_db_driver.db_close()
        
        # 200 (OK)
        result_num = 200
        return f"Process with process_name: {process_name} created.", result_num
    
    except Exception as e:
        print("Error creating process: {e}") # 本当はここでLoggerを使いたい
        
        # 500 (NG)
        result_num = 500
        return f"Error creating process with process_name: {process_name}.\nError: {str(e)}", result_num


#既存プロセス編集
@bp.route('/edit', methods=['POST'])
def process_edit(project_id:int) -> int:
    """
    既存のプロジェクト情報を変更する関数。
    プロジェクト名の情報変更があった場合、その内容をDBに更新する。
    Method: POST
    jsonファイル例:
    {
        "process_id": 12345,
        "process_name": "ほげほげ",
        "status_id": 2,
        "deadline": "2023-02-23"
    }

    Return:
        200(OK) or 500(NG)

    Args:
        project_id (int): 各プロジェクトに割り振られたID

    Returns:
        int: 200(OK) or 500(NG)
    """

    # 処理開始
    print(f"処理開始: /{project_id}/edit")
    
    # dbDriverの生成
    regain_db_driver = dbDriver()

    ### プロセス名の更新があった場合、これをDBに反映（Update）する。
    try:
        # requestにより情報取得
        params = request.get_json()

        process_name, process_id = params["process_name"], params["process_id"]
        status_id = params["status_id"]
        deadline = params.get("deadline","0000-00-00")
        if deadline == "" :
            deadline = "0000-00-00"
        print(f"project_name: {process_name}, project_id: {process_id}")

        # プロジェクト一覧更新SQL
        process_update_sql = sql_temp.PROCESS_UPDATE_SQL.format(
            process_name = process_name,
            process_id = process_id,
            status_id = status_id,
            deadline = deadline
        )

        rows = regain_db_driver.sql_run(process_update_sql)
        rows = regain_db_driver.sql_run("COMMIT")
        
        regain_db_driver.db_close()

        # 200 (OK)
        result_num = 200
        return f"Process with process_id: {process_id} edited.", result_num
    
    except Exception as e:
        print(f"Error editing process: {e}") # 本当はここでLoggerを使いたい
        
        # 500 (NG)
        result_num = 500
        return f"Error editing process with process_id: {process_id}.\nError: {str(e)}", result_num


#既存プロセス削除
@bp.route('/delete', methods=['DELETE'])
def process_delete(project_id:int) -> int:
    """
    既存プロセス削除処理。
    受け取ったprocess_idに対応するプロジェクトを削除する。

    jsonファイル例:
    {
        "process_id": 12345
    }

    Args:
        project_id (int): 各プロジェクトに割り振られたID

    Returns:
        int: 200(OK) or 500(NG)
    """
    # 処理開始
    print(f"処理開始: /{project_id}/delete")
    
    # dbDriverの生成
    regain_db_driver = dbDriver()

    ### プロジェクト名の更新があった場合、これをDBに反映（Update）する。
    try:
        # requestにより情報取得
        params = request.get_json()
        print(f"params: {params}")

        process_id = params["process_id"]
        print(f"process_id: {process_id}")

        # プロジェクト一覧更新SQL
        process_delete_sql = sql_temp.PROCESS_DELETE_SQL.format(process_id=process_id)
        print(process_delete_sql)
        rows = regain_db_driver.sql_run(process_delete_sql)
        rows = regain_db_driver.sql_run("COMMIT")

        regain_db_driver.db_close()

        # 200 (OK)
        result_num = 200
        return f"Process with process_id: {process_id} deleted.", result_num

    except Exception as e:
        print("Error deleting process: {e}") # 本当はここでLoggerを使いたい

        # 500 (NG)
        result_num = 500
        return f"Error deleting process with process_id: {process_id}.\nError: {str(e)}", result_num

#既存プロセス選択、タスク一覧表示
@bp.route('/<int:process_id>')
def task_get(project_id:int, process_id:int) -> str:
    """
    タスク一覧を表示。
    Method: GET

    Args:
        project_id (int): 各プロジェクトに割り振られたID
        process_id (int): 各プロセスに割り振られたID

    Returns:
        str: htmlテンプレート (tasks.html)
    """
    
    #dbDriverの生成
    regain_db_driver = dbDriver()

    try:
        #プロジェクト名取得
        project_name = regain_db_driver.sql_run(sql_temp.PROJECT_NAME_SELECT_SQL.format(project_id = project_id))[0]["project_name"]

        #プロセス名取得
        process_name = regain_db_driver.sql_run(sql_temp.PROCESS_NAME_SELECT_SQL.format(process_id = process_id))[0]["process_name"]

        #タスク一覧取得SQL
        task_select_sql = sql_temp.TASK_SELECT_SQL.format(
            process_id = process_id
        )
        tasks = regain_db_driver.sql_run(task_select_sql)
            
        #タスクステータス一覧取得
        status_names = regain_db_driver.sql_run(sql_temp.TASK_STATUS_NAME_SELECT_SQL)
            
        #優先度一覧取得
        priorities = regain_db_driver.sql_run(sql_temp.TASK_PRIORITY_SELECT_SQL)
        
        #dbDriverのクローズと値返却
        regain_db_driver.db_close()
        return render_template('tasks.html', 
                            title='tasks', 
                            tasks=tasks, 
                            status_names = status_names, 
                            priorities = priorities,  
                            project_id = project_id,
                            project_name = project_name, 
                            process_id = process_id,
                            process_name = process_name)
    
    except Exception as e:
        print("Error getting task: {e}") # 本当はここでLoggerを使いたい
        return f"Error getting task with process_id: {process_id}.\nError: {str(e)}", 500
