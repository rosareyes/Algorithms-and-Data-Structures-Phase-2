# -*- coding: utf-8 -*-



from binarysearchtree import BinarySearchTree

import csv      #read files csv, tsv
import os.path  #to work with files and directory https://docs.python.org/3/library/os.path.html
import queue    #package implementes a queueu, https://docs.python.org/3/library/queue.html
import re       #working with regular expressions

def checkFormatHour(time):
    """checks if the time follows the format hh:dd"""
    pattern = re.compile(r'\d{2}:\d{2}')  # busca la palabra foo
    
    if pattern.match(time):
        data=time.split(':')
        hour=int(data[0])
        minute=int(data[1])
        if hour in range(8,20) and minute in range(0,60,5):
            return True
    
    return False

""" Algorithms analysis:
What is the time complexity of each function? Explain best and worst cases. You can
include a comment within your code as an answer """


#number of all possible appointments for one day
NUM_APPOINTMENTS=144

class Patient:
    """Class to represent a Patient"""
    def __init__(self,name,year,covid,vaccine,appointment=None):

        self.name=name
        self.year=year
        self.covid=covid
        self.vaccine=vaccine
        self.appointment=appointment     #string with format hour:minute

    def setAppointment(self,time):
        """gets a string with format hour:minute"""
        self.appointment=time
        
    def __str__(self):
        return self.name+'\t'+str(self.year)+'\t'+str(self.covid)+'\t'+str(self.vaccine)+'\t appointment:'+str(self.appointment)

    def __eq__(self,other):
        return  other!=None and self.name == other.name 



