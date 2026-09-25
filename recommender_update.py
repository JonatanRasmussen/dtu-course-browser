

def run_recommender_embeddings_update():
    """Recreate embeddings based on the most recent scraped course data"""
    # Lazy-import here to avoid Crash in main.py if wrong version of dependencies are installed
    # Basically, if this code does not run, it should not prevent the rest of main.py from working
    from website.recommend_utils import CourseRecommender
    print("=== Starting recommender update ===")
    rec = CourseRecommender(eager_load=True)
    rec.fit(force_recreate=True)
    print("=== Recommender update complete ===")

if __name__ == "__main__":
    run_recommender_embeddings_update()