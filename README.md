# FastAPI Academy

FastAPI Academy is a small FastAPI learning platform that turns a demo API into a guided beginner-friendly course. The homepage behaves like a course dashboard, and the practice lab lets you call live endpoints directly from the browser.

## What’s Included

- A course-style homepage with lessons, progress, and endpoint references
- Live API practice buttons for common FastAPI concepts
- Route and response model examples
- Query, path, header, cookie, and form handling
- Simple token-based auth demo
- Middleware and background task examples
- Swagger UI and ReDoc links

## Project Structure

- `main.py` - FastAPI app entrypoint and HTML homepage
- `static/style.css` - Learning platform styling
- `static/script.js` - Browser interactions for the practice lab
- `venv/` - Local Python virtual environment

## Requirements

- Python 3.13 or compatible
- FastAPI installed in the local virtual environment

## Run Locally

If the virtual environment already exists, activate it and start the dev server:

```powershell
.\venv\Scripts\python.exe -m fastapi dev
```

If your shell has `fastapi` on PATH, this also works:

```powershell
fastapi dev
```

Open the app in your browser at:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Practice Lab Endpoints

- `GET /status` - health check
- `GET /users/me` - protected current-user example
- `GET /users/{user_id}` - path parameter validation example
- `GET /users` - list users with query parameters
- `POST /users` - create a user with a Pydantic model
- `PUT /users/{user_id}` - update a user
- `DELETE /users/{user_id}` - delete a user
- `POST /token` - demo OAuth2 token endpoint
- `POST /login` - form-based login example
- `GET /items/{item_id}` - path, query, header, and cookie example
- `POST /models` - background task example
- `GET /models/{model_name}` - enum-based route example
- `GET /redirect` - redirect to docs

## Demo Auth

The app uses a simple demo bearer token for the protected route examples.

- Username: `alice`
- Password: `secret`
- Token returned by `/token`: `fake-token`

## Notes

- The UI is designed as a learning platform, not a production LMS.
- Some endpoints intentionally return demo data so the examples stay simple and readable.
- The project uses a local `venv` so VS Code and the FastAPI CLI resolve imports correctly.