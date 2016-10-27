
#import spacy
#en_model = spacy.load('en')


"""

book an appointment tomorrow from 5pm to 5:30pm
put a meeting on 5th july from 8am to 8:30
place an appointment for this sunday from 5pm for 30 minutes
place a meeting appointment next sunday with Xman about
put an HR call for interview, tomorrow 10am to 11am

- proper nouns
- followed by 'for, 'with, 'about, 'related to
- remove stop words
- remove nums, puncts etc.

"""


def get_title(text):
    """
    A function that takes some
     text and creates a title by
     extracting keywords using pos
     tags an context words
    """
    #doc = en_model(text)
    return "Yahhoo"


def main():
    pass

if __name__ == u"__main__":
    main()
