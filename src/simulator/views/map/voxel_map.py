from panda3d.core import NodePath, TransparencyAttrib, LVecBase3f
from .cube_mesh import CubeMesh
from .colour import Colour, TRANSPARENT

from structures import Point

from typing import List
import random

class VoxelMap():
    root: NodePath
    traversables: NodePath
    traversables_wf: NodePath
    obstacles: NodePath
    obstacles_wf: NodePath
    start: NodePath
    goal: NodePath

    traversables_mesh: CubeMesh
    traversables_wf_mesh: CubeMesh
    obstacles_mesh: CubeMesh
    obstacles_wf_mesh: CubeMesh
    start_mesh: CubeMesh
    goal_mesh: CubeMesh

    __start_pos: Point
    __goal_pos: Point

    def __init__(self, data: List[List[List[bool]]], parent: NodePath, name: str = "voxel_map", start_pos: Point = None, goal_pos: Point = None, artificial_lighting: bool = False):
        self.obstacles_data = data
        self.traversables_data = {}
        for i in range(len(self.obstacles_data)):
            self.traversables_data[i] = {}
            for j in range(len(self.obstacles_data[i])):
                self.traversables_data[i][j] = {}
                for k in range(len(self.obstacles_data[i][j])):
                    self.traversables_data[i][j][k] = False if self.obstacles_data[i][j][k] else True
                    
        self.root = parent.attach_new_node(name)
        self.root.set_transparency(TransparencyAttrib.M_alpha)

        self.traversables_mesh = CubeMesh(self.traversables_data, name + '_traversables', artificial_lighting, hidden_faces = False)
        self.traversables = self.root.attach_new_node(self.traversables_mesh.geom_node)

        self.traversables_wf_mesh = CubeMesh(self.traversables_data, name + '_traversables_wf', artificial_lighting, hidden_faces = True)
        self.traversables_wf = self.root.attach_new_node(self.traversables_wf_mesh.geom_node)
        self.traversables_wf.setRenderModeWireframe()
        self.traversables_wf.setRenderModeThickness(2.2)

        self.obstacles_mesh = CubeMesh(self.obstacles_data, name + '_obstacles', artificial_lighting, hidden_faces = False)
        self.obstacles = self.root.attach_new_node(self.obstacles_mesh.geom_node)

        self.obstacles_wf_mesh = CubeMesh(self.obstacles_data, name + '_obstacles_wf', artificial_lighting, hidden_faces = True)
        self.obstacles_wf = self.root.attach_new_node(self.obstacles_wf_mesh.geom_node)
        self.obstacles_wf.setRenderModeWireframe()
        self.obstacles_wf.setRenderModeThickness(2.2)

        cube = {}
        for x in range(0, 1):
            cube[x] = {}
            for y in range(0, 1):
                cube[x][y] = {}
                for z in range(0, 1):
                    cube[x][y][z] = True

        self.start_mesh = CubeMesh(cube, name + '_start', artificial_lighting, hidden_faces = True)
        self.start = self.root.attach_new_node(self.start_mesh.geom_node)

        self.goal_mesh = CubeMesh(cube, name + '_goal', artificial_lighting, hidden_faces = True)
        self.goal = self.root.attach_new_node(self.goal_mesh.geom_node)

        # initialise goal and origin #
        self.__start_pos = None
        self.__goal_pos = None
        self.start_pos = start_pos
        self.goal_pos = goal_pos

        # randomly initialise undefined positions
        if self.goal_pos == None or self.start_pos == None:
            map_sz = 0
            for i in range(len(self.traversables_data)):
                for j in range(len(self.traversables_data[i])):
                    map_sz += len(self.traversables_data[i][j])

            def randpos() -> Point:
                def to_coord(n: int) -> Point:
                    for i in range(len(self.traversables_data)):
                        for j in range(len(self.traversables_data[i])):
                            for k in range(len(self.traversables_data[i][j])):
                                if n == 0:
                                    return (i, j, k)
                                else:
                                    n -= 1

                def cube_exists(n: int) -> bool:
                    i, j, k = to_coord(n)
                    return self.traversables_data[i][j][k]

                def gen() -> int:
                    return random.randint(0, map_sz-1)

                n = gen()

                while not cube_exists(n):
                    n = gen()
                return to_coord(n)

            if self.start_pos == None:
                p = randpos()
                while p == self.goal_pos:
                    p = randpos()
                self.start_pos = p

            if self.goal_pos == None:
                p = randpos()
                while p == self.start_pos:
                    p = randpos()
                self.goal_pos = p

    @property
    def start_pos(self) -> str:
        return 'start_pos'

    @start_pos.getter
    def start_pos(self) -> Point:
        return self.__start_pos

    @start_pos.setter
    def start_pos(self, value: Point) -> None:
        if self.__start_pos != None:
            self.traversables_mesh.reset_cube_colour(self.__start_pos)
        self.__start_pos = value
        if self.__start_pos != None:
            self.traversables_mesh.set_cube_colour(self.__start_pos, TRANSPARENT)
            self.start.set_pos(LVecBase3f(*value))
            self.start.show()
        else:
            self.start.hide()
    @property
    def goal_pos(self) -> str:
        return 'goal_pos'

    @goal_pos.getter
    def goal_pos(self) -> Point:
        return self.__goal_pos

    @goal_pos.setter
    def goal_pos(self, value: Point) -> None:
        if self.__goal_pos != None:
            self.traversables_mesh.reset_cube_colour(self.__goal_pos)
        self.__goal_pos = value
        if self.__goal_pos != None:
            self.traversables_mesh.set_cube_colour(self.__goal_pos, TRANSPARENT)
            self.goal.set_pos(LVecBase3f(*value))
            self.goal.show()
        else:
            self.goal.hide()