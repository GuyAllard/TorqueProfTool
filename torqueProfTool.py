#!/usr/bin/env python
#
# Copyright 2015 Guy Allard
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import print_function, division

'''Convert profiler output from the Torque3D game engine into json format'''

__author__ = "Guy Allard"

import sys
import re
import json
import optparse

def consume( file_name ):
    """Iterator to read lines from file_name, stripping trailing control characters"""
    stream = sys.stdin
    
    if file_name:
        try:
            stream = open(file_name)
        except IOError:
            sys.exit("Unable to open input file")

    for line in stream:
        yield line.strip()

    stream.close()


def prune( root_function_name, functions, events ):
    """Root the call graph at the specified root function by pruning all events
       that are not descended from root_function_name"""
    if root_function_name == "":
        return events

    try:
        root_func = functions.index(root_function_name)
    except:
        sys.exit("Root does not exist in callgraph")
    
    pruned = []
    for (callchain, cost) in events:
        if root_func in callchain:
            pos = callchain.index(root_func)
            callchain = callchain[:pos+1]
        
            if len(callchain) > 0:
                pruned += [(callchain, cost)]
    return pruned


def parse( file_name, root_function_name ):
    """Parse T3D profiler output"""

    functions = []      # list of function names
    events = []         # list of call chain 'events'
    stack = []          # temporary call stack
    profile_block = 0   # the profile block currently being parsed
    renders = 0         # number of render events
    ticks = 0           # number of tick events

    for line in consume(file_name):
        # determine which profiler block we are parsing
        if len(line) == 0:
            profile_block = 1
            continue

        # skip headers
        if line.startswith("Profiler Data") or \
           line.startswith("Ordered by") or \
           line.startswith("%%NSTime"):
           continue

        # split the line on whitespace, retaining the whitespace so that
        # the function indentation level can be determined
        fields = re.split(r'(\s+)', line)

        # sanity check
        if len(fields) <> 7:
            sys.exit("This file does not appear to be a torque profile dump")

        # We can obtain the number of frames rendered by counting the number of calls to CanvasRenderControls
        # The number of 'Ticks' can be obtained by counting the number of calls to SceneGraph_scopeScene
        if profile_block == 0:
            functions += [fields[6]]
            if "CanvasRenderControls" in fields:
                renders = int(fields[4])
            elif "SceneGraph_scopeScene" in fields:
                ticks = int(fields[4])
            continue

        # skip the function named "ROOT"
        if fields[6] == "ROOT":
            continue

        # Determine the position of the current function in the call chain
        indent_level = (len(fields[5]) - 1) / 2

        # generate the call chain events
        while indent_level <= len(stack):
            events += [([functions.index(x) for (x,y) in reversed(stack)], stack.pop()[1])]

        if indent_level > len(stack):
            stack += [(fields[6], max(float(fields[2]), 0.0001))]

    # empty what's left on the stack
    while len(stack) > 0:
        events += [([functions.index(x) for (x,y) in reversed(stack)], stack.pop()[1])]    

    # prune the call graph
    events = prune(root_function_name, functions, events)
 
    # estimate framerate
    try:
        frame_rate = (renders / ticks) * (1000 / 32)
    except ZeroDivisionError:
        frame_rate = 0
        
    # generate the profile dictionary
    profile = {
                'version':  0,
                'costs':    [{'description' : 'Time'}],
                'functions':[{'name' : x} for x in functions],
                'events':   [{'callchain' : cc, 'cost':[c]} for (cc,c) in events],
                'metrics':  {'renders' : renders,
                             'ticks' : ticks,
                             'max framerate' : frame_rate}
              }
    
    if len(profile['costs']) == 0 or len(profile['functions']) == 0 or \
       len(profile['events']) == 0:
        sys.exit("Input file is not a valid T3D profiler dump")
        
    return profile


def main():
    # parse command line args
    optparser = optparse.OptionParser(
        usage="\n\t%prog [options] [file] ...")
        
    optparser.add_option(
        '-r','--root',
        type="string", dest="root_func", default="",
        help="Name of function to use as the root node")
    
    optparser.add_option(
        '-o', '--output-file',
        type="string", dest="out_filename", default="",
        help="Name of file to write output to")
        
    (options, args) = optparser.parse_args(sys.argv[1:])
    
    file_name = None
    if len(args) > 1:
        optparse.error("Incorrect number of args")
    elif len(args) == 1:
        file_name = args[0]

    # create the call graph
    profile = parse(file_name, options.root_func)
    
    # output some metrics to the console
    print("------------METRICS--------------", file=sys.stderr)
    for(key, value) in profile['metrics'].iteritems():
        print(key + ": " + str(value), file=sys.stderr)
    print("---------------------------------", file=sys.stderr)
        
    # output the callgraph in json format
    out_file = sys.stdout
    if options.out_filename <> "":
        try:
            out_file = open(options.out_filename, 'wt')
        except IOError:
            sys.exit("Could not open the output file")
        
    print(json.dumps(profile, indent=2, separators=(',', ': ')), file=out_file)
    
    


if __name__ == '__main__':
    main()
