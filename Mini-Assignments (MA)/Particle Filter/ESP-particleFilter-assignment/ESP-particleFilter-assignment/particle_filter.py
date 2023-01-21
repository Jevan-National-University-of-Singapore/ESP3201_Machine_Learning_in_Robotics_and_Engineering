from os import replace
import numpy as np
from numpy.lib import math
from numpy.random import exponential
import scipy.stats

def initialize_particles(num_particles, map_limits):
    # randomly initialize the particles inside the map limits
    particles = []

    for i in range(num_particles):
        particle = dict()

        # draw x,y and theta coordinate from uniform distribution
        # inside map limits
        particle['x'] = np.random.uniform(map_limits[0], map_limits[1])
        particle['y'] = np.random.uniform(map_limits[2], map_limits[3])
        particle['theta'] = np.random.uniform(-np.pi, np.pi)

        particles.append(particle)

    return particles


def mean_pose(particles):
    # calculate the mean pose of a particle set.
    #
    # for x and y, the mean position is the mean of the particle coordinates
    #
    # for theta, we cannot simply average the angles because of the wraparound 
    # (jump from -pi to pi). Therefore, we generate unit vectors from the 
    # angles and calculate the angle of their average 

    # save x and y coordinates of particles
    xs = []
    ys = []

    # save unit vectors corresponding to particle orientations 
    vxs_theta = []
    vys_theta = []

    for particle in particles:
        xs.append(particle['x'])
        ys.append(particle['y'])

        #make unit vector from particle orientation
        vxs_theta.append(np.cos(particle['theta']))
        vys_theta.append(np.sin(particle['theta']))

    #calculate average coordinates
    mean_x = np.mean(xs)
    mean_y = np.mean(ys)
    mean_theta = np.arctan2(np.mean(vys_theta), np.mean(vxs_theta))

    return [mean_x, mean_y, mean_theta]

def sample_motion_model(odometry, particles):
    # Samples new particle positions, based on old positions, the odometry
    # measurements and the motion noise 

    delta_rot1 = odometry['r1']
    delta_trans = odometry['t']
    delta_rot2 = odometry['r2']

    # the motion noise parameters: [alpha1, alpha2, alpha3, alpha4]
    noise = [0.1, 0.1, 0.05, 0.05]
    
    # standard deviations of motion noise
    sigma_delta_rot1 = noise[0] * abs(delta_rot1) + noise[1] * delta_trans
    sigma_delta_trans = noise[2] * delta_trans + noise[3] * (abs(delta_rot1) + abs(delta_rot2))
    sigma_delta_rot2 = noise[0] * abs(delta_rot2) + noise[1] * delta_trans
    
    # generate new particle set after motion update
    new_particles = []

    for particle in particles:
        new_particle = dict()
        #sample noisy motions
        noisy_delta_rot1 = delta_rot1 + np.random.normal(0, sigma_delta_rot1)
        noisy_delta_trans = delta_trans + np.random.normal(0, sigma_delta_trans)
        noisy_delta_rot2 = delta_rot2 + np.random.normal(0, sigma_delta_rot2)
        
        #calculate new particle pose
        new_particle['x'] = particle['x'] + \
            noisy_delta_trans * np.cos(particle['theta'] + noisy_delta_rot1)
        new_particle['y'] = particle['y'] + \
            noisy_delta_trans * np.sin(particle['theta'] + noisy_delta_rot1)
        new_particle['theta'] = particle['theta'] + \
            noisy_delta_rot1 + noisy_delta_rot2
        new_particles.append(new_particle)
    return new_particles


def eval_sensor_model(sensor_data, particles, landmarks):
    # Computes the observation likelihood of all particles, given the
    # particle and landmark positions and sensor measurements
    #
    # The employed sensor model is range only.

    sigma_r = 0.2

    #measured landmark ids and ranges
    ids = sensor_data['id']
    ranges = sensor_data['range']



    weights = []

    
    '''your code here'''
    for particle in particles: # for each particle
        weight = 1 # this weight have to multiply by each weight for each landmark
        for i in range(len(landmarks)): # for each landmark
            particle_range = math.sqrt((particle['x']-landmarks[i+1][0])**2 + (particle['y'] - landmarks[i+1][1])**2) #range of the particle from the landmark
            ''' start of likelihood function '''
            exponential_numerator = (-1) * ((sensor_data["range"][i] - particle_range)**2)
            exponential_denominator = 2 * ( sigma_r ** 2)
            weight_denom = math.sqrt(2 * math.pi * (sigma_r ** 2))
            weight *= math.exp(exponential_numerator/exponential_denominator) / weight_denom # multiplies the weight of previous landmarks
            ''' end of likelihood function'''
            
        weights.append(weight)

    weights = np.array(weights) # changing weights to numpy array
        

    '''***        ***'''


    #normalize weights
    normalizer = sum(weights)
    weights = weights / normalizer

    return weights

def resample_particles(particles, weights):
    # Returns a new set of particles obtained by performing
    # stochastic universal sampling, according to the particle weights.

    new_particles = []
    
    '''your code here'''

    wheel = []
    wheel.append([0, weights[0]])

    
    for i in range(len(weights)-1):
        wheel.append([wheel[i][1], wheel[i][1]+weights[i+1]])
    
    interval = 1/len(weights)
    current_pointer = np.random.uniform(0, 1/len(weights))


    it = 0
    while(it < len(weights)):
        if current_pointer > 1:
            break
        elif current_pointer >= wheel[it][0] and current_pointer < wheel[it][1]:
            new_particles.append(particles[it])
            current_pointer += interval
        else:
            it += 1


    
    '''***        ***'''


    return new_particles

