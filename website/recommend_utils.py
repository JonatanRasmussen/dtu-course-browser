#recommend_utils.py
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
import pickle
import traceback
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.info_consts import InfoConsts
from website.global_constants.website_consts import WebsiteConsts

# --- ONNX CHANGE: New imports ---
import onnxruntime as ort
from tokenizers import Tokenizer


class CourseRecommender:
    """ Text Similarity with Embeddings """

    # --- ONNX CHANGE: Constants for ONNX model (just folder/file names, not full paths) ---
    ONNX_MODEL_FOLDER = 'model_onnx'  # Folder name only
    ONNX_MODEL_FILE = 'model.onnx'
    TOKENIZER_FILE = 'tokenizer.json'

    EMBEDDINGS_CACHE_FILE = 'recommended_course_embeddings_cache.pkl'
    FILTERED_DF_CACHE_FILE = 'recommended_filtered_courses_df_cache.pkl'

    def __init__(self, eager_load=False):
        # --- ONNX CHANGE: Replace _model with _session and _tokenizer ---
        self._session = None      # ONNX inference session (lazy loaded)
        self._tokenizer = None    # Tokenizer (lazy loaded)
        self._model_loaded = False

        self.course_embeddings = None
        print(f"Loading course data from {FileNameConsts.name_of_pkl}.pkl")
        self.courses_df = CourseRecommender.load_course_data_df()
        print(f"Loaded {len(self.courses_df)} courses")

        if eager_load:
            print("Eager loading enabled: Initializing ONNX model now...")
            if self._load_onnx_model():
                print("ONNX model loaded successfully during initialization.")
            else:
                print("WARNING: ONNX model could not be loaded.")

    # --- ONNX CHANGE: New method to load ONNX model with path fallback ---
    def _load_onnx_model(self):
        """
        Load the ONNX model and tokenizer.
        Tries PythonAnywhere path first, then falls back to local path.
        """
        if self._model_loaded:
            return True

        # Define both possible paths
        pythonanywhere_model_path = os.path.join(
            FileNameConsts.pythonanywherecom_path_of_pkl,
            self.ONNX_MODEL_FOLDER
        )
        local_model_path = os.path.join(
            FileNameConsts.path_of_pkl,
            self.ONNX_MODEL_FOLDER
        )

        # Try PythonAnywhere path first, then local path
        model_path = None
        for path in [pythonanywhere_model_path, local_model_path]:
            tokenizer_check = os.path.join(path, self.TOKENIZER_FILE)
            onnx_check = os.path.join(path, self.ONNX_MODEL_FILE)

            if os.path.exists(tokenizer_check) and os.path.exists(onnx_check):
                model_path = path
                break

        if model_path is None:
            print(f"ONNX model files not found in either location:")
            print(f"  Tried: {pythonanywhere_model_path}")
            print(f"  Tried: {local_model_path}")
            return False

        try:
            tokenizer_path = os.path.join(model_path, self.TOKENIZER_FILE)
            onnx_path = os.path.join(model_path, self.ONNX_MODEL_FILE)

            print(f"Loading tokenizer from: {tokenizer_path}")
            self._tokenizer = Tokenizer.from_file(tokenizer_path)
            self._tokenizer.enable_padding(pad_id=0, pad_token="[PAD]", length=256)
            self._tokenizer.enable_truncation(max_length=256)

            print(f"Loading ONNX model from: {onnx_path}")
            self._session = ort.InferenceSession(onnx_path)

            self._model_loaded = True
            print("ONNX model and tokenizer loaded successfully!")
            return True

        except FileNotFoundError as e:
            print(f"ONNX model files not found: {e}")
            return False
        except Exception as e:
            print(f"Error loading ONNX model: {e}")
            traceback.print_exc()
            return False

    @property
    def model(self):
        """Property for backward compatibility - returns session if model is loaded"""
        if not self._model_loaded:
            self._load_onnx_model()
        return self._session  # Returns None if not loaded, truthy if loaded

    def _mean_pooling(self, model_output, attention_mask):
        """Average the token embeddings, ignoring padding tokens"""
        token_embeddings = model_output[0]
        input_mask_expanded = np.expand_dims(attention_mask, axis=-1)
        input_mask_expanded = np.broadcast_to(input_mask_expanded, token_embeddings.shape).astype(float)

        sum_embeddings = np.sum(token_embeddings * input_mask_expanded, axis=1)
        sum_mask = np.clip(input_mask_expanded.sum(axis=1), a_min=1e-9, a_max=None)

        return sum_embeddings / sum_mask

    def encode(self, sentences, show_progress_bar=False):
        """
        Encode sentences into embeddings using ONNX model.
        This replaces SentenceTransformer's encode() method.
        """
        if not self._model_loaded:
            if not self._load_onnx_model():
                raise RuntimeError("ONNX model not available for encoding")

        # Handle single string input
        if isinstance(sentences, str):
            sentences = [sentences]

        # Tokenize all sentences
        encoded_inputs = self._tokenizer.encode_batch(sentences)

        # Prepare numpy arrays for ONNX
        input_ids = np.array([e.ids for e in encoded_inputs], dtype=np.int64)
        attention_mask = np.array([e.attention_mask for e in encoded_inputs], dtype=np.int64)
        token_type_ids = np.array([e.type_ids for e in encoded_inputs], dtype=np.int64)

        # Run inference
        outputs = self._session.run(
            None,
            {
                'input_ids': input_ids,
                'attention_mask': attention_mask,
                'token_type_ids': token_type_ids
            }
        )

        # Apply mean pooling
        embeddings = self._mean_pooling(outputs, attention_mask)

        # Normalize embeddings (important for cosine similarity)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / np.clip(norms, a_min=1e-9, a_max=None)

        return embeddings

    @staticmethod
    def load_course_data_df():
        try:
            pythonanywhere_name_and_path_of_pkl = FileNameConsts.pythonanywherecom_path_of_pkl + FileNameConsts.name_of_pkl + ".pkl"
            df = pd.read_pickle(pythonanywhere_name_and_path_of_pkl)
        except FileNotFoundError:
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
        text = re.sub(r'<[^>]+>', ' ', str(text))
        text = re.sub(r'<br\s*/?>', ' ', text)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text.lower())
        text = ' '.join(text.split())
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
                    if processed_text:
                        course_text_parts.append(processed_text)
            combined_text = ' '.join(course_text_parts)
            combined_texts.append(combined_text)
        return combined_texts

    def fit(self, force_recreate=False):
        """Fit the model using combined course text"""
        # --- ONNX CHANGE: Check for ONNX model instead of SentenceTransformer ---
        if self.model is None:
            print("Cannot fit model: ONNX model is not available.")
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

        # --- ONNX CHANGE: Use self.encode() instead of self.model.encode() ---
        print("Creating embeddings...")
        self.course_embeddings = self.encode(filtered_texts, show_progress_bar=True)
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
        """Generates recommendations based on free text input."""
        # --- ONNX CHANGE: Check model availability ---
        if self.course_embeddings is None or self.model is None:
            print("Model not fitted or not available! Cannot recommend by text.")
            return pd.DataFrame()

        if not text_input or len(text_input.strip()) < 3:
            print("Input text too short")
            return pd.DataFrame()

        clean_text = self.preprocess_text(text_input)

        # --- ONNX CHANGE: Use self.encode() instead of self.model.encode() ---
        input_embedding = self.encode([clean_text])[0]
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

        valid_vectors = []
        valid_labels = []
        is_course_input = []

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
                # --- ONNX CHANGE: Check self.model and use self.encode() ---
                if self.model is not None:
                    clean_text = self.preprocess_text(item['value'])
                    if len(clean_text) > 2:
                        vec = self.encode([clean_text])[0]

                        text_vectors.append(vec)
                        valid_vectors.append(vec)
                        is_course_input.append(False)

                        display_text = item['value'][:20] + "..." if len(item['value']) > 20 else item['value']
                        valid_labels.append(f"input '{display_text}'")
                else:
                    print("Skipping text input: Model not available.")

        if not valid_vectors:
            return pd.DataFrame()

        course_centroid = np.mean(course_vectors, axis=0) if course_vectors else None
        text_centroid = np.mean(text_vectors, axis=0) if text_vectors else None

        if course_centroid is not None and text_centroid is not None:
            final_embedding = 0.5 * course_centroid + 0.5 * text_centroid
        elif course_centroid is not None:
            final_embedding = course_centroid
        else:
            final_embedding = text_centroid

        overall_similarities = cosine_similarity(
            [final_embedding], self.course_embeddings
        )[0]

        individual_sims = cosine_similarity(self.course_embeddings, valid_vectors)

        breakdown_col = []
        for row_sims in individual_sims:
            pairs = []
            for label, score in zip(valid_labels, row_sims):
                pairs.append({'name': label, 'score': float(score)})
            pairs.sort(key=lambda x: x['score'], reverse=True)
            breakdown_col.append(pairs)

        results_df = self.courses_df.copy()
        results_df['similarity_score'] = overall_similarities
        results_df['similarity_breakdown'] = breakdown_col

        input_course_ids = [x['value'] for x in input_list if x['type'] == 'course']
        results_df = results_df[~results_df['COURSE'].isin(input_course_ids)]

        course_input_indices = [i for i, is_course in enumerate(is_course_input) if is_course]

        if course_input_indices:
            course_sims_matrix = individual_sims[:, course_input_indices]
            max_course_sim = np.max(course_sims_matrix, axis=1)

            is_duplicate_mask = max_course_sim >= 0.99
            results_df = results_df[~is_duplicate_mask[results_df.index]]

        results_df = results_df.sort_values('similarity_score', ascending=False)

        if return_all_ranked:
            return results_df
        return results_df.head(n_recommendations)


class FilterRecommendations:
    """Filtering methods for CourseRecommender"""
    def __init__(self, eager_load=False):
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

        # --- ONNX CHANGE: Check model availability before fitting ---
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