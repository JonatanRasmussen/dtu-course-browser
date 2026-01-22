#recommend_utils.py
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
import pickle
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.info_consts import InfoConsts
from website.global_constants.website_consts import WebsiteConsts

class CourseRecommender:
    """ Text Similarity with Embeddings """
    SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'  # all-mpnet-base-v2 (unused alternative)
    EMBEDDINGS_CACHE_FILE = 'recommended_course_embeddings_cache.pkl'
    FILTERED_DF_CACHE_FILE = 'recommended_filtered_courses_df_cache.pkl'

    def __init__(self, eager_load=False):
        self._model = None  # Lazy loaded - only loads when needed
        self.course_embeddings = None
        print(f"Loading course data from {FileNameConsts.name_of_pkl}.pkl")
        self.courses_df = CourseRecommender.load_course_data_df()
        print(f"Loaded {len(self.courses_df)} courses")

        # --- EAGER LOADING LOGIC ---
        # If eager_load is True, we force the model to load right now (at startup).
        if eager_load:
            print("Eager loading enabled: Initializing model now...")
            # Accessing self.model triggers the property logic below
            if self.model is None:
                print("WARNING: Model could not be loaded (missing 'sentence_transformers' library?)")
            else:
                print("Model loaded successfully during initialization.")

    @property
    def model(self):
        """
        Loads the SentenceTransformer model.
        Wrapped in try/except to allow the code to run even if the library is missing.
        """
        if self._model is None:
            try:
                # 1. Try to import the library. If this fails, we are in "Lite Mode"
                from sentence_transformers import SentenceTransformer
                print(f"Loading sentence transformer model: '{CourseRecommender.SENTENCE_TRANSFORMER_MODEL}'")

                # 2. Try to load the model file
                try:
                    # Fix for when this code is being run at pythonanywhere.com
                    web_path = FileNameConsts.pythonanywherecom_path_of_pkl + self.SENTENCE_TRANSFORMER_MODEL
                    self._model = SentenceTransformer(web_path)
                except FileNotFoundError:
                    # Relative path used when localhosting
                    local_path = FileNameConsts.path_of_pkl + self.SENTENCE_TRANSFORMER_MODEL
                    self._model = SentenceTransformer(local_path)

            except ImportError:
                print("CRITICAL: 'sentence_transformers' not installed. Keyword search will be disabled.")
                self._model = None
            except Exception as e:
                print(f"Error loading model: {e}")
                self._model = None

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
        """Fit the model using combined course text"""
        # Safety check: If model failed to load (no library), we cannot fit.
        if self.model is None:
            print("Cannot fit model: SentenceTransformer is not available.")
            return

        if self._is_pythonanywhere():
            print("Running on PythonAnywhere - cache-only mode enabled")
            if force_recreate:
                print("Warning: force_recreate=True ignored on PythonAnywhere to protect CPU quota")

            if self.load_embeddings_cache():
                return

            cache_dir = self._get_cache_dir()
            raise RuntimeError(
                f"CRITICAL: Cache files not found on PythonAnywhere!\n"
                f"Expected location: {cache_dir}"
            )

        if not force_recreate and self.load_embeddings_cache():
            return

        print("Creating new embeddings...")
        print("Combining course texts...")
        combined_texts = self.combine_course_text()
        non_empty_indices = [i for i, text in enumerate(combined_texts) if len(text.strip()) > 10]
        print(f"Found {len(non_empty_indices)} courses with meaningful text content")
        if not non_empty_indices:
            raise ValueError("No courses found with meaningful text content!")

        self.courses_df = self.courses_df.iloc[non_empty_indices].reset_index(drop=True)
        filtered_texts = [combined_texts[i] for i in non_empty_indices]
        print("Creating embeddings...")
        self.course_embeddings = self.model.encode(filtered_texts, show_progress_bar=True)
        print(f"Created embeddings for {len(filtered_texts)} courses")

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
            # If embeddings aren't loaded, we can't recommend
            print("Warning: Embeddings not loaded. Cannot recommend.")
            return pd.DataFrame()

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

        input_embedding = np.mean(self.course_embeddings[input_indices], axis=0)
        similarities = cosine_similarity([input_embedding], self.course_embeddings)[0]

        results_df = self.courses_df.copy()
        results_df['similarity_score'] = similarities
        results_df = results_df[~results_df.index.isin(input_indices)]
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

    def recommend_by_text(self, text_input, n_recommendations=10, return_all_ranked=False):
        """ Generates recommendations based on free text input."""
        # Check if model is loaded
        if self.course_embeddings is None or self.model is None:
            print("Model not fitted or library missing! Cannot recommend by text.")
            return pd.DataFrame()

        if not text_input or len(text_input.strip()) < 3:
            print("Input text too short")
            return pd.DataFrame()

        clean_text = self.preprocess_text(text_input)
        input_embedding = self.model.encode([clean_text])[0]
        similarities = cosine_similarity([input_embedding], self.course_embeddings)[0]

        results_df = self.courses_df.copy()
        results_df['similarity_score'] = similarities
        results_df = results_df.sort_values('similarity_score', ascending=False)

        if return_all_ranked:
            return results_df
        else:
            return results_df.head(n_recommendations)

    def recommend_hybrid(self, input_list, n_recommendations=10, return_all_ranked=False):
        """
        input_list: A list of dictionaries:
                    [{'type': 'course', 'value': '01005'}, {'type': 'text', 'value': 'Machine Learning'}]
        """
        if self.course_embeddings is None:
            print("Embeddings not loaded. Cannot recommend.")
            return pd.DataFrame()

        course_vectors = []
        text_vectors = []

        valid_vectors = []      # for explanation
        valid_labels = []
        is_course_input = []    # track which inputs are courses

        # 1. Convert inputs to vectors
        for item in input_list:
            if item['type'] == 'course':
                matches = self.courses_df[self.courses_df['COURSE'] == item['value']]
                if len(matches) > 0:
                    idx = matches.index[0]
                    vec = self.course_embeddings[idx]

                    course_vectors.append(vec)
                    valid_vectors.append(vec)
                    is_course_input.append(True)

                    course_name = matches.iloc[0]['NAME']
                    valid_labels.append(f"Course {item['value']} - {course_name}")

            elif item['type'] == 'text':
                # Only try to encode text if the model is actually loaded
                if self.model is not None:
                    clean_text = self.preprocess_text(item['value'])
                    if len(clean_text) > 2:
                        vec = self.model.encode([clean_text])[0]

                        text_vectors.append(vec)
                        valid_vectors.append(vec)
                        is_course_input.append(False)

                        display_text = item['value'][:20] + "..." if len(item['value']) > 20 else item['value']
                        valid_labels.append(f"input '{display_text}'")
                else:
                    print("Skipping text input: Model not available.")

        if not valid_vectors:
            return pd.DataFrame()

        # 2. Compute centroids per input type
        course_centroid = np.mean(course_vectors, axis=0) if course_vectors else None
        text_centroid = np.mean(text_vectors, axis=0) if text_vectors else None

        # 3. Combine centroids with 50/50 weighting
        if course_centroid is not None and text_centroid is not None:
            final_embedding = 0.5 * course_centroid + 0.5 * text_centroid
        elif course_centroid is not None:
            final_embedding = course_centroid
        else:
            final_embedding = text_centroid

        # 4. Overall similarity (ranking)
        overall_similarities = cosine_similarity(
            [final_embedding], self.course_embeddings
        )[0]

        # 5. Individual similarities (explanations + filtering)
        individual_sims = cosine_similarity(self.course_embeddings, valid_vectors)

        breakdown_col = []
        for row_sims in individual_sims:
            pairs = []
            for label, score in zip(valid_labels, row_sims):
                pairs.append({'name': label, 'score': float(score)})
            pairs.sort(key=lambda x: x['score'], reverse=True)
            breakdown_col.append(pairs)

        # 6. Build result DataFrame
        results_df = self.courses_df.copy()
        results_df['similarity_score'] = overall_similarities
        results_df['similarity_breakdown'] = breakdown_col

        # --- FILTERING LOGIC ---

        # 1. Remove explicitly selected input courses
        input_course_ids = [x['value'] for x in input_list if x['type'] == 'course']
        results_df = results_df[~results_df['COURSE'].isin(input_course_ids)]

        # 2. Remove near-duplicate courses (>= 0.99 similarity to any input COURSE)
        course_input_indices = [i for i, is_course in enumerate(is_course_input) if is_course]

        if course_input_indices:
            course_sims_matrix = individual_sims[:, course_input_indices]
            max_course_sim = np.max(course_sims_matrix, axis=1)

            is_duplicate_mask = max_course_sim >= 0.99
            results_df = results_df[~is_duplicate_mask[results_df.index]]

        # --- END FILTERING ---

        results_df = results_df.sort_values('similarity_score', ascending=False)

        if return_all_ranked:
            return results_df
        return results_df.head(n_recommendations)


