#consolidated version of PreciseArm class; only includes methods needed for basic arm operation/automation
import socket 
import time

class PF3400Controller:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.connect()
        self.teachpointtype = ""

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
                

    def rcvdata(self,buffer_size=1024):
        data = self.socket.recv(buffer_size).decode()
        return data

    def close(self):
        command = "exit"
        self.sendcmd(command)
        self.socket.close()
        print("Connection closed.")

    def pause(self,time: int):
        print(f"Waiting {time} seconds")
        time.sleep(time)

    def attachRobot(self):
        command = "attach 1"
        self.sendcmd(command)
        
    def detachRobot(self):
        command = "attach 0"
        self.sendcmd(command)

    def home(self):
        command = "homeAll"
        self.sendcmd(command)
        self.pause(10)
        print("Robot homed.")

    def powerOn(self):
        command = "hp 1"
        self.sendcmd(command)

    def powerOff(self):
        command = "hp 0"
        self.sendcmd(command)

    def setMasterSpeed(self,speedpct: int):
        command = f"mspeed {speedpct}"
        self.sendcmd(command)
        print(f"Master speed set to {speedpct}")

    def halt(self):
        command = "halt"
        self.sendcmd(command)
        print("Robot halted.")

    def safeStop(self): #use as an exception handler for motion-related commands
        self.halt()
        self.enableBrake()
        self.powerOff()
    
    def setZclearance(self,location: int,zclearance: int): #z clearance in millimeters, generally around ~25mm
        command = f"locZclearance {location} {zclearance}"
        self.sendcmd(command)
        print(f"Z Clearance for Location {location} set to {zclearance}.")

    def setProfile(self,profile: int,speed: int,speed2: int,accel: int,decel: int,accelramp: float,decelramp: float,InRange: int,Straight: int):
        command = f"Profile {profile} {speed} {speed2} {accel} {decel} {accelramp} {decelramp} {InRange} {Straight}"
        self.sendcmd(command)
        print(f"Motion Profile {profile} defined.")
        #Use for defining a profile's info for the first time
        #Just like teachpoints, each profile is defined by a numeber from 1 to 20
        

    def genericProfile(self,profile: int):
        command = "Profile 50 0 100 100 0.1 0.1 10 0"
        self.sendcmd(command)
        print(f"Motion Profile {profile} set to generic.")

    def move(self,location,profile: int):
        command = f"move {location} {profile}"
        self.sendcmd(command)
        print(f"Arm moving to Teachpoint {location} with Motion Profile {profile}.")

    def appro(self,location: int,profile: int):
        command = f"moveAppro {location} {profile}"
        self.sendcmd(command)
        print (f"Arm approaching Teachpoint {location} with Motion Profile {profile}.")

    def approAndMove(self,location: int,profile: int): #consolidated form of the previous 2 methods
        command = f"moveAppro {location} {profile}"
        self.sendcmd(command)
        print(f"Arm approaching Teachpoint {location} with Motion Profile {profile}")
        self.waitForSync
        command2 = f"move {location} {profile}"
        self.sendcmd(command2)
        print(f"Arm moving to Teachpoint {location} with Motion Profile {profile}")
        self.waitForSync

    def releaseBrake(self,axisnum: int):
        command = f"releaseBrake {axisnum}"
        self.sendcmd(command)
        print("Brake released.")

    def enableBrake(self,axisnum: int):
        command = f"setBrake {axisnum}"
        self.sendcmd(command)
        print("Brake enabled.")

    def moveOneAxis(self,axisnum: int,destination: float,profile: int):
        command = f"moveOneAxis {axisnum} {destination} {profile}"
        self.sendcmd(command)

    def waitForSync(self):
        command = "waitForEom"
        self.sendcmd(command)
        #makes the arm wait until it's at its current destination before accepting any further commands

    def openGripper(self,profile: int):
        command = f"moveOneAxis 5 {self.openGripperPos} {profile}"
        self.sendcmd(command)

    def closeGripper(self,profile: int):
        command = f"moveOneAxis 5 {self.openGripperPos} {profile}"
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
            
