import search
from collections import defaultdict, Counter
import itertools
import mdp

# (30 pts) Implement Expectimax for this particular scenario and test it on these two turns.
# Does the action returned by the function match your answer? Submit your code and output.

class createProblem(search.Problem):
    def __init__(self):
        search.Problem.__init__(self, initial="D1", goal=None)

    def actions(self, state):
        actList = []
        if(state == "D1"):
            actList = ["Respond", "Redirect"]
        elif(state == "C1"):
            actList = ["~Resolved", "Resolved"]
        elif(state == "D2"):
            actList = ["Respond", "Redirect"]
        elif(state == "C3"):
            actList = ["~Resolved", "Resolved"]
        elif(state == "C4"):
            actList = ["Frustrated", "~Frustrated"]
        elif(state == "C2"):
            actList = ["Frustrated", "~Frustrated"]
        return actList

    def result(self, state, action):
        if(state == "D1" and action == "Respond"):
            newState = "C1"
        elif (state == "D1" and action == "Redirect"):
            newState = "C2"
        elif(state == "C1" and action == "~Resolved"):
            newState = "D2"
        elif(state == "C1" and action == "Resolved"):
            newState = "U1"
        elif(state == "C2" and action == "Frustrated"):
            newState = "U2"
        elif(state == "C2" and action == "~Frustrated"):
            newState = "U3"
        elif(state == "D2" and action == "Respond"):
            newState = "C3"
        elif(state == "D2" and action == "Redirect"):
            newState = "C4"
        elif(state == "C3" and action == "~Resolved"):
            newState = "U4"
        elif(state == "C3" and action == "Resolved"):
            newState = "U5"
        elif(state == "C4" and action == "Frustrated"):
            newState = "U6"
        elif(state == "C4" and action == "~Frustrated"):
            newState = "U7"
        return newState

    def path_cost(self, c, state1, action, state2):
        if(state1 == "C1" and action == "~Resolved" and state2 == "D2"):
            c = .9
        elif(state1 == "C1" and action == "Resolved" and state2 == "U1"):
            c = .1
        elif(state1 == "C2" and action == "Frustrated" and state2 == "U2"):
            c = .30
        elif(state1 == "C2" and action == "~Frustrated" and state2 == "U3"):
            c = .7
        elif(state1 == "C3" and action == "~Resolved" and state2 == "U4"):
            c =.9
        elif(state1 == "C3" and action == "Resolved" and state2 == "U5"):
            c = .1
        elif(state1 == "C4" and action == "Frustrated" and state2 == "U6"):
            c = .3
        elif(state1 == "C4" and action == "~Frustrated" and state2 == "U7"):
            c = .7
        return c

    def value(self, state, iterations):
        k=iterations
        val = 0
        U1val = 100
        U2val = 5 * k
        U3val = -100 + 5 * k
        U4val = 0
        U5val = 100
        U6val = 5 * k
        U7val = -100 + 5 * k
        C3val = (.9 * U4val) + (.10 * U5val)
        C4val = (.3 * U6val) + (.7 * U7val)
        D2val = max(C3val, C4val)
        C1val = (.9 * D2val) + (.1 * U1val)
        C2val = (.3 * U2val) + (.7 * U3val)
        if(state == "C1"):
            val = C1val
        elif(state == "C2"):
            val = C2val
        elif(state == "D2"):
            val = D2val
        elif(state == "C3"):
            val = C3val
        elif(state == "C4"):
            val = C4val
        elif(state == "U2"):
            val = 5 * k
        elif(state == "U3"):
            val = -100 + 5 * k
        elif(state == "U4"):
            val = 0
        elif(state == "U5"):
            val = 100
        elif(state == "U6"):
            val = 5 * k
        elif(state == "U7"):
            val = -100 + 5 * k
        elif(state == "D1"):
            val = max(C1val, C2val)
        return val

def expectiMax(iterations):
    planningProb = createProblem()
    runExpectiMax(planningProb, iterations)

