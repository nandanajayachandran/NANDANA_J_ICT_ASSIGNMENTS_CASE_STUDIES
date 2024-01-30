from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
import random
from rasa_sdk.events import SlotSet, AllSlotsReset
import pandas as pd
import requests
import logging


class ActionSayGreeting(Action):

    def name(self) -> Text:
        return "action_say_greeting"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        now = datetime.now()
        current_hour = now.hour
        SlotSet("book_title", None)
        SlotSet("book_author", None)
        SlotSet("book_genre", None)
        SlotSet("movie_title", None)
        SlotSet("movie_director", None)
        SlotSet("movie_genre", None)

        greeting_responses = {
            "morning": [
                "Good morning! ☀️ How can I help you find a great book or movie to start your day?",
                "Rise and shine!  Ready to explore some awesome recommendations, book or movie?",
                "Top of the morning to you!  Let's find something amazing ,book or movie, for you",
                "Hello, sunshine!  What kind of adventure are you seeking today, book or movie?",
                "Greetings, early bird!  I'm here to help you discover something delightful. Book or movie?",
                "Good morning, sport!  Ready to dive into a new story? Book or movie?",
                "Morning!  Let's find the perfect story for your morning. Book or movie?",
                "Wakey wakey, eggs and... recommendations! Book or movie, what are you in the mood for?",
                "Good morning, friend!  Let's make it a great day with a fantastic book or movie.",
                "Morning has broken, and so have I!  Just kidding, I'm here to help you with recommendations. Book or movie?",
            ],
            "afternoon": [
                "Good afternoon! ️ What kind of book or movie are you in the mood for?",
                "Hello there!  Looking for an entertaining afternoon escape? Book or movie?",
                "Welcome back!  Let's dive into some exciting recommendations. Book or movie?",
                "Howdy, partner!  Ready for some afternoon adventures in books or movies?",
                "Greetings and salutations!  What can I help you find this afternoon? Book or movie?",
                "Afternoon delight!  Let's find something to brighten your day. Book or movie?",
                "Hello, hello!  Looking for a midday pick-me-up?  I've got just the recommendations, book or movie?",
                "How's your afternoon going?  Want to spice it up with a great book or movie?",
                "Good afternoon, sunshine!  Ready to explore some new stories? Book or movie?",
                "Afternoon, friend!  Let's find the perfect way to relax and unwind. Book or a movie?",
            ],
            "evening": [
                "Good evening!  Ready to unwind with a good book or movie?",
                "Hello!  Looking for something to cozy up with tonight?",
                "Welcome!  Let's find the perfect story to end your day.",
                "Good evening, stargazer!  Ready to get lost in a book or movie?",
                "Greetings, night owl!  Let's find something to keep you entertained this evening.",
                "Hello, darkness, my old friend!  I've come to recommend books and movies again.",
                "Evening!  Ready to curl up with a good read or cozy movie?",
                "Movie night, anyone?  I've got the perfect recommendations for you.",
                "Good evening, friend!  Let's find something to help you relax and escape the day.",
                "Welcome to the evening hours!  Time to settle in with a good story.",
            ],
        }

        time_of_day = "morning" if 5 <= current_hour < 12 else "afternoon" if 12 <= current_hour < 18 else "evening"
        greeting = random.choice(greeting_responses[time_of_day])
        tip = "<br>Tip: Type Hi or Reset once you are done with recommendations for 1 category."
        message = greeting + tip
        dispatcher.utter_message(text=message)
        dispatcher.utter_message(text="<br>Tip: Type Hi or Reset once you are done with recommendations for 1 category.")

        return [SlotSet("book_title", None),
                SlotSet("book_author", None),
                SlotSet("book_genre", None),
                SlotSet("movie_title", None),
                SlotSet("movie_director", None),
                SlotSet("movie_genre", None)]


class ActionCategoryPrompt(Action):

    def name(self) -> Text:
        return "action_category_prompt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slot_value = tracker.get_slot("category")

        prompts = {
            "book": {
                "text": [
                    "Based on what criteria do you want the book suggestions: title, author, or genre?",
                    "What kind of book suggestions are you looking for: based on title, author, or genre?",
                    "How do you want to filter the book suggestions: by title, by author, or by genre?",
                    "Tell me how you want the book suggestions: by title, by author, or by genre?",
                    "What is your preferred way of getting book suggestions: title, author, or genre?",
                    "How should I narrow down the book suggestions for you: title, author, or genre?",
                    "What are you interested in when it comes to book suggestions: title, author, or genre?",
                    "How do you want me to fix the book suggestions: by title, by author, or by genre?",
                    "What type of book suggestions do you want: title, author, or genre?",
                    "In what way do you want the book suggestions: title, author, or genre?"
                ]
            },
            "movie": {
                "text": [
                    "How do you prefer the movie suggestions: based on name, director, or category?",
                    "What kind of movie suggestions do you want: name, director, or category?",
                    "By what criteria do you want the movie suggestions: name, director, or category?",
                    "What are your preferences for the movie suggestions: name, director, or category?",
                    "What type of movie suggestions are you looking for: name, director, or category?",
                    "In what way do you want the movie suggestions: by name, by director, or by category?",
                    "What is your preferred method of getting movie suggestions: name, director, or category?",
                    "How should I fix the movie suggestions for you: by name, by director, or by category?",
                    "What are you interested in when it comes to movie suggestions: name, director, or category?",
                    "How do you want to filter the movie suggestions: by name, by director, or by category?"
                ]
            }
        }

        if slot_value in prompts:
            random_prompt = random.choice(prompts[slot_value]["text"])
            dispatcher.utter_message(text=random_prompt)  # Directly send the text prompt
        else:
            dispatcher.utter_message(text="Sorry, I'm not sure what you're asking for. Can you please clarify?")

        return []


