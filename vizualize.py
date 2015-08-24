#---------------------------------------------------------------------------
# Copyright (c) 2014, pyRGBA Development Team.
#---------------------------------------------------------------------------

# Starting with GL interoperability example, by Peter Berrington.
# Going to add our ray casting functions and key/mouse control
# Now adding a second PBO for 3D
# Alex Bogert

# Vincent Steffens
# Cleaning and documenting code
# Editing interface

# No idea what these are for
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.vertex_buffer_object import *

# For command line arguments and... time.
import sys, time
# and numpy
import numpy as np
# Definitely not sure what this is about
import pycuda.driver as cuda_driver
# or this. Interface with the video card, I think.
import pycuda.gl as cuda_gl
# Not completely sure what this is about.
from pyRGBA.cameras.glcamera import GLCamera

# Not sure what these are going to be used for. Should these even be 
# declared here? Reorganize if necessary.
window = None     # Number of the glut window.
rot_enabled = True # AND
rot_mag = 0.001 # LABEL
camera = None # GOSH

#RAY CASTING values
brightness = 1.23
density_scale = 0.16

output_texture = None # pointer to offscreen render target

leftButton = False
middleButton = False
rightButton = False

eyesep = 0.003

# No idea what these are for
(pbo, pycuda_pbo) = [None]*2
(rpbo, rpycuda_pbo) = [None]*2

def exit_msg(errmsg):
    """
    TO-DO:
    ------------------------------------------------------------------------
    
    1. Un-abbreviate everything so that the code doesn't read like it was 
       written in the days of 64k memory capacity. 

    """

    print "ERROR: "+errmsg+" not specified. Exiting..."
    sys.exit(0)

def handleCommandLineArgs():
    """
    ------------------------------------------------------------------------
    """
    
    #what are globals? Global variables? What is this one used for?
    global rot_enabled

    #what is this used for? 
    ret_args = []

    #what are we about to do here?
    i = 1
    # Probably loop through the arguments
    # Where are these documented?
    # Why aren't they discussed in a docstring?
    # Why aren't they part of the interface? 
    while (i < len(sys.argv)):

        if (sys.argv[i][0] != '-'):
            print "ERROR: malformed argments"
            sys.exit(0)
        else:
            # ...what?
            arg = sys.argv[i][1:]
            if (arg.find("=") == -1):
                val = ""
                flag = arg
            else:
                val = arg[arg.find("=")+1:]
                flag = arg[:arg.find("=")]

        # we now have the flag and value
        # Yep. Totally lost. Ask Alex about that bit and come back here
        if (flag == "data"):
            if (len(val)):
                ret_args.append((flag,val))
            else:
                exit_msg("data file")
        elif (flag == "rot"):
            if (len(val)):
                if (val.lower() == "true"):
                    rot_enabled = True
                    print "Enabling Rotation"
                elif (val.lower() == "false"):
                    rot_enabled = False
                    print "Disabling Rotation"
            else:
                exit_msg("rotation")
        elif (flag == "bins"):
            if (len(val)):
                ret_args.append((flag,val))
            else:
                #bins?
                exit_msg("number of bins")
        elif (flag == "min"):
            if (len(val)):
                ret_args.append((flag,val))
            else:
                #value of what?
                exit_msg("min value")
        elif (flag == "max"):
            if (len(val)):
                ret_args.append((flag,val))
            else:
                exit_msg("max value")
        else:
            # y u no just handle it and go on?
            print "ERROR: flag: \"" + flag + "\" not recognized, exiting."
            sys.exit(0)

        i += 1

    #Is this necessary? Consider relegating to debug or verbose mode?
    print ret_args

    #Maybe run this on the VLC, redirect output to file, and just grab it and check for errors. 
    return ret_args

def updateTransfer ():
    """
    ------------------------------------------------------------------------
    """
    
    global mi, ma, bins

    from yt.mods import ColorTransferFunction
    transfer = ColorTransferFunction( (mi, ma), bins)
    transfer.map_to_colormap(mi, ma, colormap='spring', scale_func = scale_func)

    camera.setTransfer(tf = transfer)

