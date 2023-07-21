



        
import socket

#MAIN CLASS METHODS (all essential)
class PF3400Controller:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.connect()
        self.openGripperPos = 0
        self.closeGripperPos = 0
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        print("Connection successful.")

    def send_command(self, command):
        command_str = command + "\n"  # Add a newline 
        self.socket.sendall(command_str.encode())
        print(f"Sent command: {command}")

    def close(self):
        self.socket.close()
        print("Connection closed.")

    #ROBOT POWER COMMANDS

    def attachRobot(self):
        command = "attach 1"
        self.send_command(command)

    def detachRobot(self):
        command = "attach 0"
        self.send_command(command)

    def getBase(self):  #not essential
        command = "base"
        self.send_command(command)

    def setBase(self,xoff,yoff,zoff,zrot): #not essential
        command = f"base {xoff} {yoff} {zoff} {zrot}"
        self.send_command(command)

    def exitTCP(self):
        command = "exit"
        self.send_command(command)

    def home(self):
        command = "home"
        self.send_command(command)

    def homeAll(self): #not essential
        command = "homeAll"
        self.send_command(command)

    def getPowerState(self):#not essential
        command = "hp"
        self.send_command(command)

    def powerOn(self):
        command = "hp 1"
        self.send_command(command)

    def powerOff(self):
        command = "hp 0"
        self.send_command(command)

    def getMasterSpeed(self):#not essential
        command = "mspeed"
        self.send_command(command)

    def setMasterSpeed(self,speedpct):
        command = f"mspeed {speedpct}"
        self.send_command(command)

    def halt(self):
        command = "halt"
        self.send_command(command)

    def getSignal(self,sigNum):
        command = f"sig {sigNum}"
        self.send_command(command)

    def setSignal(self,sigNum,sigVal): #sets signal of sigNum to new sigVal
        command = f"sig {sigNum} {sigVal}"
        self.send_command(command)


    #LOCATION COMMANDS

    def getLocation(self,location):#not essential
        command = f"loc {location}"
        self.send_command(command)

    def getLocationAngles(self,location):#not essential
        command = f"locAngles {location}"
        self.send_command(command)

    #def setlocationangles(self,location,axis1,axis2,axis3,axis4,axis5)
    #needs 13 arguments... come back to this if we want angle-based positioning?

    def getCartesianLoc(self,location):#not essential
        command = f"locXyz {location}"
        self.send_command(command)

    def setCartesianLoc(self,location,x,y,z,yaw): #find out what yaw,pitch, and roll default values are, if static
        command = f"locXyz {location} {x} {y} {z} {yaw} 90 180"
        self.send_command(command)
    
    def getLocZclearance(self,location):#not essential
        command = f"locZclearance {location}"
        self.send_command(command)

    def setLocZclearance(self,location,zclearance):
        command = f"locZclearance {location} {zclearance}"
        self.send_command(command)

    def getLocConfig(self,location):#not essential
        command = f"locConfig {location}"
        self.send_command(command)

    def setLocConfig(self,location,config):
        command = f"locConfig {location} {config}"
        self.send_command(command)

    def getCartesianDest(self):#not essential
        command = "DestC"
        self.send_command(command)

    def recordCartesianPos(self,location):#not essential
        command = "HereC"
        self.send_command(command)
        
    def getJointDest(self):#not essential
        command = "DestJ"
        self.send_command(command)

    def recordJointPos(self,location):#not essential
        command = "HereJ"
        self.send_command(command)

    def getPos(self):#not essential
        command = "where"
        self.send_command(command)

    def getCartesianPos(self):#not essential
        command = "wherec"
        self.send_command(command)

    def getJointPos(self):#not essential
        command = "wherej"
        self.send_command(command)

    #PROFILE COMMANDS

    #most can be used to tweak one aspect of a profile, setProfile is for all at once

    def getSpeed(self,profile):#not essential
        command = f"Speed {profile}"
        self.send_command(command)

    def setSpeed(self,profile,speedpct):
        command = f"Speed {profile} {speedpct}"
        self.send_command(command)
    
    def getSpeed2(self,profile):#not essential
        command = f"Speed2 {profile}"
        self.send_command(command)

    def setSpeed2(self,profile,speedpct):
        command = f"Speed2 {profile} {speedpct}"
        self.send_command(command)

    def getAccel(self,profile):#not essential
        command = f"Accel {profile}"
        self.send_command(command)

    def setAccel(self,profile,accelpct):
        command = f"Accel {profile} {accelpct}"
        self.send_command(command)

    def getAccRamp(self,profile):#not essential
        command = f"AccRamp {profile}"
        self.send_command(command)

    def setAccRamp(self,profile,accrampval):
        command = f"AccRamp {profile} {accrampval}"
        self.send_command(command)

    def getDecel(self,profile):#not essential
        command = f"Decel {profile}"
        self.send_command(command)

    def setDecel(self,profile,decelpct):
        command = f"Decel {profile} {decelpct}"
        self.send_command(command)

    def getInRangeValue(self):#not essential
        command = f"InRange"
        self.send_command(command)

    def setInRangeValue(self,inRangeVal): 
        command = f"Inrage {inRangeVal}"
        self.send_command(command) #redundant, this function is baked into setProfile

    def getStraightValue(self,profile):
        command = f"Straight {profile}"
        self.send_command(command)

    def setStraightPath(self,profile):
        command = "Straight -1"
        self.send_command(command)

    def setJointPath(self,profile):
        command = "Straight 0"
        self.send_command(command)

    def getProfile(self,profile):
        command = f"Profile {profile}"
        self.send_command(command)
    
    def setProfile(self,profile,speed,speed2,accel,decel,accelramp,decelramp,InRange,Straight):
        command = f"Profile {profile} {speed} {speed2} {accel} {decel} {accelramp} {decelramp} {InRange} {Straight}"
        self.send_command(command)
        #Use for defining a profile's info for the first time
        #play around with decelramp and accelramp values to see if they're even worth including in this function as arguments...



    
        

    #MOTION-RELATED COMMANDS
        
    def move(self,location,profile):
        command = f"move {location} {profile}"
        self.send_command(command)

    def moveAppro(self,location,profile):
        command = f"moveAppro {location} {profile}"
        self.send_command(command)

    def moveC(self,profile,x,y,z,yaw): #argument 8: sets config property for location"
        command = f"moveC {profile} {x} {y} {z} {yaw} 90 180"
        self.send_command(command)

    #def moveJ?

    def releaseBrake(self,axisnum):
        command = f"releaseBrake {axisnum}"
        self.send_command(command)

    def enableBrake(self,axisnum):
        command = f"setBrake {axisnum}"
        self.send_command(command)

    def moveOneAxis(self,axisnum,destination,profile):
        command = f"moveOneAxis {axisnum} {destination} {profile}"
        self.send_command(command)

    def waitForSync(self):
        command = "waitforEOM"
        self.send_command(command)

    #GRIPPER COMMANDS

    #must write function that takes desired measurement of object to be picked up
    #and stores as a gripper position in a class member variable
  

 
    def setGripperPositions(self,platewidth):
        self.openGripperPos = platewidth*3 #some sort of logic to convert plate width to gripper positions
        self.closedGripperPos = platewidth*2.5

    def openGripper(self,profile):
        command = f"moveOneAxis 5 {self.openGripperPos} {profile}"
        self.send_command(command)

    def closeGripper(self,profile):
        command = f"moveOneAxis 5 {self.openGripperPos} {profile}"
        self.send_command(command)
        #must tweak gripper open and close positions depending on what it's picking up!

    