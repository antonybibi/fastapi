from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import model, schemas, utils
from auth.auth_database import get_db, engine
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer



SECRET_KEY = "QLxoP_RBa9BTY_8wYhlmw9MNfq1QDIGMAeYxzYDNUsU"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30


# Helper function that takes user data
def create_access_token(data:dict):
    to_encode = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES) 
    to_encode.update({"exp": expiry})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()

@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #check if the user exist
    existing_user = db.query(model.User).filter(model.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="username already exist")

    # hash the password
    hashed_pass = utils.hash_password(user.password)

    #Create new user instance
    new_user = model.User(
        username=user.username,
        email = user.email,
        password = hashed_pass,
        role = user.role
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Return the value (excluding password)
    return {"id" : new_user.id, "username" : new_user.username, "email" : new_user.email, "role" : new_user.role}



@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID USERNAME")
    if not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID PASSWORD")
    
    token_data = {"sub": user.username, "role": user.role}
    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username : str = payload.get("sub")
        role : str = payload.get("role")
        if username is None or role is None:
            raise credential_exception
    except JWTError:
        raise credential_exception

    return {"username": username, "role": role}

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"Message": f"Hello {current_user['username']} | you have accessed a protected route "}

def require_roles(allowed_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not enough permission")
            
        return current_user
    return role_checker


@app.get("/profile")
def get_profile(current_user: dict = Depends(require_roles(["admin", "user", "string"]))):    
    return {"Message": f"Profile of {current_user['username']} | {current_user['role']}"}


@app.get("/user/dashboard")
def user_dashboard(current_user : dict = Depends(require_roles(["user", "string"]))):
    return {"Message" : f"Welcome {current_user['username']} to your dashboard"}

@app.get("/admin/dashboard")
def admin_dashboard(current_user : dict = Depends(require_roles(["admin"]))):
    return {"Message" : f"Welcome {current_user['username']} to your admin dashboard"}