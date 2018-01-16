
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
## Local DB URI ##
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://blogmaster:spillyourguts@localhost:3306/blogmaster'

##Heroku DB URI ##
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ba4ee7c07c02a0:97201782@us-cdbr-iron-east-05.cleardb.net/heroku_53dc666f66e6252'


app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    title = db.Column(db.String(120))
    post = db.Column(db.String(560))


    def __init__(self, name, title, post):
        self.name = name
        self.post = post
        self.title = title

@app.route('/')
def redirect_me():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def index():

    blog_post_entries = BlogPost.query.all()
    if request.method == 'POST':

        search_terms = request.form['search']
        return render_template(
                                'home.html',
                                title = "Blog!",
                                blog_post_entries = blog_post_entries,
                                search_terms = search_terms,
                                )

    return render_template('home.html',title="Blog",
        blog_post_entries=blog_post_entries)


@app.route('/add-new', methods=['POST', 'GET'])
def add_new():

    if request.method == 'POST':
        print("POST from add New")
        name = request.form['name']
        post = request.form['blog_post']
        title = request.form['title']
        to_db = BlogPost(name, title, post)
        db.session.add(to_db)
        db.session.commit()
        print(to_db.id)

        return redirect('/view?post_id='+str(to_db.id))

    return render_template(
                            'add-new.html',
                            title="Blog",
                            )


@app.route('/view', methods=['POST', 'GET'])
def view_post():

    post_id = request.args.get('post_id')
    blog_post_entry = BlogPost.query.get(post_id)
    name = blog_post_entry.name
    title = blog_post_entry.title
    post_content = blog_post_entry.post
    return render_template(
                            'view-post.html',
                            name = name,
                            title = title,
                            post_content = post_content,
                            )


if __name__ == '__main__':
    app.run()
