import cPickle
import datetime
from collections import namedtuple

Appointment = namedtuple(u"Appointment", u"title start end")


def load_pickle(data_path, mode):
    """
    Takes a pickled file and loads
     all the object one by one into
     a list
    """
    obj_list = []
    try:
        with open(data_path, mode) as fp:
            while 1:
                try:
                    obj_list.append(cPickle.load(fp))
                except EOFError:
                    break
        return obj_list
    except:
        return []


def overlap(tuple1, tuple2):
    """
    A function that takes two namedtuples and
    checks if they overlap with their time ranges
    """
    if (tuple1.end < tuple2.start) or (tuple1.start > tuple2.end):
        return False
    else:
        return True


def check_clash(new_data_point, data):
    """
    A function that takes new appointment data
    and checks if the same appointment already exists
    or clashes in timing with any other existing
    appointment
    """
    if new_data_point in data:
        return True, new_data_point
    for d in data:
        if overlap(new_data_point, d):
            return True, d
    return False, None


def save_data(state, data_path=u"appointments/data.pkl"):
    """
    A functions that takes the state as a dictionary
    and a serialized list of existing appointments,
    takes the appointment detail from state and
    saves it with persistence

    """
    new_data = Appointment(title=state[u"title"], start=state[u"start"], end=state[u"end"])

    a_list = load_pickle(data_path, "rb")
    if a_list != []:
        flag, val = check_clash(new_data, a_list)
        if flag is True:
            return False, val

    with open(data_path, 'ab') as fp:
        cPickle.dump(new_data, fp)
    return True, new_data


def show_data(data_path=u"appointments/data.pkl"):
    """
    A function that retrieves serialized list
    of appointments and returns it as a list
    of namedtuples
    """
    return load_pickle(data_path, "rb")


def main():
    print show_data()

if __name__ == u"__main__":
    main()
