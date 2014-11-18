prog_draft is a basic implementation of bluetooth scanning and data logging.

Takes a mock daily roster "daily.csv" (as per TANDA rostering) and works out who is working today.

It takes note of their start time and end time for use in the scanning algorithm (hence why the daily.csv only has the first 4 colums, the rest are ignored).

Currently the program just scans for everyone in the list at once and logs the changes in state in the corresponding *name*.csv file rather than using the start and finish times to decide when to scan. Thats this weeks job.

This file is then stored locally ready to be uploaded.

Currently using the bluetooth address of my phone and two fake addresses for testing. Only the Tom.csv file shows actual test data. Have ordered parts for the Bluetooth 'smart' badges which should arrive sometime next week. 

Running code on linux laptop which is setup the same as the Rasperry Pi (the Pi is not very powerful and would be a bitch to develop on).

