import numpy as np
from geometry.geometry import Geometry

class ParametricGeometry(Geometry):

    def __init__(self, u_start, u_end, u_res, v_start, v_end, v_res, surface_func):
        super().__init__()
        
        # generate set of points on function
        delta_u = (u_end - u_start) / u_res
        delta_v = (v_end - v_start) / v_res
        positions = []

        for u_index in range(u_res +1):
            v_array = []
            for v_index in range(v_res +1):
                u = u_start + u_index * delta_u
                v = v_start + v_index * delta_v
                v_array.append(surface_func(u, v))
            positions.append(v_array)

        # texture data
        uvs = [] # uv sequence
        texture_data = []

        for u_index in range(u_res +1):
            v_array = []
            for v_index in range(v_res +1):
                u = u_index / u_res
                v =  v_index / v_res
                v_array.append( [u, v] )
            uvs.append(v_array)

        # normals
        def calcNormal(p0, p1, p2):
            v1 = np.array(p1) - np.array(p0)
            v2 = np.array(p2) - np.array(p0)
            normal = np.cross( v1, v2 )
            normal = normal / np.linalg.norm(normal)
            return normal
        
        vertex_normals = []
        for u_index in range(u_res +1):
            v_array = []
            for v_index in range(v_res +1):
                u = u_start + u_index * delta_u
                v = v_start + v_index * delta_v
                h = 0.0001 # TODO: look up what this is
                p0 = surface_func(u,    v)
                p1 = surface_func(u+h,  v)
                p2 = surface_func(u,    v+h)
                normal_vector = calcNormal(p0, p1, p2)
                v_array.append( normal_vector )
            vertex_normals.append( v_array )

        
        # store vertex data
        position_data = []
        color_data = []
        vertex_normal_data = []
        face_normal_data = []

        # default color data
        c1, c2, c3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        c4, c5, c6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]

        # group vertex data in to triangles
        # note: copy() is necessary to avoid storing references
        for x_index in range(u_res):
            for y_index in range(v_res):
                # position data
                pA = positions[x_index+0][y_index+0]
                pB = positions[x_index+1][y_index+0]
                pD = positions[x_index+0][y_index+1]
                pC = positions[x_index+1][y_index+1]
                position_data += [
                    pA.copy(), pB.copy(), pC.copy(),
                    pA.copy(), pC.copy(), pD.copy() ]

                # color data
                color_data += [
                    c1, c2, c3,
                    c4, c5, c6 ]

                # texture data
                uvA = uvs[x_index+0][y_index+0]
                uvB = uvs[x_index+1][y_index+0]
                uvD = uvs[x_index+0][y_index+1]
                uvC = uvs[x_index+1][y_index+1]
                texture_data += [
                    uvA, uvB, uvC,
                    uvA, uvC, uvD ]

                # normals
                nA = vertex_normals[x_index+0][y_index+0]
                nB = vertex_normals[x_index+1][y_index+0]
                nD = vertex_normals[x_index+0][y_index+1]
                nC = vertex_normals[x_index+1][y_index+1]
                vertex_normal_data += [
                    nA, nB, nC,
                    nA, nC, nD ]
                # face normal vectors
                fn0 = calcNormal(pA, pB, pC)
                fn1 = calcNormal(pA, pC, pD)
                face_normal_data += [
                    fn0, fn0, fn0,
                    fn1, fn1, fn1 ]

        
        
        self.addAttribute("vec3", "a_position", position_data)
        self.addAttribute("vec3", "a_color", color_data)
        self.addAttribute("vec2", "a_texCoords", texture_data)
        self.addAttribute("vec3", "a_vNormal", vertex_normal_data)
        self.addAttribute("vec3", "a_fNormal", face_normal_data)
        self.countVertecies()