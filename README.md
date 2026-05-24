# Book Management System - Backend

FastAPI backend for the Book Management System with MongoDB integration, JWT authentication, and async operations.

## Setup Instructions

### Prerequisites

- Python 3.9+
- MongoDB (local or Atlas)

### Installation

1. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your MongoDB URI and JWT secret
```

4. Run the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

## API Endpoints

### Authentication

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get current user profile (protected)

### Books

- `POST /api/books` - Create a book (protected)
- `GET /api/books` - List books with pagination, search, filter, sort
- `GET /api/books/{id}` - Get book details
- `PUT /api/books/{id}` - Update a book (protected)
- `DELETE /api/books/{id}` - Delete a book (protected)

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:

- `MONGODB_URL` - MongoDB connection string
- `JWT_SECRET` - Secret key for JWT tokens
- `ALLOWED_ORIGINS` - CORS allowed origins
