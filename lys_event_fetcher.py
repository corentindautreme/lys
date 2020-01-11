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
	'Armenia': 'Depi Evratesil',
	'Australia': 'Australia Decides',
	'Austria': '',
	'Azerbaijan': '',
	'Belarus': 'Eurofest',
	'Belgium': '',
	'Bosnia and Herzegovina': '',
	'Bulgaria': '',
	'Croatia': 'Dora',
	'Cyprus': '',
	'Czech Republic': 'Eurovision Song CZ',
	'Denmark': 'Dansk Melodi Grand Prix',
	'Estonia': 'Eesti Laul',
	'Finland': 'Uuden Musiikin Kilpailu',
	'France': '',
	'Georgia': 'Georgian Idol',
	'Germany': 'Unser Lied für ',
	'Greece': '',
	'Hungary': 'A Dal',
	'Iceland': 'Söngvakeppnin',
	'Ireland': '',
	'Israel': '',
	'Italy': 'Festival di Sanremo',
	'Latvia': 'Supernova',
	'Lithuania': 'Pabandom iš naujo',
	'Luxembourg': '',
	'Malta': 'X Factor Malta',
	'Moldova': 'O melodie pentru Europa',
	'Monaco': '',
	'Montenegro': '',
	'Morocco': '',
	'Netherlands': '',
	'North Macedonia': '',
	'Norway': 'Melodi Grand Prix',
	'Poland': '',
	'Portugal': 'Festival da Canção',
	'Romania': 'Selecția Națională',
	'Russia': '',
	'San Marino': '',
	'Serbia': 'Beovizija',
	'Slovakia': '',
	'Slovenia': 'EMA',
	'Spain': '',
	'Sweden': 'Melodifestivalen',
	'Switzerland': '',
	'Turkey': '',
	'Ukraine': 'Vidbir (Natsionalnyi Vidbir na Yevrobachennia)',
	'United Kingdom': 'Eurovision: You Decide'
}

events = [{
	'id': 1,
	'country': 'Sweden',
	'name': 'Melodifestivalen',
	'stage': 'Heat 1',
	'dateTimeCet': '2020-02-01T20:00:00',
	'watchLink': 'svtplay.se'
}]
suggested_events = [{
	'id': 0, 
	'country': 'Sweden', 
	'name': 'Melodifestivalen',
	'stage': 'Night 2', 
	'suggestedDates': ['2020-02-08T20:00:00'],
	'sourceLink': 'https://eurovoix.com/2020/01/10/sweden-melodifestivalen-2020-running-order-revealed/',
	'approved': False,
	'processed': False
}]
event_suggestions_to_be_saved = []

class Story:
	def __init__(self, country, text, sourceLink):
		self.country = country
		self.text = text
		self.sourceLink = sourceLink


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
	start_every_end_pattern = ".*(start|begin).*(every|each).*(until|end|finish)"
	every_from_to_pattern = ".*(every|each).*(start|from|between|begin).*(end|to|until|and).*"
	from_to_every_pattern = ".*(from|between).*(to|until|and).*(every|each).*"

	start_every_end = re.compile(start_every_end_pattern)
	every_from_to = re.compile(every_from_to_pattern)
	from_to_every = re.compile(from_to_every_pattern)

	begin_date = None
	end_date = None
	events = []

	if re.match(start_every_end, sentence) != None:
		try:
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
			frequency = re.sub(re.compile('[^a-zA-Z]'), '', sentence[idx_start:idx_end])
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
		except Exception as e:
			print("Error parsing repetition expression \"" + sentence + "\" against pattern \"" + start_every_end_pattern + "\" - Exception is: " + str(e))


	elif re.match(every_from_to, sentence) != None:
		try:
			print("* " + sentence)
			# Determine frequency
			idx_freq_token = min(i for i in [sentence.find(token) for token in ["every", "each"]] if i > -1)
			idx_start = sentence.find(' ', idx_freq_token) + 1
			idx_end = min(i for i in [sentence.find(token) for token in ["start", "between", "from", "begin"]] if i > -1) - 1
			frequency = re.sub(re.compile('[^a-zA-Z]'), '', sentence[idx_start:idx_end])

			# Find beginning of cycle
			idx_start = min(i for i in [sentence.find(token) for token in ["start", "between", "from", "begin"]] if i > -1)
			idx_end = min(i for i in [sentence.find(token) for token in ["end", "to", "until", "and"]] if i > -1)
			begin_expression = sentence[idx_start:idx_end]
			dates = search_dates(begin_expression, languages=['en']) or []
			if len(dates) != 1:
				return []
			else:
				begin_date = dates[0][1]

			# Find end of cycle
			idx_start = min(i for i in [sentence.find(token) for token in ["end", "to", "until", "and"]] if i > -1)
			end_expression = sentence[idx_start:]
			dates = search_dates(end_expression, languages=['en']) or []
			if len(dates) != 1:
				return []
			else:
				end_date = dates[0][1]
			
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
		except Exception as e:
			print("Error parsing repetition expression \"" + sentence + "\" against pattern \"" + every_from_to_pattern + "\" - Exception is: " + str(e))

	elif re.match(from_to_every, sentence) != None:
		try:
			# Find beginning of cycle
			idx_start = min(i for i in [sentence.find(token) for token in ["from", "between"]] if i > -1)
			idx_end = min(i for i in [sentence.find(token) for token in ["to", "until", "and"]] if i > -1)
			begin_expression = sentence[idx_start:idx_end]
			dates = search_dates(begin_expression, languages=['en']) or []
			if len(dates) != 1:
				return []
			else:
				begin_date = dates[0][1]

			# Find end of cycle
			idx_start = min(i for i in [sentence.find(token) for token in ["to", "until", "and"]] if i > -1)
			idx_end = min(i for i in [sentence.find(token) for token in ["every", "each"]] if i > -1)
			end_expression = sentence[idx_start:idx_end]
			dates = search_dates(end_expression, languages=['en']) or []
			if len(dates) != 1:
				return []
			else:
				end_date = dates[0][1]

			# Determine frequency
			idx_freq_token = min(i for i in [sentence.find(token) for token in ["every", "each"]] if i > -1)
			idx_start = sentence.find(' ', idx_freq_token) + 1
			# frequency = sentence[idx_start:].replace(' ', '').replace(',', '').replace('.', '')
			frequency = re.sub(re.compile('[^a-zA-Z]'), '', sentence[idx_start:])

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
		except Exception as e:
			print("Error parsing repetition expression \"" + sentence + "\" against pattern \"" + from_to_every_pattern + "\" - Exception is: " + str(e))

	return []