def runExpectiMax(problem, iterations):
    current = search.Node(problem.initial)
    while True:
        neighbors = current.expand(problem)
        if not neighbors:
            break
        maxNeighb = search.argmax_random_tie(neighbors,key=lambda node: problem.value(node.state, iterations))
        current = maxNeighb
        return str(maxNeighb.state) + "-" + str(problem.value(maxNeighb.state, iterations))
        # print(str(maxNeighb.state) + "-" + str(problem.value(maxNeighb.state, iterations)))
        #print(problem.value(maxNeighb.state, iterations))

class BayesNet(object):
    "Bayesian network: a graph of variables connected by parent links."

    def __init__(self):
        self.variables = []  # List of variables, in parent-first topological sort order
        self.lookup = {}  # Mapping of {variable_name: variable} pairs

    def add(self, name, parentnames, cpt):
        "Add a new Variable to the BayesNet. Parentnames must have been added previously."
        parents = [self.lookup[name] for name in parentnames]
        var = Variable(name, cpt, parents)
        self.variables.append(var)
        self.lookup[name] = var
        return self


class Variable(object):
    "A discrete random variable; conditional on zero or more parent Variables."

    def __init__(self, name, cpt, parents=()):
        "A variable has a name, list of parent variables, and a Conditional Probability Table."
        self.__name__ = name
        self.parents = parents
        self.cpt = CPTable(cpt, parents)
        self.domain = set(itertools.chain(*self.cpt.values()))  # All the outcomes in the CPT

    def __repr__(self): return self.__name__


class Factor(dict): "An {outcome: frequency} mapping."


class ProbDist(Factor):
    """A Probability Distribution is an {outcome: probability} mapping.
    The values are normalized to sum to 1.
    ProbDist(0.75) is an abbreviation for ProbDist({T: 0.75, F: 0.25})."""

    def __init__(self, mapping=(), **kwargs):
        if isinstance(mapping, float):
            mapping = {T: mapping, F: 1 - mapping}
        self.update(mapping, **kwargs)
        normalize(self)


class Evidence(dict):
    "A {variable: value} mapping, describing what we know for sure."


class CPTable(dict):
    "A mapping of {row: ProbDist, ...} where each row is a tuple of values of the parent variables."

    def __init__(self, mapping, parents=()):
        """Provides two shortcuts for writing a Conditional Probability Table.
        With no parents, CPTable(dist) means CPTable({(): dist}).
        With one parent, CPTable({val: dist,...}) means CPTable({(val,): dist,...})."""
        if len(parents) == 0 and not (isinstance(mapping, dict) and set(mapping.keys()) == {()}):
            mapping = {(): mapping}
        for (row, dist) in mapping.items():
            if len(parents) == 1 and not isinstance(row, tuple):
                row = (row,)
            self[row] = ProbDist(dist)


class Bool(int):
    "Just like `bool`, except values display as 'T' and 'F' instead of 'True' and 'False'"
    __str__ = __repr__ = lambda self: 'T' if self else 'F'


T = Bool(True)
F = Bool(False)


def P(var, evidence={}):
    "The probability distribution for P(variable | evidence), when all parent variables are known (in evidence)."
    row = tuple(evidence[parent] for parent in var.parents)
    return var.cpt[row]

def normalize(dist):
    "Normalize a {key: value} distribution so values sum to 1.0. Mutates dist and returns it."
    total = sum(dist.values())
    for key in dist:
        dist[key] = dist[key] / total
        assert 0 <= dist[key] <= 1, "Probabilities must be between 0 and 1."
    return dist

def globalize(mapping):
    "Given a {name: value} mapping, export all the names to the `globals()` namespace."
    globals().update(mapping)

def joint_distribution(net):
    "Given a Bayes net, create the joint distribution over all variables."
    return ProbDist({row: prod(P_xi_given_parents(var, row, net)
                               for var in net.variables)
                     for row in all_rows(net)})

