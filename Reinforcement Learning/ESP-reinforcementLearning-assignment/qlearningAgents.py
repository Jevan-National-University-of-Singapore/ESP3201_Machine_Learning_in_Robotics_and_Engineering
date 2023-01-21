# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent

import random,util,math
          
class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent
    
    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update
      
    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.gamma (discount rate)
    
    Functions you should use
      - self.getLegalActions(state) 
        which returns legal actions
        for a state
  """



  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)
    
    self.epsilon = args['epsilon']
    self.alpha = args['alpha']
    self.gamma = args['gamma']
    self.actionFn = args['actionFn']
    self.qTable = util.Counter()

    print(f"\nepsilon: {self.epsilon}")
    print(f"learning rate: {self.alpha}")
    print(f"gamma: {self.gamma}")



    "*** YOUR CODE HERE ***"

  
  def getQValue(self, state, action):
    """
      Returns Q(state,action)    
      Should return 0.0 if we never seen
      a state or (state,action) tuple 
    """
    "*** YOUR CODE HERE ***"

    return self.qTable[(state, action)]
    util.raiseNotDefined()
 
    
  def getValue(self, state):
    """
      Returns max_action Q(state,action)        
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    "*** YOUR CODE HERE ***"
    legalActions = self.getLegalActions(state)
    if legalActions:
      return self.getQValue(state, self.getPolicy(state))
    else:
      return 0.0
      
    util.raiseNotDefined()
    
  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    "*** YOUR CODE HERE ***"
    if self.getLegalActions(state):
      max_value = float("-inf")
      max_actions = []
      for legalAction in self.getLegalActions(state):
        if self.getQValue(state, legalAction) > max_value:
          max_actions = [legalAction]
          max_value = self.getQValue(state, legalAction)
        elif self.getQValue(state, legalAction) == max_value:
          max_actions.append(legalAction)
      return random.choice(max_actions)
    else:
      return None


    util.raiseNotDefined()

    
  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.
    
      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """  
    # Pick Action
    legalActions = self.getLegalActions(state)
    if legalActions:

      if util.flipCoin(self.epsilon):
        return random.choice(legalActions)
      
      return self.getPolicy(state)
    
    else:
      return None
    util.raiseNotDefined()

  
  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a 
      state = action => nextState and reward transition.
      You should do your Q-Value update here
      
      NOTE: You should never call this function,
      it will be called on your behalf
    """
    self.qTable[(state, action)] += self.alpha * (reward + self.gamma * self.getValue(nextState) - self.getQValue(state, action))
    return 1
    util.raiseNotDefined()

    