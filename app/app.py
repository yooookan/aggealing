from flask import Flask, render_template, request
from . import annealing

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        cat1 = request.form.get('cat1')
        cat2 = request.form.get('cat2')
        cat3 = request.form.get('cat3')
        cat4 = request.form.get('cat4')
        category_list = [cat1, cat2, cat3, cat4]
        categorys = []
        for cat in category_list:
            if not cat == 'Choose...':
                categorys.append(cat)

        res, idx, name = annealing.process(categorys)
        print(name)
        
        return render_template("result.html", present_name=name)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)