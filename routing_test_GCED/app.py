#pathが通ってない時はパスを通してました。
import sys; 
sys.path.append('routing_test_GCED')
print(sys.path)

from flask import Flask, jsonify
import create, get, edit, delete

app = Flask(__name__)
#日本語設定
app.config["JSON_AS_ASCII"] = False
#ルーティング情報
app.register_blueprint(create.bp)
app.register_blueprint(get.bp)
app.register_blueprint(edit.bp)
app.register_blueprint(delete.bp)

@app.route('/')
def project_get():
    #単純に現在地を返す
    return jsonify({"py":"app.py", "rooting":"/"})

if __name__ == "__main__":
    app.run()