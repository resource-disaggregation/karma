# Karma: Resource Allocation for Dynamic Demands

This repository contains open source code for Karma, a new resource allocation mechanism for dynamic demands. Karma introduces a new credit-based resource allocation algorithm with powerful theoretical guarantees related to Pareto efficiency, strategy-proofness, and fairness under dynamic demands, that have been shown to translate well into practice. For a full technical description of Karma, please refer to our [OSDI'23 paper](https://www.usenix.org/conference/osdi23/presentation/vuppalapati).

## Components

This repository contains the following three components:

- [algorithm/](algorithm/): Efficient implementation of the Karma algorithm provided as a library for easy integration with applications.
- [simulator/](simulator/): Simulator that can execute Karma and other relevant schemes over input demand traces for easy testing and exploration.
- [jiffy-implementation/](jiffy-implementation/): End-to-end implementation of Karma on top of a distributed elastic memory system ([Jiffy](https://github.com/resource-disaggregation/jiffy))

## Contact

Midhul Vuppalapati ([midhul@cs.cornell.edu](mailto:midhul@cs.cornell.edu))

## Citation

```
@inproceedings {karma-osdi23,
author = {Midhul Vuppalapati and Giannis Fikioris and Rachit Agarwal and Asaf Cidon and Anurag Khandelwal and {\'E}va Tardos},
title = {Karma: Resource Allocation for Dynamic Demands},
booktitle = {17th USENIX Symposium on Operating Systems Design and Implementation (OSDI 23)},
year = {2023},
isbn = {978-1-939133-34-2},
address = {Boston, MA},
pages = {645--662},
url = {https://www.usenix.org/conference/osdi23/presentation/vuppalapati},
publisher = {USENIX Association},
month = jul,
}
```