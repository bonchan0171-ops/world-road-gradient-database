"""
OpenStreetMap XML reader.

This module converts selected OSM road data into a RoadNetwork.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from wrgd.geometry.distance import calculate_distance
from wrgd.models.coordinate import Coordinate
from wrgd.models.network_edge import NetworkEdge
from wrgd.models.network_node import NetworkNode

from .road_network import RoadNetwork


class OSMReader:
    """Reader for OpenStreetMap XML road data."""

    SUPPORTED_HIGHWAYS = frozenset(
        {
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary",
            "residential",
            "unclassified",
            "service",
        }
    )

    def __init__(self, filepath: str | Path) -> None:
        """
        Initialize the OSM reader.

        Parameters
        ----------
        filepath : str | Path
            Path to the OSM XML file.
        """
        self.filepath = Path(filepath)

    def read(self) -> RoadNetwork:
        """
        Read supported roads from an OSM XML file.

        Returns
        -------
        RoadNetwork
            Road network built from supported OSM ways.

        Raises
        ------
        FileNotFoundError
            If the OSM file does not exist.
        ValueError
            If the OSM XML is invalid or contains an invalid road node.
        """
        try:
            root = ET.parse(self.filepath).getroot()
        except ET.ParseError as error:
            raise ValueError("Invalid OSM XML file.") from error

        osm_nodes = self._read_nodes(root)
        network = RoadNetwork()
        edge_id = 1

        for way in root.findall("way"):
            tags = self._read_tags(way)
            road_type = tags.get("highway")

            if road_type not in self.SUPPORTED_HIGHWAYS:
                continue

            node_ids = [
                int(ref)
                for nd in way.findall("nd")
                if (ref := nd.get("ref")) is not None
            ]

            if len(node_ids) < 2:
                continue

            way_nodes = [self._get_node(osm_nodes, node_id) for node_id in node_ids]
            oneway = self._parse_oneway(tags.get("oneway"))

            for start_node, end_node in zip(way_nodes, way_nodes[1:]):
                geometry = [
                    Coordinate(start_node.latitude, start_node.longitude),
                    Coordinate(end_node.latitude, end_node.longitude),
                ]
                distance = calculate_distance(
                    start_node.latitude,
                    start_node.longitude,
                    end_node.latitude,
                    end_node.longitude,
                )

                network.add_node(start_node)
                network.add_node(end_node)
                network.add_edge(
                    NetworkEdge(
                        id=edge_id,
                        start_node=start_node,
                        end_node=end_node,
                        distance=distance,
                        average_gradient=0.0,
                        road_type=road_type,
                        oneway=oneway,
                        geometry=geometry,
                    )
                )
                edge_id += 1

        return network

    @staticmethod
    def _read_nodes(root: ET.Element) -> dict[int, NetworkNode]:
        """Convert OSM node elements into network nodes."""
        nodes: dict[int, NetworkNode] = {}

        for element in root.findall("node"):
            node_id = element.get("id")
            latitude = element.get("lat")
            longitude = element.get("lon")

            if node_id is None or latitude is None or longitude is None:
                raise ValueError("OSM node requires id, lat, and lon attributes.")

            node = NetworkNode(
                id=int(node_id),
                latitude=float(latitude),
                longitude=float(longitude),
                elevation=None,
            )
            nodes[node.id] = node

        return nodes

    @staticmethod
    def _read_tags(element: ET.Element) -> dict[str, str]:
        """Return key/value tags from an OSM element."""
        return {
            key: value
            for tag in element.findall("tag")
            if (key := tag.get("k")) is not None and (value := tag.get("v")) is not None
        }

    @staticmethod
    def _get_node(nodes: dict[int, NetworkNode], node_id: int) -> NetworkNode:
        """Return a referenced node or raise a descriptive error."""
        try:
            return nodes[node_id]
        except KeyError as error:
            raise ValueError(f"OSM way references unknown node {node_id}.") from error

    @staticmethod
    def _parse_oneway(value: str | None) -> bool:
        """Convert the supported OSM oneway values to a boolean."""
        return value is not None and value.lower() == "yes"
