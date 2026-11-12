class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item['amount']
        return total

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        return True

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def transfer(self, amount, budget_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {budget_category.name}")
            budget_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def __str__(self):
        title = self.name.center(30, "*") + "\n"
        items = ""
        for item in self.ledger:
            desc = item['description'][:23]
            amount = f"{item['amount']:.2f}"
            items += f"{desc:<23}{amount:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    spent_amounts = []
    for category in categories:
        cat_total = 0
        for item in category.ledger:
            if item['amount'] < 0:
                cat_total += item['amount'] * -1
        spent_amounts.append(cat_total)
        
    total_spent = sum(spent_amounts)
    
    percentages = []
    if total_spent > 0:
        for amount in spent_amounts:
            percent = (amount / total_spent) * 100
            rounded_percent = (int(percent) // 10) * 10
            percentages.append(rounded_percent)
    else:
        percentages = [0 for _ in categories]
        
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}|"
        for percent in percentages:
            if percent >= i:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"
        
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"
    
    max_len = max(len(cat.name) for cat in categories)
    padded_names = [cat.name.ljust(max_len) for cat in categories]
    
    for i in range(max_len):
        chart += "     "
        for name in padded_names:
            chart += f"{name[i]}  "
        if i < max_len - 1:
            chart += "\n"
            
    return chart
