# TorqueProfTool
TorqueProfTool can be used to convert the profiler output from the Torque3D engine into a json format call graph which can be visualized using tools such as gprof2dot and graphviz.

## Example
This call-graph was generated from the profiler dump of the [Pacific demo scene](http://torque3d.wdfiles.com/local--files/communityproject%3Aperformance%3Aprofiling-and-optimisation/profilerDumpToFile241587.txt) from [Torque3D.org](http://torque3d.org).  
TorqueProfTool was used to convert the profiler dump into a json format call graph, then [gprof2dot](https://github.com/jrfonseca/gprof2dot) was used to convert the callgraph to dot graph.  
Finaly, a png image was generated using [graphviz](http://www.graphviz.org) dot.
  
  
