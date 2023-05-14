import networkx as nx
from datetime import datetime
from prettytable import PrettyTable


def generate_graph(input_GTFS: list, output_path: str, name="transport-network",
                   output_format="pajek", encoding="UTF-8") -> None:
    """ Generate the transport graph and write it in the desired format.

    :param input_GTFS: The path to the directory containing the GTFS files.
    :param output_path:  The name (and the path if the file isn't in the current working directory) of the output graph file.
    :param name: The name of the network
    :param output_format: The format of the output graph file.
    :param encoding:
    """

    graph = nx.Graph(name=name)
    build_from_GTFS(input_GTFS, graph)

    if output_format == "pajek":
        # Convert numeric attributes to string
        travel_time = nx.get_edge_attributes(graph, "travel_time")
        travel_time = {k: str(v) for k, v in travel_time.items()}
        nx.set_edge_attributes(graph, travel_time, "travel_time")

        nx.write_pajek(graph, output_path, encoding)
    elif output_format == "gml":
        nx.write_gml(graph, output_path)
    else:
        raise ValueError(f"This output format [{output_format}] is not supported. Please use pajek or gml format.")

    graph_info(graph)


def add_stops_attributes(source: str, graph: nx.Graph) -> None:
    """ Add stops attributes to the graph.

    :param graph:
    :param source:
    """

    with open(source + "/stops.txt", 'r', encoding='utf-8') as file:
        for line in file:
            fields = line.split(',')
            stop_id = fields[0]
            if stop_id.startswith('StopPoint:'):
                stop_name = fields[1]
                lat = fields[3]
                long = fields[4]

                nx.set_node_attributes(graph, {stop_id: stop_name}, "stop_name")
                nx.set_node_attributes(graph, {stop_id: lat}, "lat")
                nx.set_node_attributes(graph, {stop_id: long}, "long")


def build_from_GTFS(sources, graph) -> None:

    if sources is None:
        raise ValueError()

    for source in sources:
        with open(source + "/stop_times.txt", 'r') as file:
            file.readline()  # Skip header
            previous_stop_id = None
            departure_time = None
            for line in file:
                fields = line.split(',')

                arrival_time = fields[1]
                stop_point = fields[3]
                stop_sequence = int(fields[4])

                if stop_sequence == 0:
                    # This is the starting point of the trip
                    graph.add_node(stop_point)
                else:
                    # Compute travel time
                    # --> Check validity
                    departure_hour = int(departure_time.split(':')[0])
                    arrival_hour = int(arrival_time.split(':')[0])
                    if departure_hour > 23 or arrival_hour > 23:
                        continue
                    departure = datetime.strptime(departure_time, '%H:%M:%S')
                    arrival = datetime.strptime(arrival_time, '%H:%M:%S')

                    delta = arrival - departure
                    travel_time = int(delta.total_seconds() // 60)

                    graph.add_node(stop_point)
                    graph.add_edge(stop_point, previous_stop_id, travel_time=travel_time)

                previous_stop_id = stop_point
                departure_time = fields[2]

        add_stops_attributes(source, graph)


def graph_info(graph: nx.Graph):
    # Create a pretty table to display the basic info
    table = PrettyTable()
    table.field_names = ["Graph property", "Value"]

    # Add the graph properties to display
    table.add_row(["Nodes", graph.number_of_nodes()])
    table.add_row(["Edges", graph.number_of_edges()])
    table.add_row(["Connected components", nx.number_connected_components(graph)])
    table.add_row(["Average degree", round(sum(dict(graph.degree()).values()) / len(graph), 2)])

    # Print the pretty table
    print(table)
