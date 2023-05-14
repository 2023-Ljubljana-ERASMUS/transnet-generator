import networkx as nx
from datetime import datetime


def generate_graph(input_GTFS: list, output_path: str, output_format="pajek", encoding="UTF-8") -> None:
    """ Generate the transport graph and write it in the desired format.

    :param input_GTFS: The path to the directory containing the GTFS files.
    :param output_path:  The name (and the path if the file isn't in the current working directory)
    of the output graph file.
    :param output_format: The format of the output graph file.
    :param encoding:
    """

    network = nx.Graph()
    build_from_GTFS(input_GTFS, network)

    if output_format == "pajek":
        nx.write_pajek(network, output_path, encoding)
    elif output_format == "gml":
        nx.write_gml(network, output_path)
    else:
        raise ValueError(f"This output format [{output_format}] is not supported. Please use pajek or gml format.")


def add_stops_attributes(source: str, network: nx.Graph) -> None:
    """ Add stops attributes to the graph.

    :param network:
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

                nx.set_node_attributes(network, {stop_id: stop_name}, "stop_name")
                nx.set_node_attributes(network, {stop_id: lat}, "lat")
                nx.set_node_attributes(network, {stop_id: long}, "long")


def build_from_GTFS(sources, network) -> None:

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
                    network.add_node(stop_point)
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

                    network.add_node(stop_point)
                    network.add_edge(stop_point, previous_stop_id, travel_time=travel_time)

                previous_stop_id = stop_point
                departure_time = fields[2]

        add_stops_attributes(source, network)
