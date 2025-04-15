# pyDSV/__init__.py

from .csvLoader import CSVLoader
from .dsvTransformer import DSVTransformer

def csv2dsv(csv_file_path, dataset_name, dataset_subject, output_file=None):
    """
    """

    csv_loader = CSVLoader(csv_file_path)
    df = csv_loader.df

    if df is not None:
        dsv_transformer = DSVTransformer(df,
                                         dataset_name=dataset_name,
                                         dataset_subject=dataset_subject,
                                         output_file=output_file)
    else:
        print("Failed to load CSV. RDF transformation skipped.")