class HealthCenter2(BinarySearchTree):
    """Class to represent a Health Center. This class is a subclass of a binary search tree to 
    achive a better temporal complexity of its algorithms for 
    searching, inserting o removing a patient (or an appointment)"""


    def __init__(self,filetsv=None,orderByName=True):
        """
        This constructor allows to create an object instance of HealthCenter2. 
        It takes two parameters:
        - filetsv: a file csv with the information about the patients whe belong to this health center
        - orderByName: if it is True, it means that the patients should be sorted by their name in the binary search tree,
        however, if is is False, it means that the patients should be sorted according their appointments
        """

        #Call to the constructor of the super class, BinarySearchTree.
        #This constructor only define the root to None
        super(HealthCenter2, self).__init__()
        
        #Now we 
        if filetsv is None or not os.path.isfile(filetsv):
            #If the file does not exist, we create an empty tree (health center without patients)
            self.name=''
            #print('File does not exist ',filetsv)
        else: 
            order='by appointment'
            if orderByName:
                order='by name'

            #print('\n\nloading patients from {}. The order is {}\n\n'.format(filetsv,order))
            
            self.name=filetsv[filetsv.rindex('/')+1:].replace('.tsv','')
            #print('The name of the health center is {}\n\n'.format(self.name))
            #self.name='LosFrailes'

            fichero = open(filetsv)
            lines = csv.reader(fichero, delimiter="\t")
    
            for row in lines:
                #print(row)
                name=row[0] #nombre
                year=int(row[1]) #año nacimiento
                covid=False
                if int(row[2])==1:          #covid:0 o 1
                    covid=True
                vaccine=int(row[3])         #número de dosis
                try:
                    appointment=row[4]
                    if checkFormatHour(appointment)==False:
                        #print(appointment, ' is not a right time (hh:minute)')
                        appointment=None
                        
                except:
                    appointment=None    

                objPatient=Patient(name,year,covid,vaccine,appointment)
                #name is the key, and objPatient the eleme
                if orderByName:
                    self.insert(name,objPatient)
                else:
                    if appointment:
                        self.insert(appointment,objPatient)
                    else:
                        print(objPatient, " was not added because appointment was not valid!!!")
    
            fichero.close()




    
    def searchPatients(self,year=2021,covid=None,vaccine=None):
        """return a new object of type HealthCenter 2 with the patients who
        satisfy the criteria of the search (parameters). 
        The function has to visit all patients, so the search must follow a level traverse of the tree.
        If you use a inorder traverse, the resulting tree should be a list!!!"""
        
        """ Time Complexity:
            -Each node is visited only once in inorder traversal 
            and hence the complexity of this function is O(n).
            -Best case would be that the tree is empty.
            -Worst case would be that the patient isnt on the tree or that it is the last node visited. So its also O(n)
        """


        result=HealthCenter2()

        if self._root==None:
            print('tree is empty')
            return
      
        q=queue.Queue()
        q.put(self._root) #we save the root
        while q.empty()==False:
            current=q.get() #dequeue
            if current.left:
                q.put(current.left)
            if current.right:
                q.put(current.right)
                     
            if year == 2021 or year >= current.elem.year:               
                if covid == None:
                    if vaccine == None:
                        #Retrieves all the patients of the tree or the one that matches the input year.
                        result.insert(current.key, current.elem)
                    elif vaccine == current.elem.vaccine:
                        result.insert(current.key, current.elem)
                elif covid == current.elem.covid:
                    if  vaccine == None:
                        result.insert(current.key, current.elem)
                    elif vaccine == current.elem.vaccine:
                        print(current.elem.vaccine)
                        result.insert(current.key, current.elem)  
    
        return result
            


    def vaccine(self,name,vaccinated):
        """This functions simulates the vaccination of a patient whose
        name is name. It returns True is the patient is vaccinated and False eoc"""


        """ Time Complexity:
            The complexity of this function is O(log n). 
            -Best case would be that the patient isn't in the tree. 
            The worst case complexity is O(n) being n the number of nodes in the case our tree is skewed"""


        patient_node = self.find(name) #time complexity of find is O(h) where h is height of BST (O(log n))
        
        if patient_node is None:
            print("Patient '", name, "' not found")
            return False
        
        patient = patient_node.elem

        if patient.vaccine == 2:
            print("patient '", name, "' is vaccinated")
            self.remove(name) #time complexity is O(h). (O(log n))
            vaccinated.insert(name, patient) #time complexity is O(h). (O(log n))
            return False
        
        if patient.vaccine < 2 or patient.covid == False:
            patient.vaccine  += 1
            print("The database of the patient '", name, "' has been updated")
            print("dose until now: ", patient.vaccine)

            if patient.vaccine == 2:
                self.remove(name)
                vaccinated.insert(name, patient)
                
            return True
               
        if patient.vaccine == 1 or patient.covid == True:
            patient.vaccine = 2
            self.remove(name)
            vaccinated.insert(name, paciente)
            print("The database of the patient '", name, "' has been updated")
            print("dose until now: ", patient.vaccine)
            return True

        return None


    def makeAppointment(self,name,time,schedule):
        """This functions makes an appointment 
        for the patient whose name is name. It functions returns True is the appointment 
        is created and False eoc """

        """ Time Complexity:
            The complexity of this function is O(n log n) because BST functions are inside a loop. 
            --Best case would be that the tree is empty.
            The worst case would be O(n log n) when you traverse all the tree because the bst functions are inside a loop.
        """

        #We check if the hour has a correct format
        if checkFormatHour(time) == False:
            print("Incorrect Hour")
            return False
        patient_node = self.find(name)
           
        #We check if the patient is on the Center
        if not patient_node:
            print("Patient {} doesn´t exist".format(name))
            return False

        #We check if the patient has already 2 doses
        if patient_node:
            if patient_node.elem.vaccine == 2:
                print("Patient {} has  already both doses".format(name))
                return False

        found = schedule.search(time)  #time complexity is O(h) where h is height of BST. (O(log n))  

        if found == False:
            patient_node.elem.appointment = time
    
            schedule.insert(time, patient_node.elem)
            print("Hora libre:", time)

            return True
             
        (hour_time, min_time) = time.split(":")
        
        hour_time = int(hour_time)
        min_time = int(min_time)
        added = False
        finished = False
        
        min_pre = min_time-5
        hour_pre = hour_time
        
        min_post = min_time+5
        hour_post = hour_time
            
        while not finished:

            #We check if the minutes and hours are correct, if not they jump to the next hour or the previous one   
            if min_pre<0:
                min_pre = 55
                hour_pre -= 1
            
            if min_post >55:
                min_post = 0
                hour_post += 1
                
            if hour_post >19 and hour_pre < 8:
                finished = True
                
            #We convert the minutes and hours to correct string times with format (0x:0x) when needed.
            str_min_pre = str(min_pre)
            if min_pre<10:
                str_min_pre = "0"+str_min_pre 
            
            str_min_post = str(min_post)
            if min_post<10:
                str_min_post = "0"+str_min_post
                
            str_hour_pre = str(hour_pre)
            if hour_pre<10:
                str_hour_pre = "0"+str_hour_pre 
            
            str_hour_post = str(hour_post)    
            if hour_post<10:
                str_hour_post = "0"+str_hour_post
            
            str_pre = str_hour_pre+":"+str_min_pre
            str_post = str_hour_post+":"+str_min_post
            
            
            #Checks if the previous hour is found, if it is not, it means that it is available.
            if hour_pre >= 8:
                found_pre = schedule.search(str_pre) #time complexity is O(h) (O(log n))
            else:
                found_pre = True
                
            #Checks if the posterior hour is found, if it is not, it means that it is available.    
            if hour_post > 19:
                found_post = True
            else:
                found_post = schedule.search(str_post) #time complexity is O(h) (O(log n))
                
            
            #Here first we check the previous hour because if it is available then we assign it because its the earlier one.
            if not found_pre:
                print("Requested Hour: ", time)
                print("Closest free hour: ", str_pre)
                patient_node.elem.appointment = str_pre
                schedule.insert(str_pre, patient_node.elem) #time complexity is O(h) (O(log n))
                added = True
                finished = True
            #If there are not earlier hours available, then we check for the later ones.
            else:
                if not found_post:
                    print("Requested Hour: ", time)
                    print("Closest free hour: ", str_post)
                    patient_node.elem.appointment = str_post
                    schedule.insert(str_post, patient_node.elem) #time complexity is O(h) (O(log n))
                    added = True
                    finished = True
                else:
                    min_pre -=5
                    min_post+=5
             
        if not added:
            print("There are not slots")
        
        return added
        
                


