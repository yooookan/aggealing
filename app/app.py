from flask import Flask, render_template, request
from . import annealing

app = Flask(__name__, static_folder='./static')

@app.route("/", methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        cat1 = request.form.get('cat1')
        cat2 = request.form.get('cat2')
        cat3 = request.form.get('cat3')
        cat4 = request.form.get('cat4')
        date1 = request.form.get('date1')
        date2 = request.form.get('date2')
        date3 = request.form.get('date3')
        date4 = request.form.get('date4')
        category_list = [cat1, cat2, cat3, cat4]
        date_list = [date1, date2, date3, date4]

        categorys = []
        dates = []
        for cat in category_list:
            if not cat == 'Choose...':
                categorys.append(cat)
        for date in date_list:
            if not cat == '':
                dates.append(date)
        print(dates)

        res, idx, present_names, category_names, prices, imgs = annealing.process(categorys, dates)
        
        return render_template("result.html", date1=date_list[0], date2=date_list[1], 
                               present_name1=present_names[0], present_name2=present_names[1], 
                               category1 = category_names[0], category2 = category_names[1],
                               price1 = prices[0], price2 = prices[1],
                               image_path1=imgs[0], image_path2=imgs[1])
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)