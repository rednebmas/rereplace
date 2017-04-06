import sys
import select

if select.select([sys.stdin,],[],[],0.0)[0]:
        print("Have data!")
else:
        print("No data")
