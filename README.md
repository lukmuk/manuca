# Manuca

Manuca is a small command-line Python program to calculate various forms of the mean (or effective) atomic number and also other properties.

The name stems from it's intended use as a **M**ean **A**tomic **Nu**mber **Ca**lculator.

## Quickstart and Examples

Install the required Python packages and then run Manuca:

``pip install numpy chemparse mendeleev``

``python manuca.py``

Enter a stoichiometry, e.g. H2O and confirm with `Enter`.

<img title="H2O demo" src="images/H2O_demo.PNG" alt="Example" data-align="left">

Quit by entering `q`.

Chemparse can handle (single-level) parentheses, here for the [Fe-based superconductor](https://en.wikipedia.org/wiki/Iron-based_superconductor) Ba(Fe0.92Co0.08)2As2:

<img title="Ba122 demo" src="images/ba122_demo.PNG" alt="Example" data-align="left">

The `multi` compound mode is meant to handle more complex compounds, e.g. 73% of H2O and 27% of SiO2.

<img title="Multi-compound demo" src="images/multi_demo.PNG" alt="Example" data-align="left">

A more complicated random mixture of superconductors and BaZrO3: 42% YBa2Cu3O6.9, 42% Ba(Fe0.92Co0.08)2As2, and 16% BaZrO3:

<img title="Multi-compound demo" src="images/multi_demo2.PNG" alt="Example" data-align="left">

To finish, let's put in the periodic system (let's call it an ultra-high-entropy alloy):

<img title="Periodic table demo 1" src="images/periodictable_demo1.PNG" alt="Example" data-align="left">

... and in the end: 

<img title="Periodic table demo 2" src="images/periodictable_demo2.PNG" alt="Example" data-align="left">

The periodic-table-elements string can be generated from `mendeleev`:

```python
from mendeleev.fetch import fetch_tables
df = fetch_table('elements') #pandas data frame
print(''.join(df['symbol'].to_list()))
```

## Requirements and Installation

Manuca works by utilizing [chemparse](https://pypi.org/project/chemparse/) to evaluate the stoichiometric formula from a user input. Then, [mendeleev](https://github.com/lmmentel/mendeleev) is used to retrieve the element-specific data. NumPy is used for calculations.

- Clone or download the repository (or just `manuca.py`).

- **Optional**: Create a fresh environment:

    ``conda create -n manuca python=3.9`` 

    ``conda activate manuca``

- Install the required Python packages:

    ``pip install numpy chemparse mendeleev`` 

- Run Manuca (from the folder where the ``manuca.py`` is located):

    ``python manuca.py`` 

## Documentation

#### Output

Manuca v0.1 calculates the following outputs:

- Composition in atomic % (at.%) and weight % (wt.%)

- Mean/effective atomic numbers are calculated from the atomic numbers (<img src="https://render.githubusercontent.com/render/math?math=Z_i">), the weight fractions (<img src="https://render.githubusercontent.com/render/math?math=c_i">, and atomic fractions (<img src="https://render.githubusercontent.com/render/math?math=a_i">):
  
  - Atomic-percent average:
    
    <img src="https://render.githubusercontent.com/render/math?math=\overline{Z}=\sum_i a_i Z_i">
  
  - Müller (1954), 
    
    <img src="https://render.githubusercontent.com/render/math?math=\overline{Z}=\sum_i c_i Z_i">
  
  - Sandick & Allen (1954)
    
    <img src="https://render.githubusercontent.com/render/math?math=\overline{Z}=\sum_i a_i Z^2_i/\sum_i a_i Z_i">
  
  - Joyet (1953) / Hohn & Niedrig (1972) / Büchner (1973):
    
    <img src="https://render.githubusercontent.com/render/math?math=\overline{Z}=\sqrt{\sum_i a_i Z^2_i}">
  
  - Everhart (1960):
    
    <img src="https://render.githubusercontent.com/render/math?math=\overline{Z}=\sum_i c_i Z^2_i/\sum_i c_i Z_i">
  
  - Egerton (effective Z for EFTEM):
    
    <img src="https://render.githubusercontent.com/render/math?math=\overline{Z}_\text{eff}=\sum_i a_i Z^{1.3}_i/\sum_i a_i Z^{0.3}_i">
* Total and average molecular weight in g/mol.
