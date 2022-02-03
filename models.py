from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'posts'
    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body =  db.Column(db.String, nullable=False)
    topics = db.relationship("Topic", secondary="taggings")
    comments = db.relationship('Comment')
    
    def to__json(self, include_comments=False):
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
                "body":  self.body,
              
            }
            
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    def to__json(self):
        return {
              "id": self.id,
            "body":  self.body,
            "post_id":self.post_id
        }
    
class Topic(db.Model):
    __tablename__ =  'topics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    posts = db.relationship("Post", secondary="taggings")
    def to__json(self):
        return {
            "id":self.id,
            "name":self.name
        }
    
class Tagging(db.Model):
    __tablename__ = 'taggings'
    id = db.Column(db.Integer, primary_key = True)
    post_id =db.Column(db.Integer, db.ForeignKey('posts.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))