def all_rows(net): return itertools.product(*[var.domain for var in net.variables])

def P_xi_given_parents(var, row, net):
    "The probability that var = xi, given the values in this row."
    dist = P(var, Evidence(zip(net.variables, row)))
    xi = row[net.variables.index(var)]
    return dist[xi]

def prod(numbers):
    "The product of numbers: prod([2, 3, 5]) == 30. Analogous to `sum([2, 3, 5]) == 10`."
    result = 1
    for x in numbers:
        result *= x
    return result

def enumeration_ask(X, evidence, net):
    "The probability distribution for query variable X in a belief net, given evidence."
    i    = net.variables.index(X) # The index of the query variable X in the row
    dist = defaultdict(float)     # The resulting probability distribution over X
    for (row, p) in joint_distribution(net).items():
        if matches_evidence(row, evidence, net):
            dist[row[i]] += p
    return ProbDist(dist)

def matches_evidence(row, evidence, net):
    "Does the tuple of values for this row agree with the evidence?"
    return all(evidence[v] == row[net.variables.index(v)]
               for v in evidence)

def computeBayesNet():
    T = True
    F = False
    bayes_net = (BayesNet()
        .add('Accurate', [], 0.90)
        .add('ProblemSize', [], 0.90)
        .add('ConversationLength', ['ProblemSize'], {T: ProbDist(short=0.40, medium=0.40, long=0.20),
                                                     F: ProbDist(short=0.20, medium=0.30, long=0.50)})
        .add('Resolved', ['Accurate', 'ConversationLength'], {(T, 'short'): 0.30, (F, 'short'): 0.20, (T, 'medium'): 0.50, (F, 'medium'): 0.30,
                                                              (T, 'long'): 0.70, (F, 'long'): 0.40})
        .add('Frustrated', ['ProblemSize', 'ConversationLength', 'Accurate'], {(T, 'short', T): 0.20, (T, 'short', F): 0.40, (T, 'medium', T): 0.30,
                                                                               (T, 'medium', F): 0.50, (T, 'long', T): 0.60, (T, 'long', F): 0.80,
                                                                               (F, 'short', T): 0.30, (F, 'short', F): 0.50, (F, 'medium', T): 0.60,
                                                                               (F, 'medium', F): 0.80, (F, 'long', T): 0.70, (F, 'long', F): 0.90}))
    globalize(bayes_net.lookup)
    solution = enumeration_ask(Resolved, {ConversationLength: 'long', ProblemSize: T, Accurate: T}, bayes_net)
    print("SOLUTION: " + "\n" + str(solution))
    print("\nDISTRIBUTION TABLE: " + "\n" + str(joint_distribution(bayes_net)))
    return solution, joint_distribution(bayes_net)


