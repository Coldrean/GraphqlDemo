from flask import Flask
from flask_graphql import GraphQLView
import graphene

app = Flask(__name__)

books = []

class Book(graphene.ObjectType):
    """ Book
    """

    id = graphene.ID(description="book ID")

    name = graphene.String(description="book name")

create = lambda id, name: Book(id=id, name=name)

books.append(create(1, "The First Book"))

class Query(graphene.ObjectType):
    """ query your books
    """

    books = graphene.List(Book, description="list books")

    version = graphene.String(description="version")

    def resolve_books(self, info):
        return books

    def resolve_version(self, info):
        return "v0.1"

# Mutation

class AddBook(graphene.Mutation):
    """ Add books
    """
    Output = Book

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        book = create(len(books) + 1, name)
        books.append(book)
        return book

class Mutation(graphene.ObjectType):
    """ mutate books
    """
    add = AddBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql',
    schema=schema, graphiql=True))

app.run(port=4901, debug=True)
