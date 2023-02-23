import sys; 
sys.path.append('app')
print(sys.path)

from flask import Flask, jsonify, render_template
from db_driver import dbDriver
import project

app = Flask(__name__)
#日本語設定
app.config["JSON_AS_ASCII"] = False
#ルーティング情報
app.register_blueprint(project.bp)

#ルート、プロジェクト一覧表示
@app.route('/')
def project_get():
    #dbDriverの生成
    regain_db_driver = dbDriver()
    
    #プロジェクト一覧取得SQL
    project_list_sql = f"""
                            SELECT
                                projects.project_id,
                                project_name,
                                DATE_FORMAT(projects.estimated_time,'%k:%i') as estimated_time,
                                DATE_FORMAT(SEC_TO_TIME(IFNULL(SUM(TIME_TO_SEC(commit_time)), 0)),'%k:%i') as passed_time
                            FROM
                                projects
                                LEFT JOIN processes
                                    ON projects.project_id = processes.project_id
                                LEFT JOIN tasks
                                    ON processes.process_id = tasks.process_id
                                LEFT JOIN commits
                                    ON tasks.task_id = commits.task_id
                            GROUP BY
                                project_id
                        """
    rows = regain_db_driver.sql_run(project_list_sql)
    regain_db_driver.db_close()

    #dbDriverのクローズと値返却
    regain_db_driver.db_close()
    return render_template('projects.html', title='projects', projects=rows)
    return jsonify(rows)

#プロセスステータス名一覧
@app.route('/process_statuses_name_list_get')
def process_statuses_get():
    #dbDriverの生成
    regain_db_driver = dbDriver()
    #プロセスステータス一覧取得SQL
    name_list_sql = """
                    SELECT
                        status_id,
                        status_name
                    FROM
                        process_statuses
                    """
    rows = regain_db_driver.sql_run(name_list_sql)

    #dbDriverのクローズと値返却
    regain_db_driver.db_close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)