import json
import pandas as pd
from website.global_constants.website_consts import WebsiteConsts
from website.global_constants.file_name_consts import FileNameConsts
from recommend_courses import CourseRecommender


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


def main():
    # Initialize
    recommendation_filter = FilterRecommendations()

    # Example 0: See what filter options are available
    print("\n" + "="*80)
    print("Available filter options:")
    print("="*80)
    filter_options = recommendation_filter.get_available_filter_options()
    for category, values in filter_options.items():
        print(f"{category}: {values}")

    # Example 1: Apply filters only (no recommendations)
    print("\n" + "="*80)
    print("Example 1: Filtering courses")
    print("="*80)
    filter_criteria = {
        "language": ["eng"],
        "gradetype": ["passfail"]
    }
    filtered_courses = recommendation_filter.apply_filters(filter_criteria)
    print(f"Found {len(filtered_courses)} courses matching criteria")
    print(f"Sample courses: {list(filtered_courses)[:10]}")

    # Example 2: Get recommendations WITH filters
    print("\n" + "="*80)
    print("Example 2: Filtered recommendations based on courses")
    print("="*80)
    input_courses = ['01001', '01002']
    filter_criteria = {
        "language": ["eng"],
         "course_type": ["bsc"]
    }
    recommendations = recommendation_filter.get_filtered_recommendations(
        input_courses,
        filter_criteria=filter_criteria,
        n_recommendations=10
    )
    print("\nFiltered Recommendations:")
    recommendation_filter.recommender.display_recommendations(recommendations, show_description=False)

    # Example 3: Get recommendations WITHOUT filters
    print("\n" + "="*80)
    print("Example 3: Unfiltered recommendations")
    print("="*80)
    unfiltered_recommendations = recommendation_filter.get_filtered_recommendations(
        input_courses,
        filter_criteria=None,
        n_recommendations=5
    )
    print("\nUnfiltered Recommendations:")
    recommendation_filter.recommender.display_recommendations(unfiltered_recommendations, show_description=False)

    # Example 4: Get course details for filtered courses
    print("\n" + "="*80)
    print("Example 4: Get detailed course info for filtered courses")
    print("="*80)
    filter_criteria = {
        "language": ["dk"],
        "gradetype": ["sevenstep"]
    }
    courses_df = recommendation_filter.get_courses_by_filters(filter_criteria)
    print(f"\nFound {len(courses_df)} courses:")
    if not courses_df.empty:
        print(courses_df[['COURSE', 'NAME', 'ECTS_POINTS']].head(10))

    # Example 5: Simple filtering
    print("Example 5: Apply simple filtering")
    filter_criteria = {
        "language": ["eng"],
        "gradetype": ["passfail", "sevenstep"]
    }
    matching_courses = recommendation_filter.apply_filters(filter_criteria)
    if len(matching_courses) > 10:
        print(list(matching_courses)[:10])
    else:
        print(list(matching_courses))

    # Example 6: Filtered recommendations
    print("Example 6: Perform filtered recommendations")
    recommendations = recommendation_filter.get_filtered_recommendations(
        input_course_ids=['01001', '01002'],
        filter_criteria={"language": ["eng"], "course_type": ["bsc"]},
        n_recommendations=6
    )

if __name__ == "__main__":
    main()