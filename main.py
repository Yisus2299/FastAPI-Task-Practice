from fastapi import FastAPI, status, Request 
from database import engine, Base
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from model import User
from Router.tasks import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

# global handle integrity errors who takes DB errors and turn them into messages:
# it follows the same structure: 1- User error, Duplicated data and Error in the DB
@app.exception_handler(IntegrityError)
def integrity_exception_handler(request: Request, exc: IntegrityError):
    error_msg = str(exc.orig).lower()
    
    if "foreign key" in error_msg:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail":"Invalid User: user_id doesn't exist in the DB"}
        )
    
    if "unique" in error_msg:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail":"Duplicated data: the value already exists in the DB"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail":"Integrity error in the DB"}
    )
       


# we create a user for practicing in this case to test a couple things:
# def create_user():
#     db = SessionLocal()
#     user = db.query(User).filter(User.email == "test@gmail.com").first()
#     if not user:
#         new_user = User(email = "test@gmail.com")
#         db.add(new_user)
#         db.commit()
#         print(f"User added with the ID {new_user.id}")
#     else:
#         print(f"This user with the ID {user.id} already exists")
#     db.close()
    
# create_user()


app.include_router(router)

# main message just for testing:
@app.get("/")
def home():
    return {"Welcome to TaskAPI":"go to swagger and try everything i made up"}