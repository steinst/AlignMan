from tkinter import *
from tkinter import messagebox
import tkinter as tk
import argparse
import sqlite3
import sys

# setja cancel í laga texta reitinn
# Setja fídus sem getur lesið inn alignments svo hægt sé að skoða þau
# setja fídus til að bera saman alignments - birta tvö hlið við hlið og hafa sameiginleg í öðrum lit en þau sem eru stök
# skoða athugasemdir Hjalta og bregðast við þeim


class EditSentence:
    def __init__(self, canvas):
        global current_pair_id
        working_id, src_sent, trg_sent, conns = select_alignment(current_pair_id, False)

        self.board = Toplevel()
        self.board.title("Edit sentences")

        self.sentSrcText = Entry(self.board, font=('Arial', 16), width=200)
        self.sentSrcText.grid(row=1, column=1)
        self.sentSrcText.insert(0, src_sent)
        self.sentTrgText = Entry(self.board, font=('Arial', 16), width=200)
        self.sentTrgText.grid(row=2, column=1)
        self.sentTrgText.insert(1, trg_sent)

        updateButton = Button(self.board, text='Update sentences', command=self.update_sentences)
        updateButton.grid(row=4, column=1)
        closeButton = Button(self.board, text='Close Window', command=self.close)
        closeButton.grid(row=5, column=1)


    def close(self):
        deleteAlignments()
        updateCanvas()
        self.board.destroy()


    def update_sentences(self): #src_sent, trg_sent
        global current_pair_id
        global conn

        try:
            updating = "UPDATE ALIGNMENTS SET src_sentence = '{}', trg_sentence = '{}' WHERE id = {}".format(self.sentSrcText.get().replace("'", "''"), self.sentTrgText.get().replace("'", "''"), str(current_pair_id))
            c.execute(updating)
            conn.commit()
        except Exception as e:
            print(e)

        try:
            updating = "UPDATE ALIGNMENTS SET alignments_u1 = NULL, alignments_u2 = NULL, done1 = 0, done2 = 0 WHERE id = {}".format(str(current_pair_id))
            c.execute(updating)
            conn.commit()
        except Exception as e:
            print(e)


class WordBox:
    def __init__(self, srcBool, text, wNumber):
        self.text = text
        self.src = srcBool
        self.xPos = 0
        self.yPos = 0
        self.xSize = 0
        self.ySize = 0
        self.xConnectionPoint = 0
        self.yConnectionPoint = 0
        self.wNumber = wNumber
        self.connections = []
        self.id = 0

    def calcXConnectionPoint(self, xP, xS):
        self.xConnectionPoint = xP
        return xP

    def calcYConnectionPoint(self, yP, yS, wordType='src'):
        if wordType == 'src':
            self.yConnectionPoint = yP + yS
        else:
            self.yConnectionPoint = yP

    def setXPos(self, point):
        self.xPos = point
        self.calcXConnectionPoint(point, self.xSize)

    def setYPos(self, point):
        self.yPos = point
        self.calcYConnectionPoint(point, self.ySize)

    def setYSize(self, point):
        self.ySize = point
        self.calcYConnectionPoint(self.yPos, point)

    def setXSize(self, point):
        self.xSize = point
        self.calcXConnectionPoint(self.xPos, point)

    def toggleConnection(self, no):
        if no in self.connections:
            self.connections.remove(no)
            return False
        else:
            self.connections.append(no)
            return True


parser = argparse.ArgumentParser()
parser.add_argument('--db-name', help="DB name", default='alignments.db')
parser.add_argument('--user', '-u', default=1, choices=['1', '2'])
args = parser.parse_args()

try:
    conn = sqlite3.connect(args.db_name)
    c = conn.cursor()
except:
    print("Can't connect to database! Exiting...")
    sys.exit(0)

user = args.user

canvasWidth = 1200
canvasHeight = 250


def editSentence(event):
    sent_fix = EditSentence(canvas)