class createMDP(mdp.MDP):
    t = {
        "D1": {
            "Respond-Resolved": [(0.30, "U1")],
            "Respond-notResolved": [(0.70, "D2")],
            "Redirect-Frustrated": [(0.20, "U2")],
            "Redirect-notFrustrated": [(0.80, "U3")]
        },
        "D2": {
            "Respond-Resolved": [(0.30, "U5")],
            "Respond-notResolved": [(0.70, "U4")],
            "Redirect-Frustrated": [(0.20, "U6")],
            "Redirect-notFrustrated": [(0.80, "U7")]
        }
    }
    # elif conversationLength == 'medium':
    #     t = {
    #         "D1": {
    #             "Respond-Resolved": [(0.50, "U1")],
    #             "Respond-notResolved": [(0.50, "D2")],
    #             "Redirect-Frustrated": [(0.30, "U2")],
    #             "Redirect-notFrustrated": [(0.70, "U3")]
    #         },
    #         "D2": {
    #             "Respond-Resolved": [(0.50, "U5")],
    #             "Respond-notResolved": [(0.50, "U4")],
    #             "Redirect-Frustrated": [(0.30, "U6")],
    #             "Redirect-notFrustrated": [(0.70, "U7")]
    #         }
    #     }
    # elif conversationLength == 'long':
    #     t = {
    #         "D1": {
    #             "Respond-Resolved": [(0.70, "U1")],
    #             "Respond-notResolved": [(0.30, "D2")],
    #             "Redirect-Frustrated": [(0.60, "U2")],
    #             "Redirect-notFrustrated": [(0.40, "U3")]
    #         },
    #         "D2": {
    #             "Respond-Resolved": [(0.70, "U5")],
    #             "Respond-notResolved": [(0.30, "U4")],
    #             "Redirect-Frustrated": [(0.60, "U6")],
    #             "Redirect-notFrustrated": [(0.40, "U7")]
    #         }
    #     }

    init = "D1"

    terminals = ["U1", "U2", "U3", "U4", "U5", "U6", "U7"]

    rewards = {
        "U1": 5,
        "U2": -1,
        "U3": 5,
        "U4": -3,
        "U5": 5,
        "U6": -1,
        "U7": 5,
        "D2": 0,
        "D1": 0
    }

    def __init__(self, init, terminals, transition_matrix, reward = None, gamma=.9):
        # All possible actions.
        actlist = []
        for state in transition_matrix.keys():
            actlist.extend(transition_matrix[state])
        actlist = list(set(actlist))
        mdp.MDP.__init__(self, init, actlist, terminals, transition_matrix, reward, gamma=gamma)

    def T(self, state, action):
        if action is None:
            return [(0.0, state)]
        else:
            return self.t[state][action]

def mdpProblem(conversationLength):
    if conversationLength == 'short':
        t = {
            "D1": {
                "Respond-Resolved": [(0.30, "U1")],
                "Respond-notResolved": [(0.70, "D2")],
                "Redirect-Frustrated": [(0.20, "U2")],
                "Redirect-notFrustrated": [(0.80, "U3")]
            },
            "D2": {
                "Respond-Resolved": [(0.30, "U5")],
                "Respond-notResolved": [(0.70, "U4")],
                "Redirect-Frustrated": [(0.20, "U6")],
                "Redirect-notFrustrated": [(0.80, "U7")]
            }
        }
    elif conversationLength == 'medium':
        t = {
            "D1": {
                "Respond-Resolved": [(0.50, "U1")],
                "Respond-notResolved": [(0.50, "D2")],
                "Redirect-Frustrated": [(0.30, "U2")],
                "Redirect-notFrustrated": [(0.70, "U3")]
            },
            "D2": {
                "Respond-Resolved": [(0.50, "U5")],
                "Respond-notResolved": [(0.50, "U4")],
                "Redirect-Frustrated": [(0.30, "U6")],
                "Redirect-notFrustrated": [(0.70, "U7")]
            }
        }
    elif conversationLength == 'long':
        t = {
            "D1": {
                "Respond-Resolved": [(0.70, "U1")],
                "Respond-notResolved": [(0.30, "D2")],
                "Redirect-Frustrated": [(0.60, "U2")],
                "Redirect-notFrustrated": [(0.40, "U3")]
            },
            "D2": {
                "Respond-Resolved": [(0.70, "U5")],
                "Respond-notResolved": [(0.30, "U4")],
                "Redirect-Frustrated": [(0.60, "U6")],
                "Redirect-notFrustrated": [(0.40, "U7")]
            }
        }

    init = "D1"

    terminals = ["U1", "U2", "U3", "U4", "U5", "U6", "U7"]

    rewards = {
        "U1": 5,
        "U2": -1,
        "U3": 5,
        "U4": -3,
        "U5": 5,
        "U6": -1,
        "U7": 5,
        "D2": 0,
        "D1": 0
    }
    markov = createMDP(init, terminals, t, rewards, gamma=.9)
    solution = mdp.value_iteration(markov)
    print(solution)

def main():
    expectiMax(2)
    computeBayesNet()
    mdpProblem('medium')

if __name__ == "__main__":
    main()
