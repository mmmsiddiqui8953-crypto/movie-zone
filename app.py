#!/usr/bin/env python3
"""
Advanced Movie Recommender System
Features modern UI, robust error handling, and enhanced user experience
"""
import streamlit as st
import pandas as pd
import pickle
import base64
from typing import Tuple, Optional, Union
import time

# Page config
st.set_page_config(
    page_title="🎬 CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS styling
st.markdown("""
<style>
/* Main app styling */
.main > div {
    padding-top: 2rem;
}

/* Custom header styling */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.main-header h1 {
    color: white;
    text-align: center;
    font-size: 3rem;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.main-header p {
    color: rgba(255,255,255,0.9);
    text-align: center;
    font-size: 1.2rem;
    margin: 0.5rem 0 0 0;
}

/* Movie card styling */
.movie-card {
    background: white;
    border-radius: 15px;
    padding: 1rem;
    margin: 0.5rem;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #f0f0f0;
}

.movie-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.15);
}

/* Poster styling */
.poster-container {
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1rem;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* Selectbox styling */
.stSelectbox > div > div {
    border-radius: 10px;
    border: 2px solid #e0e0e0;
    transition: border-color 0.3s ease;
}

.stSelectbox > div > div:focus-within {
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
}

/* Success message styling */
.element-container .stSuccess {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    border: none;
    border-radius: 10px;
}

/* Info message styling */
.element-container .stInfo {
    background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
    border: none;
    border-radius: 10px;
}

/* Metrics styling */
.metric-container {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_movie_data() -> Tuple[Optional[pd.DataFrame], Optional[object], bool]:
    """Load movie data with comprehensive error handling"""
    try:
        with open('movie_data.pkl', 'rb') as f:
            movies, cosine_sim = pickle.load(f)
        if movies is not None and not movies.empty:
            return movies, cosine_sim, True
        else:
            st.error("❌ Movie data is empty or corrupted")
            return None, None, False
    except FileNotFoundError:
        st.error("❌ Movie data file not found. Please ensure 'movie_data.pkl' exists.")
        return None, None, False
    except Exception as e:
        st.error(f"❌ Error loading movie data: {e}")
        return None, None, False

@st.cache_data
def get_recommendations(title: str, movies: pd.DataFrame, cosine_sim) -> pd.DataFrame:
    """Get movie recommendations with enhanced error handling"""
    try:
        if movies is None or movies.empty:
            st.error("❌ No movie data available")
            return pd.DataFrame()
            
        # Find movie index
        matching_movies = movies[movies['title'] == title]
        if matching_movies.empty:
            st.error(f"❌ Movie '{title}' not found in database")
            return pd.DataFrame()
            
        idx = matching_movies.index[0]
        
        # Calculate similarity scores
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Top 10 excluding the movie itself
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Return recommendations with additional columns if available
        columns_to_include = ['title', 'movie_id']
        if 'overview' in movies.columns:
            columns_to_include.append('overview')
        if 'genres' in movies.columns:
            columns_to_include.append('genres')
            
        return movies[columns_to_include].iloc[movie_indices]
    
    except Exception as e:
        st.error(f"❌ Error getting recommendations: {e}")
        return pd.DataFrame()

def create_enhanced_poster(movie_id: Union[str, int], title: str) -> str:
    """Create an enhanced SVG poster with modern design"""
    gradients = [
        ('#667eea', '#764ba2'),
        ('#f093fb', '#f5576c'),
        ('#4facfe', '#00f2fe'),
        ('#43e97b', '#38f9d7'),
        ('#fa709a', '#fee140'),
        ('#a8edea', '#fed6e3'),
        ('#ffecd2', '#fcb69f'),
        ('#ff9a9e', '#fecfef')
    ]
    
    color1, color2 = gradients[int(movie_id) % len(gradients)]
    
    # Truncate title if too long
    display_title = title[:25] + '...' if len(title) > 25 else title
    
    svg = f'''
    <svg width="200" height="300" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad{movie_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{color1};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{color2};stop-opacity:1" />
            </linearGradient>
            <filter id="shadow{movie_id}" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="rgba(0,0,0,0.3)"/>
            </filter>
        </defs>
        <rect width="200" height="300" fill="url(#grad{movie_id})" rx="15" ry="15"/>
        <circle cx="100" cy="120" r="25" fill="rgba(255,255,255,0.2)" filter="url(#shadow{movie_id})"/>
        <text x="100" y="130" font-family="Arial, sans-serif" font-size="20" fill="white" text-anchor="middle" filter="url(#shadow{movie_id})">🎬</text>
        <text x="100" y="180" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="white" text-anchor="middle" filter="url(#shadow{movie_id})">{display_title}</text>
        <text x="100" y="200" font-family="Arial, sans-serif" font-size="10" fill="rgba(255,255,255,0.8)" text-anchor="middle">ID: {movie_id}</text>
        <rect x="0" y="0" width="200" height="300" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1" rx="15" ry="15"/>
    </svg>
    '''
    
    encoded = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{encoded}"

def main():
    """Enhanced main application function with modern UI"""
    
    # Custom header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 CineMatch</h1>
        <p>Discover your next favorite movie with AI-powered recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data with proper error handling
    movies, cosine_sim, data_loaded = load_movie_data()
    
    if not data_loaded or movies is None:
        st.error("❌ Cannot load movie data. Please check if 'movie_data.pkl' exists.")
        st.info("💡 Make sure you're running this from the correct directory.")
        
        # Provide more helpful information
        with st.expander("🔧 Troubleshooting", expanded=True):
            st.markdown("""
            **Common issues:**
            1. **File not found**: Ensure `movie_data.pkl` is in the same directory as this app
            2. **Corrupted file**: Try regenerating the pickle file from the original data
            3. **Permissions**: Check if you have read permissions for the file
            
            **Expected file structure:**
            ```
            movie-zone/
            ├── app.py
            ├── movie_data.pkl
            └── (other files)
            ```
            """)
        return
    
    # Enhanced sidebar with statistics
    with st.sidebar:
        st.markdown("### 📊 Dataset Statistics")
        
        # Create metrics in sidebar
        total_movies = len(movies)
        st.metric("🎬 Total Movies", f"{total_movies:,}")
        
        # Additional stats if columns are available
        if 'genres' in movies.columns:
            unique_genres = len(movies['genres'].dropna().unique()) if 'genres' in movies.columns else 0
            st.metric("🎭 Unique Genres", unique_genres)
        
        st.markdown("---")
        st.markdown("### 🚀 How CineMatch Works")
        st.markdown("""
        1. **Select** a movie you enjoyed
        2. **Analyze** content similarity using AI
        3. **Discover** 10 personalized recommendations
        4. **Explore** detailed movie information
        """)
        
        st.markdown("---")
        st.markdown("### ⚡ Features")
        st.markdown("""
        - 🎯 Content-based recommendations
        - 🎨 Modern, responsive design
        - 📱 Mobile-friendly interface
        - 🔍 Advanced search capabilities
        - 📊 Movie statistics & insights
        """)
    
    # Enhanced movie selection interface
    st.markdown("### 🔍 Find Your Next Movie")
    
    # Search and selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Add search functionality
        search_term = st.text_input(
            "🔍 Search for a movie",
            placeholder="Type to search...",
            help="Start typing to filter movies"
        )
        
        # Filter movies based on search
        if search_term:
            filtered_movies = movies[movies['title'].str.contains(search_term, case=False, na=False)]
            if not filtered_movies.empty:
                movie_options = filtered_movies['title'].tolist()
            else:
                movie_options = ["No movies found matching your search"]
                st.warning(f"No movies found matching '{search_term}'")
        else:
            movie_options = movies['title'].tolist()
        
        selected_movie = st.selectbox(
            "Or choose from the complete list:",
            movie_options,
            index=0,
            help="Select a movie to get personalized recommendations"
        )
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)  # Spacing
        get_recs = st.button(
            "✨ Get Recommendations", 
            type="primary",
            help="Click to discover similar movies",
            width="stretch"
        )
    
    # Show selected movie info with enhanced display
    if selected_movie and selected_movie != "No movies found matching your search":
        matching_movies = movies[movies['title'] == selected_movie]
        if not matching_movies.empty:
            selected_data = matching_movies.iloc[0]
            
            with st.expander(f"ℹ️ About '{selected_movie}'", expanded=False):
                col1, col2 = st.columns([1, 3])
                with col1:
                    poster = create_enhanced_poster(selected_data['movie_id'], selected_movie)
                    st.markdown('<div class="poster-container">', unsafe_allow_html=True)
                    st.image(poster, width=150)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with col2:
                    st.markdown(f"**🆔 Movie ID:** {selected_data['movie_id']}")
                    
                    if 'overview' in selected_data and pd.notna(selected_data['overview']):
                        st.markdown(f"**📝 Overview:** {selected_data['overview']}")
                    else:
                        st.markdown("**📝 Overview:** No description available")
                    
                    if 'genres' in selected_data and pd.notna(selected_data['genres']):
                        st.markdown(f"**🎭 Genres:** {selected_data['genres']}")
    
    # Enhanced recommendations display
    if get_recs and selected_movie and selected_movie != "No movies found matching your search":
        st.markdown("---")
        
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔍 Analyzing movie preferences...")
        progress_bar.progress(25)
        time.sleep(0.1)
        
        status_text.text("🧠 Computing similarity scores...")
        progress_bar.progress(50)
        
        recommendations = get_recommendations(selected_movie, movies, cosine_sim)
        progress_bar.progress(75)
        
        status_text.text("✨ Preparing recommendations...")
        progress_bar.progress(100)
        time.sleep(0.1)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        if recommendations.empty:
            st.error("❌ Could not generate recommendations. Please try another movie.")
        else:
            st.success(f"🎯 **Top 10 movies similar to '{selected_movie}'**")
            
            # Enhanced grid display
            for i in range(0, len(recommendations), 5):
                cols = st.columns(5)
                
                for j in range(5):
                    if i + j < len(recommendations):
                        movie = recommendations.iloc[i + j]
                        
                        with cols[j]:
                            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                            
                            # Enhanced poster
                            poster = create_enhanced_poster(movie['movie_id'], movie['title'])
                            st.markdown('<div class="poster-container">', unsafe_allow_html=True)
                            st.image(poster, width="stretch")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Movie details
                            st.markdown(f"**{movie['title']}**")
                            st.caption(f"🆔 ID: {movie['movie_id']}")
                            
                            # Additional info if available
                            if 'overview' in movie and pd.notna(movie['overview']):
                                overview = movie['overview'][:100] + "..." if len(str(movie['overview'])) > 100 else str(movie['overview'])
                                st.caption(f"📝 {overview}")
                            
                            if 'genres' in movie and pd.notna(movie['genres']):
                                st.caption(f"🎭 {movie['genres']}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
            
            # Enhanced statistics and information
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info("🎯 **Algorithm**: Content-based filtering using TF-IDF vectorization")
            
            with col2:
                st.info("📊 **Features**: Genres, cast, keywords, director, and plot")
            
            with col3:
                st.info("⚡ **Accuracy**: Based on movie content similarity scores")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 2rem;">
        <p>🎬 <strong>CineMatch</strong> - Powered by AI • Made with ❤️ using Streamlit</p>
        <p>Discover movies that match your taste through advanced content analysis</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()