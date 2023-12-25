# Canvas API Python wrapper
from canvasapi import Canvas, exceptions

# Regular expressions used to retrieve correct assignments
import re

# Flags information
from config import FLAGS


def compute_course_grade(canvas: Canvas):
    """
    Compute the grade for the Ethical Hacking course.
    :param canvas: Canvas object
    :return: grade A-F
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

    # Course grade before being ranged A-F
    score = 0

    # Retrieve the flag assignments with correct submissions and increase the grade accordingly
    for assignment in course.get_assignments(include=['submission']):
        match = re.match(r'^Capturing Flag ([a-fA-F0-9]+)', assignment.name)
        if match and assignment.has_submitted_submissions:
            flag = FLAGS[match.group(1)]
            match = re.search(r'{(.*?)}', assignment.submission['body'])
            if match:
                content = match.group(1)
                if content == flag['value']:
                    score += assignment.points_possible

    # Retrieve the hints user has requested and corresponding decrease value
    hints = {}
    for group in user.get_groups():
        match = re.match(r'^Flag ([0-9a-fA-F]{6}) Hint (\d+$)', group.name)
        if match:
            flag = FLAGS[match.group(1)]
            hint_number = int(match.group(2))
            hint_value = flag['hints'][hint_number - 1]

            # If hint is the last one, decrease the grade by the whole flag value
            if hint_number == len(flag['hints']):
                hints[flag['value']] = hint_value
            else:
                hints[flag['value']] = hints.get(flag['value'], 0) + hint_value

    # Decrease the grade
    for hint_value in hints.values():
        score -= hint_value

    return assign_grade(score)


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
