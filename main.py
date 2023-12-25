import logging
import sys

# Canvas API Python wrapper
from canvasapi import Canvas

# Functions and constants defined in other modules
from grade_calculator import compute_course_grade
from config import API_KEY, API_URL


def main():

    # Set up logging
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler('requests.log')
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

    logger = logging.getLogger("canvasapi")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Initialize a new Canvas object
    canvas = Canvas(API_URL, API_KEY)

    # Compute the course grade
    print(compute_course_grade(canvas))


if __name__ == "__main__":
    main()
