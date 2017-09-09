#!/usr/bin/env python

from Common import *
from Messages import INFO

from FoodList import FoodList
from Yemek import Yemek, Carb
from copy import copy
from PieChart import PieChart

from Config import user_foodlog

'''Logs food entered into system with timestamp into foodlog.txt'''

class FoodLogger:
    def __init__(self, targets=None, testmode=0):
        # Test modes:
        # 0 - inactive
        # 1 - log and record @ 1972/01/02-13:00
        # 2 - clear all tests from record
        self.path = user_foodlog

        if testmode == 2:
            self.clearTest()

        else:
            self.date = "%04d/%02d/%02d--%02d:%02d" % localtime()[0:5]
            if testmode == 1:
                self.date = "1972/01/02-13:00"

            self.foodlog = []
            self.macrofile = targets
            self.foodlist = FoodList()        # i.e. ref FoodList cobj

    # any date
    def read(self, date):
        try:
            f = open(self.path, 'r')
        except IOError:
            f = open(self.path, 'w')
            f.write("Date             \tAmn\tFood Name\n")
            f.close()
            return

        f.readline()   # Strip Header

        datelist = []  # Not really used
        date = date[0:10]

        for line in f:
            if len(line) < 5:
                continue
            ddate, amount, name = line.split('\t')

            # rough hour
            hour, min = list(map(int, ddate[-5:].split(':')))
            hour += 1 if min >= 30 else 0

            ddate = ddate[0:10]
            datelist.append(ddate)

            if date == ddate:
                # Find food if date matches
                food = copy(self.foodlist.foodmap[name.strip()])
                food.amount = amount
                food.hour = hour
                self.foodlog.append(food)
        f.close()

        return datelist

    def showTotals(self, date, showPie=True):
        self.makeTotals(date, showPie, printme=True)

    def makeTotals(self, date, showPie=False, printme=False):
        self.read(date)

        kC_total = 0
        carb_total = Carb(0, 0, 0)
        protein_total = 0
        fat_total = 0

        if len(self.foodlog) == 0:
            INFO("nothing logged for date: %s" % date)
            prevD = previousDay(ymd2secs(date.split('/')))
            if ynprompt("Print day before that (%s)? " % prevD):
                return self.makeTotals(prevD, showPie, printme)

        if printme:
            INFO('\n' * 10)
            Yemek.printFullHeader()

        after_L_head = False
        after_6_head = False

        for y in self.foodlog:
            scyem = y.scaled()

            kC_total += scyem.kC
            carb_total.add(scyem.carb)
            protein_total += scyem.prot
            fat_total += scyem.fat

            if printme:
                if not(after_L_head) and (y.hour >= 12):
                    print('        ===== Lunch ====', file=sys.stderr)
                    after_L_head = True
                if not(after_6_head) and (y.hour >= 18):
                    print('        ===== Dinner ====', file=sys.stderr)
                    after_6_head = True
                print(scyem.printout(), file=sys.stderr)

        self.pie = PieChart(carb_total, protein_total, fat_total, kC_total,
                            self.macrofile,
                            Yemek.buffer - 8, 8, printme=showPie)

        return kC_total, carb_total, protein_total, fat_total


    def clearTest(self):
        f = open(self.path, 'r')
        all = [x for x in f.readlines() if not(x.startswith('1972'))]
        f.close()

        f = open(self.path, 'w')
        for line in all:
            #            if not line.startswith('1972'):
            print(line.splitlines()[0], file=f)
        f.close()


    def log(self, name=""):
        if name == "":
            name = input("Food: ").lower()

        name = self.foodlist.info(name)  # find match

        am = -1
        unit_set = -1

        yem_obj = self.foodlist.foodmap[name]
        init_per = equiv_per = float(yem_obj.per)

        if len(yem_obj.portions.avail) != 0:
            if ynprompt("\nNote: Portions Available -- View?"):

                ports = [x for x in yem_obj.portions.avail.keys()]
                port_res = choice(ports)

                if port_res != -1:
                    kC = yem_obj.portions.avail[port_res]
                    unit_set = float(kC) / yem_obj.kC
                    equiv_per *= unit_set
                    print("kc for this:", kC, "yem kc:", yem_obj.kC,
                          "fract:", unit_set, "equiv per=", equiv_per)


        # Am is set by port_res, so no need to check port_res here
        if unit_set != -1 or am == -1:

            am_amount, unit_set = amountsplit(
                input("\nAmount consumed (e.g '50 ml')? ").strip()
            )
            scale = am_amount / equiv_per if am_amount > 30 else am_amount
            am    = scale * equiv_per
            #print("unit_set=", unit_set, " am_amount=", am_amount)

#       dater = "%04d/%02d/%02d--%02d:%02d" % localtime()[0:5]
        dater = self.date

        f = open(self.path, 'a')
        print("%s\t%.1f\t%s" % (dater, am, name), file=f)
        f.close()

        print("\n\n", file=sys.stderr)
        self.showTotals(self.date)
