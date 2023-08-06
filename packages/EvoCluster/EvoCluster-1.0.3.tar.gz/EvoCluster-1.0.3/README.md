# EVO-Cluster: An Open-Source Nature-Inspired Optimization Clustering Framework in Python

**Description**:
EvoCluster is an open source and cross-platform framework implemented in Python which includes the most well-known and recent nature-inspired meta heuristic optimizers that are customized to perform partitional clustering tasks. The goal of this framework is to provide a user-friendly and customizable implementation of the metaheuristic based clustering algorithms which canbe utilized by experienced and non-experienced users for different applications.The framework can also be used by researchers who can benefit from the implementation of the metaheuristic optimizers for their research studies. EvoClustercan be extended by designing other optimizers, including more objective func-tions, adding other evaluation measures, and using more data sets. The current implementation of the framework includes ten metaheuristic optimizers, thirty datasets, five objective functions, twelve evaluation measures, more than twenty distance measures, and ten different ways for detecting the k value. The source code of EvoCluster is publicly available at (http://evo-ml.com/evocluster/).

**Features**:
- Ten nature-inspired metaheuristic optimizers are implemented (SSA, PSO, GA, BAT, FFA, GWO, WOA, MVO, MFO, and CS).
- Five objective functions (SSE, TWCV, SC, DB, and DI).
- Thirty datasets obtained from Scikit learn, UCI, School of Computing at University of Eastern Finland, ELKI, KEEL, and Naftali Harris Blog
- Twelve evaluation measures (SSE, Purity,	Entropy,	HS,	CS,	VM,	AMI,	ARI,	Fmeasure,	TWCV,	SC,	Accuracy,	DI,	DB,	and Standard Diviation)
- More than twenty distance measures
- Ten different ways for detecting the k value
)
- The implimentation uses the fast array manipulation using [`NumPy`] (http://www.numpy.org/).
- Matrix support using [`SciPy`'s] (https://www.scipy.org/) package.
- Simple and efficient tools for prediction using [`sklearn`] (https://scikit-learn.org/stable/)
- File data analysis and manipulation tool using [`pandas`] (https://pandas.pydata.org/)
- Plot interactive visualizations using [`matplotlib`] (https://matplotlib.org/)
- More optimizers, objective functions, adatasets, and evaluation measures are comming soon.

**Installation**:
- Python 3.xx is required.

Run

    pip install EvoCluster