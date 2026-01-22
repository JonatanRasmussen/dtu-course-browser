#recommender.py
import re
import pandas as pd
from flask import Blueprint, render_template, request, jsonify
import traceback

# Import your recommendation class
from website.recommend_utils import FilterRecommendations
# Import the data source that contains the detailed course stats
from website.context_dicts import data
from website.global_constants.info_consts import InfoConsts
from .search import submit_search_field

recommender = Blueprint('recommender', __name__)
ENABLE_EAGER_LOADING = True  #Lazyload toggle

# Module-level singleton for the recommendation system
_recommendation_filter = None

def init_recommender_system():
    """Helper to initialize the system globally"""
    global _recommendation_filter
    try:
        print(f"--- SERVER STARTUP: Initializing Recommender (Eager Load: {ENABLE_EAGER_LOADING}) ---")
        _recommendation_filter = FilterRecommendations(eager_load=ENABLE_EAGER_LOADING)
        print("--- SERVER STARTUP: System Ready ---")
    except Exception as e:
        print(f"--- SERVER STARTUP FAILED: {e}")
        traceback.print_exc()
        _recommendation_filter = None

# 1. Attempt to initialize immediately when this file is imported (Server Boot)
if ENABLE_EAGER_LOADING:
    init_recommender_system()

def get_recommender():
    global _recommendation_filter
    # 2. Fallback: If it wasn't initialized (or Eager was False), do it now
    if _recommendation_filter is None:
        print("Initializing recommendation system (On-Demand)...")
        _recommendation_filter = FilterRecommendations(eager_load=ENABLE_EAGER_LOADING)
    return _recommendation_filter


@recommender.route('/recommender', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))
    return render_template('recommender.html')


@recommender.route('/recommender_v1', methods=['GET', 'POST'])
def index_v1():
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))
    return render_template('recommender_v1.html')

@recommender.route('/recommender_v2', methods=['GET', 'POST'])
def index_v2():
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

        basket_items = req_data.get('basket_items', [])

        # Backward compatibility
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

        # 1. Get Recommendations
        all_recommendations = rec.recommender.recommend_hybrid(
            basket_items,
            return_all_ranked=True
        )

        if all_recommendations.empty:
            return jsonify({'success': True, 'recommendations': [], 'message': 'No courses found matching criteria.'})

        # 2. Apply Filters
        if filter_criteria:
            allowed_courses = rec.apply_filters(filter_criteria)
            if allowed_courses:
                all_recommendations = all_recommendations[all_recommendations['COURSE'].isin(allowed_courses)]
            else:
                return jsonify({'success': True, 'recommendations': [], 'message': 'Filters excluded all results.'})

        # --- 3. Identify Unlocked / Subsequent Courses ---
        input_ids = [item['value'] for item in basket_items if item['type'] == 'course']
        unlocked_courses_data = []

        if input_ids:
            unlocked_id_set = set()
            df_full = rec.recommender.courses_df

            # Key used in your CsvCreator
            subsequent_key = InfoConsts.subsequent_courses.key_df
            no_sub_const = InfoConsts.no_subsequent_courses

            # Iterate through basket items to find what they unlock
            for input_id in input_ids:
                matches = df_full[df_full['COURSE'] == input_id]
                if not matches.empty:
                    # Get the string "01002, 02003" from the dataframe
                    val = matches.iloc[0].get(subsequent_key)

                    if val and isinstance(val, str) and val != no_sub_const:
                        # Split by comma and clean up
                        subs = [s.strip() for s in val.split(',') if s.strip()]
                        unlocked_id_set.update(subs)

            # Remove courses that are already in the basket (optional but cleaner)
            unlocked_id_set = unlocked_id_set - set(input_ids)

            if unlocked_id_set:
                # Get names for the unlocked IDs
                unlocked_rows = df_full[df_full['COURSE'].isin(unlocked_id_set)]
                for _, u_row in unlocked_rows.iterrows():
                    unlocked_courses_data.append({
                        'id': u_row['COURSE'],
                        'name': u_row['NAME']
                    })

                # Sort by ID
                unlocked_courses_data.sort(key=lambda x: x['id'])

        # 4. Format Results
        recommendations = all_recommendations.head(number_of_recommendations)
        global_data = data()
        results = []
        for _, row in recommendations.iterrows():
            cid = row['COURSE']
            description = row['COURSE_DESCRIPTION']
            if pd.isna(description) or description in ("None", "NO_DATA"):
                description = "No description available"
            else:
                description = re.sub(r'<[^>]+>', ' ', str(description))
                description = ' '.join(description.split())

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

            results.append({
                'course_id': cid,
                'name': row['NAME'],
                'similarity_breakdown': row.get('similarity_breakdown', []),
                'score': float(row['similarity_score']),
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
            'unlocked_courses': unlocked_courses_data, # This list is sent to frontend
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