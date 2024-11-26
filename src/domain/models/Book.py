class Book:
    id: str
    author: str
    title: str
    year: int
    status: bool

    def __init__(self, id, kwargs):
        self.id = id
        self.author = kwargs["author"]
        self.title = kwargs["title"]
        self.year = kwargs["year"]
        self.status = kwargs["status"]

    def __eq__(self, other):
        if not isinstance(other, Book):
            return False
        return self.id == other.id and \
               self.author == other.author and \
               self.year == other.year and \
               self.title == other.title and \
               self.status == other.status

    def to_dict(self):
        return {
            self.id: {
                "author": self.author,
                "title": self.title,
                "year": self.year,
                "status": self.status,
        }
    }