#recommender.py
import re
import pandas as pd
from flask import Blueprint, render_template, request, jsonify
import traceback

# Import your recommendation class
from website.recommend_utils import FilterRecommendations
# Import the data source that contains the detailed course stats
from website.context_dicts import data, load_dct_from_json_file
from website.global_constants.info_consts import InfoConsts
from website.global_constants.file_name_consts import FileNameConsts
from .search import submit_search_field

recommender = Blueprint('recommender', __name__)
ENABLE_EAGER_LOADING = True  #Lazyload toggle

# Module-level singleton for the recommendation system
_recommendation_filter = None
_historical_courses_cache = None
_extended_df_cache = None

def get_historical_courses():
    """Helper to lazily load and cache historical course IDs from cv_helper.json"""
    global _historical_courses_cache
    if _historical_courses_cache is None:
        cv_dict = load_dct_from_json_file(FileNameConsts.cv_helper_json)
        _historical_courses_cache = set(cv_dict.keys()) if cv_dict else set()
    return _historical_courses_cache

def get_extended_df():
    """Helper to lazily load and cache the extended dataframe containing study lines"""
    global _extended_df_cache
    if _extended_df_cache is None:
        try:
            path = FileNameConsts.pythonanywherecom_path_of_pkl + FileNameConsts.extended_pkl_name + ".pkl"
            _extended_df_cache = pd.read_pickle(path)
        except FileNotFoundError:
            path = FileNameConsts.path_of_pkl + FileNameConsts.extended_pkl_name + ".pkl"
            _extended_df_cache = pd.read_pickle(path)
    return _extended_df_cache

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
    study_lines = sorted(InfoConsts.study_lines.values_raw)
    return render_template('recommender.html', study_lines=study_lines)


@recommender.route('/recommender_v1', methods=['GET', 'POST'])
def index_v1():
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))
    study_lines = sorted(InfoConsts.study_lines.values_raw)
    return render_template('recommender_v1.html', study_lines=study_lines)

@recommender.route('/recommender_v2', methods=['GET', 'POST'])
def index_v2():
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))
    study_lines = sorted(InfoConsts.study_lines.values_raw)
    return render_template('recommender_v2.html', study_lines=study_lines)


@recommender.route('/search_courses', methods=['GET'])
def search_courses():
    """Search for courses by ID or name"""
    try:
        rec = get_recommender()
        query = request.args.get('query', '').strip().upper()
        include_historical = request.args.get('include_historical', 'false').lower() == 'true'

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
                'ects': row.get('ECTS_POINTS', ''),
                'is_historical': False
            })

        # If requested, check if the exact 5-digit query is a historical course
        if include_historical and len(query) == 5 and query.isdigit():
            if not any(r['course_id'] == query for r in results):
                hist_courses = get_historical_courses()
                if query in hist_courses:
                    results.append({
                        'course_id': query,
                        'name': '(Course no longer exists)',
                        'danish_name': '',
                        'language': '',
                        'ects': '',
                        'is_historical': True
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
        hist_courses = get_historical_courses()

        found_courses = []
        seen = set()

        for code in potential_codes:
            if code not in seen:
                if code in valid_courses:
                    course_information = rec.recommender.courses_df[
                        rec.recommender.courses_df['COURSE'] == code
                    ].iloc[0]

                    found_courses.append({
                        'course_id': code,
                        'name': course_information['NAME'],
                        'is_historical': False
                    })
                    seen.add(code)
                elif code in hist_courses:
                    found_courses.append({
                        'course_id': code,
                        'name': '(Course no longer exists)',
                        'is_historical': True
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


@recommender.route('/get_study_line_courses', methods=['POST'])
def get_study_line_courses():
    """Fetch all courses associated with a specific study line"""
    try:
        req_data = request.json
        study_line = req_data.get('study_line')

        if not study_line:
            return jsonify({'success': False, 'error': 'No study line provided'})

        df_ext = get_extended_df()

        if study_line not in df_ext.columns:
            return jsonify({'success': False, 'error': f'Study line "{study_line}" not found in database.'})

        # Filter courses where the study line column is 1
        matches = df_ext[df_ext[study_line] == 1]

        courses = []
        for _, row in matches.iterrows():
            courses.append({
                'course_id': str(row['COURSE']),
                'name': str(row['NAME'])
            })

        return jsonify({'success': True, 'courses': courses})

    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})


@recommender.route('/recommend', methods=['POST'])
def recommend():
    try:
        rec = get_recommender()
        req_data = request.json

        basket_items = req_data.get('basket_items', [])

        if not basket_items:
            return jsonify({'success': False, 'error': 'Please add courses or text description to your basket'})

        filters = req_data.get('filters', {})
        filter_criteria = {k: v for k, v in filters.items() if v}
        number_of_recommendations = int(req_data.get('n_recommendations', 9001))

        # --- INTERCEPT HISTORICAL COURSES ---
        processed_basket = []
        cv_dict = None
        hist_courses = get_historical_courses()
        valid_current_courses = set(rec.recommender.courses_df['COURSE'].tolist())

        for item in basket_items:
            if item['type'] == 'course' and item['value'] not in valid_current_courses:
                if item['value'] in hist_courses:
                    if cv_dict is None:
                        cv_dict = load_dct_from_json_file(FileNameConsts.cv_helper_json)
                    context_text = cv_dict.get(item['value'], '')
                    if context_text:
                        processed_basket.append({
                            'type': 'text',
                            'value': context_text,
                            'label': f"Historical Course {item['value']}"
                        })
                    continue
            processed_basket.append(item)

        # 1. Get Recommendations (using the processed basket)
        all_recommendations = rec.recommender.recommend_hybrid(
            processed_basket,
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

            subsequent_key = InfoConsts.subsequent_courses.key_df
            no_sub_const = InfoConsts.no_subsequent_courses

            for input_id in input_ids:
                matches = df_full[df_full['COURSE'] == input_id]
                if not matches.empty:
                    val = matches.iloc[0].get(subsequent_key)
                    if val and isinstance(val, str) and val != no_sub_const:
                        subs = [s.strip() for s in val.split(',') if s.strip()]
                        unlocked_id_set.update(subs)

            unlocked_id_set = unlocked_id_set - set(input_ids)

            if unlocked_id_set:
                unlocked_rows = df_full[df_full['COURSE'].isin(unlocked_id_set)]
                for _, u_row in unlocked_rows.iterrows():
                    unlocked_courses_data.append({
                        'id': u_row['COURSE'],
                        'name': u_row['NAME']
                    })
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
            'unlocked_courses': unlocked_courses_data,
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


@recommender.route('/cv_helper', methods=['POST'])
def cv_helper():
    """Fetch formatted course context for LLM consumption based on basket items"""
    try:
        req_data = request.json
        course_ids = req_data.get('course_ids', [])

        cv_dict = load_dct_from_json_file(FileNameConsts.cv_helper_json)

        if not cv_dict:
            return jsonify({'success': False, 'error': 'CV Helper data not found on the server.'})

        contexts = []
        for cid in course_ids:
            if cid in cv_dict:
                contexts.append(f"--- Course {cid} ---\n{cv_dict[cid]}")
            else:
                contexts.append(f"--- Course {cid} ---\nNo context available.")

        combined_text = "\n\n".join(contexts)
        return jsonify({'success': True, 'text': combined_text})

    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)})