
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 12:04:06 2020
@author: Feucht
"""
#test github

import numpy as np
import random
import matplotlib.pyplot as plot
from datetime import datetime
import pandas as pd

"-------------------------- CLASSES ------------------------------"

class point6D:
    """ First three parameters are for location, next three for the velocities """
    def __init__(self,x,y,z,v_x,v_y,v_z):
        self.location = np.array([x,y,z])
        self.velocity = np.array([v_x,v_y,v_z])
        self.velocityMagnitude= np.sqrt(self.velocity[0]**2+self.velocity[1]**2+self.velocity[2]**2)

class body:
    """ Body contains the 6D locational parameters, the mass, and an optional name """
    def __init__(self,point6D,mass=0,name=""):
        self.point6D = point6D
        self.mass = mass
        self.name = name
        
"-------------------------- FUNCTIONS ------------------------------"
def run_simulation(bodies_List,timeStep,numberOfSteps):
    completeListOfSimulatedBodies = [] # Generate List for all bodies which will contain for each body the point6D data for each step
    for currentBody in bodies_List: # Init all body entries in the list completeListOfSimulatedBodies
        completeListOfSimulatedBodies.append({"name":currentBody.name, "x":[], "y":[], "z":[],"vx":[],"vy":[],"vz":[],"velocityMagnitude":[]}) # Init: Add body to list with point6D data for each step calculated
        
        #as below the main for-loop, this is added here in order to have the initial values in the list
        # for index, body_location in enumerate(completeListOfSimulatedBodies):
        #         body_location["x"].append(bodies_List[index].point6D.location[0])
        #         body_location["y"].append(bodies_List[index].point6D.location[1])           
        #         body_location["z"].append(bodies_List[index].point6D.location[2]) 
        #         body_location["vx"].append(bodies_List[index].point6D.velocity[0])
        #         body_location["vy"].append(bodies_List[index].point6D.velocity[1])           
        #         body_location["vz"].append(bodies_List[index].point6D.velocity[2])
        #         body_location["velocityMagnitude"].append(bodies_List[index].point6D.velocityMagnitude)
    
    for i in range(0,numberOfSteps): # Loop over steps
        computeSingleStepOnAll(bodies_List,timeStep)
        
        #now add the entries in the dictionary
        report_freq=7                
        if i % report_freq == 0:
            for index, body_location in enumerate(completeListOfSimulatedBodies):
                body_location["x"].append(bodies_List[index].point6D.location[0])
                body_location["y"].append(bodies_List[index].point6D.location[1])           
                body_location["z"].append(bodies_List[index].point6D.location[2])
                body_location["vx"].append(bodies_List[index].point6D.velocity[0])
                body_location["vy"].append(bodies_List[index].point6D.velocity[1])           
                body_location["vz"].append(bodies_List[index].point6D.velocity[2])
                body_location["velocityMagnitude"].append(np.sqrt(bodies_List[index].point6D.velocity[0]**2+bodies_List[index].point6D.velocity[1]**2+bodies_List[index].point6D.velocity[2]**2))
        print(f"step {i+1} {datetime.now()}")
    return completeListOfSimulatedBodies

def computeSingleStepOnAll(bodies_List,timeStep):
    computeNewVelocitiesOnAll(bodies_List,timeStep)
    computeNewLocationsOnAll(bodies_List,timeStep)
    
def computeNewVelocitiesOnAll(bodies_List,timeStep):
    for body_index, currentBody in enumerate(bodies_List):
        acceleration3D=calculateSingleBodyAcceleration(bodies_List,body_index)
        currentBody.point6D.velocity += acceleration3D*timeStep
        
        
def computeNewLocationsOnAll(bodies_List,timeStep):
    for currentBody in bodies_List:
        currentBody.point6D.location[0] += currentBody.point6D.velocity[0] * timeStep
        currentBody.point6D.location[1] += currentBody.point6D.velocity[1] * timeStep
        currentBody.point6D.location[2] += currentBody.point6D.velocity[2] * timeStep  
        

def calculateSingleBodyAcceleration(bodies_List,body_index):
    G_const = 6.67408e-11 #m3 kg-1 s-2 
    acceleration3D=np.array([0.0,0.0,0.0]) # INIT
    i=body_index
    currentBody=bodies_List[body_index]
    
    for j, otherBody in enumerate(bodies_List): #
        if j != i: #if i=j then we got the same object, do not calc; if i!=j then calc acceleration to all other bodies
            distance=np.linalg.norm(currentBody.point6D.location-otherBody.point6D.location)
            softening=0.0**2 #immer größer als 0
            MasterCalculation= (G_const * otherBody.mass*currentBody.mass)/(distance**2+softening**2)**(3/2)
            acceleration3D[0]+=(MasterCalculation * (otherBody.point6D.location[0]-currentBody.point6D.location[0]))/currentBody.mass
            acceleration3D[1]+=(MasterCalculation * (otherBody.point6D.location[1]-currentBody.point6D.location[1]))/currentBody.mass
            acceleration3D[2]+=(MasterCalculation * (otherBody.point6D.location[2]-currentBody.point6D.location[2]))/currentBody.mass
                
    return acceleration3D #result acceleration after every comparison
   
def plot_output(bodies, outfile = None):
    fig = plot.figure(num=1,figsize=(20, 20), dpi=300)
    
    colours = ['r','b','g','y','m','c']
    ax1 = fig.add_subplot(4,1,1, projection='3d',)
    ax2 = fig.add_subplot(4,1,2,)
    ax3 = fig.add_subplot(4,1,3,)
    ax4 = fig.add_subplot(4,1,4,)
    max_range = 0
    for current_body in bodies: 
        if current_body["name"]==massMassiveName:
            max_dim = max(max(current_body["x"]),max(current_body["y"]),max(current_body["z"]))
            if max_dim > max_range:
                max_range = max_dim
            c = random.choice(colours) #for plotting
            ax1.plot(current_body["x"], current_body["y"], current_body["z"], 'r--', label = current_body["name"])
            ax2.plot(current_body["x"], current_body["z"], 'r--', label = current_body["name"])         
            ax3.plot(current_body["x"], current_body["y"], 'r--', label = current_body["name"])
            ax4.plot(current_body["y"], current_body["z"], 'r--', label = current_body["name"])
        else:
            None
        
                     

            
    ax1.set_xlim([-2500,15000])    
    ax1.set_ylim([-10000,15000])
    ax1.set_zlim([-10000,15000])
    ax1.set_xlabel('x label')  # Add an x-label to the axes.
    ax1.set_ylabel('y label')  # Add a y-label to the axes.
    ax1.set_zlabel('z label')
    ax1.set_title("3D")  # Add a title to the axes.
    
   # ax1.legend()        
     
    ax2.set_xlim([-2500,15000])    
    ax2.set_ylim([-10000,15000])
    ax2.set_xlabel('x label')  # Add an x-label to the axes.
    ax2.set_ylabel('z label')  # Add a y-label to the axes.
    ax2.set_title("x-z von vorne drauf")
   # ax2.legend()  

    ax3.set_xlim([-max_range*1.1,max_range*1.1])
    ax3.set_ylim([-max_range*1.1,max_range*1.1])
    ax3.set_xlabel('x label')  # Add an x-label to the axes.
    ax3.set_ylabel('y label')  # Add a y-label to the axes.
    ax3.set_title("x-y Von oben drauf")
   # ax3.legend() 
    
    ax4.set_xlim([-2500,1500])  
    ax4.set_ylim([-10000,15000])
    ax4.set_xlabel('y label')  # Add an x-label to the axes.
    ax4.set_ylabel('z label')  # Add a y-label to the axes.
    ax4.set_title("y-z von der Seite drauf")
    #ax4.legend() 

    ax1.legend().set_visible(False)
    ax2.legend().set_visible(False)
    ax3.legend().set_visible(False)
    ax4.legend().set_visible(False)

    plot.tight_layout(pad=1, w_pad=3, h_pad=1)
    if outfile:
        plot.savefig(outfile)
    else:
        plot.show()
        

    
"-------------------------- PROGRAM ------------------------------"
print(f"start {0} {datetime.now()}")

x_bound = 5000# therefore -10 to 10
y_bound = 50000
z_bound = 5000
massSmallObjects=5e14
massMassiveObject=5e15
massMassiveName="Massive"
bodies_List=[]
TotalBodies=200
timeStep=0.5#1s000
numberOfSteps=100000
for i in range(TotalBodies-1):
    random.seed(i)
    bodies_List.append((body(point6D(random.uniform(-x_bound,x_bound),random.uniform(-y_bound,y_bound),random.uniform(-z_bound,z_bound), random.gauss(0, 0.25),random.gauss(0, 0.25),random.gauss(0,0.25)), massSmallObjects,name=f"koerper{i}")))
    
    
#Massiv Object
bodies_List.append((body(point6D(-5500.5,0.0, 0.0,25,0.0,0.0),massMassiveObject,name=massMassiveName)))




calculatedSim=run_simulation(bodies_List, timeStep, numberOfSteps)
print(f"Do plots {datetime.now()}")
plot_output(calculatedSim,"test2.png")

table_velocityMagnitude=list()
for index,entry in enumerate(calculatedSim):
    table_velocityMagnitude.append(entry["velocityMagnitude"])
df1=pd.DataFrame(table_velocityMagnitude)

table_locationx=list()
for index,entry in enumerate(calculatedSim):
    table_locationx.append(entry["x"])
df2= pd.DataFrame(table_locationx)
    
table_locationY=list()
for index,entry in enumerate(calculatedSim):
    table_locationY.append(entry["y"])
df3= pd.DataFrame(table_locationY)

table_locationZ=list()
for index,entry in enumerate(calculatedSim):
    table_locationZ.append(entry["z"])
df4= pd.DataFrame(table_locationZ)

table_velocityX=list()
for index,entry in enumerate(calculatedSim):
    table_velocityX.append(entry["vx"])
df5= pd.DataFrame(table_velocityX)
    
table_velocityY=list()
for index,entry in enumerate(calculatedSim):
    table_velocityY.append(entry["vy"])
df6= pd.DataFrame(table_velocityY)

table_velocityZ=list()
for index,entry in enumerate(calculatedSim):
    table_velocityZ.append(entry["vz"])
df7= pd.DataFrame(table_velocityZ)

"---------------------------------------------------------------------"
# https://blog.finxter.com/matplotlib-animation/´#könnte theoretisch funktionieren und eine animierte Version erstellen....
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation 
# # Set up empty Figure, Axes and Line objects
# fig, ax = plot.subplots()
# # Set axes limits so that the whole image is included
# ax.set(xlim=(-10,10), ylim=(-10, 10))
# # Draw a blank line
# line, = ax.plot([], [])

# # Define data

# #x=calculatedSim[0]["x"][i]
# #y=calculatedSim[0]["y"][i]
# #z=calculatedSim[0]["z"][i]

# # Define animate function
# def animate(i):
#     line.set_data(i, i)
#     return line,

# # def animate(i):
# #     line.set_data(calculatedSim[0]["x"][i], calculatedSim[0]["y"][i])
# #     return line,

# anim = FuncAnimation(fig, animate, frames=TotalBodies, interval=30, blit=True)
# # Save in the current working directory
# anim.save('sin.mp4')