#create 2 PBO for stereo scopic rendering
def create_PBO(w, h):
    """
    ------------------------------------------------------------------------
    """
    
    global pbo, pycuda_pbo, rpbo, rpycuda_pbo
    num_texels = w*h
    array = np.zeros((num_texels, 3),np.float32)

    pbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, pbo)
    glBufferData(GL_ARRAY_BUFFER, array, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    pycuda_pbo = cuda_gl.RegisteredBuffer(long(pbo))

    rpbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, rpbo)
    glBufferData(GL_ARRAY_BUFFER, array, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    rpycuda_pbo = cuda_gl.RegisteredBuffer(long(rpbo))

def destroy_PBO():
    """
    ------------------------------------------------------------------------
    """
    
    global pbo, pycuda_pbo, rpbo, rpycuda_pbo
    glBindBuffer(GL_ARRAY_BUFFER, long(pbo))
    glDeleteBuffers(1, long(pbo));
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    pbo,pycuda_pbo = [None]*2

    glBindBuffer(GL_ARRAY_BUFFER, long(rpbo))
    glDeleteBuffers(1, long(rpbo));
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    rpbo,rpycuda_pbo = [None]*2

#consistent with C initPixelBuffer()
def create_texture(w,h):
    """
    ------------------------------------------------------------------------
    """
    
    global output_texture
    output_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, output_texture)
    # set basic parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    # buffer data
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 w, h, 0, GL_RGB, GL_FLOAT, None)

#consistent with C initPixelBuffer()
def destroy_texture():
    """
    ------------------------------------------------------------------------
    """
    
    global output_texture
    glDeleteTextures(output_texture);
    output_texture = None

def init_gl(w = 512 , h = 512):
    """
    ------------------------------------------------------------------------
    """
    
    Width, Height = (w, h)

    glClearColor(0.1, 0.1, 0.5, 1.0)
    glDisable(GL_DEPTH_TEST)

    #matrix functions
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    #matrix functions
    gluPerspective(60.0, Width/float(Height), 0.1, 10.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def resize(Width, Height):
    """
    ------------------------------------------------------------------------
    """
    
    global current_size
    current_size = Width, Height
    glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, Width/float(Height), 0.1, 10.0)

def do_tick():
    """
    ------------------------------------------------------------------------
    """
    
    global time_of_last_titleupdate, frame_counter, frames_per_second
    if ((time.clock () * 1000.0) - time_of_last_titleupdate >= 1000.):
        frames_per_second = frame_counter                   # Save The FPS
        frame_counter = 0  # Reset The FPS Counter
        szTitle = "%d FPS" % (frames_per_second )
        glutSetWindowTitle ( szTitle )
        time_of_last_titleupdate = time.clock () * 1000.0
    frame_counter += 1

#what is this doing here?
oldMousePos = [ 0, 0 ]
def mouseButton( button, mode, x, y ):
	"""Callback function (mouse button pressed or released).

	The current and old mouse positions are stored in
	a	global renderParam and a global list respectively"""

	global leftButton, middleButton, rightButton, oldMousePos

        if button == GLUT_LEFT_BUTTON:
	    if mode == GLUT_DOWN:
	        leftButton = True
            else:
		leftButton = False

        if button == GLUT_MIDDLE_BUTTON:
	    if mode == GLUT_DOWN:
	        middleButton = True
            else:
		middleButton = False

        if button == GLUT_RIGHT_BUTTON:
	    if mode == GLUT_DOWN:
	        rightButton = True
            else:
		rightButton = False

	oldMousePos[0], oldMousePos[1] = x, y
	glutPostRedisplay( )

