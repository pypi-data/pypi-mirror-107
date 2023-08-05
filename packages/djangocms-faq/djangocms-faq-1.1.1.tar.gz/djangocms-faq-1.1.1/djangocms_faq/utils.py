from django.utils.text import slugify

from .settings import ENABLE_FUZZY_SEARCH, FUZZY_SEARCH_PERCENTAGE


if ENABLE_FUZZY_SEARCH:
    try:
        # use fuzzy search, keep setting to True
        from fuzzywuzzy import fuzz
    except ImportError:
        # can't find package, set setting to False and print error
        print(
            "WARNING: Var DJANGOCMS_FAQ_ENABLE_FUZZY_SEARCH is set to True in your project's settings, but your installation of Python can't find the package fuzzywuzzy.\nHave you tried to install the package using \"python3 -m pip install djangocms_faq[fuzzy_search]\"?\nNot using fuzzy search for this time..."
        )
        ENABLE_FUZZY_SEARCH = False


from djangocms_faq.models import QuestionFaqPluginModel


def get_answers(query, search_in):

    if not len(query):
        return

    query = slugify(query)  # replace "AuJoürd'hui" by "aujourd-hui"

    if ENABLE_FUZZY_SEARCH:
        print("fuzzy search")
        query = slugify(query).replace(
            "-", " "
        )  # replace "AuJoürd'hui" by "aujourd hui"

    answers_questions = []
    answers_keywords = []

    # get questions
    questions = QuestionFaqPluginModel.objects.exclude(
        placeholder__page__publisher_is_draft=True
    ).filter(parent__id__in=[id for id in search_in.split()])

    # get keywords
    for question in questions:
        # str is found in question title

        if ENABLE_FUZZY_SEARCH:
            slug = slugify(question.question).replace("-", " ")
            # print(query + " - " + slug + " =>", end="")
            # print((30 - (len(query + " - " + slug))) * " " + str(fuzz.token_sort_ratio(query, slug)))
            if (
                fuzz.token_sort_ratio(query, slug)
                >= FUZZY_SEARCH_PERCENTAGE  # see https://github.com/seatgeek/fuzzywuzzy#token-sort-ratio
            ) or (query in slug):
                answers_questions.append(question)
        else:
            if query in slugify(question.question):
                answers_questions.append(question)

        # str is found in keywords
        for keyword in question.keywords.all():
            if ENABLE_FUZZY_SEARCH:
                slug = slugify(keyword).replace("-", " ")
                # print("  " + query + " - " + slug + " =>", end="")
                # print((28 - (len(query + " - " + slug))) * " " + str(fuzz.token_sort_ratio(query, slug)))
                if fuzz.token_sort_ratio(query, slug) >= FUZZY_SEARCH_PERCENTAGE:
                    answers_keywords.append(question)
            else:
                if query in slugify(keyword):
                    answers_keywords.append(question)

    # all answers
    answers = answers_questions + answers_keywords

    # get unique values
    answers = list(set(answers))

    return answers