class ActionBookRecommendation(Action):

    def name(self) -> Text:
        return "action_book_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        min_ind_b = tracker.get_slot('total_book_recommendations')
        max_ind_b = min_ind_b + 5
        category = tracker.get_slot("category")
        recommendations = []

        if category == "book":
            if tracker.get_slot("book_genre"):
                recommendations = self.fetch_recommendations_by_genre(tracker.get_slot("book_genre"), min_ind_b, max_ind_b)
            elif tracker.get_slot("book_author"):
                recommendations = self.fetch_recommendations_by_author(tracker.get_slot("book_author"), min_ind_b, max_ind_b)
            elif tracker.get_slot("book_title"):
                if min_ind_b >= 5:
                    dispatcher.utter_message(
                        text="No more recommendations are possible because the books are too different from each other")
                else:
                    recommendations = self.fetch_recommendations_by_title(tracker.get_slot("book_title"))
            else:
                dispatcher.utter_message(text="Sorry, I couldn't find any recommendations with that specific criteria.")
                return []

            if recommendations:
                html_recs = [
                    f'<a href="https://www.google.com/search?q={rec.lower().replace(" ", "+")}" target="_blank">{rec}</a>'
                    for rec in recommendations]
                dispatcher.utter_message(
                    text="Here are some recommendations:<br>* " + "<br>* ".join(html_recs[:5]))
                return [SlotSet("total_book_recommendations", max_ind_b)]
            else:
                dispatcher.utter_message(text="Sorry, I couldn't find any recommendations based on that.")

        return []

    def fetch_recommendations_by_genre(self, genre: Text, min_ind_b: int, max_ind_b: int) -> List[Text]:
        base_url = "https://openlibrary.org/search.json"
        params = {
            "q": genre,
            "fields": "title,author",
        }
        min_ind_b = min_ind_b
        max_ind_b = max_ind_b
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()

            data = response.json()
            books = data.get("docs", [])

            recommendations = []
            for book in books[min_ind_b:max_ind_b]:
                title = book.get("title")
                # author = book.get("author", [{}])[0].get("name", "Unknown Author")

                recommendations.append(f"{title}")

            return recommendations

        except requests.exceptions.RequestException as e:
            return ["Sorry, I couldn't fetch recommendations from the API at this time. Please try again later."]

    def fetch_recommendations_by_author(self, author: Text, min_ind_b: int, max_ind_b: int) -> List[Text]:
        base_url = "https://openlibrary.org/search.json"
        params = {
            "q": author,
            "mode": "ebooks",
            "fields": "title",
        }
        min_ind_b = min_ind_b
        max_ind_b = max_ind_b
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()

            data = response.json()
            books = data.get("docs", [])

            recommendations = []
            for book in books[min_ind_b:max_ind_b]:
                title = book.get("title")
                recommendations.append(f"{title}")

            return recommendations

        except requests.exceptions.RequestException as e:
            logging.exception("Error fetching recommendations from the API: %s", str(e))
            return ["Sorry, I couldn't fetch recommendations from the API at this time. Please try again later."]

    def fetch_recommendations_by_title(self, title: Text) -> List[Text]:
        books = pd.read_csv("C:\Users\Dell\Desktop\ICT_project\Submissionfolder\Readflix\actions\book_reco.csv")
        # books["text"] = books["text"].apply(" ".join)

        try:
            book_index = books.loc[books["title"].str.lower() == title.lower()].index[0]
        except IndexError:
            return ["Title not found in the dataset."]

        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vectorizer = TfidfVectorizer(stop_words=None)
        tfidf_matrix = vectorizer.fit_transform(books["text"])

        def recommend_similar_books(text):
            book_vector = tfidf_matrix.getrow(text)
            cosine_similarities = cosine_similarity(book_vector, tfidf_matrix)
            top_indices = cosine_similarities[0].argsort()[-6:-1][::-1]
            recommendations = []
            for index in top_indices:
                book = books.iloc[index]
                recommendations.append(f"{book['title']}")
            return recommendations

        return recommend_similar_books(book_index)


