from twilio.rest import Client

class InvalidAccountError(Exception):
    def __init__(self, message="Invalid account operation"):
        self.message = message
        super().__init__(self.message)


class BankAccount:
    def __init__(self, account_number, balance, phone_number):
        self.account_number = account_number
        self.balance = balance
        self.phone_number = phone_number

        # Twilio credentials (replace with your actual credentials)
        self.account_sid = ''
        self.auth_token = ''
        self.twilio_number = '+'

        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, message):
        self.client.messages.create(
            body=message,
            from_=self.twilio_number,
            to=self.phone_number
        )

    def withdraw(self, amount):
        try:
            if amount > self.balance:
                raise InvalidAccountError("Insufficient funds for withdrawal")
            self.balance -= amount
            msg = f"Withdrawal of ₹{amount:.2f} successful. Available balance: ₹{self.balance:.2f}"
            self.send_sms(msg)
            return self.balance
        except InvalidAccountError as e:
            self.send_sms(str(e))


    def deposit(self, amount):
        try:
            if amount <= 0:
                raise InvalidAccountError("Deposit amount must be positive")
            self.balance += amount
            msg = f"Deposit of ₹{amount:.2f} successful. Available balance: ₹{self.balance:.2f}"
            self.send_sms(msg)
            return self.balance 
        except InvalidAccountError as e:
            self.send_sms(str(e))



# Sample usage
try:
    account = BankAccount("U0998XXXXXX97", 10000, "+919986093964") 


    try:
        withdraw_amount = float(input("Enter amount to withdraw (₹): "))
        account.withdraw(withdraw_amount)
    except InvalidAccountError as e:
        print(f"Custom exception caught: {e}")
    finally:
        print("Withdrawal attempt completed.")

    try:
        deposit_amount = float(input("Enter amount to deposit (₹): "))
        account.deposit(deposit_amount)
    except InvalidAccountError as e:
        print(f"Custom exception caught during deposit: {e}")
    finally:
        print("Deposit attempt completed.")    

except Exception as e:
    print(f"Unexpected error: {e}")