if __name__ == '__main__':
    
    ###Testing the constructor. Creating a health center where patients are sorted by name
    o=HealthCenter2('data/LosFrailes2.tsv')
    o.draw()
    print()


    print('Patients who were born in or before than 1990, had covid and did not get any vaccine')
    result=o.searchPatients(1990, True,0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990, did not have covid and did not get any vaccine')
    result=o.searchPatients(1990, False,0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990 and got one dosage')
    result=o.searchPatients(1990, None,1)
    result.draw()
    print()

    print('Patients who were born in or before than 1990 and had covid')
    result=o.searchPatients(1990, True)
    result.draw()
    print()


    ###Testing the constructor. Creating a health center where patients are sorted by name
    schedule=HealthCenter2('data/LosFrailesCitas.tsv',False)
    schedule.draw(False)
    print()
    
    

    o.makeAppointment("Perez","08:00",schedule)
    o.makeAppointment("Losada","19:55",schedule)
    o.makeAppointment("Jaen","16:00",schedule)
    o.makeAppointment("Perez","16:00",schedule)
    o.makeAppointment("Jaen","16:00",schedule)

    o.makeAppointment("Losada","15:45",schedule)
    o.makeAppointment("Jaen","08:00",schedule)

    o.makeAppointment("Abad","08:00",schedule)
    o.makeAppointment("Omar","15:45",schedule)
    
    
    schedule.draw(False)

    vaccinated=HealthCenter2('data/vaccinated.tsv')
    vaccinated.draw(False)

    name='Ainoza'  #doest no exist
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)

    name='Abad'   #0 dosages
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
    
   

    name='Font' #with one dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
    
    name='Omar' #with two dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