def mark_event_suggestion_for_saving(suggested_event):
	# remove dates for which an event with that name already exists in list
	suggested_event.dateTimesCet = list(filter(lambda date: not any(e['dateTimeCet'][0:10] == date[0:10] and e['name'] == suggested_event.name for e in events), suggested_event.dateTimesCet))
	# remove dates for which an event suggestion for that NF was already saved
	suggested_event.dateTimesCet = list(filter(lambda date: not any(date[0:10] in list(map(lambda date: date[0:10], e['suggestedDates'])) and e['name'] == suggested_event.name for e in suggested_events), suggested_event.dateTimesCet))

	if len(suggested_event.dateTimesCet) > 0:
		event_suggestions_to_be_saved.append(suggested_event)


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
	events_for_story = []
	dates = []

	for sentence in sentences:
		sentence_events = []
		sentence_events = check_for_repetition_expression(sentence)
		for event in sentence_events:
			event.country = story.country
			event.name = get_event_for_country(story.country)
			event.sourceLink = story.sourceLink
			events_for_story.append(event)

		if len(events_for_story) > 0:
			break
		else:
			if any(word in sentence for word in ["reveal", "present", "start"]):
				continue

			sentence = re.sub(re.compile('(January|February|March|April|May|June|July|August|September|October|November|December) ([0-9]+) and ([0-9]+)'), r'\1 \2, \1 \3,', sentence)
			found_dates = search_dates(sentence, languages=['en']) or []

			# FIltering out the false positives
			found_dates = list(filter(lambda d: re.match(re.compile("[a-z ]*20[0-9]{2}[a-z ]*"), d[0]) == None, found_dates))
			found_dates = list(filter(lambda d: not(re.match(re.compile("^[a-zA-Z ]+$"), d[0]) != None and d[1].day == datetime.datetime.now().day), found_dates))
			found_dates = list(filter(lambda d: d[1] > datetime.datetime.now(), found_dates))
			dates.extend(list(map(lambda d: d[1].strftime("%Y-%m-%d") + "T20:00:00", found_dates)))

	if len(events_for_story) == 0:
		for i in range(1,len(dates)+1):
			date = dates[i-1]
			events_for_story.append(EventSuggestion(story.country, get_event_for_country(story.country), "Night " + str(i) if i < len(dates) else "Final", [date], story.sourceLink))

	event_suggestions.extend(events_for_story)

for event in event_suggestions:
	mark_event_suggestion_for_saving(event)
	# print(event)

for event in event_suggestions_to_be_saved:
	print(event)

# print("***")
# print("It will take place every Saturday between the 11th of January and the 15th of February")
# events = check_for_repetition_expression("It will take place every Saturday between the 11th of January and the 15th of February")
# for event in events:
# 	print(event)

# print("***")
# print("It will take place every Saturday from the 11th of January to the 15th of February")
# events = check_for_repetition_expression("It will take place every Saturday from the 11th of January to the 15th of February")
# for event in events:
# 	print(event)

# print("***")
# print("It will take place every Saturday, starting on the 11th of January and ending on the 15th of February")
# events = check_for_repetition_expression("It will take place every Saturday, starting on the 11th of January and ending on the 15th of February")
# for event in events:
# 	print(event)

# print("***")
# print("It will take place every Saturday, starting on the 11th of January and ending on the 15th of February")
# events = check_for_repetition_expression("It will take place between the 11th of January and the 15th of February every Saturday.")
# for event in events:
# 	print(event)