def writeAlignments(event = ''):
    global user
    global connections
    global current_pair_id

    connections_txt = ""
    for connection in connections:
        connections_txt += connection + ' '
    connections_txt = connections_txt.strip()

    try:
        sql_string = "UPDATE ALIGNMENTS SET alignments_u{} = '{}' WHERE id = {}".format(str(user), str(connections_txt), str(current_pair_id))
        c.execute(sql_string)
        conn.commit()
        messagebox.showinfo("Saved", "Word alignments saved")
    except Exception as e:
        print('(Write alignments error)')
        print(e)
        sys.exit(1)



def toggleDone(event):
    global user
    global current_pair_id
    try:
        status_text = ""
        c.execute("SELECT done{} FROM alignments WHERE id = {}".format(str(user), str(current_pair_id)))
        done_status = c.fetchone()[0]
        if done_status == 0:
            sql_string = "UPDATE ALIGNMENTS SET done{} = 1 WHERE id = {}".format(str(user), str(current_pair_id))
            status_text = "DONE"
        else:
            sql_string = "UPDATE ALIGNMENTS SET done{} = 0 WHERE id = {}".format(str(user), str(current_pair_id))
            status_text = "NOT DONE"
        c.execute(sql_string)
        conn.commit()
        messagebox.showinfo("Status Change", "Alignment status now set to: " + status_text)
        tl4.set('Status: ' + status_text)
    except Exception as e:
        print('(Toggle status error)')
        print(e)
        sys.exit(1)


def toggleDiscardAlignment(event):
    global user
    global current_pair_id
    try:
        #status_text = ""
        #c.execute("SELECT done{} FROM alignments WHERE id = {}".format(str(user), str(current_pair_id)))
        #done_status = c.fetchone()[0]
        print()
        sql_string = "UPDATE ALIGNMENTS SET discard = 1 WHERE id = {}".format(str(current_pair_id))
        #status_text = "Discarded"
        c.execute(sql_string)
        conn.commit()
        messagebox.showinfo("Status Change", "Pair Discarded")
        tl4.set('Status: Discarded')
    except Exception as e:
        print('(Toggle status error)')
        print(e)
        sys.exit(1)


def toggleUndiscardAlignment(event):
    global user
    global current_pair_id
    try:
        status_text = ""
        c.execute("SELECT done{} FROM alignments WHERE id = {}".format(str(user), str(current_pair_id)))
        done_status = c.fetchone()[0]
        sql_string = "UPDATE ALIGNMENTS SET discard = 0 WHERE id = {}".format(str(current_pair_id))
        status_text = "NOT DONE"
        c.execute(sql_string)
        conn.commit()
        messagebox.showinfo("Status Change", "Pair Uniscarded")
        tl4.set('Status: ' + status_text)
    except Exception as e:
        print('(Toggle status error)')
        print(e)
        sys.exit(1)


def finishPair(event = ''):
    global user
    global current_pair_id

    try:
        writeAlignments(event)
        sql_string = "UPDATE ALIGNMENTS SET done{} = 1 WHERE id = {}".format(str(user), str(current_pair_id))
        c.execute(sql_string)
        conn.commit()
        messagebox.showinfo("Next pair", "Moving on to next pair.")
        canvas.delete("all")
        writeConfidence(current_pair_id)
        alignmentID, src_sent_txt, trg_sent_txt, conns_txt = select_alignment(current_pair_id)
        setupAlignments(alignmentID, src_sent_txt, trg_sent_txt, conns_txt)
    except Exception as e:
        print('(Finish pair error)')
        print(e)
        sys.exit(1)


