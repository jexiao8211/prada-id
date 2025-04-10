# Prada ID

A web application for classifying vintage Prada clothing by season using machine learning.

## Features

- Image upload and classification
- User-contributed dataset expansion
- Continuous model improvement through user contributions
- Season classification for vintage Prada pieces

## Tech Stack

### Backend
- FastAPI
- PostgreSQL
- Redis
- Celery
- PyTorch
- scikit-learn
- OpenCV

### Frontend
- React with TypeScript
- Modern UI/UX

### Infrastructure
- Docker
- AWS S3
- Poetry

## Getting Started

### Prerequisites
- Python 3.9+
- Poetry
- Docker
- Node.js 16+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prada-id.git
cd prada-id
```

2. Install Python dependencies:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start the development servers:
```bash
# Backend
poetry run uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Project Structure

```
prada-id/
├── app/                    # Backend application
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality
│   ├── db/                # Database models and migrations
│   ├── ml/                # Machine learning models
│   └── services/          # Business logic
├── frontend/              # React frontend
├── tests/                 # Test suite
└── docker/                # Docker configuration
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 