# TransNet Generator
TransNet Generator is a Python library for generating transport networks from GTFS data. 
The library provides a convenient and efficient way to generate transport network graphs 
from one or multiple GTFS directories to a graph in Pajek or GML format, which can be used
for network analysis and visualization.

## Installation
To install TransNet Generator, you can use pip:

```python
pip install transnet-generator
```

## Usage
To use TransNet Generator, you can import the ``transnet_generator`` module and use the ``generate_graph`` function:

```python
from transnet_generator import generate_graph

input_GTFS = ["path/to/gtfs/directory1", "path/to/gtfs/directory2"]
output_path = "path/to/output/graph"

generate_graph(input_GTFS, output_path)
```

The ``generate_graph`` function takes two required arguments:

``input_GTFS`` - A list containing the paths to the directories containing the GTFS files.  
``output_path`` - The path to the output graph file.

## Supported Output Formats
TransNet Generator supports the following output formats:

Pajek (.net)  
GML (.gml)  

To specify the output format, simply pass the desired format as a string to the ``output_format`` parameter 
of the ``generate_graph`` function.

## Examples

Here's an example of how to generate a graph file in Pajek format from one GTFS directory:

```python
from transnet_generator import generate_graph

input_GTFS = ["path/to/gtfs/directory"]
output_path = "path/to/output/graph.net"

generate_graph(input_GTFS, output_path, format="pajek")
```

Here's an example of how to generate a graph file in GML format from three GTFS directories:

```python
from transnet_generator import generate_graph

input_GTFS = ["path/to/gtfs/directory1", "path/to/gtfs/directory2", "path/to/gtfs/directory3"]
output_path = "path/to/output/graph.gml"

generate_graph(input_GTFS, output_path, format="gml")
```

## License
TransNet Generator is released under the MIT License. See the LICENSE file for details.