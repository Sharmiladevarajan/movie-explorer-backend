# Movie Explorer - Complete Features Guide

## 🎬 Core Features

### Movie Management
- **Full CRUD Operations**: Create, Read, Update, Delete movies
- **Advanced Filtering**: Filter by genre, director, actor, year
- **Search**: Full-text search across titles and descriptions
- **Cast Management**: Add/edit multiple cast members per movie with roles
- **Language Support**: Select from 12+ languages for each movie
- **Ratings**: Rate movies from 0-10

### Actor Management
- **Actor Profiles**: Detailed actor pages with filmography
- **Role Tracking**: Track which character each actor played
- **Automatic Linking**: Actors are automatically created when adding cast
- **Full CRUD**: Add, edit, and delete actors independently

### Director Management
- **Director Profiles**: Comprehensive director pages with complete filmography
- **Automatic Creation**: Directors created automatically when adding movies
- **Filmography View**: See all movies by a director with ratings

### Review System
- **Movie Reviews**: Add reviews with ratings and comments
- **User Attribution**: Track who wrote each review
- **Full CRUD**: Create, read, update, delete reviews
- **Average Ratings**: Automatically calculated from all reviews

## 🎨 UI Features

### Netflix-Style Homepage (Default)
- **Horizontal Scrolling**: Smooth scrolling categories by genre
- **Hover Effects**: Movie cards expand on hover
- **Arrow Navigation**: Left/right arrows for each category
- **Hero Section**: Featured movie with rotating quotes
- **Responsive Design**: Works on all screen sizes

### Movie Cards
- **Rich Information**: Title, director, year, rating, genre
- **Cast Preview**: Shows main cast members
- **Quick Actions**: Edit and delete buttons
- **Smooth Animations**: Hover effects and transitions

### Forms
- **Dynamic Cast Input**: Add unlimited cast members with add/remove buttons
- **Language Selection**: Dropdown with 12+ language options
- **Validation**: Client and server-side validation
- **Error Handling**: Clear error messages
- **Loading States**: Visual feedback during submissions

## 🔧 Technical Features

### Backend (FastAPI)
- **RESTful API**: Clean, documented endpoints
- **Swagger Docs**: Interactive API documentation at `/docs`
- **Database Pool**: Efficient PostgreSQL connection management
- **Input Validation**: Pydantic models for type safety
- **Error Handling**: Comprehensive error responses
- **Testing**: pytest test suite included
- **Linting**: flake8, black, mypy for code quality

### Frontend (Next.js)
- **TypeScript**: Full type safety
- **React Hooks**: Modern React patterns
- **Tailwind CSS**: Utility-first styling
- **Client-Side Routing**: Fast page navigation
- **API Integration**: Clean axios-based API client
- **Testing**: Jest test suite included
- **ESLint**: Code quality and consistency

## 📊 Database Schema

### Tables
- **movies**: Core movie data with language support
- **actors**: Actor information and bios
- **directors**: Director information
- **genres**: Genre categories with descriptions
- **reviews**: User reviews and ratings
- **movie_actors**: Many-to-many relationship with roles
- **movie_genres**: Many-to-many genre associations

### Relationships
- Movies can have multiple actors (with roles)
- Movies can have multiple genres
- Movies have one director
- Movies can have multiple reviews
- Automatic cascade deletion for related data

## 🚀 API Endpoints

### Movies
- `GET /api/movies` - List all movies with filtering
- `GET /api/movies/{id}` - Get single movie with cast
- `POST /api/movies` - Create movie with cast
- `PUT /api/movies/{id}` - Update movie and cast
- `DELETE /api/movies/{id}` - Delete movie
- `GET /api/movies/by-genre/grouped` - Get movies grouped by genre
- `GET /api/movies/genre/{genre_name}` - Get movies by genre

