## Python/Flask Public Blog Codealong

We're going to build the backend of our public blog database that we saw in unit 2, except in flask rather than express. 

We're not going to worry about building a frontend today. In your final form as Python developers, you can just make a python backend and attach a react frontend to it. 

Let's go to dbdesigner.net and illustrate what tables we need. <br><br>

![screenshot](pythonblog1.png)

**How to get started with an existing Python project** 

(as opposed to starting from scratch; analogous to cloning down an express project and running `npm install`)

```
git clone git clone git@git.generalassemb.ly:SEIR-1011/python-flask-public-blog.git
```

```
cd python-flask-public-blog
```
We can't just "npm install" at this point, b/c we would install the dependencies globally. There's an extra step we have to run (create and activate a virtual environment):

```
python3 -m venv virt-env
```
Now activate the virtual environment:
```
source virt-env/bin/activate
```
`which python3` should give you the folder you're in (not a global folder)

Let's do our first install from requirements.txt file (think package.json)
```
pip3 install -r requirements.txt
```

        ASIDE: (this doesn't appear to be useful for WSL users, but for Mac users it may be. Maybe skip this altogether.)

        If you accidentally globally install dependencies, you need to clean it up...

        $ deactivate
        
        $ pip3 list
        
        Copy the list of dependencies that appears and paste the list into a new file in VS Code. REMOVE `pip` FROM THE LIST so you won't have to reinstall it later. Remove all the version numbers from the list items (so you have just names of dependencies, one per line)

        alt+cmd+down_arrow creates a cursor at beginning of each line
        cmd+rt_arrow places all cursors at end of line 
        backspace to delete all the numbers
        on first line go end of line white space, shift+rt_arrow highlights all the newline characters
        space
        highlight the 2 spaces after the first word and then cmd+d to highlight all the duplicate spaces
        with all the intervening whitespaces still highlighted, backspace to get rid of extra spaces

        At the beginning of the big block of text you now have, put `pip3 uninstall -y` and then copy and paste the whole text into your command line after that and run it. You'll now have all your dependencies (except `pip`, if you removed it from the list) uninstalled.

        To get ipython back, run `pip3 install ipython`

**Setting up our DB tables**

Set up DB url

```
touch .env
```
```
DATABASE_URL=postgresql://localhost:5432/flask_public_blog
```

(windows users modify with `postgres` and your database password)
```
DATABASE_URL=postgresql://postgres:YOUR_DATABASE_PASSWORD@localhost:5432/flask_public_blog
```

```
alembic init migrations
```

In alembic.ini, comment out line 42 (` sqlalchemy.url = driver ...`)

env.py
```
from dotenv import load_dotenv
load_dotenv()
import os
```
after `config = context.config...`  :

```
config.set_main_option('sqlalchemy.url', os.environ.get('DATABASE_URL'))
```

```
alembic upgrade head
```

Gives error message "No module named 'psycopg2'" (i.e. forgot to put it in requirements.txt)

```
pip3 install psycopg2
```

If you are an M1 chip person who found Tuesday that this library didn't work for you, but psycopg2-binary did work for you, you should do that.
If you found that you needed to prepend some LD flags to do this "LDFLAGS=`echo $(pg_config --ldflags)` pip3 install psycopg2", you should do that.

In node, when you npm install something, it automatically gets put in package.json. Not the case with requirements.txt. To get newly added dependencies into requirements.txt run 

```
pip3 freeze
``` 

which spits that out into a machine readable format, and then run 

```
pip3 freeze > requirements.txt
``` 

to send that new list into requirements.txt

Now you'll need to create a database:
```
createdb NAMEOFYOURDATABASE
```

```
alembic upgrade head
``` 
should now give you: 
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

Let's make some migrations
```
alembic revision -m create-posts
```

Let's build a posts table - modify revision file as so:
```
def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('body', sa.String)
    )

def downgrade():
    op.drop_table('posts')
```
Now run the revision:
```
alembic upgrade head
```
Check psql to verify that our new 'posts' table is in there.

Let's create a comments table: 
```
alembic revision -m create-comments
```
then in revision file:

```
def upgrade():
    op.create_table(
        'comments', 
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('body', sa.String),
    )

def downgrade():
    op.drop_table('comments')
```

How to add a column to comments table after initial creation?

```
alembic revision -m add-post_id-to-comments
```

```
def upgrade():
    op.add_column('comments', sa.Column('post_id', sa.Integer))

def downgrade():
    op.remove_column('comments', 'post_id')
```

Let's create a topics table:

```
alembic revision -m create-topics
```    

```
def upgrade():
    op.create_table(
        'topics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )


def downgrade():
    op.drop_table('topics')
```

Let's create a taggings table:
```
alembic revision -m create-taggings
```
```
def upgrade():
    op.create_table(
        'taggings',
        sa.Columm('id', sa.Integer, primary_key=True),
        sa.Column('post_id', sa.Integer), 
        sa.Column('topic_id', sa.Integer)
    )

def downgrade():
    op.drop_table('taggings')
```
```
alembic upgrade head
```

If you make a mistake and need to go backwards and undo 1 revision (or -X for X revisions):
```
alembic downgrade -1
```

In Express in sequelize we would go to our models folder and we would have a separate file for each model. In python importing stuff from a file within a folder is a little trickier (to be covered at a later time, perhaps). We'll keep things simple by using a single file for all our models.

Make a single file called `models.py` at top level of project. Remember, capitalization matters!

Tip: put your migration for that model side-by-side in VS Code with models.py to see what columns you need to have in your model.

```
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String)
    # TODO: hasMany comments

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    # TODO: declare a foreign key
    post_id = db.Column(db.Integer)

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Tagging(db.Model):
    __tablename__ = 'taggings'
    id = db.Column(db.Integer, primary_key=True)
    #TODO foreign key
    post_id = db.Column(db.Integer)
    topic_id = db.Column(db.Integer)
```    


We're going to pause on hooking up our foreign keys and associations until we actually need them b/c we're going to create some routes to let us do CRUD on our posts before we hook up any associations.

**Hook up some CRUD routes**

make `application.py` in top level folder

```
import os 
from flask import Flask
app = Flask(__name__) # this is unique to Flask, node doesn't require this, this is always the name of the current file that you're in

if __name__ == '__main__':
    port = os.environ.get('PORT') or 5000
    app.run(port=port, debug=True)
```
The above is the bare minimum required to run a flask server. 

run `python3 application.py` to see that it works

Let's talk about importing things in Python. When you say import models, it looks for a file on the same level as models.py and all variables declared are accessible as a property of models. 

Add `import models` below `from flask import Flask`

```
from flask import Flask
import models
```

I.e. we declared Post, Comment, Topic, Tagging in models.py, but we can't simply write `print(Post)` in application.py. We instead can write `print(models.Post)` below `import models` and it'll work. 

```
import models
print(models.Post)
```


(Alternatively you could destructure your imports):
```
from models import Post, Topic
print(Post)
print(Topic)
```

Next, we need to do a setup step that has no analog in express. We need to form a connection between our db and our web server. 

(some heading info is similar to our env.py)

application.py:
```
from dotenv import load_dotenv
.
.
.
load_dotenv()
.
.
.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
```
(alembic needed to know this to run our migrations, but flask needs to know it to run our whole app.)
```
.
.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
models.db.init_app(app)
.
.
.
```
(this connects our db ORM with our flask app)

All we need to do now is to build our routes. 

Start with a root route:

```
def root():
    return 'ok'
app.route('/', methods=["GET"])(root)
```

To see our routes:
```
FLASK_APP=application.py flask routes
```

In express we could res.json, res.render, res.send etc. Flask just figures out what format it's supposed to be and handles it. If it's a string, it sends back plain text, if it's a dictionary it sends back json. 

```
def root():
    return {"message": "ok"}
app.route('/', methods=["GET"])(root)
```

Now hit http://localhost:5000 in postman and you should get 'ok' returned.

So for all the points we want to have json returned for, we have to return a dictionary. 

In express res.send sent plain text, and res.json sent json format text. Flask just figures out what the format should be; if it's a string it send it as plain text, if you put a dictionary it figures out that it's supposed to send a json response.

What that tells us is that for all of our endpoints that we want to return json, we have to code it to return a dictionary in application.py.


Let's start making some CRUD routes for posts.

For each of these routes it helps to have a naming convention. After defining each function you have to app.route it. 

```
def posts_index():
    return 'hello from posts index'
app.route('/posts', methods=["GET"])(posts_index)
```

Now postman GET  http://localhost:5000/posts

Now: 
```
def posts_index():
    posts = models.Post.query.all()
    return posts
    # return 'hello from posts index'
```

Now postman http://localhost:5000/posts
and see error 
```
"TypeError: The view function did not return a valid response...but it was a list "
``` 
In other words it isn't OK to return a list as a datatype. 

Which datatype should it actually be?  Dictionary, b/c flask converts it to json because json is what our front end is set up to read. 

So how to convert this list into a dictionary?

```
def posts_index():
    posts = models.Post.query.all()
    return {"posts": posts}
```    

Now postman http://localhost:5000/posts and we get 
```
{
    "posts": []
}
```
Cool Let's now make our endpoint for creating posts. 

application.py

```
def posts_create():
    return 'hello from posts_create'
app.route('/posts', methods=["POST"])(posts_create)
```
Now POST to postman http://localhost:5000/posts

Let's modify it so it actually does something:

Notice flask has no `(req,res)`. Why? At the top add to this line 
```
from flask import Flask
``` 
and make it 
```
from flask import Flask, request
```

then: 
```
def posts_create():
    post = models.Post(
        title=request.json["title"],
        body=request.json["body"],
    )
    models.db.session.add(post)
    models.db.session.commit()
```

req.body has become request.json

also add a return statement. for starters, let's try:
```
models.db.session.add(post)
models.db.session.commit()
return post
```

It gives us an error of "NameError: name &#x27;request&#x27; is not defined "

First problem is that we have to add a body to our request in postman. 

```
{
    "title": "test post 1",
    "body": "testing 1"
}
```

Second problem is that we have to modify this line 
```
return post
``` 
to 
```
return {"post": post}
```

then postman and see this error:

```
"TypeError: Object of type Post is not JSON serializable"
```
It sees the post, but there's no built in way to turn that post into key/value pairs. 

in application.py we could do this: 

```
def posts_create():
.
.
        return {
            "id": post.id,
            "title": post.title,
            "body":  post.body
        }
```
But a better approach is for your controller methods not to get cluttered up with all this `"id": post.id, "title": post.title, "body":  post.body` which will give you a lot of eye strain. So instead let's define a method in our post class called to_json:

models.py
```
class Post(db.Model):
.
.
.
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "body":  self.body
        }

```

In python "self" is used instead of "this"

Notice `self` is being passed in as an argument. That's because in python every method that is defined within a class has to get "self" as its first argument, that's just a python rule.

Now in application.py change 
```
return {"post": post}
``` 
to  
```
return {"post": post.to_json()}
```

and run postman again and you should get a success message:

```
{
    "post": {
        "body": "testing 2",
        "id": 3,
        "title": "test post 2"
    }
}
```
Interesting note: we didn't have to `app.use` like in express.

What happens when we postman GET `http://localhost:5000/posts` now? Error:
```
TypeError: Object of type Post is not JSON serializable
```
How would we now fix this?

application.py

```
return {"posts": posts.to_json()}
``` 
won't work. postman GET `http://localhost:5000/posts` to confirm. Why? It's a list and doesn't have a to_json method. 

Instead, we need 
```
return {"posts": [p.to_json() for p in posts]}
```
Yes, this feels wrong and backwards but it works. Run GET in postman now. You need to wrap it in [] so it becomes a list. 

Guess what we can do if two methods have the same route string? i.e. app.route('/posts') where one is a GET and the other is a POST. We can actually combine them. 

```
def all_posts():
    if request.method == 'GET':
        posts = models.Post.query.all()
        return {"posts": [p.to_json() for p in posts]}
    elif request.method == 'POST':
        post = models.Post(
            title=request.json["title"],
            body=request.json["body"],
        )
        models.db.session.add(post)
        models.db.session.commit()
        return {"post": post.to_json()}
app.route('/posts', methods=["GET"])(posts_index)

```
Then comment out posts_create() and posts_index() methods in application.py. I didn't incorporate this into my dry run. This is a very pythonic thing, other languages don't have this. 

Now check your routes with `FLASK_APP=application.py flask routes`

But going forward to writing our SHOW, DELETE, and EDIT routes, let's use this condensed method approach. 

```
def single_post():
    return('this is a single post')
app.route('/posts/<int:id>', methods=["GET", "PUT", "DELETE"])(single_post)
```
<int:id> could potentially be another datatype i.e. <string:name>

BEWARE the trailing slashes! For post, put, delete requests, trailing slashes matter. 
```
/posts/<int:id>
``` 
will behave differently from 
```
/posts/<int:id>/
```
Take home point: pick a way and stick with it, / OR no /. 

Now check your routes with `FLASK_APP=application.py flask routes`

```
def single_post():
    if request.method == "GET":
        return('this is a GET single post')
    elif request.method == "PUT":
        return('this is a edit single post')
    elif request.method == "DELETE":
        return('this is a delete single post')
app.route('/posts/<int:id>', methods=["GET", "PUT", "DELETE"])(single_post)
```

Postman 
```
GET `http://localhost:5000/posts/2
``` 
and what happens?
```
Error `TypeError: single_post() got an unexpected keyword argument &#x27;id&#x27;`
```
This is because whenever you have a wildcard in one of your routes, you need to give that function a parameter corresponding to that wildcard. So change 
```
def single_post():
``` 
to 
```
def single_post(id_of_post):
.
.
.
app.route('/posts/<int:id_of_post>', methods=["GET", "PUT", "DELETE"])(single_post)
```

Now postman GET, PUT and DELETE to see the routes work. 

We now can think about how to get a dynamic id in /posts/<int:id> . In express we would have done that with `req.params`. How do we do that here? Actually it just comes built into your function. 

**READ one post**
```
if request.method == "GET":
    post = models.Post.query.filter_by(id=id_of_post).first()
    # return post.to_json()
    return { "post": post.to_json(), "message": "post found successfully" }
```

We include `.to_json` because a post cannot be sent as a response.

**EDIT one post**

Make your code DRY... Move `post = ...` up a line so it can be used by all conditionals for GET, PUT, and DELETE. 

Then 
```
elif request.method == "PUT":
    post.title = request.json["title"]
    post.body = request.json["body"]
    models.db.session.add(post)
    models.db.session.commit()
    return { "post": post.to_json() }
```

**DELETE one post**

```
elif request.method == "DELETE":
    models.db.session.delete(post)
    models.db.session.commit()
    return { "post": post.to_json() }
```

Postman PUT and DELETE to see that they work

How do we handle errors in our views?

Very similar to how we did it in express async/await -- instead of try/catch we use try and except. But in javascript you catch whatever error that happens. In python (and most other languages) you except in different ways based on the error that it is. In other words, an "attribute" error is different from a "key not found" is different from "dictionary" errors is different from "can't find index in list". So when you except, you have to specify what kind of error you want to result from running this block. 

```
def single_post(id_of_post):
    try:
    .
    .
    .
    except AttributeError:
        return "something happened in the attributes"
    except KeyError:
        return "something happend with the keys"
```

Try postmanning a PUT with the body of:
```
{
    "title": null,
    "body": "testing something"
}
```
This violates sqlalchemy's rules (see the response box in postman). Notice that for this particular error we will need to import a library at the top of application.py:

```
import sqlalchemy
```

and then add another except:
```
except sqlalchemy.exc.IntegrityError:
    return "something happened with sqlalchemy"
```

Now re-run postman and see that your error is returned.

The most general catch-all error to have is:
```
except Exception as something:
    print(something)
    return "something went wrong, very general we aren't specifying what"
```

Alternate way of error handling is inline tuple at top of route block:

```
def single_post(id_of_post):
    post = models.Post.query.filter_by(id=id_of_post).first()
    if post == None:
        return { "message": "Post not found" }, 404
```

Moooooving on........

**Associations**

Let's create a comment under a post. 

Time to backpedal to our associations and put them in place. 

models.py
```
class Comment(db.Model):
.
.
.
post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

class Post(db.Model):
.
.
.
comments = db.relationship('Comment')

```

This is going to give you some magic methods, just like sequelize does. 

Now let's build this route POST `/posts/:id/comments`

Go back to application.py and add:
```
def single_post_comments(id):
    return 'hi"
app.route('/posts/<int:id>/comments', methods=["POST"])(single_post_comments)
```

Postman POST `http://localhost:5000/posts/3/comments` to verify it's hooked up.

Create a comment for a post that already exists.

look up that post 
```
def single_post_comments(id):
    post = models.Post.query.filter_by(id=id).first() 
    comment = models.Comment(body=request.json["body"])
    post.comments
```

In `models.py` Post has an attribute called "comments" which is a list. Although it's currently empty, it is still a list. And just like any list you can `append()` into it. In `application.py` change `post.comments` to `post.comments.append(comment)`. After that add new lines 
```
post.comments.append(comment)
models.db.session.add(post)
models.db.session.add(comment)
models.db.session.commit()
```
So this is using that association -- it's a lot like a sequelize association (instead of `post.add(comment)`)
```
return {
    ""post": post.to_json(), 
    "comment"" comment.to_json() 
}
```

What else do we need? In `models.py` we need to make a function in the Comment model.

```
class Comment(db.Model):
.
.
.
    def to_json(self):
        return {
            "id": self.id,
            "body": self.body
        }
```

Now postman POST `http://localhost:5000/posts/3/comments` and in the body put 

```
{
    "body": "test comment 1"
}
```

Should get a successful response.

It would be nice to know the post's id in the response. So add a line in `models.py`:

```
    def to_json(self):
        return {
            "id": self.id,
            "body": self.body,
            "post_id": self.post_id
        }
```

Check psql `select * from comments;`

Now let's write code that when we get a single post, the post will have the comments of that post attached to it. 

application.py
```
def single_post(id_of_post):
.
.
.
if request.method == 'GET':
    comments = post.comments
    return { "post": post.to_json(), "comments": [c.to_json() for c in comments]}
```

Now postman `http://localhost:5000/posts/3`

What about "includes" i.e. what about looking up the associations all in the same query? In sqlalchemy that is done by default.

Now let's make sure that whenever a post is returned, it also returns its comments in json form. add `"comments": [c.to_json() for c in self.comments]` as below:

```
class Post(db.Model):
.
.
.
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "body":  self.body,
            "comments": [c.to_json() for c in self.comments]
        }
```        

Postman GET `http://localhost:5000/posts/3`

This might be TOO powerful -- you may not always want to return all a post's comments when you get a post. You could create a conditional (didn't include in my code) to give the developer the option of getting the attached comments or not:

