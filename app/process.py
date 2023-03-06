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
#受信JSON例
# {
#   "process_name":"processのなまえ",
#   "estimated_time":"24:00",
#   "deadline":"2023-02-05"
# }
@bp.route('/create', methods=['POST'])
def process_create(project_id):
    params = request.get_json()
    process_name = params["process_name"]
    estimated_time = params.get("estimated_time","0:00")
    estimated_time += ":00"
    deadline = params.get("deadline","0000-00-00")

    #dbDriverの生成
    regain_db_driver = dbDriver()
    
    #process生成SQL文
    process_insert_sql = f"""
                        INSERT INTO
                            processes (process_name, project_id, estimated_time, deadline)
                        VALUES
                            ('{process_name}', {project_id}, CAST('{estimated_time}' as TIME), CAST('{deadline}' as DATE))
                        """
    rows = regain_db_driver.sql_run(process_insert_sql)
    rows = regain_db_driver.sql_run("COMMIT")

    #dbDriverのクローズと200OK返却
    regain_db_driver.db_close()
    return jsonify()



#既存プロセス編集
@bp.route('/edit', methods=['POST'])
def process_edit(project_id):
    """
    既存のプロジェクト情報を変更する関数。
    プロジェクト名の情報変更があった場合、その内容をDBに更新する。
    Method: POST
    jsonファイル例:
    {
        "process_id": 12345
        "process_name": "ほげほげ"
    }
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
        print(f"project_name: {process_name}, project_id: {process_id}")

        # プロジェクト一覧更新SQL
        process_update_sql = sql_temp.PROCESS_UPDATE_SQL.format(
            process_name = process_name,
            process_id = process_id
        )

        rows = regain_db_driver.sql_run(process_update_sql)
        rows = regain_db_driver.sql_run("COMMIT")
        result_num = regain_db_driver.db_close()
        result = "OK"
    
    except:
        print("Something Failed...") # 本当はここでLoggerを使いたい
        result = "NG"

    # 処理終了
    print(f"処理終了: /{project_id}/edit")

    return jsonify(
                {
        'status': result
        }
    )

#既存プロセス削除
@bp.route('/delete', methods=['POST'])
def process_delete(project_id):
    """
    既存プロセス削除処理。
    受け取ったprocess_idに対応するプロジェクトを削除する。

    jsonファイル例:
    {
        "process_id": 12345
    }

    Returns:
        json: {
        'status': "OK" or "NG"
        }
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
        result = "OK"

    except:
        print("Something Failed...") # 本当はここでLoggerを使いたい
        result = "NG"
    
    # 処理終了
    print(f"処理終了: /{project_id}/delete")

    return jsonify(
                {
        'status': result
        }
    )

#既存プロセス選択、タスク一覧表示
@bp.route('/<int:process_id>')
def task_get(project_id, process_id):
    
    #dbDriverの生成
    regain_db_driver = dbDriver()

    #タスク一覧取得SQL
    task_list_sql = f"""
                    SELECT
                        tasks.task_id,
                        task_name,
                        DATE_FORMAT(estimated_time,'%k:%i') as estimated_time,
                        DATE_FORMAT(deadline,'%m/%e') as deadline,
                        DATE_FORMAT(sec_to_time(IFNULL(sum(time_to_sec(commit_time)),0)),'%k:%i') as passed_time,
                        status_name,
                        priority_name
                    FROM 
                        tasks
                        left join commits
                            on tasks.task_id = commits.task_id
                        left join task_statuses
                            on tasks.status_id = task_statuses.status_id
                        left join priorities
                            on tasks.priority_id = priorities.priority_id
                    WHERE 
                        process_id = {process_id}
                    GROUP BY
                        task_id
                    """
    tasks = regain_db_driver.sql_run(task_list_sql)
        
    #タスクステータス一覧取得SQL
    name_list_sql = """
                    SELECT
                        status_name
                    FROM
                        task_statuses
                    """
    status_names = regain_db_driver.sql_run(name_list_sql)
        
    #優先度一覧取得SQL
    name_list_sql = """
                    SELECT
                        priority_name
                    FROM
                        priorities
                    """
    priorities = regain_db_driver.sql_run(name_list_sql)

    #dbDriverのクローズと値返却
    regain_db_driver.db_close()
    # return jsonify(rows)
    return render_template('tasks.html', title='tasks', tasks=tasks, status_names = status_names, priorities = priorities)