class ActionMovieRecommendation(Action):

    def name(self) -> Text:
        return "action_movie_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        min_ind_m = tracker.get_slot('total_movie_recommendations')
        max_ind_m = min_ind_m + 5
        category = tracker.get_slot("category")
        recommendations = []
        if category == "movie":
            if tracker.get_slot("movie_genre"):
                recommendations = self.fetch_recommendations_by_genre(tracker.get_slot("movie_genre"), min_ind_m, max_ind_m)
            elif tracker.get_slot("movie_director"):
                if min_ind_m >= 5:
                    dispatcher.utter_message(text="Sorry, the TMDB api is unable to fetch any more results.")
                else:
                    recommendations = self.fetch_recommendations_by_director(tracker.get_slot("movie_director"), min_ind_m, max_ind_m)
            elif tracker.get_slot("movie_title"):
                if min_ind_m >= 5:
                    dispatcher.utter_message(text="No more recommendations are possible as the movies are too different")
                else:
                    recommendations = self.fetch_recommendations_by_title(tracker.get_slot("movie_title"))
            else:
                dispatcher.utter_message(text="Sorry, I couldn't find any recommendations with that specific criteria.")
                return []

            if recommendations:
                html_recs = [
                    f'<a href="https://www.google.com/search?q={rec.lower().replace(" ", "+")}" target="_blank">{rec}</a>'
                    for rec in recommendations]
                dispatcher.utter_message(text="Here are some recommendations:<br>* " + "<br>* ".join(html_recs[min_ind_m:max_ind_m]))
                return [SlotSet("total_movie_recommendations", max_ind_m)]
            else:
                dispatcher.utter_message(text="Sorry, I couldn't find any recommendations based on that.")

        return []

    def fetch_recommendations_by_genre(self, genre: Text, min_ind_m: int, max_ind_m: int) -> List[Text]:

        api_key = "-------------------"
        base_url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": api_key,
            "with_genres": genre,
            "sort_by": "popularity.desc",
            "include_adult": "false",
            "page": 1,
            "language": "en-US"
        }
        min_ind_m = min_ind_m
        max_ind_m = max_ind_m
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            recommendations = []
            for movie in data["results"]:
                recommendations.append(movie["title"])

            return recommendations

        except requests.exceptions.RequestException as e:
            print(f"Error fetching recommendations: {e}")
            return ["Error fetching recommendations from TMDB. Please try again later."]

    def fetch_recommendations_by_director(self, director: Text, min_ind_m: int, max_ind_m: int) -> List[Text]:

        api_key = '-------------'
        api_endpoint = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={director}'
        response = requests.get(api_endpoint)

        if response.status_code == 200:
            # Parse the JSON response
            json_data = response.json()
            movies = json_data["results"]
            recommendations = []
            for movie in movies:
                recommendations.append(movie["title"])
            return recommendations
        else:
            return ["The API is not responding."]


    def fetch_recommendations_by_title(self, title: Text) -> List[Text]:
        movies = pd.read_csv("C:\Users\Dell\Desktop\ICT_project\Submissionfolder\Readflix\actions\movie_reco.csv")
        # movies["text"] = movies["text"].apply(" ".join)

        try:
            movie_index = movies.index[movies["Movie Name"].str.lower() == title.lower()].tolist()[0]
        except IndexError:
            return ["Title not found in the dataset."]

        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(movies["text"])

        def recommend_similar_movies(text):
            movie_vector = tfidf_matrix[text]
            cosine_similarities = cosine_similarity(movie_vector, tfidf_matrix)
            top_indices = cosine_similarities[0].argsort()[-6:-1][::-1]
            recommendations = []
            for index in top_indices:
                movie = movies.iloc[index]
                recommendations.append(f"* {movie['Movie Name']}")
            return recommendations

        return recommend_similar_movies(movie_index)


class ActionMoreRecommendations(Action):
    def name(self) -> Text:
        return "action_more_recommendations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        category = tracker.get_slot("category")

        if category == "movie":
            num_slot = "total_movie_recommendations"
        elif category == "book":
            num_slot = "total_book_recommendations"
        else:

            dispatcher.utter_message(text="Sorry, I don't know how to recommend that category.")

            return []

        num_recommendations = tracker.get_slot(num_slot)

        if num_recommendations >= 20:

            dispatcher.utter_message(text="Sorry, I have no more recommendations for you.")

            return []
        else:
            events = []

            if category == "movie":
                movie_recommender = ActionMovieRecommendation()
                events += movie_recommender.run(dispatcher, tracker, domain)
            elif category == "book":
                book_recommender = ActionBookRecommendation()
                events += book_recommender.run(dispatcher, tracker, domain)

            if not events:
                dispatcher.utter_message(text="Sorry, I have no more recommendations for you at this time.")
                return []

            return events


class ActionResetAllSlots(Action):
    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]
