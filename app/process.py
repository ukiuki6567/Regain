#プロセスに対するcreate,edit,delete,process選択処理の定義

from flask import jsonify, Blueprint, request, render_template
from db_driver import dbDriver
import task

#プロセスのルーティング/<int:project_id>
bp = Blueprint('process', __name__, url_prefix="/<int:project_id>")
#タスクへのルーティング情報
bp.register_blueprint(task.bp)

#新規プロセス作成
@bp.route('/create', methods=['POST'])
def process_create(project_id):
    params = request.get_json()
    process_name = params["process_name"]
    status_name = params.get("status_name","未着手")
    estimated_time = params.get("estimated_time","0:00")
    estimated_time += ":00"
    deadline = params.get("deadline","0000-00-00")

    #dbDriverの生成
    regain_db_driver = dbDriver()
    
    #process生成SQL文
    process_insert_sql = f"""
                        INSERT INTO
                            processes (process_name, status_id, project_id, estimated_time, deadline)
                        SELECT
                            '{process_name}', status_id, {project_id}, CAST('{estimated_time}' as TIME), CAST('{deadline}' as DATE)
                        FROM
                            process_statuses
                        WHERE
                            status_name = '{status_name}'
                        """
    rows = regain_db_driver.sql_run(process_insert_sql)
    rows = regain_db_driver.sql_run("COMMIT")

    #dbDriverのクローズと200OK返却
    regain_db_driver.db_close()
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