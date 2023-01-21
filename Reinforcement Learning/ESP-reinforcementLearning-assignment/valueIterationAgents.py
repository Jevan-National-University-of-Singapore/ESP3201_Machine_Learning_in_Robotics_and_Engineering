# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util
import random as r
from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*
        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.
          
          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        
        "*** YOUR CODE HERE ***"
        x = self.mdp.getStates()

        # Value iterations
        for i in range(self.iterations):
            # Create temp value dictionary [for the "batch" version of value iteration--to preserve self.values
            # unaltered between iterations for the computeQValueFromValues() subroutine calls]
            space = util.Counter()
            # Traverse states ("batch" version iteration)
            for state in x:
                # Compute best actions for states where actions exist (states that are not terminal)
                if not self.mdp.isTerminal(state):
                    # Extract possible actions for the current state
                    poss = self.mdp.getPossibleActions(state)
                    # Iterate through actions and capture the q-value of the highest-scoring action
                    max_v = max(self.getQValue(state, a) for a in poss)
                    # Add this value to the state-value space
                    space[state] = max_v
            # Save the results of a complete value iteration after having finished traversing the states
            # I.e., "full backup" (per Sutton & Barto)
            self.values = space
            total_v = 0
            for s in self.mdp.getStates():
                total_v += abs(self.values[s])
                print(f"{(round(total_v,2))}")



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def getPolicy(self, state):
        """
          The policy is the best action in the given state
          according to the values computed by value iteration.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        a = dict()
        poss = self.mdp.getPossibleActions(state)
        for x in poss:
            a[x] = self.getQValue(state, x)

        max_v = max(a.values())
        lst = []
        for (x,y) in a.items():
            if y == max_v:
                lst.append(x)
        return r.choice(lst)
        

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)
    
    def getQValue(self, state, action):
        """
          The q-value of the state action pair
          (after the indicated number of value iteration
          passes).  Note that value iteration does not
          necessarily create this quantity and you may have
          to derive it on the fly.
        """
        "*** YOUR CODE HERE ***"
        q_v = 0.0
        for (x, prob) in self.mdp.getTransitionStatesAndProbs(state, action):
            v = self.values[x]
            gamma = self.discount
            r = self.mdp.getReward(state, action, x)
            q_v += prob * (r + v * gamma)

        return q_v
        
        

 

