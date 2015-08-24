# Astrovisualization
Code development for visualization in the lab

NOTES
===========================================================================

* Be sure to consult Suresh when desinging new visualization. Give his 
  expertise, it may be a good idea to consult him frequently when changes 
  to the visualization design become possible. 

* Consult Manfred for machine learning and algorithm design help. 


GENERAL PROJECT OUTLINE
===========================================================================

* Project
	* Visualization
		* Interface Upgrades
			* Make a click halt that rotation or kill it completely
			* Freely movable camera
			* Minimizable infoboxes with halo catalog data
			* Toggleable control menu (possibly just in an infoboxlikething)

		Visualization Additions
			* Translucent triaxial ellipsoid
			* Fundamental components (the 3d axis arrows for the ellipsoid)
			* Figure out a way to visualize orientation

	Data Analysis
		* I still need to clarify what it is I want to do here. I'll 
		  probably have a better idea once I associate the web and halo
		  data. 
		* But
		* If there's an OBVIOUS way to do feature discovery, try it.
		  But beware the Collatz conjecture. Don't get stuck. 
		* But calculate a bunch of stuff. Joel told me a few things. 
		* I probably wrote this down.
		* God this medication is nice. 

	Web Data / Halo Catalog Association
		* Didn't Doug do something with this?
		* This is definitely where I'm trailing.

	General Astro
		* Talk to Joel about special relativity
		* Review and re-memorize the group axioms
		* Learn about compactness


TO-DO
===========================================================================

1. Read through the code and figure it out and comment it

   Where I Am
   ------------------------------------------------------------------------

   Legend:
   √: Done as much as possible for now
   -: Done as much as is reasonable for now
   !: Blocked by question.
   ~: In progress
   *: Unstarted

   √ Preamble
   - Exit Message 
   ! Handle Command Line Args
   * Update Transfer
   * Create PBO (bundle these into an object and make these methods?)
   * Destroy PBO
   * Create texture
   * Destroy texture (maybe same here)
   * Init GL
   * Resize
   * Do Tick
   * Mouse Button
   * Mouse Motion
   * Key Pressed
   * Idle (can this be eliminated? it's one line)
   * Display
   * Process
   * Process Image
   * Display Image (maybe an image object)
   * Scale Func

   List of things that it's probably worthwhile to keep track of
   ------------------------------------------------------------------------
 
   a. Add docstrings to everything.
   b. Make the code legible to non-authors
   c. Un-abbreviate everything so that the code doesn't read like it was 
       written in the days of 64k memory capacity. 
   d. Remember that spaces, not tabs. Perhaps convert for dev convenience 
      then switch back at the end? I feel like this could cause disaster.
   e. Clean up line width
   f. Learn what a callback function is
   g. Consider sending iteratively skimming the document in finer and 
      finer detail as a method of absorhing everything there is to 
      absorb greedily by easiest. Then proofread and send to Alex with 
      any lingering questions.
   h. Learn about globals
   

   y. Track Interface Elements:
      * all options must start with a -
      * Perhaps add a debug or verbose mode, and suppress more than 
        minimum output. 
   
   z. Track questions for Alex and blocked sections:
      * in handleCommandLineArgs(), first while loop, first else 
        statement: 
        - What is going on here? 
        - What's the equals sign for?
        - What is the purpose of setting 'flag' and 'val' here?

    	--> Question is blocking: 
    	    * handleCommandLineArgs()


