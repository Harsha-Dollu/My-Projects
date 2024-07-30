import tkinter as tk
from tkinter import messagebox
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load movies data from CSV file
movies_data = pd.read_csv("TeluguMovies_dataset.csv")

selected_features = ["Certificate", "Genre", "Overview", "Rating"]
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna("")

combined_features = movies_data['Certificate'] + ' ' + movies_data['Genre'] + ' ' + movies_data['Overview']

vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors)

list_of_all_titles = movies_data['Movie'].tolist()

# Function to recommend movies based on user input
def recommend_movies():
    movie_name = entry.get().strip()
    if not movie_name:
        messagebox.showinfo("Error", "Please enter a movie title.")
        return

    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    if not find_close_match:
        messagebox.showinfo("Error", "Movie not found. Please try a different title.")
        return

    close_match = find_close_match[0]
    index_of_movie = movies_data[movies_data.Movie == close_match].index[0]
    similarity_score = list(enumerate(similarity[index_of_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    
    top_movies = []
    for i, movie in enumerate(sorted_similar_movies[:15], start=1):
        index = movie[0]
        movie_name = movies_data.iloc[index]['Movie']
        rating = movies_data.iloc[index]['Rating']
        overview = movies_data.iloc[index]['Overview']
        top_movies.append((movie_name, rating, overview))
    
    top_movies.sort(key=lambda x: x[1], reverse=True)

    result_text = f"Searched movie:\n{movies_data.iloc[index_of_movie]['Movie']} - Rating: {movies_data.iloc[index_of_movie]['Rating']}\nOverview: {movies_data.iloc[index_of_movie]['Overview']}\n\n"
    result_text += "Movie recommendations:\n"
    for i, (movie, rating, overview) in enumerate(top_movies, start=1):
        result_text += f"{i}. {movie} - Rating: {rating}\nOverview: {overview}\n\n"
    
    output.delete("1.0", tk.END)  # Clear previous output
    output.insert(tk.END, result_text)

# GUI setup
root = tk.Tk()
root.title("Movie Recommendation System")
root.configure(background='palegreen')
custom_font=("Arial",12)

label = tk.Label(root, text="Search Movie/Title:", bg='palegreen', fg='black',font=custom_font)
label.pack()

entry = tk.Entry(root, width=50, bd=3,font=custom_font,cursor="arrow")
entry.pack()

button = tk.Button(root, text="Recommend Movies", command=recommend_movies, bg='brown', fg='white',font=custom_font)
button.pack()

output = tk.Text(root, height=50, width=150, bg='lightyellow', fg='black',font=custom_font)
output.pack()

root.mainloop()