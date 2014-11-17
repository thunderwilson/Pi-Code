import Tkinter
import csv
import pickle
import sys
import psutil
import os
import subprocess


class GUI(Tkinter.Tk):
    """
    Main graphical user interface for behav_gui. Used to input subject ID and
    timepoint.
    """
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.wm_title("GUI")

        label_1 = Tkinter.Label(self, text="Subject ID")
        label_1.grid(row=1, column=1)
        self.sub_input = Tkinter.StringVar()
        entry_1 = Tkinter.Entry(self, bd=5, textvariable=self.sub_input)
        entry_1.grid(row=1, column=2)

        label_2 = Tkinter.Label(self, text="Timepoint")
        label_2.grid(row=2, column=1)
        self.tp_input = Tkinter.IntVar()
        entry_2 = Tkinter.Entry(self, bd=5, textvariable=self.tp_input)
        entry_2.grid(row=2, column=2)

        label_3 = Tkinter.Label(self, text="BL: 1, 12: 3, 24: 4")
        label_3.grid(row=3, column=2)

        label_4 = Tkinter.Label(self, text="")
        label_4.grid(row=4, column=2)

        label_5 = Tkinter.Button(self, text="Done", command=self.close_window)
        label_5.grid(row=5, column=1, columnspan=2)

#        self.bind("<Return>", self.close_window)

        self.mainloop()

    def close_window(self, *args):
        """ Closes the GUI window."""
        del args
        self.destroy()


class OverwriteButton(Tkinter.Tk):
    """
    Creates a window with query (Do you wish to overwrite) and two buttons, Yes
    and No. Each sets response attribute to respective string.
    """
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.wm_title("Duplicate")
        self.response = "No"

        label_1 = Tkinter.Label(self,
                                text="Duplicate ID and TP given. Overwrite?")
        label_1.grid(row=1, column=1, columnspan=5)

        button_1 = Tkinter.Button(self, text="Yes", command=self.respond_yes)
        button_1.grid(row=2, column=2, columnspan=1)

        button_2 = Tkinter.Button(self, text="No", command=self.respond_no)
        button_2.grid(row=2, column=4, columnspan=1)

        self.mainloop()

    def respond_yes(self):
        """ Closes the GUI window and sets response to Yes."""
        self.response = "Yes"
        self.destroy()

    def respond_no(self):
        """ Closes the GUI window and sets response to No."""
        self.response = "No"
        self.destroy()


class ContinueButton(Tkinter.Tk):
    """
    Creates a window with inputted label and three buttons, Continue, Restart,
    and Quit. Each sets response attribute to respective string.
    """
    def __init__(self, label):
        Tkinter.Tk.__init__(self)
        self.wm_title("Continue")
        self.response = "Quit"

        label_1 = Tkinter.Label(self, text=label)
        label_1.grid(row=1, column=1, columnspan=5)

        label_2 = Tkinter.Label(self, text="Do you wish to move on?")
        label_2.grid(row=2, column=1, columnspan=5)

        button_1 = Tkinter.Button(self, text="Continue",
                                  command=self.continue_)
        button_1.grid(row=3, column=1, columnspan=1)

        button_2 = Tkinter.Button(self, text="Restart", command=self.restart)
        button_2.grid(row=3, column=3, columnspan=1)

        button_3 = Tkinter.Button(self, text="Quit", command=self.close_window)
        button_3.grid(row=3, column=5, columnspan=1)

        self.mainloop()

    def continue_(self):
        """ Closes the GUI window."""
        self.response = "Continue"
        self.destroy()

    def restart(self):
        """ Closes the GUI window."""
        self.response = "Restart"
        self.destroy()

    def close_window(self):
        """ Closes the GUI window."""
        self.response = "Quit"
        self.destroy()


class RetryButton(Tkinter.Tk):
    """
    Creates a window with one inputted label and two buttons- Restart and Quit.
    Each sets response attribute to respective string.
    """
    def __init__(self, label):
        Tkinter.Tk.__init__(self)
        self.wm_title("Problem")
        self.response = "Restart"

        label_1 = Tkinter.Label(self, text=label)
        label_1.grid(row=1, column=1, columnspan=5)

        button_1 = Tkinter.Button(self, text="Restart", command=self.restart)
        button_1.grid(row=2, column=1, columnspan=1)

        button_2 = Tkinter.Button(self, text="Quit", command=self.quit_)
        button_2.grid(row=2, column=5, columnspan=1)

        self.mainloop()

    def restart(self):
        """ Closes the GUI window and sets response to Restart."""
        self.response = "Restart"
        self.destroy()

    def quit_(self):
        """ Closes the GUI window and sets response to Quit."""
        self.response = "Quit"
        self.destroy()


