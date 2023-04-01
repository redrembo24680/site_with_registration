from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intro = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


class Coment(db.Model):
    com_id = db.Column(db.Integer, primary_key=True)
    com_text = db.Column(db.Text, nullable=False)
    com_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Coment %r>' % self.com_id




@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/reviews')
def coments():
    coment = Coment.query.order_by(Coment.com_date.desc()).all()
    return render_template("reviews.html", coment=coment)


@app.route('/post/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/post/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')

    except:
        return "При видаленні виникла помилка"


@app.route('/reviews/<int:com_id>/delete')
def coment_delete(com_id):
    coment = Coment.query.get_or_404(com_id)

    try:
        db.session.delete(coment)
        db.session.commit()
        return redirect('/reviews')

    except:
        return "При видаленні виникла помилка"


@app.route('/post/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')

        except:
            return 'При редагуванні статті виникла помилка'
    else:
        return render_template("post_update.html", article=article)


@app.route('/create_review', methods=['POST', 'GET'])
def create_coment():
    if request.method == 'POST':
        com_text = request.form['com_text']

        comants = Coment(com_text=com_text)

        db.session.add(comants)
        db.session.commit()
        return redirect('/reviews')

    else:
        return render_template("create_reviews.html")


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        db.session.add(article)
        db.session.commit()
        return redirect('/posts')

    else:
        return render_template("create_article.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
