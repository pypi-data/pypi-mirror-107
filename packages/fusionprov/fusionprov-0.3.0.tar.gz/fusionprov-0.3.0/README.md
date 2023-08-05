# fusionprov
## A python package for retrieving and documenting the provenance of fusion data.

### INTRODUCTION
----------------
The FAIR4Fusion projects seeks to make data produced by the nuclear fusion community FAIR compliant. Part of this is to ensure that the provenance of fusion data is readily available such that users can be confident in the quality of the data.

This package provides a way to retrieve provenance information for a given data-set from the institute that produced/owns the data and generate provenance documents that adhere to the W3C-PROV standard.

mastprov
--------
This module provides the `MastProv` class, which is instantiated with a UDA signal. The `write_prov()` method will collate the provenance information for the signal into a W3C-PROV compliant provenance document in json and xml formats. Optionally, it will output a graphical representation of the provenance as a png.

EXAMPLE:
```
import pyuda
import fusionprov

client = pyuda.Client()
client.set_property("get_meta", True)
ip_signal = client.get("ip", 30420)
ip_prov = fusionprov.MastProv(ip_signal)
ip_prov.write_prov(graph=True)
```

The `mastprov` module can also be run from the command line:

EXAMPLE:

```> mastprov 30420 ip --graph```

Both examples will generate directories in the current working directory for json, xml and png, storing the PROV documents in the relevant location.

imasprov
--------
This module provides the ImasProv class. It's functionality is very similar to MastProv described above. The class should be instantiated with an IDS (Interface Data Structure) containing the dataset, and optionally the accompanying dataset_descritption/dataset_fair IDSs.

Currently, the prov_from_data_ids() method will generate the provenance document from information in the 'ids_properties' and 'code' trees in the IDS.

From the command line, the module will read in IDS data from your local imasdb:

```> imasprov WEST 56900 3 equilibrium --graph```

Again, the module will generate directories in the current working directory for json, xml and png, storing the PROV documents in the relevant location.

### REQUIREMENTS
----------------

NOTE: The '--graph' option enables graphical output for provenance dosuments, but requires that the graphviz package be installed. You will need to install graphviz using your package manager of choice, e.g.:

`brew install graphviz`

Additionally, the mastprov module requires a local UDA installation and the imasprov module requires an IMAS installation (which may include UDA depending on your environment).

### INSTALLATION
----------------
This tool currently runs as a standalone package, available on PyPi, but may be adapted into a UDA plugin in the future. Provided that other dependencies are present, simply run:

`pip install fusionprov`
