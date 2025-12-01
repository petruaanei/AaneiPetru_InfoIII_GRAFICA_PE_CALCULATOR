import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np


def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Lab1 - Primul triunghi", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    vertices = np.array([
         0.3,  0.8, 0.0,
        -0.2, -0.2, 0.0,
         0.8, -0.2, 0.0
    ], dtype=np.float32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    vertex_shader_src = """
    #version 330 core
    layout (location = 0) in vec3 position;
    void main()
    {
        gl_Position = vec4(position, 1.0);
    }
    """
    fragment_shader_src = """
    #version 330 core
    out vec4 FragColor;
    void main()
    {
        FragColor = vec4(1.0, 1.0, 1.0, 1.0);
    }
    """
    shader_program = compileProgram(
        compileShader(vertex_shader_src, GL_VERTEX_SHADER),
        compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)
    )

    glClearColor(0.1, 0.1, 0.1, 1.0)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader_program)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
