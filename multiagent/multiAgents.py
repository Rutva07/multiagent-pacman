# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #return successorGameState.getScore()
        score = successorGameState.getScore()
    
        distance = 99999
        for food in newFood.asList():
            distance = min(manhattanDistance(newPos, food), distance)
        score += 10/ distance

        for ghostState, scaredTime in zip(newGhostStates, newScaredTimes):
            ghostDistance = manhattanDistance(newPos, ghostState.getPosition())
            if scaredTime > 0: 
                score += 5/ghostDistance
            else: 
                if ghostDistance < 2:  
                    score = score - 100  
                else:
                    score -= 1/ghostDistance 

        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #make easy internal funcn, consider depth
        def minimax(index, depth, state):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # max
            if index == 0:
                best = -9999999
                for action in state.getLegalActions(index):
                    successor = state.generateSuccessor(index, action)
                    score = minimax(1, depth, successor)  
                    best = max(best, score)
                return best
            # min
            else:
                nextAgent = index + 1 if index + 1 < state.getNumAgents() else 0
                nextDepth = depth + 1 if nextAgent == 0 else depth
                best = 9999999
                for action in state.getLegalActions(index):
                    successor = state.generateSuccessor(index, action)
                    score = minimax(nextAgent, nextDepth, successor)
                    best = min(best, score)
                return best

        bestAction = None
        bestScorePossbile = -9999999
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = minimax(1, 0, successor)
            if score > bestScorePossbile:
                bestScorePossbile = score
                bestAction = action
        return bestAction
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #same logic
        def alpha_beta_search(index, depth, state, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            #max
            if index == 0:
                bestScore = -9999999
                for action in state.getLegalActions(index):
                    successor = state.generateSuccessor(index, action)
                    score = alpha_beta_search(1, depth, successor, alpha, beta)
                    bestScore = max(bestScore, score)
                    alpha = max(alpha, bestScore)
                    if beta < alpha:
                        break 
                return bestScore
            #min
            else:
                nextAgent = index + 1 if index + 1 < state.getNumAgents() else 0
                nextDepth = depth + 1 if nextAgent == 0 else depth
                bestScore = 9999999
                for action in state.getLegalActions(index):
                    successor = state.generateSuccessor(index, action)
                    score = alpha_beta_search(nextAgent, nextDepth, successor, alpha, beta)
                    bestScore = min(bestScore, score)
                    beta = min(beta, bestScore)
                    if beta < alpha:
                        break  
                return bestScore

        bestAction = None
        bestScore = -9999999
        alpha = -9999999
        beta = 9999999
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = alpha_beta_search(1, 0, successor, alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            alpha = max(alpha, bestScore)
        return bestAction
    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(index, depth, state):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            #max
            if index == 0:
                bestScore = -9999999
                for action in state.getLegalActions(index):
                    successor = state.generateSuccessor(index, action)
                    score = expectimax(1, depth, successor)
                    bestScore = max(bestScore, score)
                return bestScore

            #average
            else:
                nextAgent = index + 1 if index + 1 < state.getNumAgents() else 0
                nextDepth = depth + 1 if nextAgent == 0 else depth
                scores = []
                for action in state.getLegalActions(index):
                    successor = state.generateSuccessor(index, action)
                    score = expectimax(nextAgent, nextDepth, successor)
                    scores.append(score)
                return sum(scores) / len(scores) 

        bestAction = None
        bestScore = -9999999
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = expectimax(1, 0, successor)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction
    

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    
    -So my idea was to consider factors such as food items, capsules, and obviously ghosts
    -First I gathered all items that I needed, like list of distances for food, capsules, ghost(one for active and one for sacred)
    -Main task was to assign scores depending upon above mentioned parameters
    -Well I tried, and first few trials leaded to pacman stopping at one place and it started moving only when ghost comes near it
    It was able to complete the game but less points
    -So I tried various values till I found the one that got me full points
    -Now, I was getting full points at this but I saw that my pacman freezed at very end and this like two times before ghost came near it and pacman finished eating remaining food
    -So I tried to give him penalty for food and capsules left and voila it worked perfectly
     
    """
    "*** YOUR CODE HERE ***"
    #got all items
    score = currentGameState.getScore()
    pacmanPos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    ghostDistances = []
    scaredGhostDistances = []

    #got everything required
    for ghost in ghostStates:
        ghostPos = ghost.getPosition()
        distance = manhattanDistance(pacmanPos, ghostPos)
        if ghost.scaredTimer > 0:
            scaredGhostDistances.append(distance)
        else:  
            ghostDistances.append(distance)
    foodDistances = [manhattanDistance(pacmanPos, foodPos) for foodPos in food.asList()]
    capsuleDistances = [manhattanDistance(pacmanPos, capsule) for capsule in capsules]

    #assignment of scores
    if foodDistances:
        score += 10 / min(foodDistances)  
    if capsuleDistances:
        score += 1 / min(capsuleDistances)  
    if ghostDistances:
        score -= 2 / (min(ghostDistances) +1) 
    if scaredGhostDistances:
        score += 10 / min(scaredGhostDistances)
    score -= 4*len(food.asList())
    score -= 20*len(capsules) 
    return score


# Abbreviation
better = betterEvaluationFunction
