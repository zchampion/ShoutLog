from __future__ import print_function
import datetime

'''
    Project:            Shout Wall Log Program
    Programmer:         Zachary Champion
    Date Last Updated:  23 December 2016
    Python Version:     2.7
'''


class ShoutLog:
    def __init__(self, weeksback=0, rate=0.10):
        self.rate = rate
        if datetime.date.today().weekday() == 6 and datetime.datetime.now().hour == 0: weeksback = 1
        self.weekname = self.get_weekname(weeksback)
        self.filename = self.weekname + '.klat'
        self.shouts = self.count_shouts()
        self.bugs = self.count_bug_reports()
        self.tests = self.count_tests()
        self.invoice = self.get_invoice()

    def __str__(self):
        string = \
            "Log:            " + self.filename + '\n' + \
            "Shouts:         " + str(self.shouts) + '{: >13}'.format(str(self.shouts/5.0) + '%\n')

        if self.bugs > 0:
            string += "Bug Reports:    " + str(self.bugs) + "\n"
        if self.tests > 0:
            string += "Wall Tests:     " + str(self.tests) + "\n"

        string += "Invoice Amount: $" + '{:.2f}'.format(self.invoice)

        return string

    def get_weekname(self, weeksback):
        today = datetime.date.today()
        idx = (today.weekday() + 1) % 7
        sun = today - datetime.timedelta((7 * weeksback) + idx)
        sat = today - datetime.timedelta((7 * weeksback) + idx - 6)
        weekname = '{:%m.%d}-{:%m.%d}'.format(sun, sat)
        return weekname

    def create_newlog(self):
        print("Creating \"" + self.filename + "\"")
        readShouts = open(self.filename, 'w')
        readShouts.write("Shout Wall Log - Week of " + self.weekname + "\n" + \
                         '*' * 37 + '\n')
        readShouts.close()

    def count_shouts(self):
        shouts = 0
        try:
            readShouts = open(self.filename)

        except:
            print("Error opening the file \"" + self.filename + "\"")
            self.create_newlog()
            return 0

        for line in readShouts:
            if line.split()[0].lower() == "[shout]": shouts += 1

        readShouts.close()
        return shouts

    def count_bug_reports(self):
        bugs = 0
        try:
            readBugs = open(self.filename)

            for line in readBugs:
                if line.split()[0].lower() == "[bug]": bugs += 1

        except:
            print("Error opening/writing to the file.")
            return 0

        readBugs.close()
        return bugs

    def count_tests(self):
        tests = 0
        try:
            readTests = open(self.filename)

            for line in readTests:
                if line.split()[0].lower() == "[test]": tests += 1

        except:
            print("Error opening/reading from the file.")
            return 0

        readTests.close()
        return tests

    def get_invoice(self):
        invoice = self.shouts * self.rate

        if invoice > 50:
            invoice = 50.0

        invoice += self.get_bug_invoice() + self.tests * 5.0

        return invoice

    def get_bug_invoice(self):
        invoice = 0.00
        try:
            log = open(self.filename)

        except:
            print("Error opening the file (" + self.filename + ").")

        for line in log:
            lineItems = line.split()

            if lineItems[0].lower() == "[bug]":
                invoice += float(lineItems[1])

        log.close()
        return invoice

    def timestamp(self):
        return '{:%a %m.%d %X}'.format(datetime.datetime.now())

    def write_log_entry(self, entry):
        try:
            if entry != "":
                log = open(self.filename, 'a')

                log.write("[Shout] " + self.timestamp() + " \"" + entry + "\"\n")
                self.shouts += 1
            else:
                return

        except:
            print("Error opening/reading from the file (" + self.filename + ").")

        log.close()

    def write_bug_report(self, bug_dsc, rate):
        try:
            log = open(self.filename, 'a')

            log.write("[Bug] " + '{:.2f}'.format(rate) + self.timestamp() + " \"" + bug_dsc + "\"\n")
            self.bugs += 1

        except:
            print("Error opening the file (" + self.filename + ").")

        log.close()

    def write_test_entry(self):
        try:
            log = open(self.filename, 'a')

            log.write("[Test] " + self.timestamp() + "\n")
            self.tests += 1

        except:
            print("Error opening the file (" + self.filename + ").")

        log.close()

    def summarize(self):
        self.shouts = self.count_shouts()
        self.bugs = self.count_bug_reports()
        self.tests = self.count_tests()
        self.invoice = self.get_invoice()
        print(str(self))

    def finalize(self):
        finalized = False

        try:
            log = open(self.filename)

            for line in log:
                if line == '{:*^41}'.format(' Final Invoice ') + '\n':
                    finalized = True

        except:
            print("Error opening the file.")

        log.close()

        if not finalized:
            invoice_string = '{:*^41}'.format(' Final Invoice ') + '\n' + \
                "Shout Wall Invoice - Week of " + self.weekname + '\n' + \
                "Username: QueenFluffyShadow\n" + \
                "Paypal Email: Belgarion270@gmail.com\n" + \
                "Shouts Completed: " + str(self.shouts) + '\n'

            if self.bugs > 0:
                invoice_string += "Bug Reports: " + str(self.bugs) + '\n'

            if self.tests > 0:
                invoice_string += "Shout Wall Tests: " + str(self.tests) + '\n'

            invoice_string += \
                "Paypal Amount: $" + '{:.2f}'.format(self.invoice) + '\n' + \
                "*" * 41

            try:
                log = open(self.filename, 'a')

                log.write(invoice_string)
                print(invoice_string)

            except:
                print("Error opening the file.")

            log.close()

        else: print("Log already finalized.")

    def insertlostshouts(self, numlost):
        for _ in range(numlost):
            self.write_log_entry("-lost shout-")


