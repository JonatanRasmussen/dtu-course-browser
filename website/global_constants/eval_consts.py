

class EvalConsts:
    learning = 'LEARNING'
    motivation = 'MOTIVATION'
    feedback = 'FEEDBACK'
    workload = 'WORKLOAD'
    list_of_evals = [learning, motivation, feedback, workload]
    rating = 'RATING'
    score_1 = "1"
    score_2 = "2"
    score_3 = "3"
    score_4 = "4"
    score_5 = "5"
    star = "STAR"
    votes = "VOTES"
    average_score = "AVERAGE_SCORE"
    upvote_ratio = "UPVOTE_RATIO"
    tier = "TIER"
    no_evaluations = "No data"
    # Concatenations
    rating_tier = rating+'_'+tier
    learning_tier = learning+'_'+tier
    motivation_tier = motivation+'_'+tier
    feedback_tier = feedback+'_'+tier
    workload_tier = workload+'_'+tier
    rating_average_score = rating+'_'+average_score
    learning_average_score = learning+'_'+average_score
    motivation_average_score = motivation+'_'+average_score
    feedback_average_score = feedback+'_'+average_score
    workload_average_score = workload+'_'+average_score
    rating_votes = rating+'_'+votes
    learning_votes = learning+'_'+votes
    motivation_votes = motivation+'_'+votes
    feedback_votes = feedback+'_'+votes
    workload_votes = workload+'_'+votes
    workload_1_star = workload+'_'+score_1+'_'+star
    workload_2_star = workload+'_'+score_2+'_'+star
    workload_3_star = workload+'_'+score_3+'_'+star
    workload_4_star = workload+'_'+score_4+'_'+star
    workload_5_star = workload+'_'+score_5+'_'+star