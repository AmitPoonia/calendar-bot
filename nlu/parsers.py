from pyparsing import *
import datetime
import parsedatetime
cal = parsedatetime.Calendar()


CL = CaselessLiteral
KW = CaselessKeyword
CLs = lambda x: Combine(CL(x) + Optional(CL(u"s")))

jan = KW(u"january") | KW(u"jan")
feb = KW(u"february") | KW(u"feb")
mar = KW(u"march") | KW(u"mar")
apr = KW(u"april") | KW(u"apr")
may = KW(u"may")
jun = KW(u"june") | KW(u"jun")
jul = KW(u"july") | KW(u"jul")
aug = KW(u"august") | KW(u"aug")
sep = KW(u"september") | KW(u"sep")
oct = KW(u"october") | KW(u"oct")
nov = KW(u"november") | KW(u"nov")
dec = KW(u"december") | KW(u"dec")
months_ = (jan | feb | mar | apr | may | jun | jul | aug | sep | oct | nov | dec)

nums_ = Word(u"0123456789")
floats_ = Combine(nums_ + Optional(CaselessLiteral(".") + nums_))

all_weekdays_ = [u"sunday", u"monday", u"tuesday", u"wednesday", u"thursday", u"friday", u"saturday"]
weekend_days_ = [u"saturday", u"sunday"]
week_days_ = [u"monday", u"tuesday", u"wednesday", u"thursday", u"friday"]

day_, week_, month_, night_, holiday_, year_, today_, tomorrow_, tonight_, weekend_, fortnight_ = \
    map(CLs, u"day week month night holiday year today tomorrow tonight weekend fortnight".split())

the_, a_, after_ = map(KW, u"the a after".split())
of_, dash_, slash_f_ = map(CL, u"of - /".split())
tomorrow_plus1 = Optional(the_ | a_) + day_ + after_ + tomorrow_

date_ = lambda d: (unicode(d.day) + u"/" + unicode(d.month) + u"/" + unicode(d.year))
func1 = lambda t: date_(datetime.date.today() + datetime.timedelta(days=2))
func2 = lambda t: date_(cal.parseDT(t[0])[0])
tomorrow_plus1.setParseAction(func1)
tomorrow_.setParseAction(func2)
today_.setParseAction(func2)
tonight_.setParseAction(func2)


dd_Reg = Regex("[0-9]{1,2}")
mm_Reg = Regex("[0-9]{1,2}")
yyyy_Reg = Regex("[0-9]{4}")

sp_ = Regex(u'[\s]*')
spp_ = Regex(u'[\s]+')
dash_sp = sp_ + dash_ + sp_
num_suffixes = [u"st", u"th", u"nd", u"rd"]
nums_sfx = Combine(nums_ + Optional(oneOf(num_suffixes)))

hours_, minutes_ = map(CLs, "hour minute".split())
ampm = Regex("([0-9]{1,2}(am|pm))")
oclock = Regex("([0-9]{1,2}(oclcok))")

nums_month = nums_sfx + Optional(of_ | dash_sp) + months_
month_nums = months_ + Optional(dash_sp | the_) + nums_sfx
ddmmyyyy1 = dd_Reg + dash_ + mm_Reg + dash_ + yyyy_Reg
ddmmyyyy2 = dd_Reg + slash_f_ + mm_Reg + slash_f_ + yyyy_Reg
ddmonthyyyy1 = nums_sfx + months_ + yyyy_Reg
monthddyyyy1 = months_ + nums_sfx + yyyy_Reg

unit_ = (hours_ | minutes_)
duration = Combine(nums_ + (dash_ | spp_) + unit_)
timepoint = (ampm | oclock)
datepoint = (ddmonthyyyy1 | monthddyyyy1 |
             nums_month | month_nums |
             ddmmyyyy1 | ddmmyyyy2 |
             tomorrow_plus1 | tomorrow_ | today_ | tonight_)


