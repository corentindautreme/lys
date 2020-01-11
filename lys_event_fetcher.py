import xml.etree.ElementTree as ET
import datetime
import requests
import re
from dateparser.search import search_dates

# str = 'Melodi Grand Prix 2020 will begin on January 11 and continue every Saturday until February 15. '
# print(search_dates(str, languages=['en']))
# print(search_dates('Sanremo 2020 will begin on February 4 and will run each night until February 8.', languages=['en']))

national_selections = {
	'Albania': 'Festivali i Këngës',
	'Andorra': '',
	'Armenia': '',
	'Australia': 'Australia Decides',
	'Austria': '',
	'Azerbaijan': '',
	'Belarus': 'Eurofest',
	'Belgium': '',
	'Bosnia and Herzegovina': '',
	'Bulgaria': '',
	'Croatia': 'Dora',
	'Cyprus': '',
	'Czech Republic': '',
	'Denmark': 'Dansk Melodi Grand Prix',
	'Estonia': 'Eesti Laul',
	'Finland': '',
	'France': '',
	'Georgia': '',
	'Germany': '',
	'Greece': '',
	'Hungary': '',
	'Iceland': 'Söngvakeppnin',
	'Ireland': '',
	'Israel': '',
	'Italy': 'Festival di Sanremo',
	'Latvia': 'Supernova',
	'Lithuania': '',
	'Luxembourg': '',
	'Malta': '',
	'Moldova': '',
	'Monaco': '',
	'Montenegro': '',
	'Morocco': '',
	'Netherlands': '',
	'North Macedonia': '',
	'Norway': 'Melodi Grand Prix',
	'Poland': '',
	'Portugal': '',
	'Romania': '',
	'Russia': '',
	'San Marino': '',
	'Serbia': 'Beovizija',
	'Slovakia': '',
	'Slovenia': '',
	'Spain': '',
	'Sweden': 'Melodifestivalen',
	'Switzerland': '',
	'Turkey': '',
	'Ukraine': '',
	'United Kingdom': ''
}

class Story:
	def __init__(self, country, text, sourceLink):
		self.country = country
		self.text = text
		self.dates = []
		self.sourceLink = sourceLink

	def __str__(self):
		string = self.country + "[\n"
		for date in self.dates:
			string += str(date) + "\n"
		return string + "]"

	def addDate(self, story_date):
		if not any(d.datetime == story_date.datetime for d in self.dates):
			self.dates.append(story_date)

class StoryDate:
	def __init__(self, datetime, sentence, context):
		self.datetime = datetime
		self.sentence = sentence
		self.context = context

	def __str__(self):
		return "(" + self.datetime.strftime("%Y-%m-%dT%H:%M:%S") + ", " + self.sentence + " [" + self.context + "])"


class EventSuggestion:
	def __init__(self, country, name, stage, dateTimesCet, sourceLink):
		self.id = 0
		self.country = country
		self.name = name
		self.stage = stage
		self.dateTimesCet = dateTimesCet
		self.sourceLink = sourceLink
		self.accepted = False
		self.closed = False

	def __str__(self):
		return "{" + str(self.id) + ", " + self.country + ", " + self.name + ", " + self.stage + ", " + str(self.dateTimesCet) + ", " + self.sourceLink + "}"


def create_story(item):
	categories = list(map(lambda c: c.text, item.findall('category')))
	country = ""
	for cat in categories:
		if cat in countries:
			country = cat
	content = item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text.replace('<!--[CDATA[', '').replace(']]>', '').replace('\n', '.')
	try:
		content = content[0:content.index('<div')]
	except ValueError:
		pass
	content = re.sub(re.compile('<.*?>'), '', content)
	# content = re.sub(re.compile(r"\\x[a-z0-9]+"), '', content)
	content = re.sub(re.compile(r"&#[0-9]+;"), '', content)
	return Story(country, content, item.find('link').text)


def is_temporal_sentence(sentence):
	temporal_expressions = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "night", "evening", "tonight", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "week", "month"]
	return any(e in sentence for e in temporal_expressions)


def is_day_of_week(string):
	return string in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def get_event_for_country(country):
	return national_selections.get(country)

