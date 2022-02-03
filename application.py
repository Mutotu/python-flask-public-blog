import os
from dotenv import load_dotenv
from flask import Flask, request,jsonify,json
import sqlalchemy
import models
# Alternatively
# from models import Post, Topic, 
load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
models.db.init_app(app)



def root():
    return {
        "message":"ok"
    }
app.route('/', methods=["GET"])(root)

# Read all
# def posts_index():
#     posts = models.Post.query.all()
#     # return dict(posts)
#     return {'posts':[p.to__json() for p in posts]}
# app.route('/posts', methods=['GET'])(posts_index)

# #Create one
# def posts_create():
#     post = models.Post(
#         title = request.json["title"],
#         body = request.json["body"],
#     )
#     models.db.session.add(post)
#     models.db.session.commit()
#     return {"post":post.to__json()}
# app.route('/posts', methods=["POST"])(posts_create)


def all_posts():
    if request.method == 'GET':
        posts = models.Post.query.all()
        return {"posts":[p.to__json() for p in posts] }
    elif request.method == "POST":
        post = models.Post(
            title = request.json["title"],
            body=request.json["body"]
        )
        models.db.session.add(post)
        models.db.session.commit()
        return {"post":post.to__json()}
app.route('/posts', methods=["GET","POST"])(all_posts)

def single_post(id_of_post):
    try:
        post = models.Post.query.filter_by(id=id_of_post).first()
        
        if request.method == "GET":
            comments = post.comments
            # return { "post": post.to_json(), "comments": [c.to_json() for c in comments]}
            return { "post": post.to_json(include_comments=True)}
        elif request.method == "PUT":
            post.title = request.json["title"]
            post.body = request.json["body"]
            models.db.session.add(post)
            models.db.session.commit()
            return {
                "post": post.to__json()
            }
        elif request.method == "DELETE":
            models.db.session.delete(post)
            models.db.session.commit()
            return {"post": post.to_json()}
   
    except AttributeError:
        return "Attribute error"
    # except KeyError:
        # return " Key error" 
    # except Exception as e:
        # return {'error' :e }
    # except sqlalchemy.exc.IntegrityError:
    #     return "something happened with sqlalchemy"
   
app.route('/posts/<int:id_of_post>', methods=["GET", "PUT","DELETE"])(single_post)



def single_post_comments(id):
    post = models.Post.query.filter_by(id=id).first() 
    comment = models.Comment(body=request.json["body"])
    post.comments.append(comment)
    models.db.session.add(post)
    models.db.session.add(comment)
    models.db.session.commit()  
    return {
        "post": post.to__json(),
        "comment": comment.to__json()
    }


app.route('/posts/<int:id>comments', methods=["POST"])(single_post_comments)



def single_topic_single_post(topic_id, post_id):
    post= models.Post.query.filter_by(id=post_id).first()
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



if __name__ == '__main__':
    port = os.environ.get('PORT') or 5000
    app.run(port=port, debug=True)
