from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import time
import pdfgen
from reportlab.pdfgen import canvas
import webbrowser,os

try:
	os.mkdir("C:\\InvoiceGenerator")
except:
	pass
class header:
	def __init__(self,CustomerName,CustomerContact):
		self.InvoiceNumber=time.time()
		self.CustomerName=CustomerName
		self.CustomerContact=CustomerContact
		timedate=time.asctime()
		self.date=timedate[4:8]+timedate[8:10]+", "+timedate[20:24]+"."
		self.time=" "+timedate[11:20]
class product:
	def __init__(self,name,quantity,rate,tax,discount):
		self.name=name
		self.quantity=quantity
		self.rate=rate
		self.tax=tax
		self.total=(quantity*rate)-discount
		self.discount=discount
root = Tk()
root.title("E-INVOICE GENERATOR")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#6666ff")

PRODUCTNAME = StringVar()
QUANTITY = IntVar()
RATE = IntVar()
TAX = IntVar()
TOTAL = IntVar()
DISCOUNT=IntVar()
CustomerName=StringVar()
CustomerContact=StringVar()


Products=[]

def printinvoice():
    head=header(CustomerName.get(),CustomerContact.get())
    pdf= canvas.Canvas("C:\\InvoiceGenerator\\"+str(int(head.InvoiceNumber))+".pdf")
    pdfgen.header(head,pdf)
    pdfgen.middle(pdf)
    ycooridinate=650
    x=1

    for item in Products:
        currproduct=product(item[0],item[1],item[2],item[5],item[3])
        pdf.drawString(35,ycooridinate,str(x))
        x=x+1
        pdf.setFont("Courier-Bold",9)
        ycooridinate=pdfgen.additem(currproduct,pdf,ycooridinate)
    pdf.setFont("Courier-Bold",11)
    pdfgen.footer(pdf,Products)
    pdf.save()
    webbrowser.open("C:\\InvoiceGenerator\\"+str(int(head.InvoiceNumber))+".pdf")
	


def SubmitData():
    product=PRODUCTNAME.get()
    quantity=QUANTITY.get()
    rate=RATE.get()

    dis=float((quantity*rate)*(DISCOUNT.get()/100))
    total=float(QUANTITY.get()*RATE.get()-dis)
    tax=float(TAX.get()*0.01*total)

    Products.append((product,quantity,rate,dis,total,tax))
    tree.delete(*tree.get_children())
    for data in (Products):
        tree.insert('', 'end', values=(data))
    PRODUCTNAME.set("")
    QUANTITY.set(1)
    RATE.set(0)


def DeleteData():
    if not tree.selection():
       result = tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this item?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            print(selecteditem)
            for item in range(len(Products)):
            	if((Products[item])[0]==selecteditem[0]):
            		break
            del(Products[item])
            print(Products)

def AddNewWindow():
    global NewWindow
    PRODUCTNAME.set("")
    QUANTITY.set("")
    RATE.set("")
    NewWindow = Toplevel()
    NewWindow.title("E-INVOICE GENERATOR")
    width = 400
    height = 330
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()

    
    #===================FRAMES==============================
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    Form = Frame(NewWindow)
    Form.pack(side=TOP, pady=10)
 
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="Add Item", font=('arial', 16), bg="#66ff66",  width = 300)
    lbl_title.pack(fill=X)
    lbl_productname = Label(Form, text="Product name", font=('arial', 14), bd=5)
    lbl_productname.grid(row=0, sticky=W)
    lbl_quantity = Label(Form, text="Quantity", font=('arial', 14), bd=5)
    lbl_quantity.grid(row=1, sticky=W)
    lbl_rate = Label(Form, text="Rate", font=('arial', 14), bd=5)
    lbl_rate.grid(row=2, sticky=W)
    taxlabel=Label(Form,text="Tax(%)",font=('arial',14),bd=5)
    taxlabel.grid(row=3,sticky=W)
    discountLabel= Label(Form,text="Discount(%)",font=('arial',14),bd=5)
    discountLabel.grid(row=4,sticky=W)
    nameLabel=Label(Form,text="Customer Name:",font=('arial',14),bd=5)
    nameLabel.grid(row=5,sticky=W)
    nameLabel=Label(Form,text="Customer Contact:",font=('arial',14),bd=5)
    nameLabel.grid(row=6,sticky=W)



    #===================ENTRY===============================
    Product = Entry(Form, textvariable=PRODUCTNAME, font=('arial', 14))
    Product.grid(row=0, column=1)
    Quantity = Entry(Form, textvariable=QUANTITY, font=('arial', 14))
    Quantity.grid(row=1, column=1)
    Rate= Entry(Form, textvariable=RATE,  font=('arial', 14))
    Rate.grid(row=2, column=1)
    Product.focus()
    Tax=Entry(Form,textvariable=TAX, font=('arial',14))
    Tax.grid(row=3,column=1)
    discountEntry=Entry(Form,textvariable=DISCOUNT, font=('arial',14))
    discountEntry.grid(row=4,column=1)
    nameEntry=Entry(Form,textvariable=CustomerName,font=('arial',14))
    nameEntry.grid(row=5, column=1)
    nameEntry=Entry(Form,textvariable=CustomerContact,font=('arial',14))
    nameEntry.grid(row=6, column=1)
    RATE.set(0)
    TAX.set(0)
    QUANTITY.set(1)



    btn_addcon = Button(Form, text="Add Item to Cart", width=50, command=SubmitData)
    btn_addcon.grid(row=7, columnspan=2, pady=10)

#============================FRAMES======================================
Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500,  bg="#6666ff")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="#6666ff")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)
#============================LABELS======================================
lbl_title = Label(Top, text="Shop Name", font=('arial', 16), width=500)
lbl_title.pack(fill=X)

#============================BUTTONS=====================================
btn_add = Button(MidLeft, text="Add New Item", bg="#66ff66", command=AddNewWindow)
btn_add.pack()
btn_delete = Button(MidRight, text="Remove Selected Item", bg="red", command=DeleteData)
btn_delete.pack(side=RIGHT)
btn_about= Button(TableMargin,text="About Developer  \t\t\t\t\t\t\t\t\t\t\t\t\t",command=pdfgen.About)
btn_about.pack(side=BOTTOM)
btn_print= Button(TableMargin,text="Print Invoice",bg="lightgreen",command=printinvoice)
btn_print.pack(side=BOTTOM)

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("Product Name", "Quantity", "Rate","Discount", "Total", "Tax"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('Product Name', text="Product Name", anchor=W)
tree.heading('Quantity', text="Quantity", anchor=W)
tree.heading('Rate', text="Rate", anchor=W)
tree.heading('Discount',text="Discount",anchor=W)
tree.heading('Total', text="Total", anchor=W)
tree.heading('Tax', text="Tax", anchor=W)
tree.column('#0',width=0)
tree.column('#1', stretch=NO, minwidth=0, width=250)
tree.column('#2', stretch=NO, minwidth=0, width=70)
tree.column('#3', stretch=NO, minwidth=0, width=90)
tree.column('#4', stretch=NO, minwidth=0, width=80)
tree.column('#5', stretch=NO, minwidth=0, width=120)
tree.pack()
root.mainloop()
