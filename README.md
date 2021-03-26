# Blitz Work

## Blitz Work is a Django-based framework for rapid application development

### How to use

1. Add blitz_work to installed apps in settings.py.

   ```python
   INSTALLED_APPS = [
    ...,
    ...,
    'blitz_work',
   ]
   ```

2. Create the models.

   ```python
   from django.db import models


    class Author(models.Model):
        name = models.CharField(verbose_name="Name", max_length=255)
        birth_date = models.DateField(verbose_name="Birth date")


        class Meta:
            verbose_name = "Author"
            verbose_name_plural = "Authors"

        def __str__(self):
            return self.name



    class Book(models.Model):
        title = models.CharField(verbose_name="Title", max_length=255)
        publication_date = models.DateField(verbose_name="Publication date")
        authors = models.ManyToManyField(Author,verbose_name="Authors")


        class Meta:
            verbose_name = "Book"
            verbose_name_plural = "Books"

        def __str__(self):
            return self.title

   ```

3. Create the template.

    ```html
        {% extends 'blitz_base_offline.html' %}
        {% block main %}
            &lt;nav class="navbar navbar-expand-lg navbar-light bg-light"&gt;
                &lt;a class="navbar-brand" href="#"&gt;Test&lt;/a&gt;
                &lt;button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation"&gt;
                    &lt;span class="navbar-toggler-icon"&gt;&lt;/span&gt;
                &lt;/button&gt;
                &lt;div class="collapse navbar-collapse" id="navbarNavDropdown"&gt;
                    &lt;ul class="navbar-nav"&gt;
                    &lt;li class="nav-item"&gt;
                        &lt;a class="nav-link" href="{% url 'book/view' %}"&gt;Libros&lt;/a&gt;
                    &lt;/li&gt;
                    &lt;li class="nav-item"&gt;
                        &lt;a class="nav-link" href="{% url 'author/view' %}"&gt;Autores&lt;/a&gt;
                    &lt;/li&gt;
                    &lt;/ul&gt;
                &lt;/div&gt;
            &lt;/nav&gt;
            {% block content %}{% endblock %}
        {% endblock %}
    ```

4. Create the views.

    ```python
        from Book.models import Author, Book
        from blitz_work.blitzcrud import BlitzCRUD


        class BookCRUD(BlitzCRUD):
            show_title = True
            show_caption = False
            caption_is_title = True
            extend_template = "base.html"
            data = Book

        class AuthorCRUD(BlitzCRUD):
            show_title = True
            show_caption = False
            caption_is_title = True
            extend_template = "base.html"
            data = Author
    ```

5. Include the URLs.

   ```python
    from app.views import AuthorCRUD, BookCRUD
    from django.urls import path,include
    from blitz_work.blitzcrud import get_urls

    urlpatterns = [
        path('book/', include(get_urls(BookCRUD,"book"))),
        path('author/', include(get_urls(AuthorCRUD,"author"))),
    ]
   ```

6. More help

   1. Include Blitz Work help urls in urls.py

       ```python
       from blitz_work.urls import urlpatterns

       urlpatterns = [
            path('',include(urlpatterns)),
       ]
       ```

   2. Run the server.

        ```bash
        python manage.py runserver localhost:8000
        ```

   3. Go to the url [blitz-doc-en/](http://localhost:8000/blitz-doc-en/) or [blitz-doc-es/](http://localhost:8000/blitz-doc-es/)
