#!/usr/bin/env python

# COMPLETELY UNUSED
#
#
#


class MoneyLogger:

	period_map = {'day':1, 'week': 5, 'month':20}

	def __init__(self, target=abspath("../")+"/logs/targets.txt",
			     file=abspath("../")+"/logs/money_log.txt"):
		self.logfile = file

		f = open(target,'r')
		for line in f:
			if line.startswith("money"):
				self.limit, self.period = map(lambda x: x.strip(), line.split('=')[1].split('/'))
				break

		self.limit = float(self.limit)
		try:
			self.period = int(self.period)	# if num days
		except ValueError:
			self.period = MoneyLogger.period_map[self.period]

		self.daily_limit = self.limit/self.period

		print self.daily_limit

		self.mlog = [] # Tuple array of [item,amount] for today
		self.date = "%04d/%02d/%02d--%02d:%02d" % localtime()[0:5]


	def printheader(self, buffer):
		print >> sys.stderr, "Item%sAmount" % ( ((buffer-4) if buffer > 4 else buffer)* ' ')
		print >> sys.stderr, "=" * (buffer+13)


	def printout(self, it_am, buff):
		print >> sys.stderr, "%*s   %.2f" % (buff, it_am[0], it_am[1])


	# any date
	def read(self,date):
		try:
			f=open(self.logfile,'r')
		except IOError:
			f=open(self.logfile,'w')
			f.write("Date             \tItem\tAmount\n")
			f.close()
			return

#		f.readline()   # Strip Header

		for line in f:
			if len(line) < 5:
				continue
			ddate, item, amount = line.split('\t')

#			print line
			if date[0:10] == ddate[0:10]:
				#Find items if date matches
				self.mlog.append( [item.strip(), float(amount.strip())] )
		f.close()


	def showTotals(self,date):
		self.read(date)

		if len(self.mlog)==0:
			print >> sys.stderr, "nothing logged for that day!"
			exit(-1)

		maxlen_name=len(reduce(lambda x,y: ( x if (len(x[0]) > len(y[0])) else y ), self.mlog)[0])
		print >> sys.stderr, '\n'*10

		print >> sys.stderr, "NOO1"
		print >> sys.stderr, self.printheader(maxlen_name)
		print >> sys.stderr, "NOO2"

		total = 0.0;

#		for itam in self.mlog:
#			it, am = itam
#			total += am
#			print >> sys.stderr, self.printout([it,am], maxlen_name)

		print >> sys.stderr,""
		print >> sys.stderr, "Total:\t%f" % total

		#Allowed
		print >> sys.stderr, "Allowed:\t%f" % (total - self.daily_limit)
		print >> sys.stderr, "Remain:\t%f with %d days to go" % (self.limit - total, self.period-1)


	def log(self, name=""):
		if name=="":
			name = raw_input("Item: ").strip().lower()

		am = float(raw_input("\nCost? ").strip())
		dater = "%04d/%02d/%02d--%02d:%02d" % localtime()[0:5]

		f=open(self.logfile,'a')
		print >> f, "%s\t%s\t%.2f" % (dater,name, am)
		f.close()

		print >> sys.stderr, "\n\n"
		self.showTotals(self.date)

w=MoneyLogger()
#w.log()
w.showTotals(w.date)
