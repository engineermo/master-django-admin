from faker import Faker

faker = Faker()

from main.models import Blog, Comment

for blog in Blog.objects.iterator():
    comments = [Comment(text=faker.paragraph(), blog=blog) for _ in range(0, 3)]
    Comment.objects.bulk_create(comments)


from main.models import Category
Category.objects.create(name= 'Web development')
Category.objects.create(name= 'Data Science')
Category.objects.create(name= 'Python')
Category.objects.create(name= 'Django Security')
