from pymongo import MongoClient
from mongoengine import *
import datetime

client = MongoClient()
# явне вказання хосту та порту
# client = MongoClient('localhost',27017)
# Mongo URI формат
# client = MongoClient('mongodb://localhost:27017')
db = client.kovalenkoOS16K
# dictionary-style
# db = client['kovalenkoOS16K']
# insert one record
posts = db.posts
post_data = {
    'Title': 'MongoDB and Python',
    'Content': 'PyMongo is funny thing',
    'Author': 'Scott'
}
result = posts.insert_one(post_data)
print('One post: {0}'.format(result.inserted_id))
# insert many records
post_1 = {
    'Title': 'Testing: criteria and methods',
    'Content': 'Testing criteria. Testing methods',
    'Author': 'Maryna V. Didkovska'
}
post_2 = {
    'Title': 'Learning Python',
    'Content': 'Python tips and interesting features',
    'Author': 'Mark Lutz'
}
post_3 = {
    'Title': 'MongoDB basics',
    'Content': 'MongoDB tips',
    'Author': 'Peter Membrey'
}
post_4 = {
    'Title': 'Python Pocket Reference',
    'Content': 'Need-to-know information about Python',
    'Author': 'Mark Lutz'
}
new_result = posts.insert_many([post_1, post_2, post_3, post_4])
print('Multiple posts: {0}'.format(new_result.inserted_ids))
# getting record
searched_post = posts.find_one({'Author': 'Maryna V. Didkovska'})
print("Found record: ",searched_post)
# getting multiple records
searched_posts = posts.find({'Author': 'Mark Lutz'})
print("Found records: ",searched_posts)
for post in searched_posts:
    print("Record: ",post)
# using mongoengine
connect('mongoengine_test_kovalenko16K', host='localhost', port=27017)

class Author(Document):
    name = StringField(required=True, max_length=50)
class Post(Document):
    title = StringField(required=True, max_length=200)
    content = StringField(required=True)
    author = ReferenceField(Author)
    published = DateTimeField(default=datetime.datetime.now())

    @queryset_manager
    def live_posts(self, queryset):
        return queryset.filter(title='MongoDB: The second edition')

# add new record using Post class
author = Author(name='Kristina Chodorow')
author.save()
post_5 = Post(
    title='MongoDB: The Definitive Guide',
    content='The definitive guide for MongoDB',
    author= author
)
post_5.save()
print("New record title: ",post_5.title)
post_5.title = 'MongoDB: The second edition'
post_5.save()
print("New title for record: ",post_5.title)
print("The number of posts with name 'MongoDB: The second edition': ",len(Post.live_posts()))
# trying to add record without required field
#test_post = Post(content='some content', author='Sam')
#test_post.save()