models.py
```
class Post(db.Model):
.
.
.
    def to_json(self, include_comments=False):
        if include_comments:
            return {
                "id": self.id,
                "title": self.title,
                "body":  self.body,
                "comments": [c.to_json() for c in self.comments]
            }
        else:
            return {
                "id": self.id,
                "title": self.title,
                "body":  self.body
            }
```            
application.py:
```
def single_post(id_of_post):
.
.
.
    if request.method == "GET":
        # comments = post.comments
        return { "post": post.to_json()
        (include_comments=True)
    }
```

Post has many comments. What if we also want the comment to have a post relationship? Actually, sqlalchemy is not set up to do it this way:
```
class Comment(db.Model):
.
.
.
    post = db.relationship('Post')
```

At this point if you postman 
```
GET `http://localhost:5000/posts/3`
``` 
you'll get a warning in terminal 
```
SAWarning: relationship 'Comment.post' will copy column posts.id to column comments.post_id, which conflicts with relationship(s): 'Post.comments' (copies posts.id to comments.post_id). If this is not the intention...back_populates
```

So sqlalchemy is not actually set up for you to have hasMany and belongsTo on two different models (for reasons that aren't totally clear).

To make this work you would have to put in your Post model a backref attribute:
```
class Post(db.Model):
    .
    .
    .
    comments = db.relationship('Comment', backref="post")
