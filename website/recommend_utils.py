import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
import nltk
from nltk.corpus import stopwords
import re
import os
import pickle
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.info_consts import InfoConsts
from website.global_constants.website_consts import WebsiteConsts

class CourseRecommender:
    """ Text Similarity with Embeddings """
    SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'
    EMBEDDINGS_CACHE_FILE = 'recommended_course_embeddings_cache.pkl'
    FILTERED_DF_CACHE_FILE = 'recommended_filtered_courses_df_cache.pkl'

    def __init__(self):
        self._model = None  # Lazy loaded - only loads when needed
        self.course_embeddings = None
        print(f"Loading course data from {FileNameConsts.name_of_pkl}.pkl")
        self.courses_df = CourseRecommender.load_course_data_df()
        print(f"Loaded {len(self.courses_df)} courses")

    @property
    def model(self):
        """Lazy load the SentenceTransformer model only when needed"""
        if self._model is None:
            from sentence_transformers import SentenceTransformer  # Lazy import
            print(f"Loading sentence transformer model: '{CourseRecommender.SENTENCE_TRANSFORMER_MODEL}'")
            self._model = SentenceTransformer(CourseRecommender.SENTENCE_TRANSFORMER_MODEL)
        return self._model

    @staticmethod
    def load_course_data_df():
        try:
            # Fix for when this code is being run at pythonanywhere.com
            pythonanywhere_name_and_path_of_pkl = FileNameConsts.pythonanywherecom_path_of_pkl + FileNameConsts.name_of_pkl + ".pkl"
            df = pd.read_pickle(pythonanywhere_name_and_path_of_pkl)
        except FileNotFoundError:
            # Relative path used when localhosting
            name_and_path_of_pkl = FileNameConsts.path_of_pkl + FileNameConsts.name_of_pkl + ".pkl"
            df = pd.read_pickle(name_and_path_of_pkl)
        return df

    def _is_pythonanywhere(self):
        """Detect if running on PythonAnywhere"""
        return os.path.exists(FileNameConsts.pythonanywherecom_path_of_pkl)

    def _get_cache_dir(self):
        """Get the appropriate cache directory"""
        if self._is_pythonanywhere():
            return FileNameConsts.pythonanywherecom_path_of_pkl
        return FileNameConsts.path_of_pkl

    def save_embeddings_cache(self):
        """Save embeddings and filtered dataframe to cache files"""
        try:
            cache_dir = self._get_cache_dir()
            embeddings_path = os.path.join(cache_dir, self.EMBEDDINGS_CACHE_FILE)
            df_path = os.path.join(cache_dir, self.FILTERED_DF_CACHE_FILE)

            print(f"Saving embeddings cache to {embeddings_path}")
            with open(embeddings_path, 'wb') as f:
                pickle.dump(self.course_embeddings, f)

            print(f"Saving filtered dataframe cache to {df_path}")
            self.courses_df.to_pickle(df_path)

            print("Cache saved successfully!")
            return True
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")
            return False

    def load_embeddings_cache(self):
        """Load embeddings and filtered dataframe from cache files"""
        try:
            cache_dir = self._get_cache_dir()
            embeddings_path = os.path.join(cache_dir, self.EMBEDDINGS_CACHE_FILE)
            df_path = os.path.join(cache_dir, self.FILTERED_DF_CACHE_FILE)

            if not os.path.exists(embeddings_path) or not os.path.exists(df_path):
                print(f"Cache files not found at {cache_dir}")
                print(f"  Looking for: {embeddings_path}")
                print(f"  Looking for: {df_path}")
                return False

            print(f"Loading embeddings cache from {embeddings_path}")
            with open(embeddings_path, 'rb') as f:
                self.course_embeddings = pickle.load(f)

            print(f"Loading filtered dataframe cache from {df_path}")
            self.courses_df = pd.read_pickle(df_path)

            print(f"Cache loaded successfully! {len(self.courses_df)} courses with embeddings ready.")
            return True
        except Exception as e:
            print(f"Warning: Could not load cache: {e}")
            return False

    def preprocess_text(self, text):
        if pd.isna(text) or text == "None" or text == "NO_DATA":
            return ""
        text = re.sub(r'<[^>]+>', ' ', str(text))  # Remove HTML tags
        text = re.sub(r'<br\s*/?>', ' ', text)  # Remove <br /> tags specifically
        text = re.sub(r'[^a-zA-Z\s]', ' ', text.lower())  # Clean and preprocess course descriptions
        text = ' '.join(text.split())  # Remove extra whitespace
        return text

    def combine_course_text(self):
        """Combine all relevant text columns for each course"""
        combined_texts = []
        text_columns = [
            InfoConsts.course_description.key_df,
            InfoConsts.learning_objectives.key_df,
            InfoConsts.course_content.key_df,
            InfoConsts.remarks.key_df,
            InfoConsts.old_recommended_prerequisites.key_df,
            InfoConsts.recommended_prerequisites.key_df,
            InfoConsts.mandatory_prerequisites,
        ]
        for _, row in self.courses_df.iterrows():
            course_text_parts = []
            for col in text_columns:
                if col in self.courses_df.columns:
                    processed_text = self.preprocess_text(row[col])
                    if processed_text:  # Only add non-empty text
                        course_text_parts.append(processed_text)
            # Join all text parts for this course
            combined_text = ' '.join(course_text_parts)
            combined_texts.append(combined_text)
        return combined_texts

    def fit(self, force_recreate=False):
        """Fit the model using combined course text

        Args:
            force_recreate (bool): If True, recreate embeddings even if cache exists.
                                   Ignored on PythonAnywhere for safety.
        """
        # On PythonAnywhere, always try cache first and refuse to create new embeddings
        if self._is_pythonanywhere():
            print("Running on PythonAnywhere - cache-only mode enabled")
            if force_recreate:
                print("Warning: force_recreate=True ignored on PythonAnywhere to protect CPU quota")

            if self.load_embeddings_cache():
                return  # Successfully loaded from cache

            # Cache not found on PythonAnywhere - this is a critical error
            cache_dir = self._get_cache_dir()
            raise RuntimeError(
                f"CRITICAL: Cache files not found on PythonAnywhere!\n"
                f"Expected location: {cache_dir}\n"
                f"Expected files:\n"
                f"  - {self.EMBEDDINGS_CACHE_FILE}\n"
                f"  - {self.FILTERED_DF_CACHE_FILE}\n\n"
                f"Please generate cache locally and upload these files to PythonAnywhere.\n"
                f"To generate cache locally, run: python recommend_courses.py"
            )

        # Local development - normal behavior
        if not force_recreate and self.load_embeddings_cache():
            return  # Successfully loaded from cache

        print("Creating new embeddings...")
        print("Combining course texts...")
        combined_texts = self.combine_course_text()
        # Filter out courses with no meaningful text
        non_empty_indices = [i for i, text in enumerate(combined_texts) if len(text.strip()) > 10]
        print(f"Found {len(non_empty_indices)} courses with meaningful text content")
        if not non_empty_indices:
            raise ValueError("No courses found with meaningful text content!")
        # Filter dataframe and texts to only include courses with content
        self.courses_df = self.courses_df.iloc[non_empty_indices].reset_index(drop=True)
        filtered_texts = [combined_texts[i] for i in non_empty_indices]
        print("Creating embeddings...")
        # Create embeddings - this is where self.model is accessed, triggering lazy load
        self.course_embeddings = self.model.encode(filtered_texts, show_progress_bar=True)
        print(f"Created embeddings for {len(filtered_texts)} courses")

        # Save to cache
        self.save_embeddings_cache()

    def clear_cache(self):
        """Delete cache files to force recreation of embeddings"""
        if self._is_pythonanywhere():
            print("Warning: Refusing to clear cache on PythonAnywhere to protect CPU quota")
            return

        try:
            cache_dir = self._get_cache_dir()
            embeddings_path = os.path.join(cache_dir, self.EMBEDDINGS_CACHE_FILE)
            df_path = os.path.join(cache_dir, self.FILTERED_DF_CACHE_FILE)

            if os.path.exists(embeddings_path):
                os.remove(embeddings_path)
                print(f"Deleted {embeddings_path}")

            if os.path.exists(df_path):
                os.remove(df_path)
                print(f"Deleted {df_path}")

            print("Cache cleared successfully!")
        except Exception as e:
            print(f"Error clearing cache: {e}")

    def find_course_by_id(self, course_id):
        """Helper method to find course info"""
        matches = self.courses_df[self.courses_df['COURSE'] == course_id]
        if len(matches) > 0:
            return matches.iloc[0]
        return None

    def recommend_courses(self, input_course_ids, n_recommendations=10, return_all_ranked=False):
        if self.course_embeddings is None:
            raise ValueError("Model not fitted! Call fit() first.")
        # Get indices of input courses
        input_indices = []
        found_courses = []
        for course_id in input_course_ids:
            matches = self.courses_df[self.courses_df['COURSE'] == course_id]
            if len(matches) > 0:
                input_indices.append(matches.index[0])
                found_courses.append(course_id)
            else:
                print(f"Warning: Course {course_id} not found in dataset")
        if not input_indices:
            print("No valid input courses found!")
            return pd.DataFrame()
        print(f"Using courses as input: {found_courses}")
        # Average embeddings of input courses
        input_embedding = np.mean(self.course_embeddings[input_indices], axis=0)
        # Calculate similarities
        similarities = cosine_similarity([input_embedding], self.course_embeddings)[0]
        # Create results dataframe
        results_df = self.courses_df.copy()
        results_df['similarity_score'] = similarities
        # Remove input courses from recommendations
        results_df = results_df[~results_df.index.isin(input_indices)]
        # Sort by similarity
        results_df = results_df.sort_values('similarity_score', ascending=False)
        if return_all_ranked:
            return results_df
        else:
            return results_df.head(n_recommendations)

    def get_course_info(self, course_id):
        """Get detailed info about a specific course"""
        course = self.find_course_by_id(course_id)
        if course is not None:
            return {
                'course_id': course['COURSE'],
                'name': course['NAME'],
                'ects': course['ECTS_POINTS'],
                'institute': course['INSTITUTE'],
                'description': course['COURSE_DESCRIPTION'][:200] + '...' if len(str(course['COURSE_DESCRIPTION'])) > 200 else course['COURSE_DESCRIPTION']
            }
        return None

    def display_recommendations(self, recommendations_df, show_description=True):
        """Pretty print recommendations"""
        if recommendations_df.empty:
            print("No recommendations found.")
            return
        print(f"\nTop {len(recommendations_df)} Recommendations:")
        print("=" * 80)
        for idx, (_, row) in enumerate(recommendations_df.iterrows(), 1):
            print(f"{idx}. {row['COURSE']} - {row['NAME']}")
            print(f"   Similarity: {row['similarity_score']:.3f} | ECTS: {row['ECTS_POINTS']} | Institute: {row['INSTITUTE']}")
            if show_description and pd.notna(row['COURSE_DESCRIPTION']):
                desc = str(row['COURSE_DESCRIPTION'])[:150]
                print(f"   Description: {desc}{'...' if len(str(row['COURSE_DESCRIPTION'])) > 150 else ''}")
            print()

    def analyze_course_content(self, course_id):
        """Analyze what text content is available for a specific course"""
        course = self.find_course_by_id(course_id)
        if course is None:
            print(f"Course {course_id} not found")
            return
        print(f"Content analysis for {course_id} - {course['NAME']}")
        print("=" * 60)
        text_columns = ['COURSE_DESCRIPTION', 'LEARNING_OBJECTIVES', 'COURSE_CONTENT', 'REMARKS']
        for col in text_columns:
            content = course[col]
            if pd.notna(content) and str(content).strip() not in ['None', 'NO_DATA', '']:
                print(f"{col}: {len(str(content))} characters")
                print(f"  Preview: {str(content)[:100]}...")
            else:
                print(f"{col}: No content")
            print()


