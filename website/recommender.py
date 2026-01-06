import re
import pandas as pd
from flask import Blueprint, render_template, request, jsonify
import traceback

# Import your recommendation class
from website.recommend_utils import FilterRecommendations
# Import the data source that contains the detailed course stats
from website.context_dicts import data
from .search import submit_search_field

recommender = Blueprint('recommender', __name__)

# Module-level singleton for the recommendation system
_recommendation_filter = None

def get_recommender():
    global _recommendation_filter
    if _recommendation_filter is None:
        print("Initializing recommendation system...")
        _recommendation_filter = FilterRecommendations()
    return _recommendation_filter


@recommender.route('/recommender', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))
    return render_template('recommender.html')


@recommender.route('/recommender_v1', methods=['GET', 'POST'])
def index_v1():
    """Route for the V1 version of the recommender interface"""
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))
    return render_template('recommender_v1.html')

@recommender.route('/recommender_v2', methods=['GET', 'POST'])
def index_v2():
    """Route for the V1 version of the recommender interface"""
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))
    return render_template('recommender_v2.html')


@recommender.route('/search_courses', methods=['GET'])
def search_courses():
    """Search for courses by ID or name"""
    try:
        rec = get_recommender()
        query = request.args.get('query', '').strip().upper()

        if not query or len(query) < 1:
            return jsonify({'success': True, 'results': []})

        df = rec.recommender.courses_df

        mask = (
            df['COURSE'].str.contains(query, case=False, na=False) |
            df['NAME'].str.contains(query, case=False, na=False) |
            df['DANISH_NAME'].str.contains(query, case=False, na=False)
        )

        matches = df[mask].head(20)

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


@recommender.route('/extract_courses', methods=['POST'])
def extract_courses():
    """Extract course codes from raw text"""
    try:
        rec = get_recommender()
        data_req = request.json
        raw_text = data_req.get('text', '')

        potential_codes = re.findall(r'\b\d{5}\b', raw_text)
        valid_courses = set(rec.recommender.courses_df['COURSE'].tolist())

        found_courses = []
        seen = set()

        for code in potential_codes:
            if code in valid_courses and code not in seen:
                course_information = rec.recommender.courses_df[
                    rec.recommender.courses_df['COURSE'] == code
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


@recommender.route('/recommend', methods=['POST'])
def recommend():
    try:
        rec = get_recommender()
        req_data = request.json

        # Expecting a list of mixed items now
        # Format: [{'type': 'course', 'value': '01005'}, {'type': 'text', 'value': 'biology'}]
        basket_items = req_data.get('basket_items', [])

        # Backward compatibility: If basket is empty, check for old inputs and convert them
        if not basket_items:
            old_ids = req_data.get('course_ids', [])
            old_text = req_data.get('text_input', '')

            if old_ids:
                if isinstance(old_ids, str):
                    old_ids = [c.strip().upper() for c in old_ids.split(',') if c.strip()]
                for c in old_ids:
                    basket_items.append({'type': 'course', 'value': c})

            if old_text:
                basket_items.append({'type': 'text', 'value': old_text})

        if not basket_items:
            return jsonify({'success': False, 'error': 'Please add courses or text description to your basket'})

        filters = req_data.get('filters', {})
        filter_criteria = {k: v for k, v in filters.items() if v}
        number_of_recommendations = int(req_data.get('n_recommendations', 9001))

        # Use the new hybrid method directly from the inner recommender class
        all_recommendations = rec.recommender.recommend_hybrid(
            basket_items,
            return_all_ranked=True
        )

        if all_recommendations.empty:
            return jsonify({'success': True, 'recommendations': [], 'message': 'No courses found matching criteria.'})

        # Apply filters manually since we bypassed the wrapper class method
        if filter_criteria:
            allowed_courses = rec.apply_filters(filter_criteria)
            if allowed_courses:
                all_recommendations = all_recommendations[all_recommendations['COURSE'].isin(allowed_courses)]
            else:
                # Filters resulted in 0 allowed courses
                return jsonify({'success': True, 'recommendations': [], 'message': 'Filters excluded all results.'})

        # Slice the results
        recommendations = all_recommendations.head(number_of_recommendations)

        # --- Formatting Logic ---
        global_data = data()
        results = []
        for _, row in recommendations.iterrows():
            cid = row['COURSE']

            # Clean description
            description = row['COURSE_DESCRIPTION']
            if pd.isna(description) or description in ("None", "NO_DATA"):
                description = "No description available"
            else:
                description = re.sub(r'<[^>]+>', ' ', str(description))
                description = ' '.join(description.split())

            # Helper to safely extract data from the global dict
            def get_stat(category, default=""):
                try:
                    if hasattr(global_data, 'get'):
                        cat_dict = global_data.get(category)
                    else:
                        cat_dict = getattr(global_data, category, None)

                    if cat_dict and cid in cat_dict:
                        return cat_dict[cid]
                    return default
                except:
                    return default

            # Build the rich result object
            results.append({
                'course_id': cid,
                'name': row['NAME'],
                # Pass the breakdown list to the frontend
                'similarity_breakdown': row.get('similarity_breakdown', []),
                'ects': row['ECTS_POINTS'],
                'institute': row['INSTITUTE'],
                'description': description[:200] + '...' if len(description) > 200 else description,
                'responsible': get_stat('responsible', 'NO_DATA'),
                'course_type': get_stat('course_type', ''),
                'language': get_stat('language', ''),
                'season': get_stat('season', ''),
                'schedule': get_stat('schedule', ''),
                'exam': get_stat('exam', ''),
                'signups': get_stat('signups', 0),
                'grade': get_stat('grade', ''),
                'fail': get_stat('fail', 0),
                'rating': get_stat('rating', ''),
                'votes': get_stat('votes', 0),
                'workload': get_stat('workload', ''),
                'rating_tier': get_stat('rating_tier', '0'),
                'workload_tier': get_stat('workload_tier', '0')
            })

        return jsonify({
            'success': True,
            'recommendations': results,
            'basket_items': basket_items,
            'filters_applied': filter_criteria
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})


@recommender.route('/course_info/<course_id>', methods=['GET'])
def course_info(course_id):
    try:
        rec = get_recommender()
        info = rec.recommender.get_course_info(course_id.upper())
        if info:
            return jsonify({'success': True, 'info': info})
        else:
            return jsonify({'success': False, 'error': f'Course {course_id} not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})