import requests
import sys

def get_interwiki_map(wd_item):
	r = requests.get(f'https://www.wikidata.org/wiki/Special:EntityData/{wd_item}.json').json()
	return r['entities'][wd_item]['sitelinks']

def check_wiki(wd_item, wiki_db):
	interwiki = get_interwiki_map(wd_item)
	if wiki_db in interwiki:
		return interwiki[wiki_db]['url']
	else:
		return False

if __name__ == '__main__':
	to_check = [
        ('Template:In lang',                  'Q66459516'),
		('Template:Subscription required',    'Q10963822'),
		('Template:Registration required',    'Q14397387'),
		('Template:Refbegin',                 'Q6681068'),
		('Template:Refend',                   'Q5612555'),
		('Template:Wayback',                  'Q10972291'),
		('Template:WebCite',                  'Q6563200'),
		('Template:Webarchive',               'Q27850769'),
		('Template:Dead link',                'Q5909236'),
        ('Template:Source',                   'Q17589610'),
		('Module:Citation/CS1/Configuration', 'Q15403810')]

	for label, wd_item in to_check:
		url = check_wiki(wd_item, sys.argv[1])
		if url is not False:
			print(f'{label}: {url}')
