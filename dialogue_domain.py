from dialogue_db import *

welcome_message = u"Hi I am the calendar bot, what appointment can I make for you?"

zero_state = {u"text": None,
              u"title": None,
              u"start": None,
              u"end": None,
              u"persist": False,
              u"session_over": False,
              u"response": None,
              u"outofscope_count": 0}


def create_booking(state):
    if state[u"intent"] == u"create_booking" and state[u"response"] is None:
        state[u"response"] = u"your booking is: " + \
                             str(state[u"title"]) + \
                             str(state[u"start"]) + \
                             str(state[u"end"]) + \
                             u"do you confirm?"
    return state


def edit_booking(state):
    if state[u"intent"] == u"edit_booking" and state[u"response"] is None:
        state[u"response"] = u""
    return state


def remove_booking(state):
    if state[u"intent"] == u"remove_booking" and state[u"response"] is None:
        state[u"response"] = u""
    return state


def help(state):
    if state[u"intent"] == u"help" and state[u"response"] is None:
        state[u"response"] = u"just tell me your appointment detail"
    return state


def confusion(state):
    if state[u"intent"] == u"confusion" and state[u"response"] is None:
        state[u"response"] = u"You just tell me your appointment detail"
    return state


def outofscope(state):
    if state[u"intent"] in [u"out_of_scope", u"root"] and state[u"response"] is None:
        state[u"response"] = u"didn't understand what you just said"
        state[u"outofscope_count"] += 1
    return state


def restart(state):
    if state[u"intent"] == u"restart" and state[u"response"] is None:
        state = zero_state
        state[u"response"] = u"Lets start over again from beginning. "
    elif state[u"outofscope_count"] > 2:
        state = zero_state
        state[u"response"] = u"Lets start over again from beginning. "
    return state


def yes(state):
    if state[u"intent"] == u"yes" and state[u"response"] is None:
        try:
            save_data(state)
            state[u"persist"] = True
            state[u"response"] = u"ok booked this: " + state["title"]
        except:
            state[u"response"] = u"couldn't book"
    return state


def no(state):
    if state[u"intent"] == u"no" and state[u"response"] is None:
        state[u"response"] = u"Okay, what you want to change?"
    return state


def intro(state):
    if state[u"intent"] == u"intro" and state[u"response"] is None:
        state[u"response"] = u"Hi, how can I help you?"
    return state


def outro(state):
    if state[u"intent"] == u"outro" and state[u"response"] is None:
        state[u"response"] = u"bye"
        state[u"session_over"] = True
    return state


def thanking(state):
    if state[u"intent"] == u"thanking" and state[u"response"] is None:
        state[u"response"] = u"you are welcome. "
    return state


def profanity(state):
    if state[u"intent"] == u"profanity" and state[u"response"] is None:
        state[u"response"] = u"hey don't be rude I am just a bot, blame my programmer, bye"
        state[u"session_over"] = True
    return state


def show(state):
    if state[u"intent"] == u"show" and state[u"response"] is None:
        appointments = map(lambda d: str(d), show_data())
        state[u"response"] = u"Your appointments are: " + u' '.join(appointments)
        state[u"session_over"] = True
    return state


def main():
    print show_data()


if __name__ == u"__main__":
    main()