class LabelMaker(Tkinter.Tk):
    """
    Creates a window with an inputted title and label and a close button
    labeled "Okay".
    """
    def __init__(self, title, label):
        Tkinter.Tk.__init__(self)
        self.wm_title(title)
        label_1 = Tkinter.Label(self, text=label)
        label_1.grid(row=1, column=1, columnspan=5)

        button_1 = Tkinter.Button(self, text="Okay", command=self.close_window)
        button_1.grid(row=2, column=3, columnspan=1)

        self.mainloop()

    def close_window(self):
        """ Closes the GUI window."""
        self.destroy()


def get_curr_order(task_order_csv, task_order, subject_id, subject_tp, tp_dict,
                   col_beg, col_end, set_overwrite, all_tasks):
    """
    Takes subject ID, timepoints, organization of task counterbalancing, and
    current list of task counterbalances (from csv) and returns correct order
    for given subject and timepoint, as well as updates list of lists (from
    csv). How can I clean up inputs? There are too many already and I'm
    considering one more.
    """
    with open(task_order_csv, 'r') as file_:
        task_file = list(csv.reader(file_, delimiter=','))

    subjects = [row[0] for row in task_file]

    if subject_tp in tp_dict.keys():
        curr_order_list = task_order[tp_dict.get(subject_tp)]
    else:
        top = RetryButton(str(subject_tp) + " is not an acceptable timepoint.")
        if top.response == "Restart":  # <-- Is there a cleaner way to do this?
            run_script()
            sys.exit()
        else:
            sys.exit()

    # Find row corresponding to subject in csv. If subject is new, append an
    # empty row to fill in.
    try:
        subject_pos = subjects.index(subject_id)
    except Exception:  # <-- Which exception can I use to pass without error?
        subject_pos = len(subjects)
        task_file.append([""] * len(task_file[0]))

    # If correct position in spreadsheet is empty, fill in with correct list.
    # Else, offer option to overwrite or quit.
    curr_order = curr_order_list[(subject_pos-1) % len(curr_order_list)]
    if not task_file[subject_pos][col_beg[tp_dict.get(subject_tp)]]:
        task_file[subject_pos][0] = subject_id
        task_file[subject_pos][col_beg[tp_dict.get(subject_tp)]:
                               col_end[tp_dict.get(subject_tp)]] = curr_order
        if all_tasks is True:
            LabelMaker("Order", "The current order is: " +
                       ", ".join(curr_order))
        return curr_order, task_file, set_overwrite
    else:
        if set_overwrite == 0:
            top = OverwriteButton()
            if top.response == "Yes":
                set_overwrite = 1
                if all_tasks is True:
                    LabelMaker("Order", "The current order is: " +
                               ", ".join(curr_order))
                return curr_order, task_file, set_overwrite
            else:
                sys.exit()
        else:
            return curr_order, task_file, set_overwrite


def safe_name(process):
    """
    Check for names of processes in psutil.process_iter and, if
    permission denied, returns "None".
    """
    try:
        return process.name
    except Exception:  # <-- Which exception can I use to pass without error?
        return "None"


def execute_file(run_file):
    """
    Opens E-Run (or other specified) file and waits for E-Run to no longer be
    in current processes before continuing.
    """
    if os.name == 'nt':
        subprocess.Popen(run_file, shell=True)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', run_file))
    open_proc = True

    while open_proc is True:
        data = list(psutil.process_iter())
        if any(["gedit" in safe_name(Proc) for Proc in data]):
            open_proc = True
        else:
            open_proc = False


