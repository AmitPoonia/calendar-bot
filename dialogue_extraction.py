import datetime
from nlu.ner_title import get_title
from nlu.ner_datetime import get_dt_detail
from nlu.intent_classification import model_predict

intent_clf_path = u"nlu/data/intent/intent_classifier/intent_classifier.clf"
intent_map_path = u"nlu/data/intent/intent_classifier/intent_map.json"
data_vec_path = u"nlu/data/intent/vectorizer"


def update_state(state, entities):
    """
     A function that takes the current state and
     extracted entities, updates the state using
     the entities
    """
    if entities[u"intent"] in [u"edit_booking"]:
        state[u"intent"] = entities[u"intent"]
        if state[u"title"] != entities[u"title"]:
            state[u"title"] = entities[u"title"]
        if state[u"start"] != entities[u"start"]:
            state[u"start"] = entities[u"start"]
        if state[u"end"] != entities[u"end"]:
            state[u"end"] = entities[u"end"]

    elif entities[u"intent"] in [u"yes"]:
        state[u"intent"] = entities[u"intent"]
    else:
        state[u"intent"] = entities[u"intent"]
        state[u"start"] = entities[u"start"]
        state[u"end"] = entities[u"end"]
        state[u"title"] = entities[u"title"]
    return state


def get_entities(state):
    """
    The main extraction function, takes the state from
    dialogue manager and returns intent,
    title and time entities
    """

    dt_detail = get_dt_detail(state[u"text"])
    print dt_detail
    try:
        start = dt_detail[u"timepoints"][0]
        end = dt_detail[u"timepoints"][1]
    except:
        start = None
        end = None
    title = get_title(state[u"text"])
    intent = model_predict(state[u"text"], intent_clf_path, intent_map_path, data_vec_path)

    ents = {u"intent": intent[0], u"title": title, u"start": start, u"end": end}
    state = update_state(state, ents)
    return state


def main():
    pass

if __name__ == u"__main__":
    main()


