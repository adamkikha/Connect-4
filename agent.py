

# FOUR_IN_A_ROW = 1000
# BLANKS_ON_BOTH_SIDES = 3
# THREE = 250
# TWO = 100
# ONE = 40


from puzzle import Puzzle


class Agent:

    def __init__(self,puzzle : Puzzle):
        self.num_col = puzzle.num_col
        self.num_row = puzzle.num_row
        self.rows = puzzle.rows
        self.columns = puzzle.columns
        self.nw_digs = puzzle.nw_digs
        self.ne_digs = puzzle.ne_digs
    
    def prune_minmax(self,state : str,k : int,max : bool,playable,alpha = None,beta = None):
        if k == 0:
            return None , self.heu(state)
        if alpha is None:
            alpha = -100
            beta = 100
        if max:
            index = max_move = -1
            value = max_value = -100
            player = "1"
            for index , p in self.get_moves(playable):
                move = self.transition(index,state,player)
                _ , value = self.prune_minmax(move,k-1,not max , p,alpha,beta)
                if value > max_value:
                    max_value = value
                    max_move = index
                
                if value >= beta:
                    break
                
                if value > alpha:
                    alpha = value
            if max_value == -100:
                return index , value
            return max_move , max_value
        else:
            index = min_move = -1
            value = min_value = 100
            player = "2"
            for index , p in self.get_moves(playable):
                move = self.transition(index,state,player)
                _ , value = self.prune_minmax(move,k-1,not max,p,alpha,beta)
                if value < min_value:
                    min_value = value
                    min_move = index
                
                if value <= alpha:
                    break
                
                if value < beta:
                    beta = value
            if min_value == 100:
                return index , value        
            return min_move , min_value
    
    def minmax(self,state : str,k : int,max : bool,playable):
        if k == 0:
            return None , self.heu(state)
        if max:
            max_move = -1
            max_value = -100
            player = "1"
            for index , p in self.get_moves(playable):
                move = self.transition(index,state,player)
                _ , value = self.minmax(move,k-1,not max , p)
                if value > max_value:
                    max_value = value
                    max_move = index
                    
            return max_move , max_value
        else:
            min_move = -1
            min_value = 100
            player = "2"
            for index , p in self.get_moves(playable):
                move = self.transition(index,state,player)
                _ , value = self.minmax(move,k-1,not max,p)
                if value < min_value:
                    min_value = value
                    min_move = index
                    
            return min_move , min_value
        
    def transition(self,index,old_state,player):
        state = list(old_state)
        state[index] = player
        state = "".join(state)
        return state
     
    def get_moves(self,playable):
        moves = []
        if playable[3] < 42:
            p = playable.copy()
            p[3] += 7
            moves.append((playable[3],p))
        i = 1
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
    
    def west_check(self,state : str):
        score = 0
        for row in self.rows:
            if state[row[3]] != "0":
                player = state[row[3]]
                score += self.eval_seq(state,row,player)
            else:
                return score
        return score
                
    def nw_check(self,state : str):
        score = 0
        for dig in self.nw_digs:
            if state[dig[2]] != "0":
                if state[dig[2]] == state[dig[3]]:    
                    player = state[dig[2]]
                    score += self.eval_seq(state,dig,player)
        return score
    
    def north_check(self,state : str):
        score = 0
        for col in self.columns:
            if state[col[3]] != "0":
                if state[col[2]] == state[col[3]]:
                    player = state[col[3]]
                    score += self.eval_seq(state,col,player)
        return score
    
    def ne_check(self,state : str):
        score = 0
        for dig in self.ne_digs:
            if state[dig[2]] != "0":
                if state[dig[2]] == state[dig[3]]:    
                    player = state[dig[2]]
                    score += self.eval_seq(state,dig,player)
        return score
    
    def heu(self,state) -> int:
        score = 0
        score += self.west_check(state)
        score += self.nw_check(state)
        score += self.north_check(state)
        score += self.ne_check(state)
        return score