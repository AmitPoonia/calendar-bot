from parsers import *
import datetime
cal = parsedatetime.Calendar()


def to_dp_object(dp):
    """
    Takes a parsed datepoint object
    and converts it into a datetime
    object
    """
    try:
        d = dp[0][0]
        return cal.parseDT(d)[0]
    except:
        return datetime.datetime.today()


def to_tp_object(tp, dp):
    """
    Takes timepoint object list
    and converts each of it into
    a datetime object of given day
    which is the second arg
    """
    try:
        to = []
        for t in tp:
            tobj = cal.parseDT(t[0])[0]
            tobj.replace(month=dp.month)
            tobj.replace(day=dp.day)
            tobj.replace(year=dp.year)
            to.append(tobj)
        return sorted(to)
    except:
        return [None, None]


def to_minutes(dur_obj):
    """
    This functions converts
    a parsed duration object from
    hours to minutes
    """
    dur = list(dur_obj)
    if dur == []:
        return None
    else:
        c = nums_.searchString(dur[0][0])[0][0]
        u = unit_.searchString(dur[0][0])[0][0]
        if u.startswith(u"minute"):
            return int(c)
        elif u.startswith(u"hour"):
            return int(c)*60
        else:
            return None


def get_dt_detail(text):
    """
    A function that takes some text and
    extracts any date time entities from
    it if any, and returns it as a dict
    """
    results = {u"datepoint": None, u"timepoints": None, u"duration": None}
    if text != u"" or text != None:
        results[u"datepoint"] = to_dp_object(datepoint.searchString(text))
        results[u"timepoints"] = to_tp_object(timepoint.searchString(text), results[u"datepoint"])
        results[u"duration"] = to_minutes(duration.searchString(text))

    return results


def main():
    print get_dt_detail("meeting with dave from 5pm to 6pm for 1 hour")

if __name__ == "__main__":
    main()
