from Common import *

class Journal:
	'''Keep a journal of what you did that was good, and what you that was bad and generate a daily score'''
	
	def __init__(self, path='../logs/journal.txt'):
		self.file = path
		self.datemap= {}
		self.dates =  []
		

	def read(self):
		try:
			f = open(self.file,'r')
		except IOError:
			f = open(self.file,'w')
			f.write("Date     \tScore\tActivity")
			f.close()
			f = open(self.file,'r')


		f.readline()

		for line in f:
			timestamp, score, activity = line.split('\t')

			log_date = timestamp[:10]
			if log_date not in self.datemap:
				self.datemap[log_date] = []
				self.dates.append(log_date)
			self.datemap[log_date].append( (int(score), activity.strip()) )
		f.close()


	@staticmethod
	def out(stamp,score,activity):
		return "%s\t%d\t%s\n" % (stamp,score,activity)



	def logReady(self,stamp,score,activity):
		f = open(self.file, 'a')
		strr = Journal.out(stamp,score,activity)
		print strr
		f.write(strr)
		f.close()


	def log(self,activity='e', score='e'):
		if activity == 'e':
			activity = raw_input("Activity: ")
			toke = activity.split(',')
			try:
				score = int(toke[-1])
				activity = ','.join(toke[:-1])
			except ValueError:
				pass

		if score =='e':
			while True:
				try:
					score = int(raw_input("Score: "))
					break
				except ValueError:
					print "Not a valid integer, try again"
		
		score = int(score)
		self.logReady(now(), score, activity.strip())


#	def maketotal(self):
#		self.totals=[]
#		for d in sef.dates:


	def showToday(self):
		print self.datemap
		tod= self.datemap[today()]
		for d,s,a in tod:
			print Journal.out(d,s,a)


j = Journal()
#j.log("Ate 5 chocolate biscuits", -5)
j.showToday()

