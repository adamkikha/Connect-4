

# FOUR_IN_A_ROW = 1000
# BLANKS_ON_BOTH_SIDES = 3
# THREE = 250
# TWO = 100
# ONE = 40


from puzzle import Puzzle


class Agent:

    def __init__(self, alpha_beta : bool , k : int,puzzle : Puzzle):
        self.k = k
        self.alpha_beta = alpha_beta
        self.num_col = puzzle.num_col
        self.num_row = puzzle.num_row
        self.rows = puzzle.rows
        self.columns = puzzle.columns
        self.nw_digs = puzzle.nw_digs
        self.ne_digs = puzzle.ne_digs
        self.playable = puzzle.playable
                
    def minmax(self,state,k,max : bool):
        if k == 0:
            return self.heu(state)
        if max:
            pass
        else:
            pass
        
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