root = Tk()
frame = Frame(root, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
xscroll = Scrollbar(frame, orient=HORIZONTAL)
xscroll.grid(row=2, column=0, sticky=E + W)
yscroll = Scrollbar(frame)
yscroll.grid(row=1, column=1, sticky=N + S)
frame.pack(fill=BOTH, expand=1)

infoframe = Canvas(frame, bd=0)
infoframe.grid(row=0, column=0, sticky=N + S + E + W)
infoframe.configure(width=1200, height=50)
canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
canvas.grid(row=1, column=0, sticky=N + S + E + W)
canvas.configure(width=canvasWidth, height=canvasHeight, scrollregion=canvas.bbox("all"))
xscroll.config(command=canvas.xview)
yscroll.config(command=canvas.yview)
controlframe = Canvas(frame, bd=0)
controlframe.grid(row=3, column=0, sticky=N + S + E + W)
controlframe.config(background="white")
controlframe.configure(width=1200, height=100)
press_w = tk.Button(controlframe, text="Edit Sentence (w)", width=20, command=editSentence)
press_w.grid(row=4, column=0)
press_s = tk.Button(controlframe, text="Save (s)", width=20, command=writeAlignments)
press_s.grid(row=4, column=2)
press_f = tk.Button(controlframe, text="Finish Pair (f)", width=20, command=finishPair)
press_f.grid(row=4, column=3, sticky=W)
press_d = tk.Button(controlframe, text="Done/Not Done (d)", width=20, command=toggleDone)
press_d.grid(row=4, column=4, sticky=W)
press_x = tk.Button(controlframe, text="Discard (x)", width=20, command=toggleDiscardAlignment)
press_x.grid(row=4, column=5, sticky=E)
press_z = tk.Button(controlframe, text="Undiscard (z)", width=20, command=toggleUndiscardAlignment)
press_z.grid(row=4, column=6, sticky=E)

#Button(self.board, text='Update sentences', command=self.update_sentences)
#        updateButton.grid(row=4, column=1)

tl1 = StringVar()
tl2 = StringVar()
tl3 = StringVar()
tl4 = StringVar()
test_label1 = Label(infoframe, textvariable=tl1)
test_label1.grid(row=0, column=0, sticky=W)
test_label4 = Label(infoframe, textvariable=tl4)
test_label4.grid(row=0, column=1, padx=75, sticky=W)
test_label2 = Label(infoframe, textvariable=tl2)
test_label2.grid(row=1, column=0, sticky=W)
test_label3 = Label(infoframe, textvariable=tl3)
test_label3.grid(row=1, column=1, padx=75, sticky=W)

wordBoxes = {}
lastClickedId = None
lastClickedSrc = None
connections = []
connecting_lines = {}
current_pair_id = 0


def get_info(current_id):
    global user
    c.execute("select count(*) from alignments where done{} = 0 and discard is not 1".format(str(user)))
    alignments_left = c.fetchone()[0]
    c.execute("select count(*) from alignments where done{} = 1 and discard is not 1".format(str(user)))
    alignments_finished = c.fetchone()[0]
    c.execute("select count(*) from alignments where done{} < 2 and discard is not 1".format(str(user)))
    alignments_total = c.fetchone()[0]
    c.execute("select count(*) from alignments where id <= {} and discard is not 1".format(str(current_id)))
    alignments_order = c.fetchone()[0]
    c.execute("select discard from alignments where id = {}".format(str(current_id)))
    alignments_discard = c.fetchone()[0]
    c.execute("select done{} from alignments where id = {}".format(str(user), str(current_id)))
    alignment_done = c.fetchone()[0]
    if alignments_discard == 1:
        alignment_done = 3
    return alignments_left, alignments_finished, alignments_total, alignments_order, alignment_done


def select_alignment(alignment_no = 0, notDone=True, direction = 'none'):
    global user
    try:
        if notDone:
            try:
                c.execute("select min(id) from alignments where done{} = 0 and discard is not 1 and id >= {}".format(str(user), str(alignment_no)))
                working_id = c.fetchone()[0]
            except:
                c.execute("select max(id) from alignments where discard is not 1 and done{} < 2".format(str(user)))
                working_id = c.fetchone()[0]
        else:
            if direction == 'prev':
                c.execute("select max(id) from alignments where id < {}".format(str(alignment_no)))
            elif direction == 'next':
                c.execute("select min(id) from alignments where id > {}".format(str(alignment_no)))
            else:
                c.execute("select min(id) from alignments where id >= {}".format(str(alignment_no)))
            working_id = c.fetchone()[0]

        if working_id == None:
            c.execute("select max(id) from alignments where done{} < 2".format(str(user)))
            working_id = c.fetchone()[0]

    except Exception as e:
        print(e)
        working_id = alignment_no

    sqlstring = "select src_sentence, trg_sentence, alignments_u{} from alignments where id = {}".format(str(user), str(working_id))
    c.execute(sqlstring)
    src_sent, trg_sent, conns = c.fetchone()
    return working_id, src_sent, trg_sent, conns


def deleteAlignments():
    global current_pair_id

    try:
        sql_string = "UPDATE ALIGNMENTS SET alignments_u1 = alignments_u2 = NULL  WHERE id = {}".format(str(current_pair_id))
        c.execute(sql_string)
        conn.commit()
        messagebox.showinfo("Sentences updated", "Previous word alignments deleted")
    except Exception as e:
        print('(Delete alignments error)')
        print(e)
        sys.exit(1)


def info_window():
    board = Toplevel()
    board.title("Settings and shortcuts")
    s5Var = StringVar()
    s6Var = StringVar()
    s7Var = StringVar()
    s8Var = StringVar()
    s9Var = StringVar()
    s10Var = StringVar()
    s5Var.set("s-button - Save alignment")
    s6Var.set("x-button - Discard pair")
    s6Var.set("z-button - Undiscard pair")
    s6Var.set("d-button - Go to previous alignment without saving")
    s7Var.set("f-button - Finish and save alignment - Go to next")
    s8Var.set("o-button/LEFT-arrow - Go to previous alignment without saving")
    s9Var.set("p-button/RIGHT-arrow - Go to next alignment without saving")
    s10Var.set("w-button - Edit sentences")
    square5Label = Label(board, textvariable=s5Var)
    square5Label.grid(row=1, column=1)
    square6Label = Label(board, textvariable=s6Var)
    square6Label.grid(row=2, column=1)
    square7Label = Label(board, textvariable=s7Var)
    square7Label.grid(row=3, column=1)
    square8Label = Label(board, textvariable=s8Var)
    square8Label.grid(row=4, column=1)
    square9Label = Label(board, textvariable=s9Var)
    square9Label.grid(row=5, column=1)
    square10Label = Label(board, textvariable=s10Var)
    square10Label.grid(row=6, column=1)


def insert_sentences(sent1, sent2, conns_txt):
    global wordBoxes
    global connections
    global current_pair_id
    startX = 0
    startY = 80
    buffer = 8
    orderCnt = 0

    src_ids = []
    trg_ids = []
    sent1_width = 0
    sent2_width = 0
    for i in sent1:
        currWord = WordBox(True, i, orderCnt)
        currWord.setYPos(startY)

        currWord.id = canvas.create_text(0, currWord.yPos + currWord.ySize/2, activefill='blue', text=currWord.text, justify='left', font=('Arial', 16))
        r=canvas.create_rectangle(canvas.bbox(currWord.id), fill='white')
        canvas.tag_lower(r)
        wordBoxes[currWord.id] = currWord
        src_ids.append(currWord.id)

        currWidth = canvas.bbox(currWord.id)[2] - canvas.bbox(currWord.id)[0]
        sent1_width += currWidth + (buffer*2)
        currYBound = canvas.bbox(currWord.id)[3]
        currWord.setXSize(currWidth)
        startX += buffer + currWidth / 2
        currWord.setXPos(startX)
        canvas.move(currWord.id, startX, 0)
        canvas.move(r, startX, 0)
        startX += currWidth / 2
        currWord.calcYConnectionPoint(currYBound,0)
        canvas.tag_bind(currWord.id, '<Button-1>', onObjectClick)
        orderCnt += 1



    startY += 80
    startX = 0
    orderCnt = 0

    for i in sent2:
        currWord = WordBox(False, i, orderCnt)
        currWord.setYPos(startY)

        currWord.id = canvas.create_text(0, currWord.yPos + currWord.ySize / 2, activefill='blue', text=currWord.text, justify='center', font=('Arial', 16))
        r=canvas.create_rectangle(canvas.bbox(currWord.id), fill='white')
        canvas.tag_lower(r)
        wordBoxes[currWord.id] = currWord
        trg_ids.append(currWord.id)

        currWidth = canvas.bbox(currWord.id)[2] - canvas.bbox(currWord.id)[0]
        sent2_width = currWidth + (buffer*2)
        currYBound = canvas.bbox(currWord.id)[1]
        currWord.setXSize(currWidth)
        startX += buffer + currWidth / 2
        currWord.setXPos(startX)
        canvas.move(currWord.id, startX, 0)
        canvas.move(r, startX, 0)
        startX += currWidth / 2
        currWord.calcYConnectionPoint(currYBound,0)

        canvas.tag_bind(currWord.id, '<Button-1>', onObjectClick)
        orderCnt += 1

    if sent1_width > sent2_width:
        scrollwidth = sent1_width
    else:
        scrollwidth = sent2_width

    canvas.configure(width=canvasWidth, height=canvasHeight, scrollregion=(0, 0, scrollwidth, canvasHeight))

    try:
        connections = []
        for connection in conns_txt.split():
            print(connection)
            src_word_num = connection.split('-')[0]
            trg_word_num = connection.split('-')[1]
            src_word = wordBoxes[src_ids[int(src_word_num)]]
            trg_word = wordBoxes[trg_ids[int(trg_word_num)]]
            line = canvas.create_line(src_word.xConnectionPoint, src_word.yConnectionPoint, trg_word.xConnectionPoint, trg_word.yConnectionPoint, fill="green", width=2)
            connections.append(connection)
            connecting_lines[connection] = line
            src_word.toggleConnection(trg_word.wNumber)
            trg_word.toggleConnection(src_word.wNumber)
    except:
        connections = []

    alignments_left, alignments_finished, alignments_total, alignments_order, alignment_done = get_info(current_pair_id)

    done_text = ''
    if alignment_done == 3:
        done_text = 'Discarded!'
    elif alignment_done:
        done_text = 'DONE'
    elif alignment_done == False:
        done_text = 'NOT DONE'

    tl1.set("Alignment: " + str(alignments_order) + ' of ' + str(alignments_total))
    tl2.set(str(alignments_finished) + " alignments finished")
    tl3.set(str(alignments_left) + " alignments left")
    tl4.set('Status: ' + done_text)


def updateConnections(objId, objSrc, obj):
    global lastClickedId
    global lastClickedSrc
    global connections
    global wordBoxes

    if objSrc:
        tempString = str(wordBoxes[objId].wNumber) + '-' + str(wordBoxes[lastClickedId].wNumber)
    else:
        tempString = str(wordBoxes[lastClickedId].wNumber) + '-' + str(wordBoxes[objId].wNumber)

    obj.toggleConnection(wordBoxes[lastClickedId].wNumber)
    test = wordBoxes[lastClickedId].toggleConnection(obj.wNumber)
    if test:
        connections.append(tempString)
        line = canvas.create_line(obj.xConnectionPoint, obj.yConnectionPoint, wordBoxes[lastClickedId].xConnectionPoint, wordBoxes[lastClickedId].yConnectionPoint, fill="green", width=2)
        connecting_lines[tempString] = line
    else:
        connections.remove(tempString)
        canvas.delete(connecting_lines[tempString])

    lastClickedId = None
    lastClickedSrc = None
    print(connections)


def onObjectClick(event):
    global lastClickedId
    global lastClickedSrc
    global wordBoxes

    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)

    temp_num = event.widget.find_closest(x, y)[0]
    print(temp_num)
    try:
        obj = wordBoxes[temp_num]
    except:
        obj = wordBoxes[temp_num-1]
        temp_num = temp_num-1
    src = obj.src
    id = obj.id
    print(canvas.bbox(temp_num))

    if (lastClickedSrc == None) or (src == lastClickedSrc):
        print('first')
        lastClickedId = id
        lastClickedSrc = src
    else:
        print('other')
        updateConnections(id, src, obj)


