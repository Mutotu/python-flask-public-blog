# Public blog... in flask!
It's throwback Thursday! Remember this gem? https://git.generalassemb.ly/SEIR-1011/express-public-blog

### Overview
We will build a flask app that provides a backend for a public blog. We need to satisfy all the following use cases:

| http verb  | route | notes | 
| ------------- | ------------- | --- | 
|GET    | /                              | just says 'ok' |
|GET    | /posts                         | doesn't include comments on each post |
|GET    | /posts/:id                     | includes the comments at a separate json key |
|POST   | /posts                         | returns the post that got created|
|PUT    | /posts/:id                     | returns the edited post |
|DELETE | /posts/:id                     | returns the deleted post |
|POST   | /posts/:id/comments            | returns the post and the comment that got created at 2 separate json keys|
|GET    | /topics                        | |
|POST   | /topics                        | returns the topic that got created|
|PUT    | /topics/:topicId/posts/:postId | associates a post with a topic, returns the post and topic at separate json keys|
|DELETE | /topics/:topicId/posts/:postId | disassociates a post from a topic, returns the post and topic at separate json keys |
|GET    | /topics/:id/posts              | returns the topic and the post as separate json keys|


### Setup
1. Clone down the repo & `cd` into it
1. `python3 -m venv virt-env` to set up a virtual environment folder in this project
1. activate your virtual environment (different commands for mac vs windows). your `pip3 list` should be mostly empty
1. `pip3 install -r requirements.txt`; this is like `npm i` after cloning down an express repo. It downloads everything in `requirements.txt`

### Notes
- simplest possible approach: 1 file for models, all routes in application.py
- trailing slashes matter on your routes!
- `to_json` & `__repr__`
- if you define the belongsTo / hasMany on both ends, you get a warning that you're supposed to use backref instead. backref successfully defines the inverse
- building a m-t-m: need a table, a class w/ 2 ForeignKey declarations, and a secondary
- decorators
- multiple methods in a single route
