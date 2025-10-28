import re
import pandas as pd
from flask import Flask, render_template, request, jsonify
from recommend_filtering import FilterRecommendations
import traceback

app = Flask(__name__, template_folder='.')

# Initialize the recommendation system (this will take a moment on startup)
print("Initializing recommendation system...")
recommendation_filter = None

def get_recommender():
    global recommendation_filter
    if recommendation_filter is None:
        recommendation_filter = FilterRecommendations()
    return recommendation_filter

@app.route('/')
def index():
    return render_template('recommender.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        recommender = get_recommender()  # Fixed bug here - was app.recommender
        data = request.json
        course_ids = [c.strip().upper() for c in data.get('course_ids', '').split(',') if c.strip()]  # Parse input courses
        if not course_ids:
            return jsonify({'success': False, 'error': 'Please enter at least one course ID'})
        filters = data.get('filters', {})  # Parse filters
        filter_criteria = {k: v for k, v in filters.items() if v}
        number_of_recommendations = int(data.get('n_recommendations', 10))

        # Get recommendations
        if filter_criteria:
            recommendations = recommender.get_filtered_recommendations(
                course_ids,
                filter_criteria=filter_criteria,
                n_recommendations=number_of_recommendations
            )
        else:
            recommendations = recommender.get_filtered_recommendations(
                course_ids,
                filter_criteria=None,
                n_recommendations=number_of_recommendations
            )

        results = []
        # Convert to list of dicts for JSON serialization
        for _, row in recommendations.iterrows():
            description = row['COURSE_DESCRIPTION']
            if pd.isna(description) or description == "None" or description == "NO_DATA":
                description = "No description available"
            else:
                description = re.sub(r'<[^>]+>', ' ', str(description))  # Remove HTML tags
                description = ' '.join(description.split())  # Remove extra whitespace

            results.append({
                'course_id': row['COURSE'],
                'name': row['NAME'],
                'similarity': f"{row['similarity_score']:.3f}",
                'ects': row['ECTS_POINTS'],
                'institute': row['INSTITUTE'],
                'description': description[:200] + '...' if len(description) > 200 else description
            })

        return jsonify({
            'success': True,
            'recommendations': results,
            'input_courses': course_ids,
            'filters_applied': filter_criteria
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/course_info/<course_id>', methods=['GET'])
def course_info(course_id):
    try:
        recommender = get_recommender()
        info = recommender.recommender.get_course_info(course_id.upper())
        if info:
            return jsonify({'success': True, 'info': info})
        else:
            return jsonify({'success': False, 'error': f'Course {course_id} not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Initialize on startup
    print("Pre-loading recommendation system...")
    get_recommender()
    print("Ready!")
    app.run(debug=True, port=5000)