def writeConfidence(current_pair_id):
    sqlstring = "select alignments_u1, alignments_u2, done1, done2 from alignments where id = {}".format(str(current_pair_id))
    c.execute(sqlstring)
    a1, a2, d1, d2 = c.fetchone()
    print(a1)
    print(a2)
    print(d1)
    print(d2)

    sure = []
    probable = []

    if d1 == d2 == 1:
        list1 = a1.strip().split()
        list2 = a2.strip().split()
        one2one1 = []
        one2one2 = []
        for i in list1:
            srcCnt = 0
            trgCnt = 0
            src_i_1, trg_i_1 = i.strip().split('-')
            for j in list1:
                src_j_1, trg_j_1 = j.strip().split('-')
                if src_i_1 == src_j_1:
                    srcCnt += 1
                if trg_i_1 == trg_j_1:
                    trgCnt += 1
            if srcCnt == trgCnt == 1:
                one2one1.append(i)
        for i in list2:
            srcCnt = 0
            trgCnt = 0
            src_i_2, trg_i_2 = i.strip().split('-')
            for j in list2:
                src_j_2, trg_j_2 = j.strip().split('-')
                if src_i_2 == src_j_2:
                    srcCnt += 1
                if trg_i_2 == trg_j_2:
                    trgCnt += 1
            if srcCnt == trgCnt == 1:
                one2one2.append(i)

        print(one2one1)
        print(one2one2)

        sure = set.intersection(set(one2one1), set(one2one2))
        print('sure')
        print(sure)
        probable = set.union(set(list1), set(list2)) - sure
        print('probable')
        print(probable)

    if len(list(sure) + list(probable)) > 0:
        confidence_string = ''
        for i in list(sure):
            confidence_string += i + ':S '
        for i in list(probable):
            confidence_string += i + ':P '
        confidence_string.strip()
        try:
            sql_string = "UPDATE ALIGNMENTS SET confidence = '{}' WHERE id = {}".format(str(confidence_string), str(current_pair_id))
            c.execute(sql_string)
            conn.commit()
        except Exception as e:
            print('(Write confidence error)')
            print(e)


