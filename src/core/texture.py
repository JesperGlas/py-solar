from typing import Dict
import pygame as pg
from OpenGL.GL import *

class Texture(object):

    def __init__(self, file_name: str, properties: Dict={}) -> None:
        
        # pygame object for storing pixel data;
        #   can load from image or manipulate directly
        self._Surface = None

        # reference of available texture from GPU
        self._TextureRef = glGenTextures(1)

        # default property values
        self._Properties: Dict = {
            "magFilter" : GL_LINEAR,
            "minFilter" : GL_LINEAR_MIPMAP_LINEAR,
            "wrap"      : GL_REPEAT
        }

        # overwrite default property values
        self.setProperties(properties)

        if file_name is not None:
            self.loadImage(file_name)
            self.uploadData()

    def loadImage(self, file_name: str) -> None:
        self._Surface = pg.image.load(file_name)

    def setProperties(self, properties: Dict) -> None:
        for name, data in properties.items():
            if name in self._Properties.keys():
                self._Properties[name] = data
            else: # unknown property type
                raise Exception(f"Texture has no property with name: {name}")

    def uploadData(self) -> None:
        
        # store image dimensions
        width   = self._Surface.get_width()
        height  = self._Surface.get_height()

        # convert image data to string buffer
        pixel_data = pg.image.tostring(self._Surface, "RGBA", 1)

        # specify texture used;
        glBindTexture(GL_TEXTURE_2D, self._TextureRef)

        # stream pixel data to texture buffer
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            width, height, 0, GL_RGBA,
            GL_UNSIGNED_BYTE, pixel_data )

        # generate mipmap image from uploaded pixel data
        glGenerateMipmap(GL_TEXTURE_2D)

        # specify technique for magnifying/minifying textures
        glTexParameteri(GL_TEXTURE_2D,
            GL_TEXTURE_MAG_FILTER, self._Properties["magFilter"] )
        glTexParameteri(GL_TEXTURE_2D,
            GL_TEXTURE_MIN_FILTER, self._Properties["minFilter"] )

        # specify what happends to texture coordinates outside range [0, 1]
        glTexParameteri(GL_TEXTURE_2D,
            GL_TEXTURE_WRAP_S, self._Properties["wrap"] )
        glTexParameteri(GL_TEXTURE_2D,
            GL_TEXTURE_WRAP_T, self._Properties["wrap"] )

        # set default border color to white;
        #   important for rendering shadows
        glTexParameterfv(GL_TEXTURE_2D,
            GL_TEXTURE_BORDER_COLOR, [1, 1, 1, 1] )
