from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime


class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    director_name: str = Field(..., min_length=1, max_length=255)
    release_year: int = Field(..., ge=1888, le=2030)
    genre_name: str = Field(..., min_length=1, max_length=100)
    rating: Optional[float] = Field(None, ge=0, le=10)
    description: Optional[str] = None

    @validator('title', 'director_name', 'genre_name')
    def strip_whitespace(cls, v):
        if v:
            v = v.strip()
            if not v:
                raise ValueError('Field cannot be empty or only whitespace')
        return v


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    director_name: Optional[str] = Field(None, min_length=1, max_length=255)
    release_year: Optional[int] = Field(None, ge=1888, le=2030)
    genre_name: Optional[str] = Field(None, min_length=1, max_length=100)
    rating: Optional[float] = Field(None, ge=0, le=10)
    description: Optional[str] = None

    @validator('title', 'director_name', 'genre_name')
    def strip_whitespace(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Field cannot be empty or only whitespace')
        return v


class MovieResponse(BaseModel):
    id: int
    title: str
    director: str
    release_year: int
    genre: str
    rating: Optional[float]
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    movie_id: int = Field(..., gt=0)
    reviewer_name: str = Field(..., min_length=1, max_length=255)
    rating: float = Field(..., ge=0, le=10)
    comment: Optional[str] = None

    @validator('reviewer_name')
    def strip_whitespace(cls, v):
        if v:
            v = v.strip()
            if not v:
                raise ValueError('Reviewer name cannot be empty')
        return v


class ReviewResponse(BaseModel):
    id: int
    movie_id: int
    reviewer_name: str
    rating: float
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DirectorResponse(BaseModel):
    id: int
    name: str
    bio: Optional[str]
    birth_year: Optional[int]

    class Config:
        from_attributes = True


class GenreResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    detail: str
    error_type: Optional[str] = None
