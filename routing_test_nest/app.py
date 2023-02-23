#pathが通ってない時はパスを通してました。
import sys; 
sys.path.append('routing_test_nest')
print(sys.path)

from flask import Flask, jsonify
import project

app = Flask(__name__)
#日本語設定
app.config["JSON_AS_ASCII"] = False
#ルーティング情報
app.register_blueprint(project.bp)

#ルート、プロジェクト一覧表示
@app.route('/')
def project_get():
    #単純に現在地を返す
    return jsonify({"py":"app.py", "rooting":"/"})

if __name__ == "__main__":
    app.run()