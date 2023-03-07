#pathが通ってない時はパスを通してました。
import sys; 
#sys.path.append('import_test')
print(sys.path)

from flask import Flask, render_template
from db_driver import dbDriver

app = Flask(__name__)

@app.route('/')
def mariadb():
    #dbDriverの生成とSQL実行
    regain_db_driver = dbDriver()
    rows = regain_db_driver.sql_run("select project_id, project_name, estimated_time from projects")
    regain_db_driver.db_close()
    return render_template('hello.html', title='MariaDB', projects=rows, memo = "memo")

if __name__ == "__main__":
    app.run()