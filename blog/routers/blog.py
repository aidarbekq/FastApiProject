from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from .. import schemas, models, hashing
from .. database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()


@router.get('/blog/list', response_model=List[schemas.ShowBlog], tags=['blog'])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['blog'])
def get_object(id, response: Response, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).get(models.Blog.id == id)
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id: {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'msg': f'Blog with id: {id} not found.'}
    return blog


@router.post('/blog/create', status_code=status.HTTP_201_CREATED, tags=['blog'] )
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/delete/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'Done'


@app.put('/blog/update/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
    blog.update(request.dict())
    db.commit()
    return 'Updated'

