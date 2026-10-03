# MST 0441 interactive notebooks

Interactive notebooks for MST 0441 Consumers, Trade and Business Strategy at BI Norwegian Business School. They run in Google Colab: click a link, then run the first cell.

Each session has two pages.

- **Guided** asks one question at a time and draws the next piece of the figure only when the answer is right. A wrong answer gets a hint, never the answer. Use it before the solutions are posted.
- **Sandbox** shows every number and has live sliders. Use it to check your own solutions and to try changes the problem set held fixed. A sandbox is published after the solutions for that session are posted.

## Open a session

### Part one: Consumers

| Session | Topic | Guided | Sandbox |
| --- | --- | --- | --- |
| 2 | Budgets, preferences and the MRS | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s02_guided.ipynb) | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s02_sandbox.ipynb) |
| 3 | Demand, comparative statics and labour supply | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s03_guided.ipynb) | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s03_sandbox.ipynb) |
| 4 | Intertemporal choice | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s04_guided.ipynb) | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s04_sandbox.ipynb) |
| 5 | Assets and choice under uncertainty | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s05_guided.ipynb) | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s05_sandbox.ipynb) |
| 6 | General equilibrium and exchange | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s06_guided.ipynb) | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s06_sandbox.ipynb) |
| 7 | Market failure and externalities | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s07_guided.ipynb) | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s07_sandbox.ipynb) |

### Part two: Trade

| Session | Topic | Guided | Sandbox |
| --- | --- | --- | --- |
| 8 | Firms, tasks and technology (AI) | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s08_guided.ipynb) | [open](https://colab.research.google.com/github/JEBgit0/mst0441-colab/blob/main/notebooks/s08_sandbox.ipynb) |
| 9 | Comparative advantage: Ricardo | after 5 Oct | after solutions |
| 10 | Heckscher-Ohlin and factor prices | after 9 Oct | after solutions |
| 11 | Monopolistic competition, gravity and trade policy | after 16 Oct | after solutions |

### Part three: Strategy

| Session | Topic | Guided | Sandbox |
| --- | --- | --- | --- |
| 12 | Static games and Nash equilibrium | after 26 Oct | after solutions |
| 13 | Dynamic games and credibility | after 2 Nov | after solutions |
| 14 | Incomplete information and signaling | after 9 Nov | after solutions |
| 15 | Repeated games, collusion and competition policy | after 16 Nov | after solutions |

The dates are when the notes for that session unlock (06:00). The guided page follows after that, and the sandbox after the solutions are posted.

## How to use a notebook

1. Open a link above. You need a Google account.
2. Run the first code cell (Shift + Enter). It downloads the course code from this repository.
3. Run the cell under each part to start it. The parts can be done in any order.

Have pen and paper ready for the guided pages: the exam wants the derivation, so write each step down before you type it in.

## What is in this repository

| Folder | Contents |
| --- | --- |
| `notebooks/` | The pages students open: `sNN_guided.ipynb` and `sNN_sandbox.ipynb` for session NN. |
| `lab/` | The Python code behind the pages. |

Inside `lab/`:

| Files | Role |
| --- | --- |
| `guided.py` | The engine for the guided pages. It knows nothing about economics. |
| `guided_sNN.py` | The questions, hints and figures for session NN. |
| `answers_sNN.py` | Salted hashes of the answers for session NN. Generated, do not edit by hand. |
| `sandbox.py` | The base class for the sandbox labs. |
| `sandbox_sNN.py` | The labs for session NN. |
| `consumer_theory.py`, `uncertainty.py`, `equilibrium.py`, `externality.py`, `firms.py` | The economics: the maths behind sessions 2 to 4, 5, 6, 7 and 8. |

## About the answers

The guided pages do not store answers in plain text. Each answer is kept as a salted hash, and what a student types is hashed the same way and compared. This stops a glance at the code from giving the answer away. It is not security: the answers are small numbers, so they can be found by brute force. It only has to cost more than solving the problem.

## Run it on your own computer

You need Python (tested on 3.12) with `numpy`, `matplotlib`, `ipywidgets` and Jupyter.

```
git clone https://github.com/JEBgit0/mst0441-colab
pip install numpy matplotlib ipywidgets notebook
```

Open a notebook from the `notebooks/` folder. The first cell finds `lab/` by itself.

## Use

Students and staff of MST 0441 at BI Norwegian Business School are free to use, run and copy this material for the course. All other rights are reserved: there is no open licence, so ask before reusing or redistributing it elsewhere.
