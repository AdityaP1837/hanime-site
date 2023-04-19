from flask import Flask, render_template
from data import Hanime_Brain

app = Flask(__name__)
resource = Hanime_Brain()


@app.route('/')
def home():
    page_info = resource.main_page()
    return render_template("main-page.html", mpage_details=page_info)


@app.route('/hanime/<name>/')
def hanime_page(name):
    hanime_details = resource.hanime_page(name)
    return render_template("hanime-page.html", page_info=hanime_details)


@app.route('/hanime/watch/<name>/<ep_num>')
def hanime_watch_page(name, ep_num):
    watch_data = resource.watch_page(name, ep_num)
    return render_template("hanime-watch.html", page_details=watch_data)


@app.route('/pick-your-poison')
def pick_your_poison():
    content = resource.pick_your_poison()
    return render_template('pick-your-poison.html', details_info=content)


@app.route('/series/<name>/')
def series_page(name):
    details = resource.series_page(name)
    about = name.title()
    return render_template("series-page.html", about=about, series_details=details)


@app.route('/tag/<tag>/')
def release_page(tag):
    details = resource.series_page(tag)
    about = tag
    return render_template("series-page.html", about=about, series_details=details)


if __name__ == '__main__':
    app.run(debug=True)