### Actors
- `GET /api/actors` - List all actors
- `GET /api/actors/{id}` - Get actor details
- `GET /api/actors/{id}/profile` - Get actor with filmography
- `POST /api/actors` - Create actor
- `PUT /api/actors/{id}` - Update actor
- `DELETE /api/actors/{id}` - Delete actor

### Directors
- `GET /api/directors` - List all directors
- `GET /api/directors/{id}` - Get director details
- `GET /api/directors/{id}/profile` - Get director with filmography
- `POST /api/directors` - Create director
- `PUT /api/directors/{id}` - Update director
- `DELETE /api/directors/{id}` - Delete director

### Reviews
- `GET /api/reviews/movie/{movie_id}` - Get movie reviews
- `POST /api/reviews` - Create review
- `PUT /api/reviews/{id}` - Update review
- `DELETE /api/reviews/{id}` - Delete review

### Genres
- `GET /api/genres` - List all genres
- `POST /api/genres` - Create genre
- `PUT /api/genres/{id}` - Update genre
- `DELETE /api/genres/{id}` - Delete genre

## 🎯 Usage Examples

### Adding a Movie with Cast
```json
POST /api/movies
{
  "title": "Inception",
  "director_name": "Christopher Nolan",
  "release_year": 2010,
  "genre_name": "Sci-Fi",
  "rating": 8.8,
  "language": "English",
  "description": "A thief who enters dreams...",
  "cast": [
    {"actor_name": "Leonardo DiCaprio", "role": "Cobb"},
    {"actor_name": "Marion Cotillard", "role": "Mal"},
    {"actor_name": "Tom Hardy", "role": "Eames"}
  ]
}
```

### Updating Movie Cast
```json
PUT /api/movies/1
{
  "title": "Inception",
  "director_name": "Christopher Nolan",
  "release_year": 2010,
  "genre_name": "Sci-Fi",
  "cast": [
    {"actor_name": "Leonardo DiCaprio", "role": "Dom Cobb"},
    {"actor_name": "Ellen Page", "role": "Ariadne"}
  ]
}
```

## 🌟 Best Practices

### Frontend
- Use TypeScript for type safety
- Follow React hooks patterns
- Keep components small and focused
- Use Tailwind utility classes
- Handle loading and error states

### Backend
- Use Pydantic models for validation
- Close database connections properly
- Return appropriate HTTP status codes
- Log errors for debugging
- Write tests for new features

### Database
- Use indexes for frequently queried fields
- Handle cascade deletions carefully
- Use transactions for multi-step operations
- Validate data before insertion
- Regular backups recommended

## 📱 Responsive Design

The UI adapts to all screen sizes:
- **Desktop**: Full Netflix-style horizontal scrolling
- **Tablet**: Adjusted card sizes and spacing
- **Mobile**: Vertical scrolling with touch support

## 🔒 Data Validation

### Server-Side
- Required fields enforced
- Type validation via Pydantic
- Rating range: 0-10
- Year range: 1888-2030
- SQL injection prevention

### Client-Side
- HTML5 form validation
- TypeScript type checking
- Real-time error feedback
- Duplicate prevention

## 🎨 Theming

The UI uses a glassmorphism design with:
- Purple/Cyan gradient accents
- Semi-transparent cards
- Smooth transitions
- Hover effects
- Glass blur effects
- Responsive typography

## 🔍 Search & Filter

- **Text Search**: Search by movie title
- **Genre Filter**: Filter by genre name
- **Director Filter**: Filter by director name
- **Actor Filter**: Filter by actor name
- **Year Filter**: Filter by release year
- **Combined Filters**: Use multiple filters together

## 📈 Performance

- Connection pooling for database
- Lazy loading for movie lists
- Debounced search
- Optimized queries with indexes
- Minimal re-renders in React
- CSS transforms for smooth animations

## 🐛 Error Handling

- User-friendly error messages
- Validation errors highlighted
- Network error recovery
- 404 handling
- 500 error logging
- Graceful degradation
