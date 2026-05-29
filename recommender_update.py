from website.recommend_utils import CourseRecommender

def run_recommender_embeddings_update():
    """Recreate embeddings based on the most recent scraped course data"""
    print("=== Starting recommender update ===")
    rec = CourseRecommender(eager_load=True)
    rec.fit(force_recreate=True)
    print("=== Recommender update complete ===")

if __name__ == "__main__":
    run_recommender_embeddings_update()