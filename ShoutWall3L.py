"""
    Project:            Shout Wall Log Program (Linux)
    Programmer:         Zachary Champion
    Python Version:     3.5
"""
from datetime import date, datetime, timedelta

# User's username and PayPal email address, only used for putting together the invoice.
Username = "TheFluffyQ"
Email = "Belgarion270@gmail.com"
os_dir_string = "/home/queen/Programs/shoutrec/Shout Logs/"


class ShoutLog:
    def __init__(self, last_week=False, pay_rate=0.10):
        self.rate = pay_rate
        self.week_name = self.get_week_name(
            1 if date.today().weekday() == 6 and datetime.now().hour == 0 or last_week else 0)
        # Look for "last week" if Pacific time is still in last week relative to my time.
        self.filename = os_dir_string + self.week_name + '.klat'
        self.shouts = self.count_shouts()
        self.bugs = self.count_bug_reports()
        self.tests = self.count_tests()
        self.invoice = self.get_invoice()

    def __str__(self):
        string = \
            "Log:            " + self.week_name + '\n' + \
            "Shouts:         " + str(self.shouts) + '{: >13}'.format(str(self.shouts/5.0) + '%\n')

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

        except:
            print("Error opening the file \"" + self.filename + "\"")
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

        except:
            print("Error counting the bug reports in file \"{}\".".format(self.filename))

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

        except:
            print("Error counting the tests in file \"{}\".".format(self.filename))

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

        except:
            print("Error opening the file (" + self.filename + ").")

    def write_test_entry(self):
        try:
            log = open(self.filename, 'a')

            log.write("[Test] " + self.timestamp() + " " + input("Value of test: ") + " \"" +
                      input("Description of test: ") + "\"\n")
            self.tests += 1

            log.close()

        except:
            print("Error opening the file (" + self.filename + ").")

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
                "Username: {}\n".format(Username) + \
                "Paypal Email: {}\n".format(Email) + \
                "Shouts Completed: {:3}".format(self.shouts) + '\n'

            if self.bugs > 0:
                invoice_string += "Bug Reports: " + str(self.bugs) + '\n'

            if self.tests > 0:
                invoice_string += "Shout Wall Tests: " + str(self.tests) + '\n'

            invoice_string += \
                "Paypal Amount: $" + '{:.2f}'.format(self.invoice) + '\n' + \
                "*" * 41

            try:
                log = open(self.filename, 'w')

                log.write(invoice_string + '\n' + log_contents)
                print(invoice_string)

                log.close()

            except:
                print("Error opening the file.")

        else:
            print("Log \'{}\' already finalized.".format(self.filename))

    def insert_lost_shouts(self, num):
        for _ in range(num):
            self.write_log_entry("-lost shout-")

    # Create a function to manage the script rather than having it all in main.


if __name__ == "__main__":
    print("**************************************************************\n" +
          "Shout Wall Log Python Model 2.0")

    shoutLog = ShoutLog()
    print("Log file \'" + shoutLog.week_name + ".klat" + "\'. Shouts: " + str(shoutLog.shouts) + '\n')

    cmd = input("> ")
    while cmd != "/done":

        if cmd.lower() == "/log":
            session = shoutLog.shouts

            prompt = ""
            if (session + 1) % 5 == 0:
                if (session + 1) % 10 == 0:
                    prompt += '0'
                else:
                    prompt += '5'

            else:
                prompt += '>'

            prompt += '> '

            log_cmd = input(prompt)
            while log_cmd == "":
                log_cmd = input(prompt)

            while log_cmd.lower() != "/done":
                shoutLog.write_log_entry(log_cmd)
                session += 1

                prompt = ""
                if (session + 1) % 5 == 0:

                    if (session + 1) % 10 == 0:
                        prompt += '0'
                    else:
                        prompt += '5'

                else:
                    prompt += '>'

                prompt += '> '

                log_cmd = input(prompt)
                while log_cmd == "":
                    log_cmd = input(prompt)

        elif cmd.lower() == "/bug":
            bug = input("What's the bug? Tell me what's a-happenin'!\n")

            if bug.lower() != "/cancel":
                rate = float(input("What was the bounty on that bug's head? $"))
                shoutLog.write_bug_report(bug, rate)

        elif cmd.lower() == "/test":
            shoutLog.write_test_entry()

        elif cmd.lower() == "/summary" or cmd.lower() == "/sum":
            shoutLog.summarize()

        elif cmd.lower() == "/help" or cmd.lower() == "/cmd":
            print(
                "/log: write a shout log entry\n" +
                "/bug: log a bug report\n" +
                "/test: log a Shout Wall test attended\n" +
                "/summary: refresh the statistics and display the summary\n" +
                "/lost: insert a number of lines into the current log of lost shouts\n")

        elif cmd.lower() == "/finalize" or cmd.lower() == "/fin":
            last_shoutLog = ShoutLog(last_week=True)
            last_shoutLog.finalize()

        elif cmd.lower() == "/lost":
            number_lost = int(input("Insert how many lost shouts?\n"))
            shoutLog.insert_lost_shouts(number_lost)

        else:
            print("Command not recognized.")

        cmd = input("\n> ")
