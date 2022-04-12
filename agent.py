from puzzle import Puzzle

# AI agent class
class Agent:

    def __init__(self,puzzle : Puzzle):
        self.num_col = puzzle.num_col
        self.num_row = puzzle.num_row
        self.rows = puzzle.rows
        self.columns = puzzle.columns
        self.nw_digs = puzzle.nw_digs
        self.ne_digs = puzzle.ne_digs
        self.parent_map = dict()
        
    # min max with alpha beta pruning
    def prune_minmax(self,state : str,k : int,max : bool,playable,alpha = None,beta = None):
        # if max depth reached
        if k == 0:
            heu = self.heu(state)
            parent_key = str(len(self.parent_map.keys()))
            self.parent_map[parent_key] = (str(heu),[],max)  
            return None , heu , parent_key
        if alpha is None:
            alpha = -100
            beta = 100
            
        # keeps track of children
        children = []
        if max:
            index = max_move = -1
            value = max_value = -100
            player = "1"
            for index , p in self.get_moves(playable):
                # get new state from playable index
                move = self.transition(index,state,player)
                _ , value , parent_key = self.prune_minmax(move,k-1,not max , p,alpha,beta)
                # add the child's chosen value , the index , and it's key in the parent map
                children.append((str(value),str(index),str(parent_key)))
                
                if value > max_value:
                    max_value = value
                    max_move = index
                # to prune unnessary nodes
                if value >= beta:
                    break
                # updates alpha
                if value > alpha:
                    alpha = value
            # if index is not assigned
            if index == -1:
                max_value = self.heu(state)
                max_move = index
                
            # add the node to the parent map with it's children , chosen value and it's type
            parent_key = str(len(self.parent_map.keys()))
            self.parent_map[parent_key] = (str(max_value),children,max)
            return max_move , max_value , parent_key
        else:
            index = min_move = -1
            value = min_value = 100
            player = "2"
            for index , p in self.get_moves(playable):
                # get new state from playable index
                move = self.transition(index,state,player)
                _ , value , parent_key = self.prune_minmax(move,k-1,not max,p,alpha,beta)
                # add the child's chosen value , the index , and it's key in the parent map
                children.append((str(value),str(index),str(parent_key)))
                if value < min_value:
                    min_value = value
                    min_move = index
                # to prune unnessary nodes
                if value <= alpha:
                    break
                # updates beta
                if value < beta:
                    beta = value
            # if index is not assigned        
            if index == -1:
                min_value = self.heu(state)
                min_move = index
            # add the node to the parent map with it's children , chosen value and it's type
            parent_key = str(len(self.parent_map.keys()))
            self.parent_map[parent_key] = (str(min_value),children,max)        
            return min_move , min_value, parent_key
    # min max with alpha beta pruning
    def minmax(self,state : str,k : int,max : bool,playable):
        # if max depth reached
        if k == 0:
            heu = self.heu(state)
            parent_key = str(len(self.parent_map.keys()))
            self.parent_map[parent_key] = (str(heu),[],max)  
            return None , heu , parent_key
        
        # keeps track of children
        children = []
        if max:
            index = max_move = -1
            value = max_value = -100
            player = "1"
            for index , p in self.get_moves(playable):
                # get new state from playable index
                move = self.transition(index,state,player)
                _ , value , parent_key = self.minmax(move,k-1,not max , p)
                # add the child's chosen value , the index , and it's key in the parent map
                children.append((str(value),str(index),str(parent_key)))
                if value > max_value:
                    max_value = value
                    max_move = index
            # if index is not assigned
            if index == -1:
                max_value = self.heu(state)
                max_move = index
            parent_key = str(len(self.parent_map.keys()))
            self.parent_map[parent_key] = (str(max_value),children,max)       
            return max_move , max_value , parent_key
        else:
            index = min_move = -1
            value = min_value = 100
            player = "2"
            for index , p in self.get_moves(playable):
                # get new state from playable index
                move = self.transition(index,state,player)
                _ , value , parent_key = self.minmax(move,k-1,not max,p)
                # add the child's chosen value , the index , and it's key in the parent map
                children.append((str(value),str(index),str(parent_key)))
                if value < min_value:
                    min_value = value
                    min_move = index
            # if index is not assigned
            if index == -1:
                min_value = self.heu(state)
                min_move = index
            parent_key = str(len(self.parent_map.keys()))
            self.parent_map[parent_key] = (str(min_value),children,max)
            return min_move , min_value , parent_key
        
    # returns new string after playing in that index
    def transition(self,index,old_state,player):
        state = list(old_state)
        state[index] = player
        state = "".join(state)
        return state
    
    # returns available indecies to play in  
    def get_moves(self,playable):
        moves = []
        # explores middle row first as it's more promising
        if playable[3] < 42:
            # to keep track of available indicies in each state
            p = playable.copy()
            p[3] += 7
            moves.append((playable[3],p))
        i = 1
        
        # checks remaining columns from center to sides
        while i < 4:
            if playable[3+i] < 42:
                p = playable.copy()
                p[3+i] += 7
                moves.append((playable[3+i],p))
            if playable[3-i] < 42:
                p = playable.copy()
                p[3-i] += 7
                moves.append((playable[3-i],p))
            i += 1
        return moves    
    
    # evaluates a column , row or diagonal by returning number of connected fours
    # for a certian player (negative if player 2)          
    def eval_seq(self,state : str,seq : list,player : str):
        score = 0
        i = 0
        c = 0
        while i < len(seq):
            c = 0
            while i < len(seq) and state[seq[i]] != player:
                i += 1
            while i < len(seq) and state[seq[i]] == player:
                c += 1
                i += 1            
            if c > 3:
                score = c - 3
                break

        if player == "2":
            score *= -1
        return score
    
    # checks all rows using eval
    def west_check(self,state : str):
        score = 0
        for row in self.rows:
            if state[row[3]] != "0":
                player = state[row[3]]
                score += self.eval_seq(state,row,player)
            else:
                return score
        return score
    
    # checks all main diagonals using eval            
    def nw_check(self,state : str):
        score = 0
        for dig in self.nw_digs:
            if state[dig[2]] != "0":
                if state[dig[2]] == state[dig[3]]:    
                    player = state[dig[2]]
                    score += self.eval_seq(state,dig,player)
        return score
    
    # checks all columns using eval
    def north_check(self,state : str):
        score = 0
        for col in self.columns:
            if state[col[3]] != "0":
                if state[col[2]] == state[col[3]]:
                    player = state[col[3]]
                    score += self.eval_seq(state,col,player)
        return score
    
    # checks all sec. diagonals using eval
    def ne_check(self,state : str):
        score = 0
        for dig in self.ne_digs:
            if state[dig[2]] != "0":
                if state[dig[2]] == state[dig[3]]:    
                    player = state[dig[2]]
                    score += self.eval_seq(state,dig,player)
        return score
    
    # checks all the board for connected fours
    def heu(self,state) -> int:
        score = 0
        score += self.west_check(state)
        score += self.nw_check(state)
        score += self.north_check(state)
        score += self.ne_check(state)
        return score