# Canvas API Python wrapper
from canvasapi import Canvas, exceptions

# Regular expressions used to retrieve correct assignments
import re

# Flags information
from config import FLAGS


def compute_course_grade(canvas: Canvas):
    """
    Compute the grade for the Ethical Hacking course, and print a summary in the standard output.
    :param canvas: Canvas object to use for API calls
    """
    # Ethical Hacking course - ID 41678
    try:
        course = canvas.get_course(41678)
    except exceptions.Forbidden:
        print("You are not enrolled in the course.")
        return
    except exceptions.InvalidAccessToken:
        print("Invalid access token.")
        return

    # User corresponding to given API key
    user = canvas.get_current_user()

    # Flags found and their corresponding scores
    scores = {}

    # Retrieve the flag assignments with correct submissions and set the scores to flag value
    for assignment in course.get_assignments(include=['submission']):
        match = re.match(r'^Capturing Flag ([a-fA-F0-9]{6})', assignment.name)
        if match and assignment.has_submitted_submissions:
            flag_name = match.group(1)
            flag = FLAGS[flag_name]
            if flag['value'] in assignment.submission['body']:
                scores[flag_name] = assignment.points_possible

    max_score = sum(scores.values())

    # Retrieve the hints user has requested and decrease the corresponding scores
    nb_hints = 0
    for group in user.get_groups():
        match = re.match(r'^Flag ([0-9a-fA-F]{6}) Hint (\d+$)', group.name)
        if match:
            flag_name = match.group(1)
            hint_number = int(match.group(2))
            if flag_name in scores:
                nb_hints += 1
                flag = FLAGS[flag_name]
                hint_value = flag['hints'][hint_number - 1]
                scores[flag_name] = max(0, scores[flag_name] - hint_value)

    score = sum(scores.values())

    print(f"My grade on the course is currently {assign_grade(score)}. This corresponds to a score of"
          f" {int(score)}/{int(max_score)}. I submitted {len(scores)} flags, and I requested {nb_hints} hints.")


def assign_grade(score: int):
    """
    Assign a correct grade A-F to a given score in the Ethical Hacking course.
    :param score: score on the course between 0 and 180
    :return: grade A-F
    """
    if 0 <= score <= 180:
        if score >= 162:
            return 'A'
        elif score >= 126:
            return 'B'
        elif score >= 90:
            return 'C'
        elif score >= 54:
            return 'D'
        elif score >= 36:
            return 'E'
        else:
            return 'F'
    else:
        return 'Invalid score'
