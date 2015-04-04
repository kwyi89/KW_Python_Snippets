
# coding: utf-8

# In[3]:

import math
import random
import time

from collections import deque # for fast appends and pops on either end
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse

TICKS_PER_SEC = 60

# Size of sectors used to ease block loading.
SECTOR_SIZE = 16

WALKING_SPEED = 5
FLYING_SPEED = 15

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0 # About the height of a block.

# To derive the formula for calculating jump speed, first solve
# v_t = v_0 + a * t
# for the time at which you achieve max height, where a is the accelration
# due to gravity and v_t = 0. This gives:
# t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in 
# s = s_0 + v_0 * t + (a * t^2) / 2
JUMP_SPPED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2

def cube_vertices(x, y, z, n):
    """ Return the vertices of the cub at position x, y, z with size 2*n. """
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
    ]

def tex_coord(x, y, n=4):
    """ Return the bounding vertices of the texture square. """
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side."""
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result


TEXTURE_PATH = 'texture.png'

GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]

def normalize(position):
    """ Accepts 'position' of arbitrary precision and returns the block
    containing that position.
    
    Parameters
    ----------
    position : tuple of len 3
    
    Returns
    ----------
    block_position : tuple of ints of len 3
    
    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)

def sectorize(position):
    """ Returns a tuple representing the sector for the given 'position'.
    
    Parameters
    ----------
    position : tuple of len 3
    
    Returns
    ----------
    sector : tuple of len 3
    
    """
    x, y, z = normalize(position)
    x, y, z = x / SECTOR_SIZE, y / SECTOR_SIZE, z / SECTOR_SIZE
    return (x, 0, z)

class Model(object):
    
    def __init__(self):
        
        # A Batch is a collection of vertex lists for batched rendering.
        self.batch = pyglet.graphics.Batch()

        # A TextureGroup manages an OpenGL texture.
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())
        
        # A mapping from position to the texture of the block at that position.
        # This defines all the blocks that are currently in the world.
        self.world = {}
        
        # Same mapping as 'world' but only contains blocks that are shown.
        self.shown = {}
        
        # Mapping from sector to a list of positions inside that sector.
        self.sectors = {}
        
        # Simple function queue implementation. The queue is populated with
        # _show_block() and _hide_block() calls
        self.queue = deque()
        
        self._initialize()
        
    def _initialize(self):
        """ Initialize the world by placing all the blocks.
        
        """
        n = 80 # 1/2 width and height of world
        s = 1 # step size
        y = 0 # inital y height
        for x in xrange(-n, n + 1, s):
            for z in xrange(-n, n + 1, s):
                # create a layer stone and grass everywhere.
                self.add_block((x, y - 2, z), GRASS, immediate=False)
                self.add_block((x, y - 3, z), STONE, immediate=False)
                if x in (-n, n) or z in (-n, n):
                    # create outer walls.
                    for dy in xrange(-2, 3):
                        self.add_block((x, y + dy, z), Stone, immediate=False)
                        
        # generate the hills randomly
        o = n - 10
        for _ in xrange(120):
            a = random.randint(-o, o) # x position of the hill
            b = random.randint(-o, o) # z position of the hill
            c = -1 # base of the hill
            h = random.randint(1, 6) # height of the hill
            s = random.randint(4, 8) # 2 * s is the side length of the hill
            d = 1 # how quickly to taper off the hills
            t = random.choice([GRASS, SAND, BRICK])
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    if (x - a) ** 2 + (z -b) ** 2 > (s + 1) ** 2:
                        continue
                    if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                        continue
                    self.add_block((x, y, z), t, immediate=False)
                s -= d # decrement side length so hills taper off
                
    def hit_test(self, position, vector, max_distance=8):
        """ Line of sight search from current position. If a block is
        intersected it is returned, along with the block previously in the line
        of sight. If no block is found, return None, None.
        
        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check visibility from.
        vector : tuple of len 3
            The line of sight vector.
        max_distance : int
            How many blocks away to search for a hit.
            
        """
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in xrange(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None
    
    def exposed(self, position):
        """ Returns False is given 'position' is surrounded on all 6 sides by
        blocks, True otherwise.
        
        """
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
            return False
        
    def add_block(self, position, texture, immediate=True):
        """ Add a block with the given 'texture' and 'position' to the world.
        
        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to add.
        texture : list of len 3
            The coordinates of the texture squares. Use 'tex_coords()' to
            generate.
        immediate : bool
            Wheter or not to draw the block immediately.
            
        """
        if position in self.world:
            self.remove_block(position, immediate)
        self.world[position] = texture
        self.sectors.setdefault(sectorize(position), []).append(position)
        if immediate:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)
            
    def remove_block(self, position, immediate=True):
        """ Remove the block at the given 'position'.
        
        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to remove.
        immediate : bool
            Wheter or not to immediately remove block from canvas.
            
        """
        del self.world[position]
        self.sectors[sectorize(position)].remove(position)
        if immediate:
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position)
            
    def check_neighbors(self, position):
        """ Check all blocks surrounding 'position' and ensure their visual
        state is current. This means hiding blocks that are not exposed and ensuring
        that all exposed blocks are shown. Usually used after a block
        is added or removed.
        
        """
        x, y, z = position
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if key not in self.world:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.hide_block(key)
    
    def show_block(self, position, immediate=True):
        """ Show the block at the given 'position'. This method assumes
        the block has already been added with add_block()
        
        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        immediate : bool
            Whether or not to show the block immediately.
            
        """
        texture = self.world[position]
        self.shown[position] = texture
        if immediate:
            self._show_block(position, texture)
        else:
            self._enqueue(self._show_block, position, texture)


# In[ ]:



