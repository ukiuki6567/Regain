import sys; 
sys.path.append('app')
print(sys.path)

from flask import Flask, jsonify, render_template
from db_driver import dbDriver
import project

from sql_template import SQLTemplates as sql_temp

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
    
    try:
        #プロジェクト一覧取得SQL
        project_list_sql = sql_temp.PROJECT_SELECT_SQL.format(
            project_estimated_time_sum = sql_temp.PROJECT_ESTIMATED_TIME_SUM_SELECT_SQL
        )
        rows = regain_db_driver.sql_run(project_list_sql)
    except Exception as e:
        print ('=== エラー内容 ===')
        print ('type:' + str(type(e)))
        print ('args:' + str(e.args))
        print ('e自身:' + str(e))
        return jsonify() # 本当はエラーページの表示をしたい

    #dbDriverのクローズと値返却
    regain_db_driver.db_close()
    # return render_template('projects.html', title='projects', projects=rows)
    return 200

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=80)