class FilterRecommendations:
    """Filtering methods for CourseRecommender"""
    def __init__(self):
        self.recommender = FilterRecommendations.initialize_course_recommender()
        self.filter_dct = FilterRecommendations.load_dct_from_json_file()
        print(f"Loaded filter dictionary with categories: {list(self.filter_dct.keys())}")

    def apply_filters(self, filter_criteria):
        """
        Apply filters to get a set of courses matching criteria.
        Args:
            filter_criteria (dict): Dictionary with format: {"category_name": ["value1", "value2"], "another_category": ["value3"]}
            Example: {"language": ["eng"], "gradetype": ["passfail", "sevenstep"]}
        Returns:
            set: Set of course IDs matching all filter criteria
        """
        if not filter_criteria:
            return set(self.recommender.courses_df['COURSE'].tolist())  # No filters applied - return all courses
        temp_dct = {}
        filters_found = 0
        for category, values in filter_criteria.items():  # Build temporary dictionary with courses for each category
            if category not in self.filter_dct:
                print(f"Warning: Category '{category}' not found in filter dictionary")
                continue
            # Collect courses for all values in this category
            category_courses = []
            for value in values:
                if value in self.filter_dct[category]:
                    filters_found += 1
                    category_courses.extend(self.filter_dct[category][value])
                else:
                    print(f"Warning: Value '{value}' not found in category '{category}'")
            if category_courses:
                temp_dct[category] = category_courses
        if not temp_dct:
            print("No valid filters found, returning empty set")
            return set()
        courses_to_display = None
        for category, course_list in temp_dct.items():  # Intersect all category course lists
            course_set = set(course_list)
            if courses_to_display is None:
                courses_to_display = course_set
            else:
                courses_to_display = courses_to_display.intersection(course_set)
        print(f"Applied {filters_found} filters across {len(temp_dct)} categories, found {len(courses_to_display)} matching courses")
        return courses_to_display if courses_to_display else set()

    def get_filtered_recommendations(self, input_course_ids, filter_criteria=None, n_recommendations=10):
        """ Get course recommendations with optional filtering.
        Args:
            input_course_ids (list): List of course IDs to base recommendations on
            filter_criteria (dict): Optional filter criteria (same format as apply_filters)
            n_recommendations (int): Number of recommendations to return
        Returns:
            pd.DataFrame: Filtered and sorted recommendations
        """
        all_recommendations = self.recommender.recommend_courses(input_course_ids, return_all_ranked=True)  # Get all recommendations (ranked)
        if not filter_criteria:
            return all_recommendations.head(n_recommendations)
        allowed_courses = self.apply_filters(filter_criteria)
        if not allowed_courses:
            print("No courses match the filter criteria")
            return pd.DataFrame()
        filtered_recommendations = all_recommendations[all_recommendations['COURSE'].isin(allowed_courses)]
        return filtered_recommendations.head(n_recommendations)  # Filter recommendations to only include allowed courses

    def get_available_filter_options(self):
        """Get all available filter categories and their values, return dct of categories and their possible values"""
        filter_options = {}
        for category, values_dict in self.filter_dct.items():
            filter_options[category] = list(values_dict.keys())
        return filter_options

    def get_courses_by_filters(self, filter_criteria):
        """ Get course details for courses matching filter criteria (without using recommender).
        Args: filter_criteria (dict): Filter criteria dictionary
        Returns: pd.DataFrame: DataFrame with matching courses """
        matching_course_ids = self.apply_filters(filter_criteria)
        if not matching_course_ids:
            return pd.DataFrame()
        # Get course details from recommender's dataframe
        matching_courses = self.recommender.courses_df[self.recommender.courses_df['COURSE'].isin(matching_course_ids)]
        return matching_courses

    @staticmethod
    def initialize_course_recommender():
        recommender = CourseRecommender()
        recommender.fit()
        return recommender

    @staticmethod
    def load_dct_from_json_file():
        """Load in dictionary from json file"""
        file_name = WebsiteConsts.json_filter_dct
        try:
            pythonanywhere_dct_name = FileNameConsts.pythonanywherecom_path_of_pkl + file_name + '.json'
            with open(pythonanywhere_dct_name) as f:
                dct = json.load(f)
            return dct
        except FileNotFoundError:
            try:
                dct_name = FileNameConsts.path_of_pkl + file_name + '.json'
                with open(dct_name) as f:
                    dct = json.load(f)
                return dct
            except Exception as e:
                print(f"Error: Dictionary with file name {file_name} was not found in {FileNameConsts.path_of_pkl}")
                print(f"Exception: {e}")
                return {}