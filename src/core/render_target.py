from OpenGL.GL import *
import pygame as pg
from core.texture import Texture
from typing import Dict

class RenderTarget(object):

    def __init__(self, resolution=[512, 512], texture: Texture=None, properties: Dict={}) -> None:
        
        self._Width, self._Height = resolution

        if texture is not None:
            self._Texture = texture
        else:
            self._Texture = Texture(None, {
                "magFilter":    GL_LINEAR,
                "minFilter":    GL_LINEAR,
                "wrap":         GL_CLAMP_TO_EDGE })
            self._Texture.setProperties(properties)
            self._Texture._Surface = pg.Surface(resolution)
            self._Texture.uploadData()

        # Create a framebuffer
        self._FramebufferRef = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self._FramebufferRef)
        # Configure color buffer to use this texture
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                                self._Texture._TextureRef, 0)
        # Generate a buffer to store depth information
        depth_buffer_ref = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, depth_buffer_ref)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, self._Width, self._Height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_buffer_ref)
        # Check framebuffer status
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise Exception("Framebuffer status error")