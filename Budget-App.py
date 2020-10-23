class Category:
    spendmemory = list()
    def __init__ (self, catname):
        self.catname = catname
        self.ledger = list()
        self.credited = 0
        self.debited = 0
        self.ledgerbalance = self.credited - self.debited
        #print(self.catname, 'has been initialised.')
    def deposit(self, amt, desc=''):
        self.credited += amt
        self.depobj = {'amount': amt, 'description': desc}
        self.ledger.append(self.depobj)
        #print('This ', amt ,' was deposited for ' + desc)
        self.get_balance()       
    def withdraw(self, amt, desc=''):
        if self.check_funds(amt) is True:
            self.debited += amt
            self.withdobj = {'amount': -1 * amt, 'description': desc}
            self.ledger.append(self.withdobj)
            self.spendmemory.append({'category': self.catname, 'amt': amt})
            # print('This ', amt ,' was withdrawn for ' + desc)
            self.get_balance()
            return True
        else:
            return False
        
    def get_balance(self):
        self.ledgerbalance = self.credited - self.debited
        return self.ledgerbalance
    
    def transfer(self, amt, trfto):
        if self.check_funds(amt) is True:
            self.withdraw(amt, 'Transfer to ' + trfto.catname)
            trfto.deposit(amt, 'Transfer from ' + self.catname)
            return True
        else:
            return False
    def check_funds(self, amt):
        if amt < self.ledgerbalance:
            return True
        else:
            return False
        
    def __str__(self):
        num = (30 - len(self.catname)) // 2
        stars = ''
        headline = ''
        i = 0
        while i < num:
            stars += '*'
            i+=1
        if (30 - len(self.catname)) % 2 == 0:
            headline = stars + self.catname + stars
        else:
            headline = stars + self.catname + stars + '*'
        total = 0
        toprint = ''
        for item in self.ledger:
            total += item['amount']
            toprint += item['description'][:23] + str('{:.2f}'.format(item['amount'])).rjust(30 - len(item['description'][:23])) + '\n'
        totalline = 'Total: '+ str('{:.2f}'.format(total))
        return headline + '\n' + toprint + totalline

food = Category('Food')
clothing = Category('Clothing')
food.deposit(8000, 'initial deposit bla bla bla bal bla bla')
clothing.deposit(8000, 'Sallah')
clothing.transfer(1000, food)
food.withdraw(3000, 'beans')
clothing.withdraw(4000, 'belt')
food.get_balance()
print(food)
#print(Category.spendmemory)


def create_spend_chart(*args):    
    categoryamt = dict()  
    totalspent = 0
    for cat in Category.spendmemory:
        totalspent += cat['amt']
        categoryamt[cat['category']] = categoryamt.get(cat['category'], 0) + cat['amt']
    #print(totalspent)        
    #print(categoryamt)
    #print(categoryamt.items())
    catsinpercent = list()
    for eachcat, amt in categoryamt.items():
        percentoftotal = round(((amt/totalspent)/10.0)*1000)
        catsinpercent.append((percentoftotal, eachcat))
    #print('this', catsinpercent)
    # print(catsinpercent[0][1])
    numofdash = (len(catsinpercent) * 3) + 1
    longestcat = 0
    for each in catsinpercent:
        if len(each[1]) > longestcat:
            longestcat = len(each[1])
    # print (longestcat) 
    
    toprint = 'Percentage spent by category\n'
    cal = 100
    while cal >= 0:
        toprint += str(cal).rjust(3) + '| '
        for eachcategory in catsinpercent:
            if eachcategory[0] >= cal:
                toprint += 'o  '
            else:
                toprint += '   '
                #break
        toprint += '\n'
        cal -= 10
    toprint += '    '+('-'*numofdash)+ '\n'
    loop_var = 0
    for i in range(longestcat):
        toprint += '     '
        for j in range(len(catsinpercent)):
            if len(catsinpercent[j][1]) - 1 < loop_var:
                toprint += '   '
            else:
                toprint += catsinpercent[j][1][loop_var] + '  '
        loop_var += 1
        if i != longestcat - 1:
            toprint+="\n"
    print(toprint)
    return toprint
create_spend_chart(food, clothing)
