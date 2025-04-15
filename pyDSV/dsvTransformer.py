# pyDSV/dsvTransformer.py

import re

from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDFS, DCTERMS


class DSVTransformer:
    """
    A class to transform a pandas DataFrame into a RDF graph using the DSV ontology.

    Attributes:
        df (pandas.DataFrame): The DataFrame to transform into RDF.
        dataset_name (str): The name of the dataset, used to generate the dataset URI.
        dataset_subject (str): The subject of the dataset, used in RDF triples.
        output_file (str, optional): If provided, the RDF graph will be saved to this file in JSON-LD format.
        graph (rdflib.Graph): The RDF graph to hold the dataset's RDF data.
        namespace (rdflib.Namespace): The namespace for generating URIs.
        DSV (rdflib.Namespace): The DSV ontology namespace.

    Methods:
        make_dataset_uri(): Generates a URI for the dataset.
        make_dataset_schema_uri(): Generates a URI for the dataset schema.
        make_column_uri(): Generates a URI for each column in the dataset.
        add_structural_layer(): Adds the structural layer to the RDF graph, including dataset and column details.
        transform(): Performs the transformation of the DataFrame into the RDF graph.
        save_to_jsonld(): Serializes the RDF graph to JSON-LD format and saves it to a file.
        get_graph(): Returns the RDF graph.
    """

    def __init__(self, df, dataset_name, dataset_subject, 
                 base_namespace="http://example.org/", output_file=None):
        """
        Initializes the DSVTransformer with the provided dataset and configurations.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data to transform.
            dataset_name (str): The name of the dataset, used to build the dataset URI.
            dataset_subject (str): The subject associated with the dataset, used in RDF.
            base_namespace (str): The base namespace to use for generating URIs (default is "http://example.org/").
            output_file (str, optional): If specified, the RDF graph will be saved to this JSON-LD file.
        
        Raises:
            ValueError: If the dataset is invalid or improperly configured.
        """
        self.df = df
        self.dataset_name = re.sub(r'[^a-zA-Z0-9]', '_', dataset_name)
        self.dataset_subject = dataset_subject
        self.output_file = output_file

        self.graph = Graph()
        self.namespace = Namespace(base_namespace)
        self.DSV = Namespace("https://w3id.org/dsv-ontology#")
        self.graph.bind("ex", self.namespace)
        self.graph.bind("dsv", self.DSV)

        self.transform()
        if self.output_file:
            self.save_to_jsonld(self.output_file)


    def make_dataset_uri(self, dataset_name):
        """
        Constructs a URI for the dataset using the base namespace and the dataset name.

        Args:
            dataset_name (str): The name of the dataset.

        Returns:
            rdflib.URIRef: A URIRef representing the URI of the dataset.
        """
        dataset_uri = URIRef(f"{self.namespace}{dataset_name}")
        return dataset_uri
    
    def make_dataset_schema_uri(self, dataset_uri):
        """
        Generates a URI for the dataset schema based on the dataset URI.

        Args:
            dataset_uri (rdflib.URIRef): The URI of the dataset.

        Returns:
            rdflib.URIRef: A URIRef representing the URI of the dataset schema.
        """
        dataset_schema_uri = URIRef(dataset_uri+'/datasetSchema')
        return dataset_schema_uri
    
    def make_column_uri(self, dataset_uri, column_name):
        """
        Generates a URI for a specific column in the dataset, cleaning the column name for URI use.

        Args:
            dataset_uri (rdflib.URIRef): The URI of the dataset.
            column_name (str): The name of the column to generate a URI for.

        Returns:
            rdflib.URIRef: A URIRef representing the URI of the column.
        """
        clean_column_name = re.sub(r'[^a-zA-Z0-9]', '_', column_name)
        column_uri = URIRef(f"{dataset_uri}/column/{clean_column_name}")
        return column_uri

    def add_structural_layer(self, graph, dataset_uri, dataset_name, 
                             dataset_subject, dataset_schema_uri, df):
        """
        Adds the structural layer to the RDF graph, including the dataset and its columns.

        Args:
            graph (rdflib.Graph): The RDF graph to modify.
            dataset_uri (rdflib.URIRef): The URI of the dataset.
            dataset_name (str): The name of the dataset.
            dataset_subject (str): The subject associated with the dataset.
            dataset_schema_uri (rdflib.URIRef): The URI of the dataset schema.
            df (pandas.DataFrame): The DataFrame containing the data to add to the graph.
        """
        graph.add((dataset_uri, RDF.type, self.DSV.Dataset))
        graph.add((dataset_uri, DCTERMS.title, Literal(dataset_name)))
        graph.add((dataset_uri, DCTERMS.subject, Literal(dataset_subject)))
        graph.add((dataset_uri, self.DSV.datasetSchema, dataset_schema_uri))
        
        graph.add((dataset_schema_uri, RDF.type, self.DSV.DatasetSchema))

        for column_name in df.columns:
            column_uri = self.make_column_uri(dataset_uri, column_name)
            graph.add((dataset_schema_uri, self.DSV.column, column_uri))
            graph.add((column_uri, RDF.type, self.DSV.Column))
            graph.add((column_uri, RDFS.label, Literal(column_name)))
    
    def transform(self):
        """
        Transforms the pandas DataFrame into an RDF graph using the DSV ontology.

        This method generates the dataset URI, dataset schema URI, and populates the RDF graph
        with the dataset and column information.
        """
        dataset_uri = self.make_dataset_uri(self.dataset_name)
        dataset_schema_uri = self.make_dataset_schema_uri(dataset_uri)
        
        self.add_structural_layer(self.graph, dataset_uri, self.dataset_name, 
                                  self.dataset_subject, dataset_schema_uri, self.df)

    def save_to_jsonld(self, output_file):
        """
        Serializes the RDF graph to JSON-LD format and saves it to a file.

        Args:
            output_file (str): The path where the RDF graph should be saved in JSON-LD format.
        """
        self.graph.serialize(destination=output_file, format="json-ld")
    
    def get_graph(self):
        """
        Returns the RDF graph.

        Returns:
            rdflib.Graph: The RDF graph containing the dataset information.
        """
        return self.graph