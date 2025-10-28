import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import LatentDirichletAllocation
from sentence_transformers import SentenceTransformer
import nltk
from nltk.corpus import stopwords
import re
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.info_consts import InfoConsts


class CourseRecommender:
    """ Text Similarity with Embeddings """
    SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'

    def __init__(self):
        print(f"Loading sentence transformer model: '{CourseRecommender.SENTENCE_TRANSFORMER_MODEL}'")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.course_embeddings = None
        print(f"Loading course data from {FileNameConsts.name_of_pkl}.pkl")
        self.courses_df = CourseRecommender.load_course_data_df()
        print(f"Loaded {len(self.courses_df)} courses")

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

    def fit(self):
        """Fit the model using combined course text"""
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
        # Create embeddings
        self.course_embeddings = self.model.encode(filtered_texts, show_progress_bar=True)
        print(f"Created embeddings for {len(filtered_texts)} courses")

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


# Usage
def main():
    # Initialize recommender
    recommender = CourseRecommender()

    # Analyze a few courses first to see what content we have
    print("Analyzing sample courses:")
    recommender.analyze_course_content('01001')
    recommender.analyze_course_content('01002')

    # Fit the model
    print("\nFitting the model...")
    recommender.fit()

    # Get recommendations based on the math courses from your sample
    print("\nGetting recommendations for math courses 01001 and 01002:")
    recommendations = recommender.recommend_courses(['01001', '01002'], n_recommendations=5)

    # Display results nicely
    recommender.display_recommendations(recommendations)

    # You can also try single course recommendations
    print("\nRecommendations based on just 01001:")
    single_recs = recommender.recommend_courses(['01001'], n_recommendations=3)
    recommender.display_recommendations(single_recs, show_description=False)


if __name__ == "__main__":
    main()