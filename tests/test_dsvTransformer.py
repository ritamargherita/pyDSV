import pytest
import pandas as pd
from unittest.mock import MagicMock
from pyDSV.dsvTransformer import DSVTransformer
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDFS, DCTERMS

@pytest.fixture
def sample_dataframe():
    data = {
        'col1': [1, 2, 3],
        'col2': ['A', 'B', 'C'],
        'col3': [4.5, 5.5, 6.5]
    }
    return pd.DataFrame(data)

@pytest.fixture
def transformer(sample_dataframe):
    return DSVTransformer(
        df=sample_dataframe,
        dataset_name="sample_dataset",
        dataset_subject="SampleSubject"
    )

def test_dsv_transformer_initialization(transformer):
    assert transformer.df is not None
    assert transformer.dataset_name == "sample_dataset"
    assert transformer.dataset_subject == "SampleSubject"
    assert transformer.graph is not None 

def test_graph_contains_expected_triples(transformer):
    graph = transformer.get_graph()
    namespace = transformer.namespace
    dsv = transformer.DSV
    dataset_uri = namespace["sample_dataset"]
    dataset_schema_uri = URIRef(f"{dataset_uri}/datasetSchema")

    assert (dataset_uri, RDF.type, dsv.Dataset) in graph
    assert (dataset_uri, DCTERMS.title, Literal("sample_dataset")) in graph
    assert (dataset_uri, DCTERMS.subject, Literal("SampleSubject")) in graph
    assert (dataset_uri, dsv.datasetSchema, dataset_schema_uri) in graph

    assert (dataset_schema_uri, RDF.type, dsv.DatasetSchema) in graph

    col_uri = URIRef(f"{dataset_uri}/column/col1")
    assert (dataset_schema_uri, dsv.column, col_uri) in graph
    assert (col_uri, RDF.type, dsv.Column) in graph
    assert (col_uri, RDFS.label, Literal("col1")) in graph