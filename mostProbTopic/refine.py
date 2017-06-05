import sys
import os

dir_name = os.path.dirname(os.path.abspath(__file__)) + "\\"

def Preprocess(question,tl):
	from nltk.stem.snowball import SnowballStemmer
	stemmer = SnowballStemmer("english")

	text = ""
	file_name = dir_name + "Manual_text.txt"
	with open(file_name,'r') as f:
		text = f.read().replace('. ','\n').replace(',','').replace(';','').replace(':','').replace('(','').replace(')','')

	file_name = dir_name + "stop.txt"
	stopwords_io_stream = open(file_name, 'r')
	stopwords = stopwords_io_stream.read().split()

	file_name = dir_name + "donot.txt"
	donotwords_io_stream = open(file_name, 'r')
	donotwords = donotwords_io_stream.read().split()
	textlist = text.split('\n')
	linelist = []
	for line in textlist:
		# print(line)
		words = line.lower().split()
		# print(words)
		refined_words = [word for word in words if word not in stopwords]
		refined_words = [stemmer.stem(word) if word not in donotwords else word for word in refined_words]
		# print(refined_words)
		line = " ".join(refined_words)
		linelist.append(line)
	# refined = [words for words in textlist if words not in stopwords]
	# print(refined)
	text = "\n".join(linelist)

	file_name = dir_name + "Output.txt"
	text_file = open(file_name, "w")
	text_file.write(text)
	text_file.close()
	topicslist = ['Parts', 'Components', 'Away from water', 'Dry', 'Voltage', 'Damaged', 'Broken', 'Outdoor usage', 'Supervised usage', 'children', 'mentally challenged', 'Surgery', 'Consulting Dentist', 'Electromagnetic Impact', 'Pacemaker', 'Alternative', 'Different Uses', 'Discomfort', 'Pain', 'Commercial Use', 'Other Manufacturer', 'Replace', 'Renew', 'Cleaning', 'Toothpaste', 'Brush head', 'Collective', 'All Dangers', 'Safety', 'Dangers', 'Warnings', 'Scrub', 'Motion', 'Pressure', 'Collective', 'How to Best Use Brush', 'Techniques to Use Brush', 'Quadpacer', 'Beeper', 'Info about Modes', 'Clean', 'White', 'Polish', 'Gum care', 'Sensitive', 'Modes', 'Modes', 'Ways to Use', 'Quadpacer', 'Info', ' About Easy-start', 'Activate', 'Enable', 'Start', 'Deactivate', 'Disable', 'Stop', 'Easy-Start', 'Info', 'About Charging', 'Wall socket', 'USB', 'Charging', 'Battery', 'Cleaning', 'Rinse', 'Wash', 'Store', 'Keep Aside', 'Cleaning', 'Maintenance', 'Rinse', 'Wash', 'Storing', 'Info', 'Model', 'Battery Removal', 'Disposal', 'Throw Away', 'Trash', 'Service', 'Care Center', 'Warranty', 'Guarantee', 'Issues', 'Problems', 'Doesn’t Work', ' Doesn’t Start', 'Issues', 'Problems', 'Warranty', 'Guarantee', 'Service', 'Doesn’t Work']
	topicslist = tl
	topicslist = list(set(topicslist))

	file_name = dir_name + "Topic.txt"
	file = open(file_name,"w")
	cnt = 0
	for topic in topicslist:
		words = topic.lower().replace('-',' ').replace('.','').split()
		stemmed_words = [stemmer.stem(word) if word not in donotwords else word for word in words]
		topic = " ".join(stemmed_words).replace('-',' ').replace('.','')
		# print(topic)
		file.write(topic)
		if cnt < len(topicslist)-1:
			file.write("\n")
		cnt += 1
	file.close()
	cnt = 0
	file_name = dir_name + "Topic"
	file2 = open(file_name,"w")
	for topic in topicslist:
		file2.write(topic.strip())
		if cnt < len(topicslist)-1:
			file2.write("\n")
		cnt += 1
	file2.close()
	return question