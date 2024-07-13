import pickle
import streamlit as st
import numpy as np
import os


st.header("Books Recommended System Using ML")

file_path_model = os.path.join(os.getcwd(),'..','artifacts','model.pkl')
file_path_books_name = os.path.join(os.getcwd(),'..','artifacts','books_name.pkl')
file_path_final_rating = os.path.join(os.getcwd(),'..','artifacts','final_rating.pkl')
file_path_book_pivot = os.path.join(os.getcwd(),'..','artifacts','book_pivot.pkl')


model = pickle.load(open(file_path_model,'rb'))
books_name = pickle.load(open(file_path_books_name,'rb'))
final_rating = pickle.load(open(file_path_final_rating,'rb'))
book_pivot = pickle.load(open(file_path_book_pivot,'rb'))

def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []
    
    for book_id in suggestion:
        book_name.append(book_pivot.columns[book_id])
        
    for name in book_name[0]:
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)
        
    for ids in ids_index:
        url = final_rating.iloc[ids]['img_url']
        poster_url.append(url)
        
    return poster_url
        
def recommend_books(book_name):
    book_list = []
    book_id = np.where(book_pivot.columns == book_name)[0][0]
    distance , suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)
    
    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
        books = book_pivot.columns[suggestion[i]]
        for j in books:
            book_list.append(j)
            
            
    return book_list, poster_url
    
selected_books = st.selectbox(
    "Type or select a book",
    books_name
)

if st.button('Show Recommendation'):
    recommendation_books , poster_url = recommend_books(selected_books)
    col1,col2,col3,col4,col5 = st.columns(5)
    
    with col1:
        st.text(recommendation_books[1])
        st.image(poster_url[1])
    
    with col2:
        st.text(recommendation_books[2])
        st.image(poster_url[2])
        
    with col3:
        st.text(recommendation_books[3])
        st.image(poster_url[3])
        
    with col4:
        st.text(recommendation_books[4])
        st.image(poster_url[4])
        
    with col5:
        st.text(recommendation_books[5])
        st.image(poster_url[5])