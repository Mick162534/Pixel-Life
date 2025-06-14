class BushNode:
    def __init__(self, x, y, amount=50, regrowth_time=400):
        self.x = x
        self.y = y
        self.amount = amount
        self.max_amount = amount
        self.regrowth_time = regrowth_time
        self.regrow_timer = 0
        self.is_depleted = False

    def harvest(self, amount_requested):
        if self.is_depleted:
            return 0
        taken = min(self.amount, amount_requested)
        self.amount -= taken
        if self.amount <= 0:
            self.is_depleted = True
            self.regrow_timer = self.regrowth_time
        return taken

    def tick(self):
        if self.is_depleted:
            self.regrow_timer -= 1
            if self.regrow_timer <= 0:
                self.amount = self.max_amount
                self.is_depleted = False
