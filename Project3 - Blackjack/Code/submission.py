import util
import math
import random
from collections import defaultdict
from util import ValueIteration

############################################################
# Problem 2a

# If you decide 2a is true, prove it in blackjack.pdf and put "return None" for
# the code blocks below.  If you decide that 2a is false, construct a
# counterexample.


class CounterexampleMDP(util.MDP):

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if
        # you deviate from this)
        return 0
        # END_YOUR_CODE

    # Return set of actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if
        # you deviate from this)
        if state == 0:
            return [-1, 1]
        else:
            return [state]
        # END_YOUR_CODE

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if
        # you deviate from this)
        if state == 0:
            return [(-1, 0.9, 0), (1, 0.1, 10)]
        else:
            return [(state, 1, 0)]
        # END_YOUR_CODE

    def discount(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if
        # you deviate from this)
        return 1
        # END_YOUR_CODE

############################################################
# Problem 3a


class BlackjackMDP(util.MDP):

    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.
    # The second element is the index (not the value) of the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.
    # The final element is the current deck.
    def startState(self):
        # total, next card (if any), multiplicity for each card
        return (0, None, (self.multiplicity,) * len(self.cardValues))

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None.
    # When the probability is 0 for a particular transition, don't include that
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if
        # you deviate from this)
        if state[2] == None or sum(state[2]) == 0:
            return []

        valueInHand, peekedIndex = state[0], state[1]
        deckCardCounts, totalCardNum = state[2], sum(state[2])
        possibleStates = []

        if action == 'Quit':
            return [((valueInHand, None, None), 1, valueInHand)]

        elif action == 'Peek':
            # The player peeked twice.
            if peekedIndex:
                return []

            for index, item in enumerate(deckCardCounts):
                if item:
                    peeked = index
                    peekPr = float(item) / totalCardNum
                    temp_state = (
                        (valueInHand, peeked, deckCardCounts), peekPr, -self.peekCost)
                    possibleStates.append(temp_state)
            return possibleStates

        elif action == 'Take':
            if not peekedIndex:
                for index, item in enumerate(deckCardCounts):
                    if item:
                        takePr = float(item) / totalCardNum
                        valueInHand_update = valueInHand + \
                            self.cardValues[index]
                        if valueInHand_update > self.threshold:
                            temp_state = (
                                (valueInHand_update, None, None), takePr, 0)
                            possibleStates.append(temp_state)
                        else:
                            deckCardCounts_update = [i for i in deckCardCounts]
                            for i, item_tmp in enumerate(deckCardCounts):
                                if i == index:
                                    deckCardCounts_update[i] = item_tmp - 1
                                else:
                                    deckCardCounts_update[i] = item_tmp
                            deckCardCounts_update = tuple(
                                deckCardCounts_update)

                            if sum(deckCardCounts_update):
                                temp_state = (
                                    (valueInHand_update, None, deckCardCounts_update), takePr, 0)
                            else:
                                temp_state = (
                                    (valueInHand_update, None, None), takePr, valueInHand_update)
                            possibleStates.append(temp_state)
                return possibleStates

            else:
                valueInHand_update = valueInHand + self.cardValues[peekedIndex]
                if valueInHand_update > self.threshold:
                    return [((valueInHand_update, None, None), 1, 0)]
                else:
                    deckCardCounts_update = [i for i in deckCardCounts]
                    for index, item in enumerate(deckCardCounts):
                        if index == peekedIndex:
                            deckCardCounts_update[index] = item - 1
                        else:
                            deckCardCounts_update[index] = item
                    deckCardCounts_update = tuple(deckCardCounts_update)

                    return [((valueInHand_update, None, deckCardCounts_update), 1, 0)]
        else:
            return []
        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 3b


def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the optimal action at
    least 10% of the time.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you
    # deviate from this)
    myBlackjack = BlackjackMDP(
        cardValues=[5, 7, 9, 50], multiplicity=1, threshold=20, peekCost=1)
    return myBlackjack
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action


class QLearningAlgorithm(util.RLAlgorithm):

    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        # terminal state
        if newState == None:
            return
        Q_max = max(self.getQ(newState, nextAction)
                    for nextAction in self.actions(newState))
        Q_target = reward + self.discount * Q_max
        scale = self.getStepSize() * (Q_target - self.getQ(state, action))

        for f, v in self.featureExtractor(state, action):
            self.weights[f] += scale * v
        # END_YOUR_CODE

# Return a singleton list containing indicator feature for the (state, action)
# pair.  Provides no generalization.


def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning
# Small test case
smallMDP = BlackjackMDP(
    cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)
largeMDP = BlackjackMDP(
    cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)

smallMDP.computeStates()
largeMDP.computeStates()

def problem_4b():
    print("\nProblem 4b")
    print("\n********smallMDP********")
    rl_small = QLearningAlgorithm(smallMDP.actions, smallMDP.discount(),
                                  identityFeatureExtractor, 0.2)
    util.simulate(smallMDP, rl_small, 30000, 200, False)
    rl_small.explorationProb = 0
    # ValueIteration
    vi = ValueIteration()
    vi.solve(smallMDP)
    # Compare these two algorithms
    total_actions = 0
    same_actions = 0
    for state, action in vi.pi.iteritems():
        same_actions += (rl_small.getAction(state) == action)
        total_actions += 1
    print("Total Actions: %d\n"
          "Different Actions: %d(%.3f)" % (total_actions,  total_actions - same_actions,
                                         (total_actions - same_actions) * 1.0 / total_actions))


    # Large test case

    print("\n********LargeMDP********")
    rl_large = QLearningAlgorithm(largeMDP.actions, largeMDP.discount(),
                                  identityFeatureExtractor, 0.2)
    util.simulate(largeMDP, rl_large, 30000, 300, False)
    rl_large.explorationProb = 0
    # ValueIteration
    vi2 = ValueIteration()
    vi2.solve(largeMDP)
    # Compare these two algorithm
    total_actions = 0
    same_actions = 0
    for state, action in vi2.pi.iteritems():
        same_actions += (rl_large.getAction(state) == action)
        total_actions += 1
    print("Total Actions: %d\n"
          "Different Actions: %d(%.3f)" % (total_actions, total_actions - same_actions,
                                         (total_actions - same_actions) * 1.0 / total_actions))


############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs (see
# identityFeatureExtractor()).
# Implement the following features:
# - indicator on the total and the action (1 feature).
# - indicator on the presence/absence of each card and the action (1 feature).
#       Example: if the deck is (3, 4, 0 , 2), then your indicator on the presence of each card is (1,1,0,1)
#       Only add this feature if the deck != None
# - indicator on the number of cards for each card type and the action (len(counts) features).  Only add these features if the deck != None
def blackjackFeatureExtractor(state, action):
    # BEGIN_YOUR_CODE (our solution is 9 lines of code, but don't worry if you
    # deviate from this)
    valueInHand, peekedIndex, deckCardCounts = state
    results = []
    results.append(((valueInHand, action), 1))
    if deckCardCounts:
        results.append(((tuple([1 if x else 0 for x in deckCardCounts]), action), 1))
        for index, item in enumerate(deckCardCounts):
            results.append(((index, item, action), 1))
    return results
    # END_YOUR_CODE

############################################################
# Problem 4d: What happens when the MDP changes underneath you?!

# Original mdp
originalMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)

# New threshold
newThresholdMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)

def problem_4d():
    if not hasattr(originalMDP, 'states'):
        originalMDP.computeStates()
    if not hasattr(newThresholdMDP, 'states'):
        newThresholdMDP.computeStates()

    VI = ValueIteration()
    VI.solve(originalMDP, 0.001)
    fixedVI = util.FixedRLAlgorithm(VI.pi)
    VIReward = util.simulate(newThresholdMDP, fixedVI, numTrials=30000)

    QL = QLearningAlgorithm(originalMDP.actions, originalMDP.discount(), blackjackFeatureExtractor, 0.2)
    QLReward = util.simulate(newThresholdMDP, QL, numTrials=30000)

    VI_reward = float(sum(VIReward))/len(VIReward)
    QL_reward = float(sum(QLReward))/len(QLReward)
    print ("\nProblem 4d")
    print ("Value Iteration reward",VI_reward)
    print ("Q-Learning reward",QL_reward)

if __name__ == '__main__':
    problem_4b()
    problem_4d()