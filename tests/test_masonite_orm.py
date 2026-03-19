from masoniteorm.models import Model

from dumpdie.dd import dump


class User(Model):
    __fillable__ = ['name', 'email']

class Post(Model):
    __fillable__ = ['title', 'content', 'user_id']

def test_dump_masonite_orm_model(capsys):
    user = User()
    user.name = "John Doe"
    user.email = "john@example.com"

    dump(user)

def test_dump_masonite_collection(capsys):
    user1 = User()
    user1.name = "User 1"

    user2 = User()
    user2.name = "User 2"

    data = [user1, user2]
    print_var(data)

def test_dump_masonite_nested_relationship(capsys):
    user = User()
    user.name = "Author"

    post = Post()
    post.title = "First Post"
    post.user = user  # Manual assignment to simulate relationship

    dump(post)

    captured = capsys.readouterr()
    assert "Post" in captured.out
    assert "First Post" in captured.out
    assert "User" in captured.out
    assert "Author" in captured.out

def test_dump_masonite_recursive_relationship(capsys):
    user = User()
    user.name = "Cyclic User"

    post = Post()
    post.title = "Cyclic Post"

    # Create recursion
    user.latest_post = post
    post.author = user

    dump(user)

    captured = capsys.readouterr()
    assert "User" in captured.out
    assert "Cyclic User" in captured.out
    assert "Post" in captured.out
    assert "Cyclic Post" in captured.out
    assert "*recursion*" in captured.out
