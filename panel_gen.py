#-----------------------------------------------------------------------#
#                                                                       #
# A call generator thing for the Rainier Panel switch at the            #
# Connections Museum, Seattle WA.                                       #
#                                                                       #
# Written by Sarah Autumn, 2017                                         #
# I have no idea what I'm even doing.                                   #
# This program assumes the following:                                   #
#       - You are at the museum.                                        #
#       - You have access to the Panel switch                           #
#       - Your name is Sarah Autumn                                     #
#                                                                       #
#-----------------------------------------------------------------------#

import time
import os 
import sys
import subprocess
from tabulate import tabulate
from numpy import random
from pathlib import Path
from pycall import CallFile, Call, Application

# Main class for calling lines. Contains all the essential vitamins and minerals.
# It's an important part of a balanced breakfast.
class Line():
    def __init__(self, ident):
        self.status = 0
#        self.orig = lines_loaded.pop() 
        self.term = self.p_term()
        self.timer = random.randint(4,20)
        self.ident = ident

    def set_timer(self):
        self.timer = random.randint(15,55)
        return self.timer

    def tick(self):
        # Decrement timers by 1 every second until it reaches 0
        # Also check status and call or hangup as necessary.

        self.timer -= 1
        if self.timer == 0:
            if self.status == 0:
                self.call()
            else:
                self.hangup()
        return self.timer

    def p_term(self):
        term_office = random.choice(panel.nxx, p=panel.trunk_load)      # Using weight, pick an office to call.
        term_station = random.randint(5000,5999)                        # Pick a random station that appears on our final frame.
        term = int(str(term_office) + str(term_station))                # And put it together.
        return term

    def call(self):
        # Dialing takes ~12.6 seconds. This should be somewhat consistent value because its done
        # by Asterisk / DAHDI. We're going to set a timer for call duration here, and then a few lines down,
        # we're gonna tell Asterisk to set its own wait timer to the same value - 10. This should give us a reasonable
        # buffer between the program's counter and whatever Asterisk is doing.

        self.timer= random.randint(20,60)                               # Reset the timer for the next go-around.

        c = Call('DAHDI/r6/wwwww%s' % self.term)                        # Call DAHDI, Group 6. Wait a second before dialing.
        a = Application('Wait', str(self.timer - 10))                   # Make Asterisk wait once the call is connected.
        cf = CallFile(c,a, user='asterisk', archive = True)             # Make the call file
        cf.spool()                                                      # and throw it in the spool

        self.status = 1                                                 # Set the status of the call to 1 (active)

    def hangup(self):
         # This isn't doing that much, since Asterisk is managing the hangup.
         # Really, it's not timed very well, since its just for show.
         # I'll have to come back to this and figure it out.

        self.timer = random.randint(10,45)                              # Set a timer to wait before another call starts.
        self.status = 0                                                 # Set the status of this call to 0.
        self.term = self.p_term()                                       # Pick a new termingating line. 
#        lines_loaded.insert(0,self.orig)
#        self.orig = lines_loaded.pop()
        if Path("/var/spool/asterisk/outgoing/" + str(self.term) + ".call").is_file():  # Delete the call file if there is one.
            os.remove("/var/spool/asterisk/outgoing/" + str(self.term) + ".call")       # Yep
        else:
            return

class Switch():                                                 # Lets make a switch!
    def __init__(self):
        self.kind = "panel"
        self.max_dialing = 6                                    # We are limited by the number of senders we have.
        self.max_calls = 5                                      # Max number of calls that can be in progres, dialing or not. Lower is safer.
        self.max_office = 1                                     # Load for panel intraoffice trunks...
        self.max_district = 0                                   # ....needs to equal 1 or numpy gets mad.
        self.max_5xb = .0                                       # Max trunks to 5XB. Currently not used.       
        self.max_1xb = .0                                       # Max trunks to 1XB. Currently not used.
        self.nxx = [722, 365]                                   # Office codes that can be dialed.
        self.trunk_load = [self.max_office, self.max_district]  # And put the trunk load together.

    def bullshit():
        # Insert bullshit
        return


# MAIN LOOP I GUESS
def main():

    try:
#       global lines_loaded                         # Not used here. Unnecessary.
        global panel                                # Create a variable. Has to be global for some reason.
        
#       with open('./lines.txt') as f:               # Open text file containing calling lines.
#           lines_loaded = f.read().splitlines()     # and write it to lines_available

        panel = Switch()                             # Create a switch and call it panel.

        line = [Line(n) for n in range (panel.max_calls)]       # Make lines.
        while True:                                             # While always
            for n in line:                                      # For as many lines as there are.
                n.tick()                                        # Tick the timer, and do the things.
    
            # Output handling. Clear screen, draw table, sleep 1, repeat ... 
            os.system('clear')
            table = [[n.ident, n.term, n.timer, n.status] for n in line]
            print " ------------------------------------------"
            print "|                                          |"
            print "|  Rainier Full Mechanical Call Simulator  |"
            print "|__________________________________________|\n\n"
            print tabulate(table, headers=["ident", "term", "tick", "status"], tablefmt="pipe") 

            ast_out = subprocess.check_output(['asterisk', '-rx', 'core show channels'])
            print "\n\n" + ast_out

            time.sleep(1)

    # The below is here in an attempt to gracefully handle keyboard interrupts. 
    # At least let it down easy.

    except KeyboardInterrupt:
            print ""
            print "Shutdown requested...cleaning up Asterisk spool"
            os.system("rm /var/spool/asterisk/outgoing/*.call")
    except Exception:
           traceback.print_exc(file=sys.stdout)
           sys.exit(0)

if __name__ == "__main__":
    main()
