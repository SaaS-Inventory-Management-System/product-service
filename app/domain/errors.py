"""Domain-level errors, independent of any transport (no HTTP status codes here)."""

class ArticleAlreadyExistsError(Exception):
    pass
    
class ArticleNotFoundError(Exception):
    pass

class CategoryAlreadyExistsError(Exception):
    pass

class CategoryNotFoundError(Exception):
    pass

class CategoryInUseError(Exception):
    pass