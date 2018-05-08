"""
    Project:            Shout Wall Log Program
    Programmer:         Zachary Champion
    Python Version:     3.5
"""
from datetime import date, datetime, timedelta
import os

# User's username and PayPal email address, only used for putting together the invoice.
Usernames = ["TheFluffyQ"]
Email = "Belgarion270@gmail.com"
log_dir_string = os.path.dirname(os.path.realpath(__file__)) + "/Shout Logs/"


class ShoutLog:
    def __init__(self, last_week=False, pay_rate=0.10):
        self.rate = pay_rate
        self.week_name = self.get_week_name(
            1 if date.today().weekday() == 6 and datetime.now().hour == 0 or last_week else 0)
        # Look for "last week" if Pacific time is still in last week relative to my time.
        self.filename = log_dir_string + self.week_name + '.klat'
        self.shouts = self.count_shouts()
        self.starting = self.shouts  # Remember the number of starting shouts for the num of shouts in the session.
        self.bugs = self.count_bug_reports()
        self.tests = self.count_tests()
        self.invoice = self.get_invoice()

    def __str__(self):
        string = \
            "Log:            " + self.week_name + '\n' + \
            "Shouts:         {0:3}{1: >7}%\n".format(self.shouts, self.shouts/5.0) + \
            "  this session: {0:3}{1: >7}%\n".format(self.shouts - self.starting, (self.shouts - self.starting)/5.0)

        if self.bugs > 0:
            string += "Bug Reports:    " + str(self.bugs) + "\n"
        if self.tests > 0:
            string += "Wall Tests:     " + str(self.tests) + "\n"

        string += "Invoice Amount: $" + '{:.2f}'.format(self.invoice)

        return string

    @staticmethod
    def get_week_name(weeks_back):
        today = date.today()
        idx = (today.weekday() + 1) % 7
        sun = today - timedelta((7 * weeks_back) + idx)
        sat = today - timedelta((7 * weeks_back) + idx - 6)
        week_name = '{:%m.%d}-{:%m.%d}'.format(sun, sat)
        return week_name

    def create_new_log(self):
        print("Creating \"" + self.filename + "\"")
        read_shouts = open(self.filename, 'w')
        read_shouts.write("Shout Wall Log - Week of " + self.week_name + "\n" +
                          '*' * 37 + '\n')
        read_shouts.close()

    def count_shouts(self):
        shouts = 0
        try:
            read_shouts = open(self.filename)

        except Exception as e:
            print("Error opening the file \"" + self.filename + "\"")
            print(str(e))
            self.create_new_log()
            return 0

        for line in read_shouts:
            if line != "" and line.startswith("[Shout]"):
                shouts += 1

        read_shouts.close()
        return shouts

    def count_bug_reports(self):
        bugs = 0

        try:
            read_bugs = open(self.filename)

            for line in read_bugs:
                if line.startswith("[Bug]"):
                    bugs += 1

            read_bugs.close()

        except Exception as e:
            print("Error counting the bug reports in file \"{}\".".format(self.filename))
            print(str(e))

        finally:
            return bugs

    def count_tests(self):
        tests = 0

        try:
            read_tests = open(self.filename)

            for line in read_tests:
                if line != "" and line.startswith("[Test]"):
                    tests += 1

            read_tests.close()

        except Exception as e:
            print("Error counting the tests in file \"{}\".".format(self.filename))
            print(str(e))

        finally:
            return tests

    def get_invoice(self):
        invoice = self.shouts * self.rate

        if invoice > 50:
            invoice = 50.0

        invoice += self.get_bug_invoice() + self.get_test_invoice()

        return invoice

    def get_bug_invoice(self):
        invoice = 0.00

        try:
            log = open(self.filename)

            for line in log:
                line_items = line.split()

                if line_items[0].lower() == "[bug]":
                    invoice += float(line_items[1])

            log.close()

        except Exception as e:
            print("Error getting the \"bug invoice\" from the file (" + self.filename + ").")
            print(str(e))

        return invoice

    def get_test_invoice(self):
        invoice = 0.00

        try:
            log = open(self.filename)

            for line in log:
                line_items = line.split()

                if line_items[0] == "[Test]":
                    invoice += float(line_items[4])

            log.close()

        except Exception as e:
            print("Error getting the \"bug invoice\" from the file (" + self.filename + ").")
            print(str(e))

        return invoice

    @staticmethod
    def timestamp():
        return '{:%a %m.%d %X}'.format(datetime.now())

    def write_log_entry(self, entry):
        try:
            if entry != "":
                log = open(self.filename, 'a')

                log.write("[Shout] " + self.timestamp() + " \"" + entry + "\"\n")
                self.shouts += 1

                log.close()

            else:
                return

        except Exception as e:
            print("Error opening/reading from the file (" + self.filename + "):\n" + str(e))

    def write_bug_report(self, bug_dsc, bounty):
        try:
            log = open(self.filename, 'a')

            log.write("[Bug] " + '{:.2f}'.format(bounty) + self.timestamp() + " \"" + bug_dsc + "\"\n")
            self.bugs += 1

            log.close()

        except Exception as e:
            print("Error opening the file (" + self.filename + ").")
            print(str(e))

    def write_test_entry(self):
        try:
            log = open(self.filename, 'a')

            log.write("[Test] " + self.timestamp() + " " + input("Value of test: ") + " \"" +
                      input("Description of test: ") + "\"\n")
            self.tests += 1

            log.close()

        except Exception as e:
            print("Error opening the file (" + self.filename + ").")
            print(str(e))

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

            log.close()

        except Exception as e:
            print("Error opening the file:\n" + str(e))

        if not finalized:
            log_contents = ''

            try:
                log = open(self.filename)

                for line in log:
                    if line[0] == '[':
                        log_contents += line

                log.close()

            except Exception as e:
                print(str(e))

            invoice_string = '{:*^41}'.format(' Final Invoice ') + '\n' + \
                "Shout Wall Invoice - Week of {}\n".format(self.week_name) + \
                "Total amount requested: ${:.2f}\n".format(self.invoice) + \
                "PayPal email address: {}\n".format(Email) + \
                "Total shouts completed: {:3}\n".format(self.shouts) + \
                "Username(s) used: {}\n".format(", ".join(Usernames))

            if self.bugs > 0:
                invoice_string += "Bug Reports: " + str(self.bugs) + '\n'

            if self.tests > 0:
                invoice_string += "Shout Wall Tests: " + str(self.tests) + '\n'

            try:
                log = open(self.filename, 'w')

                log.write(invoice_string + '\n' + log_contents)
                print(invoice_string)

                log.close()

            except Exception as e:
                print("Error opening the file.")
                print(str(e))

        else:
            print("Log \'{}\' already finalized.".format(self.filename))

    def insert_lost_shouts(self, num):
        for _ in range(num):
            self.write_log_entry("-lost shout-")

    # Create a function to manage the script rather than having it all in main.

    def process_candi(self, candi):
        """
        Processes a single command.
        :param candi: the command
        :return: nothing
        """
        candi = candi.lower()

        # Accept either / or . as command markers, but only if there is something to read.
        # This is so blank strings don't piss off the whole program.
        if len(candi) > 0:
            if candi[0] == '/' or candi[0] == '.':
                if candi[1:5] == "help":
                    print("/bug: log a bug report\n" +
                          "/test: log a Shout Wall test attended\n" +
                          "/summary: refresh the statistics and display the summary\n" +
                          "/lost: insert a number of lines into the current log of lost shouts\n")

                elif candi[1:4] == "fin":
                    ShoutLog(last_week=True).finalize()

                elif candi[1:4] == "sum":
                    self.summarize()

                elif candi[1:4] == "bug":
                    bug = input("What's the bug? Tell me what's a-happenin'!\n")

                    if bug.lower() != "/cancel":
                        rate = float(input("What was the bounty on that bug's head? $"))
                        self.write_bug_report(bug, rate)

                elif candi[1:5] == "test":
                    self.write_test_entry()

                elif candi[1:5] == "lost":
                    number_lost = int(input("Insert how many lost shouts?\n"))
                    self.insert_lost_shouts(number_lost)

                else:
                    print("Command not recognized.")

            # Otherwise, treat the string as a shout.
            else:
                self.write_log_entry(candi)


if __name__ == "__main__":
    print("**************************************************************\n" +
          "Shout Wall Log Python Model 2.0")

    shoutLog = ShoutLog()
    print("Log file for " + shoutLog.week_name + ".")

    cmd = input(str(shoutLog.shouts) + "> ")
    while cmd != "/done":
        shoutLog.process_candi(cmd)
        cmd = input(str(shoutLog.shouts) + "> ")
