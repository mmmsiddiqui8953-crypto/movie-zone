# 🎬 Movie Recommender System

A sophisticated movie recommendation system built with Streamlit that suggests movies based on content similarity using machine learning techniques.

## ✨ Features

- **Smart Recommendations**: Get personalized movie suggestions based on genres, keywords, cast, and directors
- **Interactive Search**: Find movies quickly with the built-in search functionality  
- **Visual Interface**: Browse recommendations with movie posters from TMDB
- **Detailed Movie Info**: View movie overviews and additional details
- **Responsive Design**: Clean, modern UI that works on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd movie-zone
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and go to `http://localhost:8501`

## 📊 Dataset

This system uses the TMDB 5000 Movie Dataset which includes:
- 4,809 movies
- Movie metadata (genres, keywords, cast, crew)
- Content-based similarity calculations using TF-IDF vectorization

## 🛠️ Technical Details

### Algorithm
- **TF-IDF Vectorization**: Converts movie features into numerical vectors
- **Cosine Similarity**: Measures similarity between movies
- **Content-Based Filtering**: Recommends movies with similar content attributes

### Files Structure
```
movie-zone/
├── app.py                          # Main Streamlit application
├── Movie_Recommendation_System.ipynb # Data preprocessing notebook
├── movie_data.pkl                   # Processed movie data and similarity matrix
├── tmdb_5000_movies.csv            # Raw movie dataset
├── tmdb_5000_credits.csv           # Movie credits dataset
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🎬 Poster System

The application uses a **3-tier poster fetching system** that prioritizes TMDB API:

### 🔄 Fetching Priority:
1. **🌐 TMDB API** (Primary) - Real-time poster fetching
2. **📋 Local Cache** (Backup) - Pre-cached popular movie posters  
3. **🎨 Custom SVG** (Fallback) - Beautiful offline-compatible placeholders

### 🚀 Benefits:
- **Real-time Updates**: Always tries to fetch the latest posters from TMDB
- **100% Reliability**: Never shows broken images
- **Offline Compatible**: Works even without internet connection
- **Multiple API Keys**: Automatic failover for rate limiting
- **Smart Timeouts**: 5-second timeout prevents hanging

### 🔧 Configuration

For optimal performance, you can set your own TMDB API key:

```bash
# Option 1: Environment Variable
export TMDB_API_KEY="your_api_key_here"

# Option 2: Create .env file
echo "TMDB_API_KEY=your_api_key_here" > .env
```

**Get your free API key:** [TMDB API Settings](https://www.themoviedb.org/settings/api)

## 🐛 Troubleshooting

### Common Issues

1. **"Movie data file not found"**
   - Ensure `movie_data.pkl` exists in the project directory
   - If missing, run the Jupyter notebook to regenerate it

2. **Slow poster loading**
   - This is normal for the first load
   - Posters are cached after the first request

3. **"No recommendations found"**
   - Try selecting a different, more popular movie
   - Ensure the movie title is spelled correctly

### Error Handling
The application includes comprehensive error handling for:
- Missing data files
- Network connectivity issues
- Invalid movie selections
- API failures

## 📈 Performance

- **Dataset Size**: 4,809 movies
- **Memory Usage**: ~180MB for similarity matrix
- **Response Time**: < 2 seconds for recommendations
- **Caching**: Streamlit caching for improved performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **TMDB**: Movie data and poster images
- **Streamlit**: Web application framework
- **scikit-learn**: Machine learning utilities
- **Pandas**: Data manipulation and analysis

---

**Made with ❤️ using Streamlit | Data from TMDB**