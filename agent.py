

# FOUR_IN_A_ROW = 1000
# BLANKS_ON_BOTH_SIDES = 3
# THREE = 250
# TWO = 100
# ONE = 40


class Agent:

    def __init__(self, alpha_beta : bool , k : int,num_col : int,num_row : int):
        self.k = k
        self.alpha_beta = alpha_beta
        self.num_col = num_col
        self.num_row = num_row
        self.rows = []
        self.columns = []
        self.nw_digs = []
        self.ne_digs = []
        self.generate_checkable()

    def generate_checkable(self):
        row = []
        for r in range(self.num_row):
            for c in range(self.num_col):
                row.append(r*self.num_col+c)
            self.rows.append(row.copy())
            row.clear()

        column = []
        for c in range(self.num_col):
            for r in range(self.num_row):
                column.append(r*self.num_col+c)
            self.columns.append(column.copy())
            column.clear()

        nw = []
        c = 0
        for r in range(self.num_row-4,-1,-1):
            i = r*self.num_col+c
            while i < self.num_col*self.num_row:
                nw.append(i)
                i += self.num_col+1
            self.nw_digs.append(nw.copy())
            nw.clear()
            i = c*self.num_col+r
            while i < self.num_col*self.num_row and i != 0:
                nw.append(i)
                i += self.num_col+1
            
            if(nw):
                self.nw_digs.append(nw.copy())
                nw.clear()
        
        ne = []
        i = 3
        j = 0
        while j < 4:
            nw.append(i+j)
            ne.append(i-j)
            i += 7
            j += 1
        self.nw_digs.append(nw.copy())
        self.ne_digs.append(ne.copy())
        nw.clear()
        ne.clear()
        c = self.num_col - 1
        for r in range(self.num_row-4,-1,-1):
            i = r*self.num_col+c
            j = c
            while i < self.num_col*self.num_row and j > -1:
                ne.append(i)
                i += self.num_col-1
                j -= 1
            self.ne_digs.append(ne.copy())
            ne.clear()
            i = self.num_col - r - 1
            j = i
            while i < self.num_col*self.num_row and j > -1 and i != 6:
                ne.append(i)
                i += self.num_col-1
                j -= 1
            if (ne):
                self.ne_digs.append(ne.copy())
                ne.clear()
                
                
    def minmax(self,state,k,max : bool):
        if k == 0:
            return self.heu(state)
        if max:
            pass
        else:
            pass
        
    def eval_seq(self,state,seq : str,player : str):
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
            if state[dig[2]] != "0" and state[dig[3]] != "0":
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
            if state[dig[2]] != "0" and state[dig[3]] != "0":
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