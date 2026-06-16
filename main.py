from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from fastapi import BackgroundTasks, Cookie, Depends, FastAPI, Form, Header, HTTPException, Path, Query, Request, status as http_status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    tax: Optional[float] = None


class ModelInfo(BaseModel):
    model_name: ModelName
    message: str
    details: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


fake_users_db: Dict[str, Dict[str, str]] = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderland",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": "false",
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI(
    title="FastAPI Core Concepts Demo",
    description="A sample app demonstrating path/query/body models, dependencies, security, middleware, and background tasks.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str((datetime.utcnow() - start_time).total_seconds())
    return response


def get_common_parameters(
    q: Optional[str] = Query(None, min_length=3, max_length=50),
    limit: int = Query(10, gt=0, le=50),
    offset: int = Query(0, ge=0),
) -> Dict[str, Optional[str]]:
    return {"q": q, "limit": limit, "offset": offset}


def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    if token != "fake-token":
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = fake_users_db.get("alice")
    if not user:
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail, "path": request.url.path})


@app.get("/", response_class=HTMLResponse)
async def homepage():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>FastAPI Beginner Lab</title>
        <link rel="stylesheet" href="/static/style.css?v=4" />
    </head>
    <body>
        <div class="page-shell learning-shell">
            <aside class="course-sidebar">
                <div class="brand-lockup">
                    <span class="brand-badge">FastAPI Beginner Lab</span>
                    <h2>Learn APIs step by step</h2>
                    <p>A small guided platform for beginners to explore routes, validation, docs, auth, and live responses.</p>
                </div>

                <nav class="course-nav" aria-label="Learning modules">
                    <a href="#overview" class="course-nav-item active">Overview</a>
                    <a href="#path" class="course-nav-item">Learning path</a>
                    <a href="#lab" class="course-nav-item">Practice lab</a>
                    <a href="#docs" class="course-nav-item">Endpoint map</a>
                </nav>

                <div class="sidebar-card">
                    <p class="sidebar-label">Start here</p>
                    <h3>From first route to protected API</h3>
                    <p>Use the practice lab to see how each FastAPI concept behaves in the browser.</p>
                    <div class="progress-track" aria-hidden="true"><span></span></div>
                    <small>Beginner path: lesson 1 of 4</small>
                </div>
            </aside>

            <main class="learning-main">
                <header class="hero" id="overview">
                    <div class="hero-copy-block">
                        <p class="hero-label">FastAPI learning platform</p>
                        <h1>Build your first API with confidence</h1>
                        <p class="hero-copy">A beginner-friendly workspace that turns this FastAPI project into short lessons, clickable API experiments, and clear endpoint references.</p>
                        <div class="hero-actions">
                            <a class="link-button primary" href="/docs">Open Swagger UI</a>
                            <a class="link-button secondary" href="/redoc">Open ReDoc</a>
                        </div>
                    </div>

                    <div class="hero-visual lesson-canvas">
                        <div class="canvas-chip">Live project</div>
                        <div class="terminal-stack" aria-hidden="true">
                            <div class="terminal-line">GET /status</div>
                            <div class="terminal-line">GET /users/1</div>
                            <div class="terminal-line">POST /token</div>
                        </div>
                        <div>
                            <strong>Practice while you read</strong>
                            <span>Every button below calls a real route from this app.</span>
                        </div>
                    </div>
                </header>

                <section class="stats-grid" aria-label="course highlights">
                    <article class="stat-card"><span>4</span><p>Beginner modules</p></article>
                    <article class="stat-card"><span>8</span><p>Demo endpoints</p></article>
                    <article class="stat-card"><span>5</span><p>Live API exercises</p></article>
                    <article class="stat-card"><span>1</span><p>Swagger docs shortcut</p></article>
                </section>

                <section class="content-grid" id="path">
                    <article class="panel lesson-panel">
                        <div class="panel-heading">
                            <div>
                                <p class="panel-kicker">Module 01</p>
                                <h2>Routes and docs</h2>
                            </div>
                            <span class="pill">Beginner</span>
                        </div>
                        <p>Start with <code>@app.get</code>, path names, and the automatic Swagger UI generated by FastAPI.</p>
                        <div class="checklist"><span>GET routes</span><span>Swagger UI</span><span>ReDoc</span></div>
                    </article>

                    <article class="panel lesson-panel">
                        <div class="panel-heading">
                            <div>
                                <p class="panel-kicker">Module 02</p>
                                <h2>Parameters and validation</h2>
                            </div>
                            <span class="pill">Beginner</span>
                        </div>
                        <p>Try path parameters, query parameters, and Pydantic response models without leaving this page.</p>
                        <div class="checklist"><span>Path params</span><span>Query params</span><span>Response models</span></div>
                    </article>

                    <article class="panel lesson-panel">
                        <div class="panel-heading">
                            <div>
                                <p class="panel-kicker">Module 03</p>
                                <h2>Simple authentication</h2>
                            </div>
                            <span class="pill">Guided</span>
                        </div>
                        <p>Use the demo token flow to understand why protected endpoints need an Authorization header.</p>
                        <div class="checklist"><span>OAuth2 bearer</span><span>Demo token</span><span>401 errors</span></div>
                    </article>

                    <article class="panel lesson-panel">
                        <div class="panel-heading">
                            <div>
                                <p class="panel-kicker">Module 04</p>
                                <h2>App behavior</h2>
                            </div>
                            <span class="pill">Next step</span>
                        </div>
                        <p>Notice health checks, middleware headers, background tasks, and redirects that make APIs practical.</p>
                        <div class="checklist"><span>Health check</span><span>Middleware</span><span>Redirects</span></div>
                    </article>
                </section>

                <section class="practice-layout" id="lab">
                    <article class="panel practice-panel">
                        <div class="panel-heading">
                            <div>
                                <p class="panel-kicker">Practice lab</p>
                                <h2>Try the API</h2>
                            </div>
                            <span class="pill accent">Interactive</span>
                        </div>

                        <div class="lab-grid">
                            <div class="lab-card">
                                <h3>Health check</h3>
                                <p>Call <code>/status</code> to confirm the API is online and returning JSON.</p>
                                <button id="btn-health">Check Status</button>
                                <pre id="health-output" class="output">No data yet.</pre>
                            </div>

                            <div class="lab-card">
                                <h3>Current learner</h3>
                                <p>Retrieve the protected profile from <code>/users/me</code> using the demo bearer token.</p>
                                <button id="btn-current-user">Load Current User</button>
                                <pre id="current-user-output" class="output">No data yet.</pre>
                            </div>

                            <div class="lab-card">
                                <h3>Search a learner</h3>
                                <p>Use <code>/users/{'{user_id}'}</code> to inspect path validation. Try <code>1</code> first.</p>
                                <div class="form-row">
                                    <input id="user-id-input" type="number" min="1" value="1" placeholder="Enter user id" />
                                    <button id="btn-user-id">Fetch User</button>
                                </div>
                                <pre id="user-id-output" class="output">No data yet.</pre>
                            </div>

                            <div class="lab-card">
                                <h3>Class roster</h3>
                                <p>Fetch the full roster from <code>/users</code>.</p>
                                <button id="btn-all-users">Load Users</button>
                                <pre id="all-users-output" class="output">No data yet.</pre>
                            </div>

                            <div class="lab-card">
                                <h3>Model catalog</h3>
                                <p>Choose a model name and watch FastAPI validate an enum path parameter.</p>
                                <div class="form-row">
                                    <select id="model-select">
                                        <option value="alexnet">alexnet</option>
                                        <option value="resnet">resnet</option>
                                        <option value="lenet">lenet</option>
                                    </select>
                                    <button id="btn-model">Get Model Info</button>
                                </div>
                                <pre id="model-output" class="output">No data yet.</pre>
                            </div>
                        </div>
                    </article>
                </section>

                <section class="docs-strip" id="docs">
                    <div>
                        <p class="panel-kicker">Reference</p>
                        <h2>Beginner endpoint map</h2>
                    </div>
                    <div class="docs-grid">
                        <div class="docs-card"><code>GET /status</code><span>Is the app running?</span></div>
                        <div class="docs-card"><code>GET /users</code><span>Return a response model list</span></div>
                        <div class="docs-card"><code>GET /users/{'{user_id}'}</code><span>Use path params and auth</span></div>
                        <div class="docs-card"><code>GET /items/{'{item_id}'}</code><span>Combine path, query, headers, cookies</span></div>
                        <div class="docs-card"><code>POST /token</code><span>Issue the demo bearer token</span></div>
                        <div class="docs-card"><code>GET /models/{'{model_name}'}</code><span>Validate enum values</span></div>
                    </div>
                </section>
            </main>
        </div>
        <script src="/static/script.js?v=4"></script>
    </body>
    </html>
    """


@app.get("/status", response_class=JSONResponse, tags=["health"], summary="Health check")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/users/me", response_model=UserOut, summary="Current user", tags=["users"])
async def read_current_user(current_user: Dict[str, str] = Depends(get_current_user)):
    return UserOut(
        id=1,
        username=current_user["username"],
        email=current_user["email"],
        full_name=current_user.get("full_name"),
        is_active=True,
        created_at=datetime.utcnow(),
    )


@app.get(
    "/users/{user_id}",
    response_model=UserOut,
    tags=["users"],
    responses={404: {"description": "User not found"}},
)
async def read_user(user_id: int = Path(..., ge=1, title="The ID of the user"), q: Optional[str] = Query(None, max_length=50), token: str = Depends(oauth2_scheme)):
    if user_id != 1:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut(
        id=user_id,
        username="alice",
        email="alice@example.com",
        full_name="Alice Wonderland",
        is_active=True,
        created_at=datetime.utcnow(),
    )


@app.get("/users", response_model=List[UserOut], tags=["users"], summary="List users")
async def read_users(common: Dict[str, Optional[str]] = Depends(get_common_parameters)):
    users = [
        UserOut(id=1, username="alice", email="alice@example.com", full_name="Alice Wonderland", is_active=True, created_at=datetime.utcnow()),
        UserOut(id=2, username="bob", email="bob@example.com", full_name="Bob Builder", is_active=False, created_at=datetime.utcnow()),
    ]
    if common["q"]:
        users = [user for user in users if common["q"].lower() in user.username.lower()]
    start = min(common["offset"], len(users))
    end = min(start + common["limit"], len(users))
    return users[start:end]


@app.post("/users", response_model=UserOut, status_code=http_status.HTTP_201_CREATED, tags=["users"], summary="Create user")
async def create_user(user: UserCreate):
    return UserOut(id=3, username=user.username, email=user.email, full_name=user.full_name, is_active=True, created_at=datetime.utcnow())


@app.put("/users/{user_id}", response_model=UserOut, tags=["users"], summary="Update user")
async def update_user(user_id: int, user: UserUpdate):
    if user_id != 1:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut(
        id=user_id,
        username="alice",
        email=user.email or "alice@example.com",
        full_name=user.full_name or "Alice Wonderland",
        is_active=user.is_active if user.is_active is not None else True,
        created_at=datetime.utcnow(),
    )


@app.delete("/users/{user_id}", status_code=http_status.HTTP_204_NO_CONTENT, tags=["users"], summary="Delete user")
async def delete_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="User not found")
    return JSONResponse(status_code=http_status.HTTP_204_NO_CONTENT, content=None)


@app.post("/token", response_model=Token, tags=["authentication"], summary="Login and receive token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "alice" or form_data.password != "secret":
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return {"access_token": "fake-token", "token_type": "bearer"}


@app.post("/login", response_class=PlainTextResponse, tags=["authentication"], summary="Form login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username != "alice" or password != "secret":
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return "Login successful"


@app.get("/items/{item_id}", response_model=Item, tags=["items"], summary="Get item")
async def read_item(
    item_id: int = Path(..., ge=1, title="The ID of the item"),
    q: Optional[str] = Query(None, description="Search query"),
    user_agent: Optional[str] = Header(None, alias="User-Agent"),
    ads_cookie: Optional[str] = Cookie(None, alias="ads_cookie"),
):
    return Item(
        name=f"Item {item_id}",
        description=f"Information for item {item_id}. q={q}, ua={user_agent}, ads_cookie={ads_cookie}",
        price=9.99,
        tax=1.23,
    )


@app.post("/models", response_model=ModelInfo, tags=["models"], summary="Create model info")
async def create_model(model_info: ModelInfo, background_tasks: BackgroundTasks):
    background_tasks.add_task(log_model_creation, model_info.model_name.value)
    return model_info


async def log_model_creation(model_name: str):
    print(f"Model created: {model_name} at {datetime.utcnow().isoformat()}")


@app.get("/models/{model_name}", response_model=ModelInfo, tags=["models"], summary="Get model details")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return ModelInfo(model_name=model_name, message="Deep Learning FTW!", details="A classic convolutional neural network architecture.")
    if model_name == ModelName.lenet:
        return ModelInfo(model_name=model_name, message="LeCNN all the images", details="A simple CNN architecture for handwritten digits.")
    return ModelInfo(model_name=model_name, message="Have some residuals", details="A residual network with skip connections.")


@app.get("/redirect", response_class=RedirectResponse, tags=["utility"], summary="Redirect to docs")
async def redirect_example():
    return RedirectResponse(url="/docs")