```
and you would then have to delete 
```
post = db.relationship('Post')` from `class Comment(db.Model):
```

But keep in mind if you don't want to define both sides of the relationship you don't have to do this.

**Many to Many**

Tagging is the join model between Topic and Comment. 

In Tagging, declare both foreign keys.

models.py
```
class Tagging(db.Model):
    .
    .
    .
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
```

Now we want Post to have many Topics
```
class Post(db.Model):
    .
    .
    .
    topics = db.relationship("Topic', secondary="taggings")
    # in sequelize, think "topic hasMany posts through taggings"
```
Now add to Topic model:

```
class Topic(db.Model):
    .
    .
    .
    posts = db.relationship('Post', secondary='taggings')
```

Now let's create a route that uses this M-T-M relationship.

application.py
```
def single_topic_single_post(topic_id, post_id):
# this is a function that will associate a topic with a post
    post = models.Post.query.filter_by(id=post_id).first()
    topic = models.Topic.query.filter_by(id=topic_id).first()
    if request.method == "PUT":
        post.topics.append(topic)
    elif request.method == "DELETE":
        post.topics.remove(topic)
    models.db.session.add(post)
    models.db.session.commit()
    return {
        "topic": topic.to_json(),
        "post": post.to_json()
    }
app.route('/topics/<int:topic_id>/posts/<int:post_id>', methods=["PUT", "DELETE"])(single_topic_single_post)
```

models.py
```
class Topic(db.Model):
.
.
.
    posts = db.relationship('Post', secondary='taggings')
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }
```

If you want to un-associate them, you could do that.

We don't have any topics yet in our database so we can't illustrate using `def single_topic_single_post(topic_id, post_id):` but this is how it works. First we also would need to create def's for create topic. We could also make routes for GET topics and POST topics, but it's the same approach as GET posts and POST posts. 

If the goal is to associate them:
```
post.topics.append(topic)
```
if the goal is to remove topic:
```
post.topics.remove(topic)
``` 
and then save the new result and return {} something. 
