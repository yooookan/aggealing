#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request
from . import annealing

#Flaskオブジェクトの生成
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        cat1 = request.form.get('cat1')
        cat2 = request.form.get('cat2')
        cat3 = request.form.get('cat3')
        cat4 = request.form.get('cat4')
        print('{}, {}, {}, {}'.format(cat1, cat2, cat3, cat4))
        res, idx, name = annealing.process()
        print(name)
        
        return render_template("result.html", present_name=name)
    else:
        return render_template("index.html")

# @app.route("/index", methods=['GET'])
# def get():
#     return render_template("index.html")

#おまじない
if __name__ == "__main__":
    app.run(debug=True)