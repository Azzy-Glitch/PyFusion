
accounts={}
def create_acc():
    acc_num=input("Enter account number: ")
    if acc_num not in accounts:
       acc_deposit=float(input("Enter amount to deposit: "))
       accounts[acc_num]=acc_deposit
       print(f"Account number:  {acc_num} created with initial deposit {acc_deposit}")
    else:
        print("Account already exists")
def deposit_money():
    acc_num=input("Enter account number: ")
    if acc_num in accounts:
      amount=input("Enter amount to deposit: ")
      accounts[acc_num]+=amount
      print(f"Deposited {amount} in {accounts[acc_num]} successfully!!")
    else:
       print("Account doesnt exist")
def withdraw():
   acc_num=input("Enter account number: ")
   if acc_num in accounts:
      withdr=input("Enter amount to withdraw: ")
      if withdr<accounts[acc_num]:
         accounts[acc_num]-=withdraw
         print(f"Successfully withdrew {withdr} from {accounts[acc_num]}")
      else:
         print("Insufficient balance!!")
   else:
      print("Invalid account number")
def check_bal():
   acc_num=input("Enter account number: ")
   if acc_num in accounts:
     print(f"Balance for {acc_num}: {accounts[acc_num]}")
   else:
     print("Account doesnt exist")
def main():
 while True:
   print("\t\tMENU")
   print("\nPRESS 1 to CREATE ACCOUNT")
   print("\nPRESS 2 to DEPOSIT MONEY ACCOUNT")
   print("\nPRESS 3 to WITHDRAW MONEY FROM ACCOUNT")
   print("\nPRESS 4 to CHECK BALANCE IN ACCOUNT")
   print("\nPRESS 5 to EXIT MENU")
   choice=input("Enter your choice: ") 
   if choice == '1':
      create_acc()
    
   elif choice == '2':
     deposit_money()
    
   elif choice == '3':
     withdraw()
     
   elif choice == '4':
     check_bal()
    
   elif choice == '5':
     print("Exiting menu.Goodbye!!")
     break
   else:
    print("invalid choice!")
main()
    