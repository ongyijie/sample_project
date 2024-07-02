import pandas as pd

class VendingMachine:
    
    def __init__(self):
        self.menu = pd.read_csv('menu.csv') # assume this is the database
        self.notes = [50, 20, 10, 5, 1] # accepted notes


    def getMenu(self):
        return self.menu


    def calcChange(self, amount_paid, total_cost):
        change = amount_paid - total_cost # amount of change
        change_dict = {}
        for note in self.notes: 
            if change >= note: # loop through the accepted notes to check if the notes can be used to make up the remaining
                count = change // note # count number of notes
                change_dict[note] = int(count)
                change -= note * count # subtract amount from total
        return change_dict


    def operate(self):
        cart = pd.DataFrame(columns=['id', 'item', 'unit_price', 'qty', 'subtotal']) # user's cart
        
        while True:
            print(self.menu)  # display updated menu
            item_id = input('Enter item ID: ').upper()  
            if item_id in self.menu['id'].to_list():  # check if item is valid
                item_name = self.menu[self.menu['id'] == item_id]['item'].values[0]
                price = float(self.menu[self.menu['id'] == item_id]['unit_price'].values[0])
                stock = int(self.menu[self.menu['id'] == item_id]['stock'].values[0])
                while True:
                    qty = input('Enter quantity: ')  
                    if qty.isdigit():  # check if input is digit
                        if int(qty) <= stock:  # check inventory
                            self.menu.loc[self.menu['id'] == item_id, 'stock'] = stock - int(qty)
                            break
                        else:
                            print('Insufficient stock...')
                    else:
                        print('Please enter only digits [0-9]')
                
                subtotal = price * int(qty)
                cart.loc[len(cart.index)] = [item_id, item_name, price, int(qty), subtotal]  # add item to cart
                
                while True:
                    cont = input('[S] Continue shopping \n[P] Proceed to pay \n>> ').upper()
                    if cont in ['P','S']:
                        break
                    else:
                        print('Invalid input. Please enter S to continue shopping or P to proceed to pay.')
                if cont == 'P':
                    break  # Break out of the outer while loop to proceed to payment else continue shopping
            else:
                print('Invalid item!')
        
        agg1 = cart.groupby(by=['id', 'item', 'unit_price'], as_index=False).agg({'qty': 'sum', 'subtotal': 'sum'})  # summarize cart by grouping identical items
        agg1.loc['Grand Total'] = agg1[['qty', 'subtotal']].sum()
        agg1 = agg1.fillna('')
        print(agg1) # print summary
        
        total_amt = agg1.loc['Grand Total', 'subtotal'] # calculate total amount
        print(f'Amount Payable: RM {total_amt:.2f}')
        
        amount_paid = 0
        while amount_paid < total_amt:
            payment = input(f'Enter payment amount (paid: RM {amount_paid:.2f}): ') # make payment
            if payment.replace('.', '', 1).isdigit(): # check if input is digit
                payment = float(payment)
                amount_paid += payment # accumulate the value of notes inserted
                if amount_paid >= total_amt:
                    break
            else:
                print('Please enter a valid amount.')
        
        change = amount_paid - total_amt
        change_dict = self.calcChange(amount_paid, total_amt)
        
        # print change
        print(f'Total amount paid: RM {amount_paid:.2f}')
        print(f'Change: RM {change:.2f}')
        print('Note(s) returned:')
        for note, count in change_dict.items():
            print(f"RM {note}: {count} note{'s' if count > 1 else ''}")
        
        
if __name__ == "__main__":
    vm = VendingMachine()
    vm.operate()