def updateCanvas():
    global current_pair_id
    canvas.delete("all")
    alignmentID, src_sent_txt, trg_sent_txt, conns_txt = select_alignment(current_pair_id)
    setupAlignments(alignmentID, src_sent_txt, trg_sent_txt, conns_txt)



def go_to_page(event, page_num, direction = 'next'):
    db_string = "select min(id) from ALIGNMENTS"
    cur = conn.cursor()
    cur.execute(db_string)
    min_page = cur.fetchone()[0]

    db_string = "select max(id) from ALIGNMENTS"
    cur = conn.cursor()
    cur.execute(db_string)
    max_page = cur.fetchone()[0]

    if (max_page == page_num) and (direction == 'next'):
        messagebox.showinfo("Not possible", "Is on last sentence.")
    elif (page_num == min_page) and (direction == 'prev'):
        messagebox.showinfo("Not possible", "Is on first sentence.")
    else:
        print("Going to", page_num)
        canvas.delete("all")
        alignmentID, src_sent_txt, trg_sent_txt, conns_txt = select_alignment(page_num, False, direction)
        setupAlignments(alignmentID, src_sent_txt, trg_sent_txt, conns_txt)




def bind_functions():
    global canvas
    global current_pair_id

    try:
        canvas.bind("<KeyPress-s>", writeAlignments)
        canvas.bind("<KeyPress-o>", lambda event: go_to_page(event, current_pair_id, 'prev'))
        canvas.bind("<Left>", lambda event: go_to_page(event, current_pair_id, 'prev'))
        canvas.bind("<KeyPress-p>", lambda event: go_to_page(event, current_pair_id, 'next'))
        canvas.bind("<Right>", lambda event: go_to_page(event, current_pair_id, 'next'))
        canvas.bind("<KeyPress-f>", finishPair)
        canvas.bind("<KeyPress-d>", toggleDone)
        canvas.bind("<KeyPress-x>", toggleDiscardAlignment)
        canvas.bind("<KeyPress-w>", editSentence)
        canvas.bind("<KeyPress-z>", toggleUndiscardAlignment)
    except Exception as e:
        print(e)

def setupAlignments(alignmentID, src_sent_txt, trg_sent_txt, conns_txt):
    global current_pair_id
    current_pair_id = alignmentID
    sent1 = src_sent_txt.split()
    sent2 = trg_sent_txt.split()

    insert_sentences(sent1, sent2, conns_txt)


if __name__ == '__main__':
    alignmentID, src_sent_txt, trg_sent_txt, conns_txt = select_alignment()
    setupAlignments(alignmentID, src_sent_txt, trg_sent_txt, conns_txt)
    canvas.focus_set()
    bind_functions()
    info_window()
    root.mainloop()
