#!/usr/bin/env python
# encoding: utf-8

import npyscreen
import curses


def terminal_dimensions():
    return curses.initscr().getmaxyx()


class Box(npyscreen.BoxTitle):
    def resize(self):
        self.max_height = int(0.73 * terminal_dimensions()[0])


class MainWindow(npyscreen.FormWithMenus):
    def create(self):
        reg = []
        for _i in range(16):    # Should really use reset functions.
            reg.append(0)
        stack = []
        for _i in range(3):    # Should really use reset functions.
            stack.append(0)

        self.show_atx = 0
        self.show_aty = 0
        self.keypress_timeout = 10
        # Bounding boxes
        _box_core = self.add(Box, name="", editable=False, relx=1, rely=1,
                             max_width=20, max_height=5)

        self.accumulator = self.add(npyscreen.TitleFixedText, relx=2, rely=2,
                                    use_two_lines=False, begin_entry_at=4,
                                    editable=False, name="ACC", value='0000')
        self.nextrely -= 1
        self.carry = self.add(npyscreen.TitleFixedText, use_two_lines=False,
                              begin_entry_at=3, relx=12, editable=False,
                              name="CY", value='0', max_length=1)
        self.nextrely += 1

        self.crb = self.add(npyscreen.TitleFixedText, use_two_lines=False,
                            begin_entry_at=4, editable=False,
                            name="CRB", value='0')
        self.nextrely -= 1
        self.pc = self.add(npyscreen.TitleFixedText, use_two_lines=False,
                           begin_entry_at=3, editable=False, relx=10,
                           name="PC", value='0')

        self.nextrely += 1
        self.add(npyscreen.Textfield, name="registers", editable=False,
                 value="       REGISTERS", color='GOOD')
        for _i in range(0, 16, 2):
            if _i < 10:
                j = " " + str(_i)
                k = " " + str(_i + 1)
            else:
                j = str(_i)
                k = str(_i + 1)
            reg[_i] = self.add(npyscreen.TitleFixedText, use_two_lines=False,
                               begin_entry_at=9, editable=False,
                               name="RP"+str(int(_i/2)) + " " + j,
                               value='0000')
            self.nextrely -= 1
            reg[_i+1] = self.add(npyscreen.TitleFixedText, use_two_lines=False,
                                 begin_entry_at=5, editable=False,
                                 relx=17, name=str(k), value='0000')
        self.nextrely += 1
        self.add(npyscreen.Textfield, name="stack", editable=False,
                 value="         STACK", color='GOOD')
        for _i in range(3):
            stack[_i] = self.add(npyscreen.TitleFixedText, use_two_lines=False,
                                 begin_entry_at=5, editable=False,
                                 name=str(_i), value='0000 0000 0000')

        # The menus are created here.
        self.m1 = self.add_menu(name="Main Menu", shortcut="^M")
        self.m1.addItemsFromList([
                ("Exit Application", self.exit_application, "X"),
        ])

    def exit_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def while_waiting(self):
        self.accumulator.value = str(int(self.accumulator.value) + 1)
        self.display()


class App(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainWindow, name='Pyntel4004')


if __name__ == "__main__":
    app = App().run()
