SCREEN_SIZE = (800, 600)
CONSTANT_FACTOR = 262144

import pygame
from pygame.locals import *
import math


class Particle(object):
    def __init__ (self, p_id, mass = 5000):
        self.p_id = p_id
        self.pos_x = 0
        self.pos_y = 0
        self.del_x = 0
        self.del_y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.accel_x = 0
        self.accel_y = 0
        self.mass = mass
        self.min_mov_x = 0
        self.min_mov_y = 0
        
    def __str__(self):
        st = "Id: %s, Pos:(%f,%f), Vel:(%f,%f),Mass:%f" % (str(self.p_id), self.pos.x, self.pos.y, self.vel.x, self.vel.y, self.mass)
        return st

    def clear_all(self):
        self.pos_x = 0
        self.pos_y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.accel_x = 0
        self.accel_y = 0

    def get_min_mov_x(self):
        return self.min_mov_x

    def get_min_mov_y(self):
        return self.min_mov_y

    ## min mov is used stop cuttoff due to roundoff error
    def set_min_mov_x(self, min_mov_x):
        self.min_mov_x = int(min_mov_x)

    ## min mov is used stop cuttoff due to roundoff error
    def set_min_mov_y(self, min_mov_y):
        self.min_mov_y = int(min_mov_y)

    def update_particle(self, delta_t):
        self.vel_x += self.accel_x * delta_t
        self.vel_y += self.accel_y * delta_t
        self.pos_x += self.vel_x * delta_t + ((self.accel_x) * (delta_t ** 2)) / 2
        self.pos_y += self.vel_y * delta_t + ((self.accel_y) * (delta_t ** 2)) / 2
        
    
    ## Returns the x coordinate of the particle's position
    def get_pos_x(self):
        return self.pos_x

    ## Returns the x coordinate of the particle's position
    def get_pos_y(self):
        return self.pos_y

    ## Returns a tuple (x, y) of the particle's position
    def get_pos_tup(self):
        return self.pos_x, self.pos_y

    def get_del_x(self):
        return self.del_x

    def get_del_y(self):
        return self.del_y

    def get_del_tup(self):
        return self.del_x, self.del_y

    ## Returns the x coordinate of the particle's position
    def get_vel_x(self):
        return self.vel_x

    ## Returns the x coordinate of the particle's position
    def get_vel_y(self):
        return self.vel_y

    ## Returns a tuple (x, y) of the particles velocity
    def get_vel_tup(self):
        return self.vel_x, self.vel_y

    ## Returns the x coordinate of the particle's acceleration
    def get_accel_x(self):
        return self.accel_x

    ## Returns the y coordinate of the particle's acceleration
    def get_accel_y(self):
        return self.accel_y

    ## Returns a tuple (x, y) of the particle's acceleration
    def get_accel_tup(self):
        return self.accel_x, self.accel_y

    ## Returns the particle's id, used to identify it in a list of particles
    def get_id(self):
        return self.p_id

    ## Returns a floating point number representing the particle's mass.
    def get_mass(self):
        return self.mass

    ## Returns True or False depending on if the particle is located within a given rectangle
    def inside_box(self, x_min, x_max, y_min, y_max):
        if self.pos_x >= x_min:
            if self.pos_x <= x_max:
                if self.pos_y >= y_min:
                    if self.pos_y <= y_max:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    ## Takes a 2D Vector object as input, and sets it as the particles pos attribute
    def set_pos_tup(self, new_pos):
        self.pos_x, self.pos_y = new_pos

    ## Takes in a floating point number, and sets the 2D Vector object pos's attribut 'x' to that value
    def set_pos_x(self, new_x):
        self.pos_x = int(new_x)

    ## Takes in a floating point number, and sets the 2D Vector object pos's attribut 'y' to that value
    def set_pos_y(self, new_y):
        self.pos_y = int(new_y)

    ## Takes a 2D Vector object as input, and sets it as the particles vel attribute
    def set_vel_tup(self, new_vel):
        self.vel_x, self.vel_y = new_vel
        
    ## Takes in a floating point number, and sets the 2D Vector object vel's attribut 'x' to that value
    def set_vel_x(self, new_x):
        self.vel_x = int(new_x)
        
    ## Takes in a floating point number, and sets the 2D Vector object vel's attribut 'y' to that value
    def set_vel_y(self, new_y):
        self.vel_y = int(new_y)

    ## Takes a 2D Vector object as input, and sets it as the particles accel attribute
    def set_accel_tup(self, new_accel):
        self.accel_x, self.accel_y = new_accel
        
    ## Takes in a floating point number, and sets the 2D Vector object accel's attribut 'x' to that value
    def set_accel_x(self, new_x):
        self.accel_x = int(new_x)
        
    ## Takes in a floating point number, and sets the 2D Vector object accel's attribut 'y' to that value
    def set_accel_y(self, new_y):
        self.accel_y = int(new_y)

    ## Sets the particle's id
    def set_id(self, newID):
        self.p_id = newID

    ## Sets the particle's mass
    def set_mass(self, new_mass):
        self.mass = int(new_mass)

