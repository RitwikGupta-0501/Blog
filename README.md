# Blog Application

This is a Django-based Blog application with Django Rest Framework (DRF) integration for API functionalities.

## Features

- **User Authentication**: Register, login, and manage profiles.
- **Blog Creation**: Write and edit blog posts (editing is only available to authors).
- **Dashboard**: Displays the 8 most recent blogs.
- **Profile Page**: Shows all blogs created by the logged-in user.
- **Blog Deletion**: Users can delete their own posts.
- **Admin Authorization**: Blocks unauthorized users from accessing the Django Admin panel (403 page for unauthorized access).

## Getting Started

### Prerequisites

- Python 3.x
- Django 4.x
- Django Rest Framework

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RitwikGupta-0501/Blog.git
   cd Blog
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the site at `http://127.0.0.1:8000/`.

## API Endpoints

- `/api/blogs/`: Get all blogs.
- `/api/blogs/<id>/`: View, edit, or delete a specific blog post.
- `/api/users/`: User registration and profile management.

## Future Enhancements

- Commenting and liking posts.
- Search functionality.
- Pagination for large datasets.
- Categories and tags for better organization.
- Enhanced SEO features.

## Contributing

Feel free to submit pull requests or open issues to discuss any changes.

## License

This project is licensed under the MIT License.

You can modify the sections as needed and add more specific details based on your project’s features.