class FilterRecommendations:
    """Filtering methods for CourseRecommender"""
    def __init__(self, eager_load=False):
        # Pass the eager_load flag down to the recommender
        self.recommender = FilterRecommendations.initialize_course_recommender(eager_load)
        self.filter_dct = FilterRecommendations.load_dct_from_json_file()
        print(f"Loaded filter dictionary with categories: {list(self.filter_dct.keys())}")

    def apply_filters(self, filter_criteria):
        if not filter_criteria:
            return set(self.recommender.courses_df['COURSE'].tolist())
        temp_dct = {}
        filters_found = 0
        for category, values in filter_criteria.items():
            if category not in self.filter_dct:
                print(f"Warning: Category '{category}' not found in filter dictionary")
                continue
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
        for category, course_list in temp_dct.items():
            course_set = set(course_list)
            if courses_to_display is None:
                courses_to_display = course_set
            else:
                courses_to_display = courses_to_display.intersection(course_set)
        print(f"Applied {filters_found} filters across {len(temp_dct)} categories, found {len(courses_to_display)} matching courses")
        return courses_to_display if courses_to_display else set()

    def get_filtered_recommendations(self, input_course_ids, filter_criteria=None, n_recommendations=10):
        all_recommendations = self.recommender.recommend_courses(input_course_ids, return_all_ranked=True)
        if not filter_criteria:
            return all_recommendations.head(n_recommendations)
        allowed_courses = self.apply_filters(filter_criteria)
        if not allowed_courses:
            print("No courses match the filter criteria")
            return pd.DataFrame()
        filtered_recommendations = all_recommendations[all_recommendations['COURSE'].isin(allowed_courses)]
        return filtered_recommendations.head(n_recommendations)

    def get_available_filter_options(self):
        filter_options = {}
        for category, values_dict in self.filter_dct.items():
            filter_options[category] = list(values_dict.keys())
        return filter_options

    def get_courses_by_filters(self, filter_criteria):
        matching_course_ids = self.apply_filters(filter_criteria)
        if not matching_course_ids:
            return pd.DataFrame()
        matching_courses = self.recommender.courses_df[self.recommender.courses_df['COURSE'].isin(matching_course_ids)]
        return matching_courses

    @staticmethod
    def initialize_course_recommender(eager_load=False):
        recommender = CourseRecommender(eager_load=eager_load)

        # Only fit if the embeddings/model are actually available
        # If model is None (library missing), fit() would fail on text encoding
        if recommender.model is not None or recommender.load_embeddings_cache():
            recommender.fit()
        else:
            print("Skipping fit(): Model not available and cache not found.")

        return recommender

    @staticmethod
    def load_dct_from_json_file():
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

    def get_text_based_recommendations(self, text_input, filter_criteria=None, n_recommendations=10):
        all_recommendations = self.recommender.recommend_by_text(text_input, return_all_ranked=True)
        if all_recommendations.empty:
            return pd.DataFrame()
        if not filter_criteria:
            return all_recommendations.head(n_recommendations)
        allowed_courses = self.apply_filters(filter_criteria)
        if not allowed_courses:
            print("No courses match the filter criteria")
            return pd.DataFrame()
        filtered_recommendations = all_recommendations[all_recommendations['COURSE'].isin(allowed_courses)]
        return filtered_recommendations.head(n_recommendations)