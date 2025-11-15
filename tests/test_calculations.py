import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(150000)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected, f"Expected {expected}, got {add(num1, num2)}"

def test_subtract():
    print("testing subtract function")
    assert(subtract(7, 3) == 4)

def test_multiply():
    print("testing multiply function")
    assert(multiply(7, 3) == 21)

def test_divide():
    print("testing divide function")
    assert(divide(12, 3) == 4)

def test_set_bank_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    # bank_account = BankAccount(150000)
    bank_account.withdraw(150)
    assert bank_account.balance == 149850

def test_deposit(bank_account):
    # bank_account = BankAccount(150000)
    bank_account.deposit(150)
    assert bank_account.balance == 150150

def test_collect_interest(bank_account):
    # bank_account = BankAccount(150000)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 165000

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (3000, 2100, 900),
    (7500, 3500, 4000),
    (12000, 7200, 4800)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    # print("TESTING FOR INSUFFICIENT FUNNS")
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(300000)


#test_add()
test_subtract()
test_multiply()
test_divide()