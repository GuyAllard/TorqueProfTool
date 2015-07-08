# TorqueProfTool
TorqueProfTool is a python script which can be used to convert the profiler output from the [Torque3D](https://github.com/GarageGames/Torque3D) engine into a json format profile which can be visualized using tools such as [gprof2dot](https://github.com/jrfonseca/gprof2dot) and [graphviz](http://www.graphviz.org).

## Example
The following call-graph was generated from the profiler dump of the [Pacific demo scene](http://torque3d.wdfiles.com/local--files/communityproject%3Aperformance%3Aprofiling-and-optimisation/profilerDumpToFile241587.txt) from [Torque3D.org](http://torque3d.org), and shows all functions which consumed at least 0.1% of the cpu time.  
TorqueProfTool was used to convert the profiler dump into json format which could then be visualized using [gprof2dot](https://github.com/jrfonseca/gprof2dot) and [graphviz](http://www.graphviz.org).  
[![pacific call graph](examples/pacific_full_thumb.png)](examples/pacific_full.png?raw=true)  
  
In addition to the profile conversion, torqueProfTool also reports some key metrics:  
**ticks**         - the number of times that the simulation was ticked  
**renders**       - the number of the times that the screen was re-drawn  
**max framerate** - an estimate of the maximum framerate during the profiled period  
The following metrics were obtained from the profiler dump above:  
```
ticks: 3343
renders: 3343
max framerate: 31.25
```
  
  
## Requirements
[Python](http://www.python.org) (Tested with python 2.7.6)
  
### Optional
[gprof2dot](https://github.com/jrfonseca/gprof2dot) for conversion to other graph formats.  
[GraphViz](http://www.graphviz.org) to visualize the call graph.  
[xdot](https://github.com/jrfonseca/xdot.py) for interactive visualization (requires [PyGTK](http://www.pygtk.org))  
### Installation
Either clone the repository using `git clone https://github.com/GuyAllard/TorqueProfTool`  
or download [this zip](https://github.com/GuyAllard/TorqueProfTool/archive/master.zip) and extract it to the desired location.  
Add the TorqueProfTool directory to your system PATH variable.
  
## Usage
```
torqueProfTool.py [options] [file] ...

Options:
  -h, --help                                    show the help message and exit
  -r ROOT_FUNC, --root=ROOT_FUNC                Name of function to use as the root node
  -o OUT_FILENAME, --output-file=OUT_FILENAME   Name of file to write output to
```
  
To reproduce the example graph above as a png image named pacific.png  
`torqueProfTool.py profilerDumpToFile241587.txt | gprof2dot -f json | dot -Tpng -o pacific.png`  

or alternatively, to use xdot for the visualization,  
`torqueProfTool.py profilerDumpToFile241587.txt | gprof2dot -f json | xdot -`  

  
