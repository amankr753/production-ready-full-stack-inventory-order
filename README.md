# Production-Ready Inventory & Order Management System

Full-stack inventory and order management platform built with FastAPI, React, PostgreSQL, SQLAlchemy, Alembic, JWT authentication, Tailwind CSS, Recharts, Docker, and Docker Compose.

## Features

- JWT authentication with bcrypt password hashing and admin/staff roles
- Product CRUD with unique SKU validation, search, filters, pagination, low-stock status, and inventory logs
- Product image uploads via `POST /products/{id}/image`
- Customer management with unique email validation and order history endpoint
- Order workflow with generated order numbers, multiple line items, server-side totals, stock deduction, oversell prevention, and stock restore on cancellation
- Printable HTML invoices via `GET /orders/{id}/invoice`
- Inventory audit logs, low-stock alerts, and out-of-stock views
- Dashboard analytics for products, customers, orders, revenue, monthly sales, top products, and inventory status
- Responsive React admin UI with sidebar navigation, loading states, toasts, forms, tables, and charts
- Dockerized backend, frontend, and PostgreSQL with health checks and named volumes
- Pytest backend coverage for authentication and order stock rules
- GitHub Actions workflow for tests and Docker build checks

## Tech Stack

Backend: Python 3.11, FastAPI, SQLAlchemy, Pydantic, Alembic, PostgreSQL, Pytest  
Frontend: React, React Router, Axios, Context API, Tailwind CSS, Recharts  
Infrastructure: Docker, Docker Compose, GitHub Actions

## Local Setup

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Start the full stack:

```bash
docker compose up --build
```

3. Seed sample data and credentials:

```bash
docker compose exec backend python scripts/seed.py
```

4. Open the app:

- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Sample credentials:

- Email: `admin@example.com`
- Password: `Password123`

## Backend Development

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
pytest
```

## Frontend Development

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL=http://localhost:8000` in `frontend/.env`.

## API Overview

Authentication:

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/profile`

Products:

- `POST /products`
- `GET /products`
- `GET /products/{id}`
- `PUT /products/{id}`
- `DELETE /products/{id}`
- `POST /products/{id}/image`

Customers:

- `POST /customers`
- `GET /customers`
- `GET /customers/{id}`
- `GET /customers/{id}/orders`
- `PUT /customers/{id}`
- `DELETE /customers/{id}`

Orders:

- `POST /orders`
- `GET /orders`
- `GET /orders/{id}`
- `PUT /orders/{id}`
- `DELETE /orders/{id}`
- `GET /orders/{id}/invoice`

Inventory and dashboard:

- `GET /inventory/logs`
- `GET /inventory/low-stock`
- `GET /inventory/out-of-stock`
- `GET /dashboard/summary`

## Deployment

Backend options:

- Render, Railway, or Fly.io
- Use the `backend/Dockerfile`
- Configure `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, and `CORS_ORIGINS`
- Run `alembic upgrade head` before starting the API

Frontend options:

- Vercel or Netlify
- Build command: `npm run build`
- Output directory: `dist`
- Set `VITE_API_URL` to the deployed backend URL

Docker Hub:

- Build backend image: `docker build -t your-dockerhub-user/inventory-backend:latest ./backend`
- Push: `docker push your-dockerhub-user/inventory-backend:latest`

## Submission Links

Replace these after publishing:

- GitHub repository: `https://github.com/your-user/inventory-order-management`
- Docker Hub backend image: `https://hub.docker.com/r/your-user/inventory-backend`
- Live frontend: `https://your-inventory-app.vercel.app`
- Live backend API: `https://your-inventory-api.onrender.com`
- API docs: `https://your-inventory-api.onrender.com/docs`

## Folder Structure

```text
backend/
  app/
    api/ core/ db/ middleware/ models/ schemas/ services/ utils/
  alembic/
  scripts/
  tests/
frontend/
  src/
    components/ context/ layouts/ pages/ routes/ services/ utils/
  nginx/
docker-compose.yml
.github/workflows/ci.yml
```

## Notes

The frontend includes product, customer, order, inventory, and dashboard workflows. The backend supports local image uploads; object storage such as S3, Cloudinary, or Supabase Storage is the recommended production extension for horizontally scaled deployments.
