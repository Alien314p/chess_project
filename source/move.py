from morabae import Square
class Move:
    def __init__(self,start,dest) -> None:
        self.start=start #type:Square
        self.dest=dest #type:Square
    
    def __eq__(self, other) -> bool:
        if self.start == other.start  and self.dest == other.dest:
            return True
        else:
            return False
    