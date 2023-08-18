from PreciseArmLibrary import PF3400Controller
import time

def main():

   
    ip = "192.168.0.1"
    port = 10100
    arm = PF3400Controller(ip,port) 
  
    arm.connect() #socket connection via Telnet
    arm.powerOn()
    arm.home()
    arm.attachRobot()
    arm.waitForSync
    

    #set teachpoints and motion profile (can make multiple profiles)
    arm.TeachPointProtocol()
    arm.setProfile(1,50,0,100,100,0.1,0.1,10,0)

    duration = 28800  #we want to execute a block of action for 8 hours
    start_time = time.time()
    while time.time() - start_time < duration:
        #open gripper
        arm.openGripper()
        #move to teachpoint 1 with motion profile 1
        arm.approAndMove(1,1)
        #close gripper, pick the object up
        arm.closeGripper()
        #move to safe height (approach)
        arm.Approach(1,1)
        
        #move to teachpoint 2
        arm.approandMove(2,1)
        #put the object down
        arm.openGripper()
        #move to safe height
        arm.Approach(2,1)
        
        #move to teachpoint 3
        arm.approAndMove(3,1)
        #pick up an object
        arm.closeGripper()
        #move to safe height
        arm.Approach(3,1)
        #bring the object to teachpoint 1
        arm.approandMove(1,1)
        #put the object down 
        arm.openGripper()

      
        pass
   
    #detach, power off, exit
    arm.detachrobot()
    arm.poweroff()
    arm.exitTCP()
    


    if __name__ == "__main__":
        main()

