from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session, select, or_

from auth import create_access_token, get_user, oauth_scheme, revoke_token, verify_token
from database.models import Shipment, User
from database.sessions import create_db_and_table, get_session
from hash import check_password, generate_password
from schemas import (
    LoginResponse,
    LoginUser,
    Ship,
    ShipmentPatch,
    UserCreate,
    UserResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # runs on startup: ensures tables exist in the db
    create_db_and_table()
    yield


app = FastAPI(title="Shipment Management API", lifespan=lifespan)


@app.post("/create-user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(data: UserCreate, session: Session = Depends(get_session)):
    # check if username or email already exists
    existing_user = session.exec(
        select(User).where(
            or_(User.username == data.username, User.email == data.email)
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is already taken",
        )

    # hash password before storing in database
    hashed = generate_password(data.password)
    new_user = User(username=data.username, email=data.email, password_hash=hashed)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@app.post("/login", response_model=LoginResponse)
def login_user(data: LoginUser, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # verify password against bcrypt hash
    if not check_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user.id)
    return LoginResponse(
        message="Login successful",
        userid=user.id,
        username=user.username,
        email=user.email,
        token=token,
    )


# example protected route - needs Bearer <token> in Authorization header
@app.get("/users/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_user)):
    return current_user


# invalidates the current bearer token so it cannot be used again
@app.post("/logout")
def logout_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth_scheme),
    session: Session = Depends(get_session),
):
    token = credentials.credentials
    verify_token(token)
    revoke_token(token, session)
    return {"message": "Logged out successfully"}


@app.post("/new-shipment", response_model=Shipment, status_code=status.HTTP_201_CREATED)
def add_shipment(data: Ship, session: Session = Depends(get_session)):
    shipment = Shipment.model_validate(data.model_dump())
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


@app.get("/shipments", response_model=list[Shipment])
def list_shipments(session: Session = Depends(get_session)):
    return session.exec(select(Shipment)).all()


@app.get("/shipments/{shipment_id}", response_model=Shipment)
def get_shipment_by_id(shipment_id: int, session: Session = Depends(get_session)):
    shipment = session.get(Shipment, shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment #{shipment_id} not found",
        )
    return shipment


@app.put("/shipments/{shipment_id}", response_model=Shipment)
def replace_shipment(
    shipment_id: int, data: Ship, session: Session = Depends(get_session)
):
    shipment = session.get(Shipment, shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment #{shipment_id} not found",
        )
    shipment.sqlmodel_update(data.model_dump())
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


@app.patch("/shipments/{shipment_id}", response_model=Shipment)
def patch_shipment(
    shipment_id: int, data: ShipmentPatch, session: Session = Depends(get_session)
):
    shipment = session.get(Shipment, shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment #{shipment_id} not found",
        )
    # only update attributes provided in the request
    patch_fields = data.model_dump(exclude_unset=True)
    shipment.sqlmodel_update(patch_fields)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


@app.delete("/shipments/{shipment_id}")
def delete_shipment(shipment_id: int, session: Session = Depends(get_session)):
    shipment = session.get(Shipment, shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment #{shipment_id} not found",
        )
    session.delete(shipment)
    session.commit()
    return {"message": f"Shipment #{shipment_id} deleted successfully"}