def run_script():
    """
    Runs full script (opens GUI windows, updates csvs, and opens E-Run files).
    """
    task_order_csv = "/home/code/behav_gui/task_order.csv"
    set_overwrite = 0
    input_window = GUI()
    subject_id = input_window.sub_input.get()
    subject_tp = input_window.tp_input.get()

    with open('/home/code/behav_gui/task_order.pickle') as file_:
        [task_order, tp_dict, col_beg, col_end] = pickle.load(file_)

    with open('/home/code/behav_gui/each_order.pickle') as file_:
        each_order = pickle.load(file_)

    with open('/home/code/behav_gui/task_info.pickle') as file_:
        task_info = pickle.load(file_)

    with open('/home/code/behav_gui/file_dict.pickle') as file_:
        file_dict = pickle.load(file_)

    all_tasks = True
    curr_order, task_file, set_overwrite = get_curr_order(task_order_csv,
                                                          task_order,
                                                          subject_id,
                                                          subject_tp,
                                                          tp_dict,
                                                          col_beg,
                                                          col_end,
                                                          set_overwrite,
                                                          all_tasks)
    with open(task_order_csv, 'w') as file_:
        file_ = csv.writer(file_)
        for row in task_file:
            file_.writerow(row)

    # Loop through tasks, reading csv/getting current task type for each and
    # adding to lists of lists ind_ord (task order or type), ind_file (read-in
    # csv as list of lists), and run_file (E-Run file corresponding to specific
    # task order or type).
    ind_ord = [[] for i in curr_order]
    ind_file = [[] for i in curr_order]
    run_file = [[] for i in curr_order]
    all_tasks = False

    for a, task in enumerate(curr_order):
        task_order_csv = task_info.get(task).get("file")
        task_order = each_order.get(task)
        col_beg = task_info.get(task).get("col_beg")
        col_end = task_info.get(task).get("col_end")
        ind_ord[a], ind_file[a], set_overwrite = get_curr_order(task_order_csv,
                                                                task_order,
                                                                subject_id,
                                                                subject_tp,
                                                                tp_dict,
                                                                col_beg,
                                                                col_end,
                                                                set_overwrite,
                                                                all_tasks)
        with open(task_order_csv, 'w') as file_:
            file_ = csv.writer(file_)
            for row in ind_file[a]:
                file_.writerow(row)

        run_file[a] = file_dict.get(task).get(ind_ord[a][0])

    # Loop through tasks and execute files in order. Ask to continue after each
    # task finishes.
    for iTask in range(len(run_file)):
        response = "Restart"
        while response == "Restart":
            execute_file(run_file[iTask])

            # When run_file is closed, move on to next.
            cont = ContinueButton(curr_order[iTask] + " is complete.")
            response = cont.response

            if response == "Quit":
                sys.exit()

    LabelMaker("Congrats!", "Congratulations. You're done.")


if __name__ == "__main__":
    run_script()


import pickle


task_order = [[['AX', 'RISE', 'Kirby', 'Decimal'],
               ['AX', 'RISE', 'Decimal', 'Kirby'],
               ['AX', 'Kirby', 'RISE', 'Decimal'],
               ['AX', 'Kirby', 'Decimal', 'RISE'],
               ['AX', 'Decimal', 'RISE', 'Kirby'],
               ['AX', 'Decimal', 'Kirby', 'RISE'],
               ['RISE', 'AX', 'Kirby', 'Decimal'],
               ['RISE', 'AX', 'Decimal', 'Kirby'],
               ['RISE', 'Kirby', 'AX', 'Decimal'],
               ['RISE', 'Kirby', 'Decimal', 'AX'],
               ['RISE', 'Decimal', 'AX', 'Kirby'],
               ['RISE', 'Decimal', 'Kirby', 'AX'],
               ['Kirby', 'AX', 'RISE', 'Decimal'],
               ['Kirby', 'AX', 'Decimal', 'RISE'],
               ['Kirby', 'RISE', 'AX', 'Decimal'],
               ['Kirby', 'RISE', 'Decimal', 'AX'],
               ['Kirby', 'Decimal', 'AX', 'RISE'],
               ['Kirby', 'Decimal', 'RISE', 'AX'],
               ['Decimal', 'AX', 'RISE', 'Kirby'],
               ['Decimal', 'AX', 'Kirby', 'RISE'],
               ['Decimal', 'RISE', 'AX', 'Kirby'],
               ['Decimal', 'RISE', 'Kirby', 'AX'],
               ['Decimal', 'Kirby', 'AX', 'RISE'],
               ['Decimal', 'Kirby', 'RISE', 'AX']],
              [['RISE', 'AX', 'Kirby', 'Decimal'],
               ['RISE', 'AX', 'Decimal', 'Kirby'],
               ['RISE', 'Kirby', 'AX', 'Decimal'],
               ['RISE', 'Kirby', 'Decimal', 'AX'],
               ['RISE', 'Decimal', 'AX', 'Kirby'],
               ['RISE', 'Decimal', 'Kirby', 'AX'],
               ['Decimal', 'RISE', 'AX', 'Kirby'],
               ['Decimal', 'RISE', 'Kirby', 'AX'],
               ['Decimal', 'AX', 'RISE', 'Kirby'],
               ['Decimal', 'AX', 'Kirby', 'RISE'],
               ['Decimal', 'Kirby', 'RISE', 'AX'],
               ['Decimal', 'Kirby', 'AX', 'RISE'],
               ['AX', 'RISE', 'Kirby', 'Decimal'],
               ['AX', 'RISE', 'Decimal', 'Kirby'],
               ['AX', 'Kirby', 'RISE', 'Decimal'],
               ['AX', 'Kirby', 'Decimal', 'RISE'],
               ['AX', 'Decimal', 'RISE', 'Kirby'],
               ['AX', 'Decimal', 'Kirby', 'RISE'],
               ['Kirby', 'RISE', 'AX', 'Decimal'],
               ['Kirby', 'RISE', 'Decimal', 'AX'],
               ['Kirby', 'AX', 'RISE', 'Decimal'],
               ['Kirby', 'AX', 'Decimal', 'RISE'],
               ['Kirby', 'Decimal', 'RISE', 'AX'],
               ['Kirby', 'Decimal', 'AX', 'RISE']],
              [['Kirby', 'AX', 'RISE', 'Decimal'],
               ['Kirby', 'AX', 'Decimal', 'RISE'],
               ['Kirby', 'RISE', 'AX', 'Decimal'],
               ['Kirby', 'RISE', 'Decimal', 'AX'],
               ['Kirby', 'Decimal', 'AX', 'RISE'],
               ['Kirby', 'Decimal', 'RISE', 'AX'],
               ['Decimal', 'Kirby', 'AX', 'RISE'],
               ['Decimal', 'Kirby', 'RISE', 'AX'],
               ['Decimal', 'AX', 'Kirby', 'RISE'],
               ['Decimal', 'AX', 'RISE', 'Kirby'],
               ['Decimal', 'RISE', 'Kirby', 'AX'],
               ['Decimal', 'RISE', 'AX', 'Kirby'],
               ['AX', 'Kirby', 'RISE', 'Decimal'],
               ['AX', 'Kirby', 'Decimal', 'RISE'],
               ['AX', 'RISE', 'Kirby', 'Decimal'],
               ['AX', 'RISE', 'Decimal', 'Kirby'],
               ['AX', 'Decimal', 'Kirby', 'RISE'],
               ['AX', 'Decimal', 'RISE', 'Kirby'],
               ['RISE', 'Kirby', 'AX', 'Decimal'],
               ['RISE', 'Kirby', 'Decimal', 'AX'],
               ['RISE', 'AX', 'Kirby', 'Decimal'],
               ['RISE', 'AX', 'Decimal', 'Kirby'],
               ['RISE', 'Decimal', 'Kirby', 'AX'],
               ['RISE', 'Decimal', 'AX', 'Kirby']]]