def mouseMotion( x, y ):
	"""Callback function (mouse moved while button is pressed).

	The current and old mouse positions are stored in
	a	global renderParam and a global list respectively.
	The global translation vector is updated according to
	the movement of the mouse pointer."""

	global camera, camera2, leftButton, middleButton, rightButton, oldMousePos
	deltaX = x - oldMousePos[ 0 ]
	deltaY = y - oldMousePos[ 1 ]

	factor = 0.001

	if leftButton == True:
            camera.rotateX( - deltaY * factor)
            camera.rotateY( - deltaX * factor)
	if middleButton == True:
	    camera.translateX( deltaX* 2.0 * factor)
	    camera.translateY( - deltaY* 2.0 * factor)
	if rightButton == True:
	    camera.scale += deltaY * factor

	oldMousePos[0], oldMousePos[1] = x, y
	glutPostRedisplay( )

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
    """
    ------------------------------------------------------------------------
    """
    
    global camera, brightness, density_scale, rot_enabled, eyesep, mi, ma, bins, tf_interval, global_min, global_max, rot_mag
    # If escape is pressed, kill everything.
    if args[0] == '\033':
        print 'Closing..'
        destroy_PBO()
        destroy_texture()
        exit()

    elif args[0] == 'r':
        if (rot_mag > 0):
            rot_mag -= 0.001
        else:
            rot_enabled = False
        print "rotation magnitude " + str(rot_mag)
    elif args[0] == 'R':
        # toggle rotation
        #rot_enabled = not rot_enabled
        rot_mag += 0.001
        rot_enabled = True
        print "rotation magnitude " + str(rot_mag)

    #change the raycaster brightness
    elif args[0] == 'b':
        brightness -= 0.1
        print "Brightness: " + str(brightness)
    elif args[0] == 'B':
        brightness += 0.1 
        print "Brightness: " + str(brightness)

    # change the raycaster density scale
    elif args[0] == 'd':
        density_scale -= density_scale/5.
        print "Density Scale: " + str(density_scale)
    elif args[0] == 'D':
        density_scale += density_scale/5.
        print "Density Scale: " + str(density_scale)

    #change the transfer scale
    elif args[0] == '-':
        print "Eye separation: " + str(eyesep)
        eyesep -= 0.001
    elif args[0] == '=':
        print "Eye separation: " + str(eyesep)
        eyesep += 0.001 

    # modify how many bins the transfer function has
    elif args[0] == 'n':
        if (bins > 2):
            bins -= 1
            updateTransfer ()
        print "bins: " + str(bins)
    elif args[0] == 'N':
        bins += 1
        print "bins: " + str(bins)
        updateTransfer ()

    # adjust the min value of transfer function
    elif args[0] == '1':
        if (mi > global_min):
            mi -= tf_interval
            updateTransfer ()
        print "TF min: " + str(mi)
    elif args[0] == '2':
        if (mi + tf_interval < ma):
            mi += tf_interval
            updateTransfer ()
        print "TF min: " + str(mi)

    # adjust the max value of transfer function
    elif args[0] == '9':
        if (ma - tf_interval > mi):
            ma -= tf_interval
            updateTransfer ()
        print "TF max: " + str(ma)
    elif args[0] == '0':
        if (ma < global_max):
            ma += tf_interval
            updateTransfer ()
        print "TF max: " + str(ma)

def idle():
    """
    ------------------------------------------------------------------------
    """
    
    glutPostRedisplay()

def display():
    """
    ------------------------------------------------------------------------
    """
    
    try:
        #process left eye
        process_image()
        display_image()

        #process right eye
        process_image(eye = False)
        display_image(eye = False)

        glutSwapBuffers()
    except:
        from traceback import print_exc
        print_exc()
        from os import _exit
        _exit(0)

def process(eye = True):
    """
    ------------------------------------------------------------------------
    """
    
    global camera, pycuda_pbo, rpycuda_pbo, eyesep, rot_mag, density_scale, brightness
    """ Use PyCuda """
    
    if (rot_enabled):
        camera.rotateX(rot_mag)
        camera.rotateY(rot_mag)
        camera.rotateZ(rot_mag)

    if (eye) :
        camera.translateX(-eyesep)
        dest_mapping = pycuda_pbo.map()
        (dev_ptr, size) = dest_mapping.device_ptr_and_size()
        camera.cast(device_ptr = dev_ptr, max_samples = 800, sample_size = 0.01, density_scale = density_scale, brightness = brightness)
        dest_mapping.unmap()
        camera.translateX(eyesep)

    else :
        camera.translateX(eyesep)
        dest_mapping = rpycuda_pbo.map()
        (dev_ptr, size) = dest_mapping.device_ptr_and_size()
        camera.cast(device_ptr = dev_ptr, max_samples = 800, sample_size = 0.01, density_scale = density_scale, brightness = brightness)
        dest_mapping.unmap()
        camera.translateX(-eyesep)

