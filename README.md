<div align="center">
<p><img src="https://i.imgur.com/mEmBXEB.png" alt="Logo" width="300"></p>
</div>

# BNXplainer

**As part of:** MSDT2526
**Built by:** Group 2.


## About the Project

While explanation methods are widely available for black-box models, explanation tools for Bayesian networks, which are interpretable white-box models, remain scarce. Our project's goal is to address this gap in XAI and make explanations more helpful for interpretation, using explanation methods and visualisation.

BNXplainer, lets users upload a Bayesian network, set evidence variables and select a target feature. From there, inference results are computed and visualised through an inference diagram and a prediction table. To support explainability, we implemented three explanation methods: Value of Information (VOI), Most Probable Explanation (MPE) and Scenario Analysis. The feedback function lets users rate and reflect on the explanations they receive, contributing to the ongoing improvement of BNXplainer.

We hope our efforts contribute to address this gap and improving how Bayesian network predictions are understood and interpreted.
![Web](https://i.imgur.com/9vDgD7V.png)


## Installation.

  
  

**To create your venv use:**

  

```

python -m venv venv

```

  

**To activate it use:**

  

Linux/Mac:

```

source venv/bin/activate

```

  

Windows:

```

venv\Scripts\activate

```

OR

```

venv\Scripts\Activate.ps1

```

  

**To install the correct packages use:**

```

pip install -r requirements.txt

```

  

**To start the app use:**

```

python src/app.py

```

It should open on `http://127.0.0.1:8050/`

  

**To leave your environment use:**

```

deactivate

```

  

Further reference: https://docs.python.org/3/library/venv.html

  
# About us

We are a team of nine Radboud University students taking the course Modern Software Development Techniques, organised by the Artificial Intelligence Department (Donders Institute), under the coordination of Dr. Bryan Souza. Our client Dr. Marcos Buenos, Assistant Professor at Radboud University, commissioned this project on explainable AI (XAI) for white-box models: implementation and visualisation.

## Contributing

  

Please consult it for further reference.

  

Make sure to read **CONTRIBUTING.md** when working in git.

  

## Architecture

  

Architecture partly adapted from: https://community.plotly.com/t/structuring-a-large-dash-application-best-practices-to-follow/62739