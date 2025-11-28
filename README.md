# BridgeIT - Career Guidance Platform

BridgeIT is a comprehensive career guidance platform that connects students with mentors, provides educational resources, and offers career path recommendations.

## Project Structure

```
bridge-it-world/
├── bridge_core/          # Main application for career guidance features
├── bridgeit_backend/     # Django project settings and configuration
├── core/                # Core application for user management and basic features
├── media/               # Uploaded media files
├── static/              # Static files (CSS, JS, images)
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Key Features

### Core App
- User authentication and management
- Profile management with roles (student, admin, guide, company)
- Exam listing and management

### Bridge Core App
- Career path recommendations
- Course catalog
- Mentor directory
- Mentorship session scheduling
- Educational resources library

## API Endpoints

### Authentication
- `/api/token/` - Obtain JWT token
- `/api/token/refresh/` - Refresh JWT token

### Core Endpoints
- `GET /api/core/user/` - Get current user information
- `POST /api/core/profile/` - Create user profile
- `GET /api/core/profile/` - List all profiles
- `GET/PUT/DELETE /api/core/profile/{id}/` - Profile detail operations
- `POST /api/core/exam/` - Create exam
- `GET /api/core/exam/` - List all exams
- `GET/PUT/DELETE /api/core/exam/{id}/` - Exam detail operations

### Bridge Core Endpoints
- `POST /api/bridge/career-path/` - Create career path
- `GET /api/bridge/career-path/` - List all career paths
- `GET/PUT/DELETE /api/bridge/career-path/{id}/` - Career path detail operations
- `POST /api/bridge/course/` - Create course
- `GET /api/bridge/course/` - List all courses
- `GET/PUT/DELETE /api/bridge/course/{id}/` - Course detail operations
- `POST /api/bridge/mentor/` - Create mentor
- `GET /api/bridge/mentor/` - List all mentors
- `GET/PUT/DELETE /api/bridge/mentor/{id}/` - Mentor detail operations
- `POST /api/bridge/session/` - Create mentorship session
- `GET /api/bridge/session/` - List all sessions
- `GET/PUT/DELETE /api/bridge/session/{id}/` - Session detail operations
- `POST /api/bridge/resource/` - Create resource
- `GET /api/bridge/resource/` - List all resources
- `GET/PUT/DELETE /api/bridge/resource/{id}/` - Resource detail operations

## Setup Instructions

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

5. Start the development server:
   ```
   python manage.py runserver
   ```

## Testing

Run tests with:
```
python manage.py test
```

## Models

### Core App Models
- **Profile**: Extended user profile with education details and career goals
- **Exam**: Educational exams with scheduling information

### Bridge Core App Models
- **CareerPath**: Detailed career path information with salary and growth data
- **Course**: Educational courses linked to career paths
- **Mentor**: Mentor profiles with expertise and experience details
- **MentorshipSession**: Scheduled mentorship sessions between mentors and students
- **Resource**: Educational resources categorized by type and career path

## Technologies Used

- Django 5.1
- Django REST Framework
- Simple JWT for authentication
- SQLite database (default, can be changed in settings)

## License

This project is proprietary and confidential.