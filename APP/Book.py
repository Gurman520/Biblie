class Book:
    """
    Кдасс Книга - является базовым классом для каждой книги.
    """
    def __init__(self, id, title, author, year, status='в наличии'):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return f"{self.id}: {self.title} by {self.author} ({self.year}) - {self.status}"