class ParticleList(object):
    def __init__(self):
        self.particle_list = []
        self.particle_ids = set()
        self.index = 0
        
    def __iter__(self):
        return self

    def get_x_edges(self):
        min_x = self.particle_list[0].get_pos_x()
        max_x = self.particle_list[0].get_pos_x()
        for particle in self.particle_list:
            if particle.get_pos_x() < min_x:
                min_x = particle.get_pos_x()
            if particle.get_pos_x() > max_x:
                max_x = particle.get_pos_x()
        return min_x, max_x

    def get_y_edges(self):
        min_y = self.particle_list[0].get_pos_y()
        max_y = self.particle_list[0].get_pos_y()
        for particle in self.particle_list:
            if particle.get_pos_y() < min_y:
                min_y = particle.get_pos_y()
            if particle.get_pos_y() > max_y:
                max_y = particle.get_pos_y()
        return min_y, max_y
        
    def get_all_ids_positions(self):
        ret_list = []
        for part in self.particle_list:
            x, y = part.get_pos_tup()
            p_id = part.get_id()
            ret_list.append((p_id, x, y))
        return iter(ret_list)

    def get_center_mass_from_ids(self, input_ids):
        cen_mass_x = 0
        cen_mass_y = 0
        temp_mass = 0
        for part in self.particle_list:
            if part.get_id() in input_ids:
                part_mass = part.get_mass()
                part_cmx = part_mass * part.get_pos_x()
                part_cmy = part_mass * part.get_pos_y()
                cen_mass_x = cen_mass_x + part_cmx
                cen_mass_y = cen_mass_y + part_cmy
                temp_mass = temp_mass + part_mass
        return (cen_mass_x / temp_mass), (cen_mass_y / temp_mass)

    def get_center_mass_from_bounds(self, x_min, x_max, y_min, y_max):
        cen_mass_x = 0
        cen_mass_y = 0
        temp_mass = 0
        for part in self.particle_list:
            pos_x, pos_y = part.get_pos_tup()
            if ((pos_x < x_max) and (pos_x >= x_min) and (pos_y < y_max) and (pos_y >= y_min)):
                part_mass = part.get_mass()
                part_cmx = part_mass * pos_x
                part_cmy = part_mass * pos_y
                cen_mass_x = cen_mass_x + part_cmx
                cen_mass_y = cen_mass_y + part_cmy
                temp_mass = temp_mass + part_mass
        return (cen_mass_x / temp_mass), (cen_mass_y / temp_mass)


    def get_center_mass_system(self):
        cen_mass_x = 0
        cen_mass_y = 0
        temp_mass = 0
        for part in self.particle_list:
            pos_x, pos_y = part.get_pos_tup()
            part_mass = part.get_mass()
            part_cmx = part_mass * pos_x
            part_cmy = part_mass * pos_y
            cen_mass_x = cen_mass_x + part_cmx
            cen_mass_y = cen_mass_y + part_cmy
            temp_mass = temp_mass + part_mass
        mass_and_center_tup = (int(temp_mass), int(cen_mass_x / temp_mass), int(cen_mass_y / temp_mass))
        return mass_and_center_tup

    def get_positions_from_ids(self, input_ids):
        pos_list = []
        for part in self.particle_list:
            if part.get_id() in input_ids:
                x, y = part.get_pos_tup()
                pos_list.append((x, y))
        return iter(pos_list)

    def get_velocities_from_ids(self, input_ids):
        vel_list = []
        for part in self.particle_list:
            if part.get_id() in input_ids:
                vx, vy = part.get_vel_tup()
                vel_list.append((vx, vy))
        return iter(vel_list)

    def get_accelerations_from_ids(self, input_ids):
        accel_list = []
        for part in self.particle_list:
            if part.get_id() in input_ids:
                ax, ay = part.get_accel_tup()
                accel_list.append((ax, ay))
        return iter(accel_list)

    def get_mass_of_list(self, input_ids):
        total_mass = 0
        for part in self.particle_list:
            if part.get_id() in input_ids:
                total_mass += part.get_mass()
        return total_mass

    def inside_box(self, x_min, x_max, y_min, y_max):
        inside_list = []
        for part in self.particle_list:
            x, y = part.get_pos_tup()
            if (x <= x_max) and (x >= x_min) and (y <= y_max) and (y >= y_min):
                inside_list.append(part.get_id())
        return iter(inside_list)

    def get_length(self):
        return len(self.particle_list)

    def reset_index(self):
        self.index = 0

    ## adds a particle object to the collection, and ensures no copies of the same particle are included
    ## by checking if it's id is in the id list.
    def add_particle(self, particle_pointer):
        particle_id = particle_pointer.get_id()
        if particle_id not in self.particle_ids:
            self.particle_ids.add(particle_id)
            self.particle_list.append(particle_pointer)

    def get_id_set(self):
        return self.particle_ids

    def get_id_iter(self):
        return iter(self.particle_ids)

    def get_particle_pointer(self, particle_id):
        for part in self.particle_list:
            if part.get_id() == particle_id:
                return part
        return None

    def is_member(self, particle_id):
        return (particle_id in self.particle_ids)

    def get_all_particles_iter(self):
        return iter(self.particle_list)

    def first_particle_pointer(self):
        return self.particle_list[0]

    @classmethod
    def get_sub_from_ids(cls, input_ids):
        ret_list = cls()
        for part in particle_list:
            if part.get_ids() in input_ids:
                ret_list.add_particle(part)
        if ret_list.get_length() > 0:
            return ret_list
        else:
            return None

