import numpy 
# number of forces
n = int(input("Enter number of loads:"))
loads  =[]
angles = []
distances =[]
for i in range (n):
   F = float(input(f"\Enter magnitude of load {i+1}(N):"))  
   angle = float(input(f"Enter anticlockwise angle with respect to x-axis{i+1}(degrees): "))
   distance = float(input(f"Enter distance from A {i+1}(meters):"))
   loads.append(F)
   angles.append(angle)
   distances.append(distance)
L= float(input("Enter length of beam:"))
Rx = 0
Ry = 0
moment=0
for i in range (n):
  angle_rad = numpy.radians(angles[i])
  Fx = loads[i]*numpy.cos(angle_rad)
  Fy = loads[i]*numpy.sin(angle_rad)
  Rx += Fx
  Ry += Fy 
  moment +=loads[i]*distances[i]*numpy.sin(angle_rad)
RBy=moment/L
print("RBy:",RBy)
RAy= Ry-RBy
print("RAy:",RAy)
print("RAx:",Rx )