def process_image(eye =  True):
    """
    ------------------------------------------------------------------------
    """
    
    global camera, output_texture, pbo, rpbo
    """ copy image and process using CUDA """
    # run the Cuda kernel
    process(eye)
    # download texture from PBO
    if (eye) : 
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER, np.uint64(pbo))
        glBindTexture(GL_TEXTURE_2D, output_texture)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 camera.width, camera.height, 0,
                 GL_RGB, GL_FLOAT, None)
    else :
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER, np.uint64(rpbo))
        glBindTexture(GL_TEXTURE_2D, output_texture)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 camera.width, camera.height, 0,
                 GL_RGB, GL_FLOAT, None)

def display_image(eye = True):
    """
    ------------------------------------------------------------------------
    """
    
    global camera
    """ render a screen sized quad """
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #matix functions should be moved
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
    glMatrixMode( GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, camera.width, camera.height)

    if (eye) :
        glDrawBuffer(GL_BACK_LEFT)
    else :
        glDrawBuffer(GL_BACK_RIGHT)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.5)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0, 1.0, 0.5)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-1.0, 1.0, 0.5)
    glEnd()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glDisable(GL_BLEND)

    glDisable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)
    glBindBuffer(GL_PIXEL_PACK_BUFFER, 0)
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, 0)

#note we may need to init cuda_gl here and pass it to camera
def main():
    """
    ------------------------------------------------------------------------
    """
    

    global bins, ma, mi, tf_interval, global_min, global_max

    ret_args = handleCommandLineArgs()

    datafile = ""

    mi, ma, bins = None, None, None

    for (flag,val) in ret_args:
        if (flag == "data"):
            datafile = val
        elif (flag == "min"):
            mi = float(val)
        elif (flag == "max"):
            ma = float(val)
        elif (flag == "bins"):
            bins = int(val)

    global window, camera, camera2
    initial_size = (1920,1080)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH | GLUT_STEREO)
    glutInitWindowSize(*initial_size)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("PyCuda GL Interop Example")

    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutReshapeFunc(resize)
    glutMouseFunc( mouseButton )
    glutMotionFunc( mouseMotion )
    glutKeyboardFunc(keyPressed)
    #glutSpecialFunc(keyPressed)
    init_gl(*initial_size)

    # create texture for blitting to screen
    create_texture(*initial_size)

    import pycuda.gl.autoinit
    import pycuda.gl
    cuda_gl = pycuda.gl

    create_PBO(*initial_size)
    # ----- Load and Set Volume Data -----
    from yt.mods import *
    import numpy as np

    # set to default file if not specified on commandline
    if (len(datafile) == 0):
        datafile = "/home/bogert/log_densities_1024.npy"
        
    data_map = np.load(datafile)
    #data_map *= -1
    
    # ----- Set Transfer Function Parameters -----
    #mi , ma = 0.0, 3.95
    #bins  = 1000

    global_min = np.amin(data_map)
    global_max = np.amax(data_map)

    # set to min/max value of data
    if (mi is None):
        mi = global_min
    if (ma is None):
        ma = global_max

    print "Setting transfer function range to (" + str(mi) + ", " + str(ma) + ")"

    # default to 10000 bins
    if (bins is None):
        bins = 10000

    print "Setting number of bins to " + str(bins)
   
    tf_interval = abs((global_max - global_min))/500

    transfer = ColorTransferFunction( (mi, ma), bins)
    transfer.map_to_colormap(mi, ma, colormap='spring', scale_func = scale_func)

    camera = GLCamera(tf = transfer, width = 1920, height = 1080, grid = data_map)

    glutMainLoop()

#This needs to be reorganized
def scale_func(v, mi, ma):
    """
    ------------------------------------------------------------------------
    """
    
    return np.minimum(1.0, (v-mi)/(ma-mi) + 0.0)

# Print message to console, and kick off the main to get it rolling.
if __name__ == "__main__":
    print "Hit ESC key to quit, 'a' to toggle animation, and 'e' to toggle cuda"
    main()
