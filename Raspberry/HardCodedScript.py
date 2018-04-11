import motorTest as Motors
import RobotArm as Robotarm
import Pump as Pump

car=Motors.Car()
rb=Robotarm.RobotArm()
pump=Pump.Pump()



def zabivane():
    rb.moveServo(1,150)
    rb.moveServo(2,30)
    rb.moveServo(3,90)
    rb.mvoeServo(1,180)
    pump.f(1)
    rb.moveServo(1,140)
    rb.moveServo(2,60)
    rb.moveServo(3,160)


def dvijenie():
    car.f(1)
    zabivane()
    car.b(1)
    car.r(3)
    car.f(1)
    zabivane()
    car.b(1)


dvijenie()
dvijenie()
dvijenie()
dvijenie()