if __name__ == "__main__":
    print("Shout Wall Log Python Model 2.0")

    shoutLog = ShoutLog()
    print("Log file \'" + shoutLog.filename + "\'. Shouts: " + str(shoutLog.shouts))
    print()

    cmd = raw_input("> ")
    while cmd != "/done":

        if cmd.lower() == "/log":
            session = shoutLog.shouts
            
            promptstring = ""
            if (session + 1) % 5 == 0:
                if (session + 1) % 10 == 0:  promptstring += '0'
                else: promptstring += '5'
            else: promptstring += '>'
            promptstring += '> '

            log_cmd = raw_input(promptstring)

            while log_cmd.lower() != "/done":
                shoutLog.write_log_entry(log_cmd)
                session += 1

                promptstring = ""
                if (session + 1) % 5 == 0:
                    if (session + 1) % 10 == 0:  promptstring += '0'
                    else: promptstring += '5'
                else: promptstring += '>'
                promptstring += '> '

                log_cmd = raw_input(promptstring)

        elif cmd.lower() == "/bug":
            bug = raw_input("What's the bug? Tell me what's a-happenin'!\n")

            if bug.lower() != "/cancel":
                rate = float(raw_input("What was the bounty on that bug's head? $"))
                shoutLog.write_bug_report(bug, rate)

        elif cmd.lower() == "/test":
            shoutLog.write_test_entry()

        elif cmd.lower() == "/summary" or cmd.lower() == "/sum":
            shoutLog.summarize()

        elif cmd.lower() == "/help" or cmd.lower() == "/cmd":
            print(\
                "/log: write a shout log entry\n" + \
                "/bug: log a bug report\n" + \
                "/test: log a Shout Wall test attended\n" + \
                "/summary: refresh the statistics and display the summary\n" + \
                "/lost: insert a number of lines into the current log of lost shouts\n")

        elif cmd.lower() == "/finalize" or cmd.lower() == "/fin":
            last_shoutLog = ShoutLog(1)
            last_shoutLog.finalize()

        elif cmd.lower() == "/lost":
            numlost = int(raw_input("Insert how many lost shouts?\n"))
            shoutLog.insertlostshouts(numlost)

        else: print("Command not recognized.")

        cmd = raw_input("\n> ")
