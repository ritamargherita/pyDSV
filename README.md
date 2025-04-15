# 🚀 _pyDSV: A Python tool for converting CSV data into RDF using the DSV ontology_ 🚀

**pyDSV** is a lightweight Python package that transforms CSV files into RDF (JSON-LD format) using the [DSV (DataSet-Variable Ontology)](https://w3id.org/dsv-ontology#) ontology. It enables structured and semantic representation of restricted access tabular data, making it more interoperable and machine-readable.

---

## 🧠 About the DataSet-Variable Ontology

This package creates RDF graphs following the **DataSetVariable Ontology**, a formal vocabulary designed for representing restricted access datasets and their metadata. The ontology was introduced in a peer-reviewed research publication:

> **Publication**: [Advancing data sharing and reusability for restricted access data on the Web: introducing the DataSet-Variable Ontology](https://doi.org/10.1145/3587259.3627559)  
> **GitHub Repository**: [github.com/ritamargherita/DataSet-Variable-Ontology](https://github.com/ritamargherita/DataSet-Variable-Ontology)

---

## 🔧 Features

- ✅ Validates and loads CSV files into pandas DataFrames
- ✅ Checks for malformed headers or inconsistent rows
- ✅ Converts tabular data into RDF triples using `rdflib`
- ✅ Outputs RDF data in JSON-LD format
- ✅ Easy-to-use Python API

---

## 📦 Installation

Install via pip:

```bash
pip install pyDSV
```

Or install directly from source:

```bash
git clone https://github.com/ritamargherita/pyDSV
cd pyDSV
pip install .
```

---

## 🐍 Python API Usage

<pre>
```python
from pyDSV.csvLoader import CSVLoader
from pyDSV.dsvTransformer import DSVTransformer

# Load CSV
loader = CSVLoader("data/example.csv")

# Transform to RDF
transformer = DSVTransformer(loader.df, "Covid19Dataset", "Public Health", output_file="output.jsonld")
```
</pre>

You can also access the RDF graph directly:

<pre>
```python
graph = transformer.get_graph()
print(graph.serialize(format="turtle"))
```
</pre>

---

## 📁 Project Structure

pyDSV/
├── pyDSV/
│   ├── __init__.py
│   ├── csvLoader.py
│   └── dsvTransformer.py
├── tests/
├── LICENSE
├── pyproject.toml
├── README.md
└── workflow.yml

---

## 👩‍💻 Author

Created by Margherita Martorana — feedback and contributions are welcome!

---

## 📚 How to Cite

If you use **pyDSV** in your research or project, please cite the following:

> Margherita Martorana. _pyDSV: A Python tool for converting CSV data into RDF using the DSV ontology_. Version 0.1.0. GitHub Repository: https://github.com/ritamargherita/pyDSV

<pre>
```bibtex
@misc{martorana2025pydsv,
  author       = {Margherita Martorana},
  title        = {pyDSV: A Python tool for converting CSV data into RDF using the DSV ontology},
  year         = {2025},
  howpublished = {\url{https://github.com/ritamargherita/pyDSV}},
  note         = {Version 0.1.0}
}
```
</pre>

**Related Publication**  
If your work is based on or contributes to the DSV Ontology, also cite the following paper:

> M. Martorana et al. _Advancing data sharing and reusability for restricted access data on the Web: introducing the DataSet-Variable Ontology_. K-CAP ’23, December 05–07, 2023, Pensacola, FL, USA. [DOI](https://doi.org/10.1145/3587259.3627559)

<pre>
```bibtex
@inproceedings{martorana2023advancing,
  title={Advancing data sharing and reusability for restricted access data on the Web: introducing the DataSet-Variable Ontology},
  author={Martorana, Margherita and Kuhn, Tobias and Siebes, Ronald and Van Ossenbruggen, Jacco},
  booktitle={Proceedings of the 12th Knowledge Capture Conference 2023},
  pages={83--91},
  year={2023}
}
```
</pre>
