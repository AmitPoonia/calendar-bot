from toolz import compose
from dialogue_domain import *
from dialogue_extraction import get_entities


def get_user_input(state):
    """
    This function takes the user
    input from console if session is
    not over in given state
    """
    if state[u"session_over"] is False:
        user_input = raw_input(u"You: ")
        state[u"text"] = user_input
    return state


def get_input_entities(state):
    """
    Takes a state and updates it based
    on information/entities extracted from
    the user input
    """
    if state[u"text"] is not None:
        state = get_entities(state)
    return state


def check_completeness(state):
    """
    A function that check if values for
    required fields for an appointment
    has been supplied by user, if not
    prompts a response for missing values
    """
    print state
    pending = []
    msg = u"Please give details for following field(s): "
    if state[u"intent"] in [u"create_booking", u"edit_booking", u"yes"]:
        if state[u"title"] is None:
            pending.append(u"title")
        if state[u"start"] is None:
            pending.append(u"start")
        if state[u"end"] is None:
            pending.append(u"end")
    if pending != []:
        state[u"response"] = msg + ', '.join(pending)
    return state


def get_response(state):
    """
    This functionas takes a state and
    returns the response using a composition
    of domain specific intent functions where
    only one of the function changes the state
    by giving a response, depending on the intent
    """
    responders = compose(show, confusion, intro,
                         outro, no, thanking,
                         yes, restart, outofscope,
                         help, create_booking)
    return responders(state)


def reply(state):
    """
    This takes the state and print
    whatever response it carries to
    the console/user, resets few flags
    and closes the session if necessary
    """
    print state[u"response"]
    state[u"response"] = None
    state[u"intent"] = None
    if state[u"persist"] is True:
        state[u"session_over"] = True
    return state

understand = compose(reply,
                     get_response,
                     check_completeness,
                     get_input_entities,
                     get_user_input)


def talk(state):
    """
    The main function which recursively
    handles the conversation, using composition
    of main set of functions to process the dialogues
    runs until session flag is True.
    """
    new_state = understand(state)
    if new_state[u"session_over"] is True:
        print u" --- This session is over ---"
    else:
        talk(new_state)


def main():
    print welcome_message
    talk(zero_state)


if __name__ == u"__main__":
    main()
