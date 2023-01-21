# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util
import random
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
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    for run in range(iterations):
        newvalues = self.values
        possiblestates = self.mdp.getStates()
            
        for state in possiblestates:
            if not self.mdp.isTerminal(state):
                validactions = self.mdp.getPossibleActions(state) 
                qvaluelist = [self.getQValue(state,action) for action in validactions]
                newvalues[state] = max(qvaluelist) #update optimal value for that state
                
    self.values = newvalues    
    

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    totalreward = 0
    transitprob = self.mdp.getTransitionStatesAndProbs(state, action)
    for nextstate, prob in transitprob:
        statereward = self.mdp.getReward(state,action,nextstate)
        #value iteration: for each next state, update with P(s',r|s,a) * [r + gamma * v(s')]
        update = prob * (statereward + self.discount * self.values[nextstate])
        totalreward += update
    return totalreward 
    #eventually stops updating q values as the discount factor makes future rewards exponentially small

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
    
    #compare policy for all current actions
    policytable = util.Counter()
    validactions = self.mdp.getPossibleActions(state)
    
    for action in validactions:
        qvalue = self.getQValue(state, action)
        policytable[action] = qvalue
        
    values = [item[1] for item in policytable.items()]
    maxvalue = max(values)
    possible = []
    
    #random choice to settle possible tiebreakers
    for action in policytable:
        if policytable[action] == maxvalue:
            #return action #if random choice not req, then i 1, i 2 infinite loop
            possible.append(action)
    
#    print('same max value:',len(possible))
    
##    return action that gives max(P(s',r|s,a) * [r + gamma * v(s')]) for that given state
    return random.choice(possible)
        
    
  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)