tp_dict = {1: 0,
           3: 1,
           4: 2,
           }

col_beg = [1, 5, 9]
col_end = [5, 9, 13]

with open('/home/code/behav_gui/task_order.pickle', 'w') as fo:
    pickle.dump([task_order, tp_dict, col_beg, col_end], fo)

each_order = {"RISE": [[['A'], ['A'], ['B'], ['B'], ['C'], ['C']],
                       [['B'], ['C'], ['A'], ['C'], ['A'], ['B']],
                       [['C'], ['B'], ['C'], ['A'], ['B'], ['A']]],
              "AX": [[['1']],
                     [['1']],
                     [['1']]],
              "Kirby": [[['Messy first'], ['Rounded first']],
                        [['Rounded first'], ['Messy first']],
                        [['Messy first'], ['Rounded first']]],
              "Decimal": [[['Messy first'], ['Rounded first']],
                          [['Rounded first'], ['Messy first']],
                          [['Messy first'], ['Rounded first']]],
              }

with open('/home/code/behav_gui/each_order.pickle', 'w') as fo:
    pickle.dump(each_order, fo)

task_info = {"RISE": {"file": "/home/code/behav_gui/r_trialsheet.csv",
                      "col_beg": [1, 2, 3],
                      "col_end": [2, 3, 4],
                      },
             "AX": {"file": "/home/code/behav_gui/a_trialsheet.csv",
                    "col_beg": [1, 2, 3],
                    "col_end": [2, 3, 4]},
             "Kirby": {"file": "/home/code/behav_gui/k_trialsheet.csv",
                       "col_beg": [1, 2, 3],
                       "col_end": [2, 3, 4]},
             "Decimal": {"file": "/home/code/behav_gui/d_trialsheet.csv",
                         "col_beg": [1, 2, 3],
                         "col_end": [2, 3, 4]},
             }

with open('/home/code/behav_gui/task_info.pickle', 'w') as fo:
    pickle.dump(task_info, fo)

file_dict = {"RISE": {"A": "/home/code/behav_gui/a.txt",
                      "B": "/home/code/behav_gui/b.txt",
                      "C": "/home/code/behav_gui/c.txt",
                      },
             "AX": {"1": "/home/code/behav_gui/ax.txt"},
             "Kirby": {"Messy first": "/home/code/behav_gui/mfk.txt",
                       "Rounded first": "/home/code/behav_gui/rfk.txt",
                       },
             "Decimal": {"Messy first": "/home/code/behav_gui/mfd.txt",
                         "Rounded first": "/home/code/behav_gui/rfd.txt",
                         },
             }

with open('/home/code/behav_gui/file_dict.pickle', 'w') as fo:
    pickle.dump(file_dict, fo)