def check_for_repetition_expression(sentence):
	start_every_end = re.compile(".*(start|begin).*(every|each).*(until|end|finish)")
	every_from_to = re.compile(".*(every|each).*(from).*(to|until).*")
	from_to_every = re.compile(".*(from).*(to|until).*(every|each).*")

	begin_date = None
	end_date = None
	events = []

	if re.match(start_every_end, sentence) != None:
		# Find beginning of cycle
		idx_start = min(i for i in [sentence.find(token) for token in ["start", "begin"]] if i > -1)
		idx_end = min(i for i in [sentence.find(token) for token in ["every", "each"]] if i > -1)
		begin_expression = sentence[idx_start:idx_end]
		dates = search_dates(begin_expression, languages=['en']) or []
		if len(dates) != 1:
			return []
		else:
			begin_date = dates[0][1]

		# Find end of cycle
		idx_start = min(i for i in [sentence.find(token) for token in ["until", "end", "finish"]] if i > -1)
		end_expression = sentence[idx_start:]
		dates = search_dates(end_expression, languages=['en']) or []
		if len(dates) != 1:
			return []
		else:
			end_date = dates[0][1]

		# Determine frequency
		idx_start = sentence.find(' ', min(i for i in [sentence.find(token) for token in ["every", "each"]] if i > -1)) + 1
		idx_end = min(i for i in [sentence.find(token) for token in ["until", "end", "finish"]] if i > -1) -1
		frequency = sentence[idx_start:idx_end]
		if len(frequency.split(' ')) > 1:
			# TODO uncovered use case: longer frequency expression or unrecognized
			return []
		if is_day_of_week(frequency):
			# happening every specified weekday between begin and end date
			it_date = begin_date
			i = 1
			while it_date < end_date:
				events.append(EventSuggestion("", "", "Night " + str(i), [it_date.strftime("%Y-%m-%d") + "T20:00:00"], ""))
				it_date += datetime.timedelta(days=7)
				i += 1
			events.append(EventSuggestion("", "", "Final", [it_date.strftime("%Y-%m-%d") + "T20:00:00"], ""))
			return events
		elif frequency in ["day", "night", "evening"]:
			it_date = begin_date
			i = 1
			while it_date < end_date:
				events.append(EventSuggestion("", "", "Night " + str(i), [it_date.strftime("%Y-%m-%d") + "T20:00:00"], ""))
				it_date += datetime.timedelta(days=1)
				i += 1
			events.append(EventSuggestion("", "", "Final", [it_date.strftime("%Y-%m-%d") + "T20:00:00"], ""))
			return events

	elif re.match(every_from_to, sentence) != None:
		pass
	elif re.match(from_to_every, sentence) != None:
		pass
	return []


source = "https://eurovoix.com/feed/"
xml = requests.get(source).content
root = ET.fromstring(xml)

items = root.find('channel').findall('item')

nf_items = filter(lambda item: ('National Selection' in list(map(lambda c: c.text, item.findall('category')))), items)
stories = []

countries = ['Albania', 'Andorra', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Israel', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Morocco', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Ukraine', 'United Kingdom']
event_suggestions = []

for item in nf_items:
	stories.append(create_story(item))

for story in stories:
	sentences = story.text.split('.')
	sentences = list(filter(lambda s: is_temporal_sentence(s), sentences))
	events = []
	dates = []

	for sentence in sentences:
		sentence_events = []
		sentence_events = check_for_repetition_expression(sentence)
		for event in sentence_events:
			event.country = story.country
			event.name = get_event_for_country(story.country)
			event.sourceLink = story.sourceLink
			events.append(event)

		if len(events) > 0:
			break
		else:
			if any(word in sentence for word in ["reveal", "present", "start"]):
				continue

			sentence = re.sub(re.compile('(January|February|March|April|May|June|July|August|September|October|November|December) ([0-9]+) and ([0-9]+)'), r'\1 \2, \1 \3,', sentence)
			# TODO: suggest multiple events from a story
			# "Ten songs will compete over two semi-finals on February 8 and 15 at the Háskólabíó Conference Hall in Reykjavík. Two songs from each semi-final will advance to the final on February 29 in Laugardalshöll in Reykjavík."
			# => replace "February 8 and 15" by "February 8, February 15" so dateparser.search_dates() can find 2 separate dates
			# => Expects 3 events on February 8, 15 and 29

			found_dates = search_dates(sentence, languages=['en']) or []

			# FIltering out the false positives
			found_dates = list(filter(lambda d: re.match(re.compile("[a-z ]*20[0-9]{2}[a-z ]*"), d[0]) == None, found_dates))
			found_dates = list(filter(lambda d: not(re.match(re.compile("^[a-zA-Z ]+$"), d[0]) != None and d[1].day == datetime.datetime.now().day), found_dates))
			found_dates = list(filter(lambda d: d[1] > datetime.datetime.now(), found_dates))

			# print(found_dates)

			# dates = list(map(lambda d: d[1].strftime("%Y-%m-%d") + "T20:00:00", found_dates))
			dates.extend(list(map(lambda d: d[1].strftime("%Y-%m-%d") + "T20:00:00", found_dates)))
			# print(dates)
			# events.append(EventSuggestion(story.country, get_event_for_country(story.country), "Final", dates, story.sourceLink))

	if len(events) == 0:
		for date in dates:
			events.append(EventSuggestion(story.country, get_event_for_country(story.country), "Final", dates, story.sourceLink))

	event_suggestions.extend(events)

for event in event_suggestions:
	print(event)
