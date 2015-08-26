# Astrovisualization
Code development for visualization in the lab

CURRENTLY
===========================================================================

* Getting Git set up on VLC


NOTES
===========================================================================

* Be sure to consult Suresh when desinging new visualization. Given his 
  expertise, it may be a good idea to consult him frequently when changes 
  to the visualization design become possible. 

* Consult Manfred for machine learning and algorithm design help. 


Agile Development Workspace
===========================================================================

Settings
---------------------------------------------------------------------------

Sprint Length: 1wk.


Sprint Log
---------------------------------------------------------------------------

Sprint 0:
* Figure out what the general picture of the entire project looks like
* Keep log of changes that need to be made (below)
* Get all of my visualization development work on GitHub and synced with 
  all relevant comps.

User Stories:
* Get from Christoph
* Get from Joel
* Get from Aldo
* Others? 

Product Backlog:
* Fill backlog
* Get user stories


Backlog (necessarily unsorted)
---------------------------------------------------------------------------

* 


GENERAL PROJECT OUTLINE
===========================================================================

* Project
	* Visualization
		* Interface Upgrades
			* Make a click halt that rotation or kill it completely
			* Freely movable camera
			* Minimizable infoboxes with halo catalog data
			* Toggleable control menu (possibly just in an infoboxlikething)

		* Visualization Additions
			* Translucent triaxial ellipsoid
			* Fundamental components (the 3d axis arrows for the ellipsoid)
			* Figure out a way to visualize orientation

	* Data Analysis
		* I still need to clarify what it is I want to do here. I'll 
		  probably have a better idea once I associate the web and halo
		  data. 
		* But
		* If there's an OBVIOUS way to do feature discovery, try it.
		  But remember the mathematicians that wasted careers on the 
		  Collatz conjecture. Don't get stuck. 
		* But calculate a bunch of stuff. Joel told me a few things. 
		  It's in my notes somewhere.
		* At very least do some supervised learning. Like train on known 
		  relations and have the program determine something like a 
		  correlation threshold. Then do combinatorial analysis on 
		  everything measurable and have the program hand to us all 
		  the linear relationships in term of what we search for. 
		* But if possible... automatic feature discovery would be 
		  cool. I wonder if you can know that you've derived everything 
		  you can from a sufficiently large finite dataset. 

	* Web Data / Halo Catalog Association
		* Import notes 

	* General Astro
		* Talk to Joel about special relativity
		* Review and re-memorize the group axioms
		* Learn about compactness


TO-DO
===========================================================================

1. Read through the code and figure it out and comment it

   Where I Am
   ------------------------------------------------------------------------

   Legend:
   * √ <--> Done as much as possible for now
   * - <--> Done as much as is reasonable for now
   * ! <--> Blocked by question.
   * ~ <--> In progress
   * * <--> Unblocked, Unstarted

   List:
   * √ Preamble
   * - Exit Message 
   * ! Handle Command Line Args
   * * Update Transfer
   * * Create PBO (bundle these into an object and make these methods?)
   * * Destroy PBO
   * * Create texture
   * * Destroy texture (maybe same here)
   * * Init GL
   * * Resize
   * * Do Tick
   * * Mouse Button
   * * Mouse Motion
   * * Key Pressed
   * * Idle (can this be eliminated? it's one line)
   * * Display
   * * Process
   * * Process Image
   * * Display Image (maybe an image object)
   * * Scale Func

   List of things that it's probably worthwhile to keep track of
   ------------------------------------------------------------------------
 
   * Add docstrings to everything.
   * Make the code legible to non-authors
   * Un-abbreviate everything so that the code doesn't read like it was 
       written in the days of 64k memory capacity
   * Remember that spaces, not tabs. Perhaps convert for dev convenience 
      then switch back at the end? I feel like this could cause disaster
   * Clean up line width
   * Learn what a callback function is
   * Consider iteratively skimming the document in finer and 
      finer detail as a method of absorbing everything there is to 
      absorb greedily by easiest, then proofread and send to Alex with 
      any lingering questions
   * Learn about globals
   * Track Interface Elements:
      * all options must start with a '-'
      * Perhaps add a debug or verbose mode, and suppress more than 
        minimum output. 
   * Track questions for Alex and blocked sections:
      * in handleCommandLineArgs(), first while loop, first else 
        statement: 
        - What is going on here? 
        - What's the equals sign for?
        - What is the purpose of setting 'flag' and 'val' here?

    	--> Question is blocking: 
    	    * handleCommandLineArgs()


Notes Accumulated While Suffering Through The UI
===========================================================================

This is an unsorted list of stuff I found while playing with the program.


The VisLab Computer
---------------------------------------------------------------------------

* Need libstdc++.so.6(GLIBCXX_3.4.15)(64Bbit)
* Need to get a mechanical keyboard 
* Need to get a mouse that doen't accumulate frictioney crud
* Might be good to get a book on general CentOS
* Need to install Flash to use GitHub --> see item 1
* Need to install Chrome to escape from FireFox --> see item 1
* I need to be using CentOS at home to bring myself up to speed on it. 


General Program Use
---------------------------------------------------------------------------

* There needs to be a quit option in the GUI


Navigation
---------------------------------------------------------------------------

* Autorotation absolutely must die, incl. 'r', 'R' to speed and slow.
  --> The entire feature must be removed.

* Mouse click-drag cube rotation is completely nonfunctional
  --> The entire feature must be removed. 
  --> Replace with mouse for direction and wasd/dpad for mov't
  --> Perhaps the delta_s for mov't could be adjusted

* How do you zoom?
  --> Doesn't matter. Feature will be eliminated. 

* This is probably good for now. Other authors will give other current 
  UI specs, and implementing flying around will make a good sprint 1 
  task. Other ideas should be gathered in the backlog. 