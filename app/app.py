#pathが通ってない時はパスを通してました。
import sys; 
sys.path.append('app')
print(sys.path)

from flask import Flask, jsonify
from db_driver import dbDriver
import project

app = Flask(__name__)
#日本語設定
app.config["JSON_AS_ASCII"] = False
#ルーティング情報
app.register_blueprint(project.bp)

#ルート、プロジェクト一覧表示
#作成中
@app.route('/')
def project_get():
    #dbDriverの生成とSQL実行
    regain_db_driver = dbDriver()
    rows = regain_db_driver.sql_run("select project_id, project_name, DATE_FORMAT(estimated_time,'%k:%i') as estimated_time from projects")
    regain_db_driver.db_close()
    # return jsonify(rows)
    
    return jsonify([
            {
                "project_id": 1,
                "project_name": "プロジェクトA",
                "estimated_time": "20:00",
                "passed_time": "27:34"
            },
            {
                "project_id": 2,
                "project_name": "プロジェクトB",
                "estimated_time": "10:00",
                "passed_time": "3:10"
            },
            {
                "project_id": 3,
                "project_name": "プロジェクトC",
                "estimated_time": "5:00",
                "passed_time": "0:00"
            }
        ]
    )

if __name__ == "__main__":
    app.run()