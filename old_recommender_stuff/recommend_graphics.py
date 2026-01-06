import re
import pandas as pd
from flask import Flask, render_template, request, jsonify
from recommend_filtering import FilterRecommendations
import traceback

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='/')
HTML_TEMPLATE_NAME = 'recommender.html'
print("Initializing recommendation system...")
recommendation_filter = None

def get_recommender():
    global recommendation_filter
    if recommendation_filter is None:
        recommendation_filter = FilterRecommendations()
    return recommendation_filter

@app.route('/')
def index():
    return render_template(HTML_TEMPLATE_NAME)

@app.route('/search_courses', methods=['GET'])
def search_courses():
    """Search for courses by ID or name"""
    try:
        recommender = get_recommender()
        query = request.args.get('query', '').strip().upper()

        if not query or len(query) < 2:
            return jsonify({'success': True, 'results': []})

        df = recommender.recommender.courses_df

        # Search by course ID or name
        mask = (
            df['COURSE'].str.contains(query, case=False, na=False) |
            df['NAME'].str.contains(query, case=False, na=False) |
            df['DANISH_NAME'].str.contains(query, case=False, na=False)
        )

        matches = df[mask].head(20)  # Limit to 20 results

        results = []
        for _, row in matches.iterrows():
            results.append({
                'course_id': row['COURSE'],
                'name': row['NAME'],
                'danish_name': row.get('DANISH_NAME', ''),
                'language': row.get('LANGUAGE', ''),
                'ects': row.get('ECTS_POINTS', '')
            })

        return jsonify({'success': True, 'results': results})

    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/extract_courses', methods=['POST'])
def extract_courses():
    """Extract course codes from raw text"""
    try:
        recommender = get_recommender()
        data = request.json
        raw_text = data.get('text', '')

        # Find all 5-digit sequences
        potential_codes = re.findall(r'\b\d{5}\b', raw_text)

        # Get valid course codes from dataframe
        valid_courses = set(recommender.recommender.courses_df['COURSE'].tolist())

        # Filter to only valid courses
        found_courses = []
        seen = set()

        for code in potential_codes:
            if code in valid_courses and code not in seen:
                course_information = recommender.recommender.courses_df[
                    recommender.recommender.courses_df['COURSE'] == code
                ].iloc[0]

                found_courses.append({
                    'course_id': code,
                    'name': course_information['NAME']
                })
                seen.add(code)

        return jsonify({
            'success': True,
            'courses': found_courses,
            'count': len(found_courses)
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        recommender = get_recommender()
        data = request.json
        course_ids = data.get('course_ids', [])

        if isinstance(course_ids, str):
            course_ids = [c.strip().upper() for c in course_ids.split(',') if c.strip()]

        if not course_ids:
            return jsonify({'success': False, 'error': 'Please select at least one course'})

        filters = data.get('filters', {})
        filter_criteria = {k: v for k, v in filters.items() if v}
        number_of_recommendations = int(data.get('n_recommendations', 100))

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
        for _, row in recommendations.iterrows():
            description = row['COURSE_DESCRIPTION']
            if pd.isna(description) or description == "None" or description == "NO_DATA":
                description = "No description available"
            else:
                description = re.sub(r'<[^>]+>', ' ', str(description))
                description = ' '.join(description.split())

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
    print("Pre-loading recommendation system...")
    get_recommender()
    print("Ready!")
    app.run(debug=True, port=5000)