def translate_to_screen(screen_size, constant_factor, x, y):
    base_x, base_y = screen_size
    new_x = ((constant_factor / 2 + x) * base_x) / constant_factor
    new_y = ((constant_factor / 2 - y) * base_y) / constant_factor
    return int(new_x), int(new_y)

def main():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0)

    clock = pygame.time.Clock()

    BLACK = (0,0,0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    x_min_mov = CONSTANT_FACTOR / SCREEN_SIZE[0]
    y_min_mov = CONSTANT_FACTOR / SCREEN_SIZE[1]

    G = 385573
    num_particles = 20

    screen.fill(WHITE)

    x_min_mov = CONSTANT_FACTOR / SCREEN_SIZE[0] + 1
    y_min_mov = CONSTANT_FACTOR / SCREEN_SIZE[1] + 1

    y_prime = CONSTANT_FACTOR
    x_prime = CONSTANT_FACTOR * 3 / 4
    m_part_list = ParticleList()

    for i in range(num_particles):
        theta = math.radians((360 * i / num_particles))
        x = (x_prime / 2) * math.cos(theta)
        y = (y_prime / 2) * math.sin(theta)
        new_particle = Particle(i + 1)
        new_particle.set_pos_x(x)
        new_particle.set_pos_y(y)
        new_particle.set_min_mov_x(x_min_mov)
        new_particle.set_min_mov_y(y_min_mov)
        m_part_list.add_particle(new_particle)

    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        delta_t = clock.tick()
        screen.lock()
        screen.fill(WHITE)
        for particle in m_part_list.get_all_particles_iter():
            accel_x_on_particle, accel_y_on_particle = 0, 0
            particle_pos_x = particle.get_pos_x()
            particle_pos_y = particle.get_pos_y()
            for other_particle in m_part_list.get_all_particles_iter():
                if other_particle != particle:
                    other_pos_x = other_particle.get_pos_x()
                    other_pos_y = other_particle.get_pos_y()
                    delta_x = other_pos_x - particle_pos_x
                    delta_y = other_pos_y - particle_pos_y
                    r_mag = math.sqrt((delta_x ** 2) + (delta_y ** 2))
                    if r_mag > 0:                        
                        a_mag = (G * other_particle.get_mass() ) / ((delta_x ** 2) + (delta_y ** 2))
                        ax, ay = a_mag * (delta_x / r_mag), a_mag * (delta_y / r_mag)
                        accel_x_on_particle += ax
                        accel_y_on_particle += ay
                        ##other_pos_v, other_pos_w = translate_to_screen(SCREEN_SIZE, CONSTANT_FACTOR, other_pos_x, other_pos_y)
                        ##particle_pos_v, particle_pos_w = translate_to_screen(SCREEN_SIZE, CONSTANT_FACTOR, particle_pos_x, particle_pos_y)
                        ##pygame.draw.line(screen, BLUE, (particle_pos_v, particle_pos_w), (other_pos_v, other_pos_w), 1)
            if accel_x_on_particle > x_min_mov:
                particle.set_accel_x(accel_x_on_particle)
            else:
                new_ax = particle.get_accel_x() + accel_x_on_particle
                particle.set_accel_x(new_ax)
            if accel_y_on_particle > y_min_mov:
                particle.set_accel_y(accel_y_on_particle)
            else:
                new_ay = particle.get_accel_y() + accel_y_on_particle
                particle.set_accel_y(new_ay)   
            particle.update_particle(delta_t)
            pos_v, pos_w = particle.get_pos_tup()
            pos_x, pos_y = translate_to_screen(SCREEN_SIZE, CONSTANT_FACTOR, pos_v, pos_w)
            pygame.draw.circle(screen, RED, (pos_x, pos_y), 2)

        screen.unlock()
        pygame.display.update()

main()
