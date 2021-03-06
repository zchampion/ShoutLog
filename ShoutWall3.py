"""
    Project:            Shout Wall Log Program
    Programmer:         Zachary Champion
    Python Version:     3.5
"""
from datetime import date, datetime, timedelta
import os

# User's username and PayPal email address, only used for putting together the invoice.
default_username = "TheFluffyQ"
Email = "Belgarion270@gmail.com"
log_dir_string = os.path.dirname(os.path.realpath(__file__)) + "/Shout Logs/"


class ShoutLog:
    def __init__(self, weeks_back=0, pay_rate=0.10):
        self.rate = pay_rate
        self.week_name = self.get_week_name(weeks_back)

        self.filename = log_dir_string + self.week_name + '.klat'

        self.usernames = self.load_usernames()
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
                          '=' * 37 + '\n')
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

                if len(line_items) > 0 and line_items[0].lower() == "[bug]":
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

                if len(line_items) > 0 and line_items[0] == "[Test]":
                    invoice += float(line_items[4])

            log.close()

        except Exception as e:
            print("Error getting the \"test invoice\" from the file (" + self.filename + ").")
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

    def write_username(self, username):
        try:
            log = open(self.filename, 'a')
            log.write("[USERNAME] {}\n".format(username))
            log.close()

            self.usernames.append(username)

        except Exception as e:
            print("Error opening the file (" + self.filename + ").")
            print(str(e))

    def load_usernames(self):
        usernames = [default_username]

        try:
            log = open(self.filename)

            for line in log:
                if line.startswith("[USERNAME]"):
                    usernames.append(line.split()[1])

        except Exception as e:
            print("Error opening the file (" + self.filename + ").")
            print(str(e))

        return usernames

    def summarize(self):
        self.shouts = self.count_shouts()
        self.bugs = self.count_bug_reports()
        self.tests = self.count_tests()
        self.invoice = self.get_invoice()
        print('\n' + str(self) + '\n')

    def finalize(self):
        finalized = False

        try:
            log = open(self.filename)

            for line in log:
                if line == '{:*^41}\n'.format(' Final Invoice '):
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
                "Username(s) used: {}\n".format(", ".join(self.usernames))

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

    def finalize_combined(self, weeks_back=1):
        # need as an argument the number of weeks back to make a combined invoice for
        # get the first day from the name of the furthest back log, start the name of the invoice
        # combine it with the last day from the last log - last week - finish the name of the invoice
        #
        # with a decrementing loop for each log (n weeks back until 1 week back):
        #     check to make sure that the log isn't already finalized. If one is, ask the user if they want to continue.
        #     Otherwise, get the totals for the log and add it to a total.
        #     mark the log as finalized
        #
        # print total invoice to the last log file

        combined_name = self.get_week_name(weeks_back).split('-')[0] + '-' + self.get_week_name(1).split('-')[1]
        invoice, shouts, bugs, tests = 0, 0, 0, 0
        names = []
        fin = False

        for week in range(weeks_back, 0, -1):
            week_log = ShoutLog(weeks_back=week)

            invoice += week_log.invoice
            shouts += week_log.shouts
            bugs += week_log.bugs
            tests += week_log.tests
            names += week_log.usernames
            names = list(set(names))

            with open(week_log.filename) as candi:
                for line in candi:
                    if line == '{:*^41}\n'.format(' Final Invoice '):
                        fin = True

        if fin and not input("One or more of the logs is already finalized.\nContinue?  ").upper().startswith("Y"):
            print("Cancelling combined finalization.")

        else:
            invoice_string = '{:*^41}'.format(' Final Invoice ') + '\n' + \
                             "Shout Wall Combined Invoice - Weeks of {}\n".format(combined_name) + \
                             "Total amount requested: ${:.2f}\n".format(invoice) + \
                             "PayPal email address: {}\n".format(Email) + \
                             "Total shouts completed: {:3}\n".format(shouts) + \
                             "Username(s) used: {}\n".format(", ".join(names))

            if self.bugs > 0:
                invoice_string += "Bug Reports: " + str(self.bugs) + '\n'

            if self.tests > 0:
                invoice_string += "Shout Wall Tests: " + str(self.tests) + '\n'

            try:
                log_contents = ""
                curr_log = ShoutLog(weeks_back=1)

                with open(curr_log.filename) as backup:
                    for line in backup:
                        if line[0] == '[':
                            log_contents += line

                with open(curr_log.filename, 'w') as log:
                    log.write(invoice_string + '\n' + log_contents)
                    print(invoice_string)

            except Exception as e:
                print("Something went wrong with opening the file.\n" + str(e))

    def insert_lost_shouts(self, num):
        for _ in range(num):
            self.write_log_entry("-lost shout-")

    def read_log(self):

        try:
            log = open(self.filename)

            print()
            for line in log:
                print(line.rstrip())
            print()

            log.close()

        except Exception as e:
            print("Error reading the file \"{}\".".format(self.filename))
            print(str(e))

    def process_candi(self, candi):
        """
        Processes a single command.
        :param candi: the command
        :return: nothing
        """
        candi = candi.lower()

        # Accept / as command markers, but only if there is something to read.
        # This is so blank strings don't piss off the whole program.
        if len(candi) > 0 and candi[0] == '/':
            if candi[1:5] == "help":
                print("/bug: log a bug report\n" +
                      "/test: log a Shout Wall test attended\n" +
                      "/summary: refresh the statistics and display the summary\n" +
                      "/lost: insert a number of lines into the current log of lost shouts\n" +
                      "/addu: add a used username to include in the final invoice\n" +
                      "/read: read the shout wall from n weeks ago. Default is current week")

            elif candi[1:4] == "fin":
                if len(candi) == 4:
                    ShoutLog(weeks_back=1).finalize()

                else:
                    ShoutLog(weeks_back=1).finalize_combined(int(candi.split()[1]))

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

            elif candi[1:5] == "addu":
                self.write_username(input("Username to add: "))

            elif candi[1:5] == "read":
                # Ask the user how many weeks back to look for the shout log of, then make a ShoutLog
                # for that week and read the file.
                candi = candi.split()

                if len(candi) > 1:
                    try:
                        wb = int(candi[1])

                    except Exception as e:
                        print("Invalid command: " + str(e))
                        wb = int(input("How many weeks back do you want to read? "))

                else:
                    wb = int(input("How many weeks back do you want to read? "))

                ShoutLog(weeks_back=wb).read_log()

            else:
                print("Command not recognized.")

        # Otherwise, treat the string as a shout.
        else:
            self.write_log_entry(candi)


if __name__ == "__main__":
    print("**************************************************************\n" +
          "Shout Wall Log Python Model 2.0")

    shoutLog = ShoutLog(weeks_back=1 if date.today().weekday() == 6 and datetime.now().hour == 0 else 0)
    # Compensates for the fact that my client uses Pacific Time & uses the appropriate log for that.
    print("Log file for " + shoutLog.week_name + ".")

    cmd = input("<{:03d}>  ".format(shoutLog.shouts + 1))
    while cmd != "/done":
        shoutLog.process_candi(cmd)
        cmd = input("<{:03d}>  ".format(shoutLog.shouts + 1))
