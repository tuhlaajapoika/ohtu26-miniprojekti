from refmanager.models.reference import (
    Article,
    Book,
    Conference,
    Thesis,
    Website,
)

REFERENCE_TYPES = {
    Article: Article.reference_type,
    Book: Book.reference_type,
    Conference: Conference.reference_type,
    Thesis: Thesis.reference_type,
    Website: Website.reference_type,
}
