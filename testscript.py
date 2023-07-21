from PF3400 import PF3400Controller
import time

def main():

   
    ip = "192.168.0.1"
    port = 10100
    arm = PF3400Controller(ip,port)
  
    arm.connect()
    print("Connecting to TCP Command Server...")
    arm.poweron()
    print("Arm power on.")
    arm.home()
    print("Robot homed.")
    arm.attachrobot()
    print("Robot attached.")
    arm.WaitforEOM()

    arm.setProfile(1,50,0,100,100,0.1,0.1,10,0)
    print("Motion Profile 1 Defined.")
    arm.setCartesianLoc(1,207,-139,-4,-134)
    print("Teachpoint 1 set.")
    arm.setCartesianLoc(2,238,-100,23,-119)
    print("Teachpoint 2 set.")
    arm.setCartesianLoc(3,100,-18,45,-100)
    print("Teachpoint 3 set.")

    print("Moving arm to Teachpoint 1.")
    arm.moveAppro(1,1)
    arm.move(1,1)
    time.sleep(5)
    print("Waiting 5 seconds.")

    print("Moving arm to Teachpoint 2.")
    arm.moveAppro(2,1)
    arm.move(2,1)
    time.sleep(5)
    print("Waiting 5 seconds.")

    print("Moving arm to Teachpoint 3.")
    arm.moveAppro(3,1)
    arm.move(3,1)
    time.sleep(5)
    print("Waiting 5 seconds.")



    arm.detachrobot()
    arm.poweroff()


    if __name__ == "__main__":
        main()

