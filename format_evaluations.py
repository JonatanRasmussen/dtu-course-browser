#%%

# Imports
# Helper functions and global constants
from scrape_evaluations import EvalScraper
from utils import Utils
from website.global_constants.config import Config
from website.global_constants.eval_consts import EvalConsts
from website.global_constants.file_name_consts import FileNameConsts

# Initialization
WORKLOAD = EvalConsts.workload
LEARNING = EvalConsts.learning
MOTIVATION = EvalConsts.motivation
FEEDBACK = EvalConsts.feedback
RATING = EvalConsts.rating
SCORE_1 = EvalConsts.score_1
SCORE_2 = EvalConsts.score_2
SCORE_3 = EvalConsts.score_3
SCORE_4 = EvalConsts.score_4
SCORE_5 = EvalConsts.score_5
STAR = EvalConsts.star
VOTES = EvalConsts.votes
AVERAGE_SCORE = EvalConsts.average_score
UPVOTE_RATIO = EvalConsts.upvote_ratio
TIER = EvalConsts.tier
NO_EVALUATIONS = EvalConsts.no_evaluations
EVAL_TYPES = [WORKLOAD, LEARNING, MOTIVATION, FEEDBACK, RATING]


class EvalFormatter:

    @staticmethod
    def quick_test_for_debugging_please_ignore():
        """ Do a quick formatting test to see if the code works."""
        course_numbers = ['01001', '02402']  # Example of valid courses for the below semesters
        course_semesters = ['F23', 'E23', 'F24']  # Example of valid semesters
        file_name = ""  # This prevents scraped data from being saved to disk
        df = EvalScraper.scrape_evaluations(course_numbers, course_semesters, file_name)
        iteration_count = 0
        for course in course_numbers:
            scraped_evals = df.loc[course].to_dict()
            formatted_evals = EvalFormatter.format_evaluations(scraped_evals, course_semesters)
            print(formatted_evals)
            Utils.display_progress(iteration_count, course, FileNameConsts.eval_format, 200)
            iteration_count += 1 # iteration_count must be incremented AFTER display progress

    @staticmethod
    def format_evaluations(scraped_evals, course_semesters):
        """Return formatted scraped evaluations and calculate statistics"""
        # Initialization
        course_eval_raw = {}
        for k in range (0, len(EVAL_TYPES)):
            course_eval_raw[EVAL_TYPES[k]] = {SCORE_1: 0, SCORE_2: 0, SCORE_3: 0, SCORE_4: 0, SCORE_5: 0}
        course_evaluations = {}
        semester_evaluations = {}

        # Loop through all possible semester and evaluation combinations
        for i in range (0, len(course_semesters)):
            semester_eval_raw = {}
            semester_eval_raw[RATING] = {SCORE_1: 0, SCORE_2: 0, SCORE_3: 0, SCORE_4: 0, SCORE_5: 0}
            for j in range (0, len(EVAL_TYPES)):
                if EVAL_TYPES[j] != RATING:
                    semester_eval_raw[EVAL_TYPES[j]] = {SCORE_1: 0, SCORE_2: 0, SCORE_3: 0, SCORE_4: 0, SCORE_5: 0}
                    # Sum up data from scraped_evaluation_dict and
                    # add it to course_evaluations and semester_evaluations
                    key = course_semesters[i]+'_'+EVAL_TYPES[j]
                    if (key in scraped_evals) and (scraped_evals[key] is not None):
                        eval_data = scraped_evals[key]
                        for k in range (0, len(eval_data)):
                            semester_eval_raw[EVAL_TYPES[j]][str(k+1)] += eval_data[k]
                            course_eval_raw[EVAL_TYPES[j]][str(k+1)] += eval_data[k]
                            if EVAL_TYPES[j] != WORKLOAD:
                                semester_eval_raw[RATING][str(k+1)] += eval_data[k]
                                course_eval_raw[RATING][str(k+1)] += eval_data[k]

                # Merge renamed data and statistics for each eval type into one dict
                semester_eval_stats = EvalFormatter.create_statistics_dict(semester_eval_raw[EVAL_TYPES[j]], course_semesters[i]+'_'+EVAL_TYPES[j]+'_')
                semester_evaluations = {**semester_evaluations, **semester_eval_stats}
                semester_eval_raw[EVAL_TYPES[j]] = Utils.rename_dict_keys(semester_eval_raw[EVAL_TYPES[j]], course_semesters[i]+'_'+EVAL_TYPES[j]+'_', '_'+STAR)
                semester_evaluations = {**semester_evaluations, **semester_eval_raw[EVAL_TYPES[j]]}

        for j in range (0, len(EVAL_TYPES)):
            # Merge raw data and statistics for entire course into one dict
            course_eval_stats = EvalFormatter.create_statistics_dict(course_eval_raw[EVAL_TYPES[j]], EVAL_TYPES[j]+'_')
            course_evaluations = {**course_evaluations, **course_eval_stats}
            course_eval_raw[EVAL_TYPES[j]] = Utils.rename_dict_keys(course_eval_raw[EVAL_TYPES[j]], EVAL_TYPES[j]+'_', '_'+STAR)
            course_evaluations = {**course_evaluations, **course_eval_raw[EVAL_TYPES[j]]}

        # Merge semester-specific and non-semester-specific data into one dict
        evaluations = {**course_evaluations, **semester_evaluations}

        return evaluations

    @staticmethod
    def find_evaluation_average(eval_dct):
        """Calculate and return averages for evaluations in a dict"""

        # Count scores and weight them (1-star ratings = *1, 5-star = *5)
        evaluation_weighted = 0
        votes = sum(eval_dct.values())
        for i in range (0, len(eval_dct)):
            evaluation_weighted += eval_dct[str(i+1)] * (i+1)

        # Find average (don't divide by 0)
        if votes == 0:
            evaluation_average = NO_EVALUATIONS
        else:
            # true_average is a number between 1-5 (center value is 3)
            evaluation_average = float(evaluation_weighted / votes)

            """ # THE FOLLOWING CODE HAS BEEN DISABLED DUE TO MAKING DATA MISLEADING
            # For workload, the deviation from center value 3 is exaggerated (up to a factor 2)
            # The scores 2.9 and 3.1 are converted to ~2.8 and ~3.2 (factor 1.95 because they are close to center value 3)
            # The scores 2.0 and 4.0 are converted to 1.5 and 4.5 (factor 1.5 because they are far from center value 3)
            # The scores 1.0 and 5.0 are unchanged (factor 1 because 1 must be minimum and 5 must be maximum)
            if eval_type == EvalConsts.workload:
                # deviation_factor is a number between 1 and 2
                deviation_factor = float(2 - (abs((evaluation_average - 3) / 2)))
                converted_average = float((evaluation_average - 3) * deviation_factor)
                evaluation_average = 3 + converted_average
            #evaluation_average = round(float(((evaluation_weighted / votes) - 3) * low_sample_size_factor + 3), 2)
            """

            # Finally, we round the value to 2 decimal places
            evaluation_average = round(evaluation_average, Config.data_decimal_precision)

        return evaluation_average

    @staticmethod
    def evaluation_upvotes(eval_dct):
        """Return percentage of students that rated positive / negative"""

        # Calculate likes / dislikes
        MINOR_UPVOTE = SCORE_4
        MAJOR_UPVOTE = SCORE_5
        number_of_votes = sum(eval_dct.values())
        positive_evaluations = eval_dct[MINOR_UPVOTE] + eval_dct[MAJOR_UPVOTE]
        if number_of_votes != 0:
            upvote_ratio = round(float(positive_evaluations / number_of_votes), 1)
        else:
            upvote_ratio = NO_EVALUATIONS
        return upvote_ratio

    @staticmethod
    def decide_group(average_score):
        """Put average_score into a group between 0 and 9"""
        tier = 0
        if average_score == NO_EVALUATIONS:
            tier  = 0
        elif average_score < 1.25:
            tier  = 1
        elif average_score < 1.75:
            tier  = 2
        elif average_score < 2.25:
            tier = 3
        elif average_score < 2.75:
            tier = 4
        elif average_score < 3.25:
            tier = 5
        elif average_score < 3.75:
            tier = 6
        elif average_score < 4.25:
            tier = 7
        elif average_score < 4.75:
            tier = 8
        else:
            tier = 9
        return tier


    @staticmethod
    def create_statistics_dict(eval_dct, semester_and_q):
        """Merge average evaluation and percentages into stat_dict"""
        votes = sum(eval_dct.values())
        average_score = EvalFormatter.find_evaluation_average(eval_dct)
        upvote_ratio = EvalFormatter.evaluation_upvotes(eval_dct)
        tier = EvalFormatter.decide_group(average_score)
        stat_dict = {semester_and_q+VOTES: votes, semester_and_q+AVERAGE_SCORE: average_score, semester_and_q+UPVOTE_RATIO: upvote_ratio, semester_and_q+TIER: tier}
        return stat_dict


#%%

if __name__ == "__main__":
    EvalFormatter.quick_test_for_debugging_please_ignore()
