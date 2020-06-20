DVND dataflow
=============

<p align="center">
  <a href="https://github.com/LabCad/dvnd-df">
    <img src="https://tokei.rs/b1/github/LabCad/dvnd-df?category=lines" alt="Current total lines.">
  </a>
  <a href="https://github.com/LabCad/dvnd-df/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License.">
  </a>
</p>

## Usefull llinks

https://www.overleaf.com/11702861nbytngsgvrxg

https://mathema.tician.de/dl/main.pdf

### Sucuri has 2 repositories

https://github.com/tiagoaoa/Sucuri/blob/master/examples/optimizaiton.py

https://bitbucket.org/flatlabs/sucuri-free

https://github.com/igormcoelho/simple-pycuda


## DEPENDENCIES

Get submodules:

`git submodule update --init --recursive`

`git pull --recurse-submodules`

Install numpy:

`pip install numpy`

## Citation

Cite this in your paper as:

```bibtex
@article{ARAUJO2020102661,
	title = "A multi-improvement local search using dataflow and GPU to solve the minimum latency problem",
	journal = "Parallel Computing",
	pages = "102661",
	year = "2020",
	issn = "0167-8191",
	doi = "https://doi.org/10.1016/j.parco.2020.102661",
	url = "http://www.sciencedirect.com/science/article/pii/S0167819120300545",
	author = "Rodolfo Pereira Araujo and Igor Machado Coelho and Leandro Augusto Justen Marzulo",
	keywords = "Dataflow, Graphics processing unit, Metaheuristics, Local search, Variable neighborhood descent"
}

@conference {dvnddf-ipdps2018,
    author={Rodolfo Pereira Araujo and Igor Machado Coelho and Leandro A. J. Marzulo},
    title={A {DVND} local search implemented on a dataflow architecture for the Minimum Latency Problem},
    booktitle={7th Worksohp on Parallel Programming Models (32nd IEEE International Parallel and Distributed Processing Symposium - IPDPS 2018)},
    year={2018}
}

@mastersthesis{dvnddf-uerj2018,
  author       = {Rodolfo Pereira Araujo},
  title        = {Estratégias de exploração de vizinhança com {GPU} para problemas de otimização},
  year         = 2018,
  address      = {Rio de Janeiro, RJ, Brasil},
  school       = {Instituto de Matemática e Estatística, Universidade do Estado do Rio de Janeiro},
  Month        = oct,
  keywords     = "Dataflow, Busca Local, Meta-heurística, Graphics Processing Unit, Variable Neighborhood Descent, Meta-heuristics, Local Search",
  howpublished = {\url{http://www.bdtd.uerj.br/tde_busca/arquivo.php?codArquivo=14632}}
}
```
