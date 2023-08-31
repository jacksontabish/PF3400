import socket
import time

class PF3400Controller:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.connect()
        self.teachpointtype = ""
        self.Zclearance = 25 #standard z clearance. change as needed
        
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        self.pause(5)
        nopcheck = "nop\n"
        self.socket.sendall(nopcheck.encode()) #sending dummy commands to check for connectivity
        self.sendcmd("nop")
        self.sendcmd("mode 0") #setting to PC mode for TCP server

    def sendcmd(self, command):
        command_str = command + "\n"  # Add a newline 
        self.socket.sendall(command_str.encode())
        #sent command, now check response...
        response = self.rcvdata()
        if response and response[0] == '0':
            print(f"Executing command {command}.")
        elif response and response[0] != '0':
            errc = response[1:4]
            print(f"Command not executed, error code: {errc}")
            #exception handling for various error codes
            if errc == "2805":
                print("2805: Unknown Command")
            elif errc == "1009":
                print("1009: Robot Not Attached")
                self.attachRobot()
            elif errc == "1010":
                print("1010: No Robot Selected")
                self.selectArm()
            elif errc == "1046":
                print("1046: Power Not Enabled")
                self.powerOn()
            elif errc == "3100" or errc =="1012":
                print("3100: Hard Envelope Error")
                self.safeStop()
           
            #Must consolidate all motion error-related error messages into one elif statement that safe stops
       
                

    def rcvdata(self,buffer_size=1024):
        data = self.socket.recv(buffer_size).decode()
        return data

    #def tcp_output(self,buffer_size=1024):
        #output = self.rcvdata(buffer_size)
        #print(f"Output: {output}")
        #return output

    def close(self):
        self.socket.close()
        print("Connection closed.")

    def pause(self,time):
        print(f"Waiting {time} seconds")
        time.sleep(time)


    #ROBOT POWER COMMANDS

    def selectArm(self):
        command = "selectRobot 1"
        self.sendcmd(command)

    def attachRobot(self):
        command = "attach 1"
        self.sendcmd(command)
        
    def detachRobot(self):
        command = "attach 0"
        self.sendcmd(command)

    def getAttachState(self):
        command = "attach"
        self.sendcmd(command)
        attachstate = self.rcvdata()
        return attachstate[2] #0=not attached, 1=attached

    def getBase(self):  #not essential
        command = "base"
        self.sendcmd(command)
        base = self.rcvdata()
        return base

    def setBase(self,xoff,yoff,zoff,zrot): #not essential
        command = f"base {xoff} {yoff} {zoff} {zrot}"
        self.sendcmd(command)

    def exitTCP(self):
        command = "exit"
        self.sendcmd(command)

    def home(self):
        command = "homeAll"
        self.sendcmd(command)
        self.pause(10)
        print("Robot homed.")
        #expected output is zero!

    def getPowerState(self):#not essential
        command = "hp"
        self.sendcmd(command)
        powerstate = self.rcvdata()
        if powerstate[2] == '0':
            return False
        elif powerstate[2] == '1':
            return True
        #0=power off, 1=power on

    def powerOn(self):
        command = "hp 1"
        self.sendcmd(command)

    def powerOff(self):
        command = "hp 0"
        self.sendcmd(command)

    def getMasterSpeed(self):#not essential
        command = "mspeed"
        self.sendcmd(command)
        mspeed = self.rcvdata()
        if len(mspeed) == 3:
            return int(mspeed[2])
        elif len(mspeed) == 4:
            return int(mspeed[2:3])
        elif len(mspeed) == 5:
            return 100
        else:
            print("Error while getting master speed.")

    def setMasterSpeed(self,speedpct):
        command = f"mspeed {speedpct}"
        self.sendcmd(command)
        print(f"Master speed set to {speedpct}")

    def halt(self):
        command = "halt"
        self.sendcmd(command)
        print("Robot halted.")

    def getSigVal(self,sigNum):
        command = f"sig {sigNum}"
        self.sendcmd(command)
        response = self.rcvdata()
        sigval = response[-1]
        
        if sigval == '0':
            return False
        else:
            return True

    def setSigVal(self,sigNum,sigVal): #sets signal of sigNum to new sigVal. 0 means off, any nonzero number means on
        command = f"sig {sigNum} {sigVal}"
        self.sendcmd(command)

        #gets state of motion (look at what these can be, and what they even mean)
    def getGPLState(self):
        command = "state"
        self.sendcmd(command)
        self.rcvdata()
        response = self.rcvdata
        state = response[2]
        if state == '0':
            gplstate = "Off"
        elif state == '1':
            gplstate == "Ready"
        elif state == '2':
            gplstate == "Executing"
        return gplstate
        #0=off, 1=ready, 2=executing(?)

    def safeStop(self): #use as an exception handler for motion-related commands
        self.halt()
        self.enableBrake()
        self.powerOff()
        

    #LOCATION COMMANDS

    def getLocation(self,location):#not essential
        command = f"loc {location}"
        self.sendcmd(command)
        location = self.rcvdata
        return location

    def getLocAngles(self,location):#not essential
        command = f"locAngles {location}"
        self.sendcmd(command)
        locAngles = self.rcvdata
        return locAngles

    #def setlocationangles(self,location,axis1,axis2,axis3,axis4,axis5)
    #needs 13 arguments... come back to this if we want angle-based positioning?

    def getCartesianLoc(self,location):#not essential
        command = f"locXyz {location}"
        self.sendcmd(command)
        locCart = self.rcvdata
        return locCart

    def createTeachPoint(self,location,x,y,z,yaw): #need to read x,y,z,yaw off of control panel for now, because
        #can't manually set teachpoints in the middle of running a script...
        herec_command = f"HereC {location}"
        self.sendcmd(herec_command) #set location profile 1 to Cartesian, record position of robot into location 1 temporarily
        #current_location = self.rcvdata() #get current location, though not needed for this method
        command = f"locXyz {location} {x} {y} {z} {yaw} 90 180"
        #now that location 1 is set to Cartesian, we can set its location
        self.sendcmd(command)

    def currentToTeachPoint(self, location: int):
       #set the robot's current location to a teachpoint in the place of a location index
       command = f"Here{self.teachpointtype} {location}" #the config parameter can be 'c' or 'j' and specifies if the location willbe Cartesian or Joint
       self.sendcmd(command)

    def TeachPointProtocol(self): 
    # TCP cmd server must be active but motor power must be off
    
        while True:
            tptype = input("Would you like to set Cartesian or Joint TeachPoints? Enter 'c' for Cartesian or 'j' for Joint: ")
        
            if tptype == "c" or tptype == "j":
                break  # Exit the loop if valid input is provided
            else:
                print("Invalid TeachPoint type! Please enter 'c' for Cartesian or 'j' for Joint.")

        self.teachpointtype = tptype
        
        while True:
            value = input("How many Teach Points do you wish to set? Enter an integer between 1 and 20: ")
        
            if value.isdigit():  # Check if input is a valid integer
                n = int(value)
                if 1 <= n <= 20:
                    break  # Exit the loop if valid input is provided
                else:
                    print("Invalid input. Please enter an integer between 1 and 20.")
            else:
                print("Invalid input. Please enter a valid integer.")

        zclear = input("Input desired Z clearance (mm).")

        for x in range(1, n):
            print(f"Move the arm to the desired location for Teach Point {x}.")
            input("Press Enter when finished moving.")
            self.currentToTeachPoint(x, tptype)
            command = f"locZClearance {x} {zclear}"
            self.sendcmd(command)
    
    def getZclearance(self,location):#not essential
        command = f"locZclearance {location}"
        self.sendcmd(command)
        zClear = self.rcvdata()
        n = len(zClear)
        return int(zClear[4:n-1])

    def setZclearance(self,location,zclearance): #z clearance in millimeters, generally around ~25mm
        command = f"locZclearance {location} {zclearance}"
        self.sendcmd(command)
        print(f"Z Clearance for Location {location} set to {zclearance}.")

    def setAllZClear(self,zclearance):
        for x in range(1,20):
            command = f"locZclearance {x} {zclearance}"
            self.sendcmd(command)

    def getLocConfig(self,location):#not essential
        command = f"locConfig {location}"
        self.sendcmd(command)
        output = self.rcvdata()
        return output[5] #0 means angles, 1 means cartesian

    def setLocConfig(self,location,config): #not essential
        command = f"locConfig {location} {config}"
        self.sendcmd(command)

    def getCartesianDest(self):#not essential
        command = "DestC"
        self.sendcmd(command)
        dest = self.rcvdata()
        return dest #will be 0 followed by 6 values

    def recordCartesianPos(self,location):#not essential
        command = "HereC"
        self.sendcmd(command)
        print(f"Teachpoint {location} set to current cartesian location.")
        
    def getJointDest(self):#not essential
        command = "DestJ"
        self.sendcmd(command)
        dest = self.rcvdata()
        return dest #will be 0 followed by 6 values

    def recordJointPos(self,location):#not essential
        command = "HereJ"
        self.sendcmd(command)
        print(f"Teachpoint {location} set to current joint location.")

    def getPos(self):#not essential
        command = "where"
        self.sendcmd(command)
        pos = self.rcvdata
        return pos

    def getCartesianPos(self):#not essential
        command = "wherec"
        self.sendcmd(command)
        pos = self.rcvdata
        return pos

    def getJointPos(self):#not essential
        command = "wherej"
        self.sendcmd(command)
        pos = self.rcvdata
        return pos

    #PROFILE COMMANDS

    #FOR ALL GETTERS, CHECK WHAT THE STANDARD OUTPUT IN TCP IS AND ADJUST METHODS ACCORDINGLY!!!
    #all setters for individual profile elements are nonessential bc there's an all-in-one setter method

    def getSpeed(self,profile):#not essential 
        command = f"Profile {profile}"
        self.sendcmd(command)
        speed = self.rcvdata()
        n = len(speed)
        return int(speed[4:n-1])

    def setSpeed(self,profile,speedpct):
        command = f"Speed {profile} {speedpct}"
        self.sendcmd(command)
        print(f"Speed for Motion Profile {profile} set to {speedpct}.")
    
    def getSpeed2(self,profile):#not essential
        command = f"Speed2 {profile}"
        self.sendcmd(command)
        speed2 = self.rcvdata()
        n = len(speed2)
        return int(speed2[4:n-1])

    def setSpeed2(self,profile,speedpct):
        command = f"Speed2 {profile} {speedpct}"
        self.sendcmd(command)
        print(f"Speed 2 for Motion Profile {profile} set to {speedpct}.")

    def getAccel(self,profile):#not essential
        command = f"Accel {profile}"
        self.sendcmd(command)
        accel = self.rcvdata()
        n = len(accel)
        return int(accel[4:n-1])

    def setAccel(self,profile,accelpct):
        command = f"Accel {profile} {accelpct}"
        self.sendcmd(command)
        print(f"Accel for Motion Profile {profile} set to {accelpct}.")

    def getAccRamp(self,profile):#not essential
        command = f"AccRamp {profile}"
        self.sendcmd(command)
        accramp = self.rcvdata()
        n = len(accramp)
        return float(accramp[4:n-1])

    def setAccRamp(self,profile,accrampval):
        command = f"AccRamp {profile} {accrampval}"
        self.sendcmd(command)
        print(f"AccelRamp for Motion Profile {profile} set to {accrampval}.")

    def getDecel(self,profile):#not essential
        command = f"Decel {profile}"
        self.sendcmd(command)
        decel = self.rcvdata() 
        n = len(decel)
        return int(decel[4:n-1])

    def setDecel(self,profile,decelpct):
        command = f"Decel {profile} {decelpct}"
        self.sendcmd(command)
        print(f"Decel for Motion Profile {profile} set to {decelpct}.")

    def getInRangeValue(self):#not essential
        command = f"InRange"
        self.sendcmd(command)
        inrangeval = self.rcvdata()
        n = len(inrangeval)
        return int(inrangeval[4:n-1])

    def setInRangeValue(self,inRangeVal): 
        command = f"Inrage {inRangeVal}"
        self.sendcmd(command) #redundant, this function is baked into setProfile

    def getStraightValue(self,profile):
        command = f"Straight {profile}"
        self.sendcmd(command)
        straightval = self.rcvdata()
        if straightval == "True":
            return True
        elif straightval == "False":
            return False

    def setStraightPath(self,profile):
        command = "Straight -1"
        self.sendcmd(command)

    def setJointPath(self,profile):
        command = "Straight 0"
        self.sendcmd(command)

    def setStraightValue(self,straightval):
        command = f"Straight {straightval}"
        self.sendcmd(command)

    def getProfile(self,profile):
        command = f"Profile {profile}"
        self.sendcmd(command)

    def setProfile(self,profile,speed,speed2,accel,decel,accelramp,decelramp,InRange,Straight):
        command = f"Profile {profile} {speed} {speed2} {accel} {decel} {accelramp} {decelramp} {InRange} {Straight}"
        self.sendcmd(command)
        print(f"Motion Profile {profile} defined.")
        #Use for defining a profile's info for the first time
        #play around with decelramp and accelramp values to see if they're even worth including in this function as arguments...

    def genericProfile(self,profile):
        command = "Profile 50 0 100 100 0.1 0.1 10 0"
        self.sendcmd(command)
        print(f"Motion Profile {profile} set to generic.")




    
        

    #MOTION-RELATED COMMANDS
        
    def move(self,location,profile):
        command = f"move {location} {profile}"
        self.sendcmd(command)
        print(f"Arm moving to Teachpoint {location} with Motion Profile {profile}.")

    def Approach(self,location,profile):
        command = f"moveAppro {location} {profile}"
        self.sendcmd(command)
        print (f"Arm approaching Teachpoint {location} with Motion Profile {profile}.")

    def approAndMove(self,location,profile): #consolidated form of the previous 2 methods
        command = f"moveAppro {location} {profile}"
        self.sendcmd(command)
        print(f"Arm approaching Teachpoint {location} with Motion Profile {profile}")
        self.waitForSync
        command2 = f"move {location} {profile}"
        self.sendcmd(command2)
        print(f"Arm moving to Teachpoint {location} with Motion Profile {profile}")
        self.waitForSync
        


    #redundant 
    def moveC(self,profile,x,y,z,yaw): #argument 8: sets config property for location"
        command = f"moveC {profile} {x} {y} {z} {yaw} 90 180"
        self.sendcmd(command)  

    #def moveJ?

    def releaseBrake(self,axisnum):
        command = f"releaseBrake {axisnum}"
        self.sendcmd(command)
        print("Brake released.")

    def enableBrake(self,axisnum):
        command = f"setBrake {axisnum}"
        self.sendcmd(command)
        print("Brake enabled.")

    def moveOneAxis(self,axisnum,destination,profile):
        command = f"moveOneAxis {axisnum} {destination} {profile}"
        self.sendcmd(command)

        #waits for the robot to reach the end of its current motion or until it is stopped by some other means. 
    def waitForSync(self):
        command = "waitForEom"
        self.sendcmd(command)

    #GRIPPER COMMANDS

    #must write function that takes desired measurement of object to be picked up
    #and stores as a gripper position in a class member variable
  

    def getGripperLoc(self):
        command = "tool"
        self.sendcmd(command)
        gripperpos = self.rcvdata()
        return gripperpos #x y z yaw pitch roll

    #Don't have GSB working at full functionality yet so don't know what these methods will look like
    #it will certainly still use 'MoveOneAxis 5 x profile' as the command 
    #x is the desired gripper position, which is still unknown
    def openGripper(self,profile):
        command = f"moveOneAxis 5 x {profile}"
        self.sendcmd(command)

    def closeGripper(self,profile):
        command = f"moveOneAxis 5 x {profile}"
        self.sendcmd(command)
        #must tweak gripper open and close positions depending on what it's picking up!

