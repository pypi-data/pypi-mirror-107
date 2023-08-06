import re
from typing import Iterable, Any, List

import networkx as nx
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import path, include
from django_koldar_utils.functions import modules

# from admin_section.AdminAppSection import AdminAppSection
# from authentication_section.AuthenticationAppSection import AuthenticationAppSection
# from booking_section.BookingAppSection import BookingAppSection
# from example_section.ExampleAppSection import ExampleAppSection
# from gdpr_section.GDPRAppSection import GDPRAppSection
# from graphql_section.GraphQLSection import GraphQLSection
# from logging_section.LoggingAppSection import LoggingAppSection
# from server_project import settings
# from utils.AbstractDjangoSection import AbstractDjangoSection
from django_koldar_utils.sections.AbstractDjangoSection import AbstractDjangoSection

import logging

LOG = logging.getLogger(__name__)
SECTION_DEPENDENCY_GRAPH: nx.DiGraph()


def setup_dependency_graph(sections: List[AbstractDjangoSection]) -> nx.DiGraph:
    """
    Setup the section dependency graph SECTION_DEPENDENCY_GRAPH
    """

    # add nodes
    for s in sections:
        LOG.info(f"Added section {s.get_app_name()}")
        SECTION_DEPENDENCY_GRAPH.add_node(s.get_app_name(), section=s)
    # add dependencies
    for source_section in sections:
        for dependency_pattern in source_section.get_section_setup_dependencies():
            for sink_section in sections:
                if sink_section == source_section:
                    continue
                m = re.search(dependency_pattern, sink_section.get_app_name())
                if m is not None:
                    LOG.info(f"{source_section.get_app_name()} depends on section {sink_section.get_app_name()}")
                    SECTION_DEPENDENCY_GRAPH.add_edge(source_section.get_app_name(), sink_section.get_app_name(), label="setup")
    return SECTION_DEPENDENCY_GRAPH


def get_ordered_sections() -> Iterable["AbstractDjangoSection"]:
    """
    Generates a list of sections, where the one with no setup dependency are outputted first
    """
    return reversed(list(nx.topological_sort(SECTION_DEPENDENCY_GRAPH)))


def generate_properties(section: "AbstractDjangoSection", settings, destination_settings: str):
    namespace = section.get_configuration_dictionary_name()
    properties = section.get_properties_declaration()
    required_keys = list(filter(lambda x: x.required, properties.values()))
    namespace_in_settings = getattr(settings, namespace, None)
    if namespace_in_settings is None and len(required_keys) > 0:
        raise ImproperlyConfigured(f"application {section.get_app_name()} requires to have set {', '.join(*required_keys)}, but you have not set event the app configuraton dictionary {namespace}!")
    for key, prop in section.get_properties_declaration().items():
        if prop.required and not hasattr(namespace_in_settings, key):
            raise ImproperlyConfigured(f"application {section.get_app_name()} requires to have set {key}, but you did not have set it in {namespace}!")
        property_in_settings = getattr(namespace_in_settings, key)
        if prop.property_type != type(property_in_settings):
            raise ImproperlyConfigured(
                f"application {section.get_app_name()} requires to have ther variable {key} set to type {prop.property_type}, but you not have set as a {type(property_in_settings)}!")
        # ok, set it in the settings
        modules.add_variable_in_module(destination_settings, key, property_in_settings)


def update_middlewares(middleswares: List[str]) -> List[str]:
    result = list(middleswares)
    for s in get_ordered_sections():
        result = s.update_middlewares(result)
    return result


def add_custom_sections() -> Iterable[str]:
    result = []
    for s in get_ordered_sections():
        for dep in s.depends_on_app():
            result.append(dep)
        result.append(s.get_app_name())
    return result


def add_app_section_paths() -> Iterable[Any]:
    result = []

    for s in get_ordered_sections():
        prefix = s.get_route_prefix()
        if prefix[-1] != "/":
            prefix = prefix + "/"
        result.append(path(prefix, include(f"{s.get_app_name()}.urls", s.get_route_options())))

    return result


def add_authentication_backends_in_project_settings() -> Iterable[str]:
    result = set()
    for s in get_ordered_sections():
        for d in s.get_authentication_backends():
            result.add(d)
    return result


def add_new_configuratons_in_project_settings():
    for s in get_ordered_sections():
        d = s.get_variables_to_add_in_project_settings()
        for var_name, var_value in d.items():
            modules.add_variable_in_module(settings.__name__, var_name, var_value)
