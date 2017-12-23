from db_manager import *
import os, platform

mode = 'home'
error = ''
running = True
class_name = None

def clear_terminal():
    os_name = platform.system()
    if 'Windows' in os_name:
        os.system('cls')
    else:
        os.system('clear')

def home():
    global error
    global mode
    global running
    global class_name

    clear_terminal()
    print 'GRADE MANAGER\n'
    
    print 'ID | Class Name'
    print '-----------------------------------'
    classes = get_classes()
    for x in xrange(len(classes)):
        print '%s%s | %s' % ((2-len(str(x)))*' ',x,classes[x].upper().replace('_',' '))
        
    if error != '':
        print '\nError: ' + error
        
    decision = raw_input('''
What do you want to do?
a) Enter the associated number to view a class.
b) Enter "A" to add a class
c) Enter "D" to drop a class
d) Enter "Q" to quit
''')

    def validCode(num):
        return num >= 0 and num < len(classes)

        
    if decision.isdigit() and validCode(int(decision)):
        mode = 'class'
        class_name = classes[int(decision)].replace('_',' ')
        error = ''
    elif decision.upper() == 'A':
        error = ''
        mode = 'add_class'
    elif decision.upper() == 'D':
        error = ''
        mode = 'drop_class'
    elif decision.upper() == 'Q':
        running = False
    else:
        error = 'Invalid option'

def add_class():
    name = raw_input('Enter name of class. Alphanumeric characters and spaces only: ')
    create_class(name.replace(' ','_'))
    return name

def display_class():
    global class_name
    global mode
    global error
    global running
    
    clear_terminal()
    print 'GRADE MANAGER\n'

    print 'Class: %s' % (class_name.upper())
    categories = get_class_info(class_name.replace(' ','_'))

    len_max_component = max([len('Component')] + [len(e[0]) for e in categories])

    
    print 'ID | Component%s | Percent | Grade (out of 100)' % ((len_max_component-9)*' ')
    print '-----------------------------------------------------------------------'

    total_percent = 0
    max_grade = calc_max_grade(categories)
    
    for x in xrange(len(categories)):
        total_percent += categories[x][1]
        print '%s%s | %s%s | %s%s | %s' % ((2-len(str(x)))*' ',x,categories[x][0],(len_max_component-len(categories[x][0]))*' ',categories[x][1],(7-len(str(categories[x][1])))*' ',categories[x][2])

    print 'Max Percent: %f' % (max_grade)
    print 'Total Percent: %d' % (total_percent)
        
    if error != '':
        print '\nError: ' + error
    
    decision = raw_input('''
What would you like to do?
A) Enter the associated number to edit a component
B) Enter "A" to add a component
C) Enter "B" to go back to all classes
D) Enter "D" to drop a component
E) Enter "Q" to quit
''')

    
    def validCode(num):
        return num >= 0 and num < len(categories)
                         
    if decision.isdigit() and validCode(int(decision)):
        error = ''
        edit_category(categories[int(decision)])
    elif decision.upper() == 'A':
        error = ''
        add_category()
    elif decision.upper() == 'B':
        error = ''
        mode = 'home'
    elif decision.upper() == 'D':
        cid = raw_input('Enter the id for the component to drop: ')
        if cid.isdigit() and validCode(int(cid)):
            error = ''
            delete_category(categories[int(cid)][0])
        else:
            error = 'Invalid category ID'
        
    elif decision.upper() == 'Q':
        running = False
    else:
        error = 'Invalid option'

    
def add_category():
    global class_name 
    category = raw_input('Enter the name of the component: ')
    percent = raw_input('Enter the percent of the component: ')
    score = raw_input('Enter the grade received (blank if not yet received): ')
    if score == '':
        score = '-'
    insert_category(class_name.replace(' ','_'),category,int(percent),score)

    
def edit_category(category):
    global class_name
    new_name = raw_input('Enter the new name of the component. Leave blank if unchanged: ')
    new_percent = raw_input('Enter the new percent of the component. Leave blank if unchanged: ')
    new_score = raw_input('Enter the new grade of the component. MUST BE FILLED. Leave blank if no grade: ')
    if new_name == '':
        new_name = category[0]
    if new_percent == '':
        new_percent = str(category[1])
    if new_score == '':
        new_score = '-'
    modify_category_entry(class_name.replace(' ','_'),category[0],new_name,int(new_percent),new_score)

def delete_category(c_name):
    global class_name
    delete_category_entry(class_name.replace(' ','_'),c_name)

def calc_max_grade(categories):
    total_grade = 0
    for c in categories:
        if c[2] == '-':
            total_grade += c[1]
        else:
            total_grade += float(c[2])/100*c[1]
    return total_grade

def drop_class():
    global mode
    global error
    
    cid = raw_input('Enter the ID of the class to drop: ')
    classes = get_classes()
    
    def validCode(num):
        return num >= 0 and num < len(classes)

    if cid.isdigit() and validCode(int(cid)):
        drop_class_table(classes[int(cid)])
        error = ''
    else:
        error = 'Invalid class ID'
    mode = 'home'
        
def run():
    global mode
    global class_name
    
    if mode == 'home':
        home()            
    elif mode == 'add_class':
        class_name = add_class()
        mode = 'class'
    elif mode == 'drop_class':
        drop_class()
    elif mode == 'class':
        display_class()

while running:
    run()


#maybe do change class name
