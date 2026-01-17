"""
COMPREHENSIVE PYTHON TESTING DEMONSTRATION
This module demonstrates multiple testing concepts in Python including:
1. Testing fundamentals
2. unittest vs pytest frameworks
3. Writing unit tests
4. Parametrized tests  
5. Fixtures
6. Mocking with unittest.mock
7. Test coverage with coverage.py

The example simulates a simple banking system to illustrate these concepts.
"""

import sys
import os
import json
import datetime
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
from decimal import Decimal, ROUND_DOWN


# ============================================================================
# BUSINESS LOGIC: SIMPLE BANKING SYSTEM
# ============================================================================

class AccountError(Exception):
    """Custom exception for account-related errors"""
    pass


class InsufficientFundsError(AccountError):
    """Raised when trying to withdraw more than available balance"""
    pass


class Transaction:
    """Represents a financial transaction"""
    
    def __init__(self, amount: float, transaction_type: str, description: str = ""):
        self.amount = amount
        self.type = transaction_type  # 'deposit', 'withdrawal', 'transfer'
        self.description = description
        self.timestamp = datetime.datetime.now()
        self.id = hash(f"{self.timestamp}_{self.amount}_{self.type}")
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary for serialization"""
        return {
            'id': self.id,
            'amount': self.amount,
            'type': self.type,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }
    
    def __repr__(self):
        return f"Transaction({self.type}, ${self.amount:.2f})"


class Account(ABC):
    """Abstract base class for bank accounts"""
    
    def __init__(self, account_number: str, owner_name: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.owner_name = owner_name
        self._balance = Decimal(str(initial_balance)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        self.transactions: List[Transaction] = []
        self._add_transaction(initial_balance, 'deposit', 'Initial deposit')
    
    @abstractmethod
    def calculate_interest(self) -> float:
        """Calculate interest for the account (to be implemented by subclasses)"""
        pass
    
    def deposit(self, amount: float, description: str = "") -> Transaction:
        """Deposit money into the account"""
        if amount <= 0:
            raise AccountError("Deposit amount must be positive")
        
        amount_decimal = Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        self._balance += amount_decimal
        transaction = self._add_transaction(float(amount_decimal), 'deposit', description)
        return transaction
    
    def withdraw(self, amount: float, description: str = "") -> Transaction:
        """Withdraw money from the account"""
        if amount <= 0:
            raise AccountError("Withdrawal amount must be positive")
        
        amount_decimal = Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        if amount_decimal > self._balance:
            raise InsufficientFundsError(
                f"Insufficient funds: ${float(self._balance):.2f} available, "
                f"${float(amount_decimal):.2f} requested"
            )
        
        self._balance -= amount_decimal
        transaction = self._add_transaction(float(amount_decimal), 'withdrawal', description)
        return transaction
    
    def get_balance(self) -> float:
        """Get current account balance"""
        return float(self._balance)
    
    def get_transaction_history(self) -> List[Transaction]:
        """Get list of all transactions"""
        return self.transactions.copy()
    
    def _add_transaction(self, amount: float, transaction_type: str, description: str = "") -> Transaction:
        """Internal method to add a transaction to history"""
        transaction = Transaction(amount, transaction_type, description)
        self.transactions.append(transaction)
        return transaction
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.account_number}, {self.owner_name})"


class SavingsAccount(Account):
    """Savings account with interest calculation"""
    
    INTEREST_RATE = 0.02  # 2% annual interest
    
    def calculate_interest(self) -> float:
        """Calculate monthly interest"""
        monthly_rate = self.INTEREST_RATE / 12
        interest = float(self._balance) * monthly_rate
        return round(interest, 2)


class CheckingAccount(Account):
    """Checking account with overdraft protection"""
    
    OVERDRAFT_LIMIT = 500.00
    
    def calculate_interest(self) -> float:
        """Checking accounts typically don't earn interest"""
        return 0.0
    
    def withdraw(self, amount: float, description: str = "") -> Transaction:
        """Override withdraw to allow overdraft up to limit"""
        if amount <= 0:
            raise AccountError("Withdrawal amount must be positive")
        
        amount_decimal = Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        available_balance = self._balance + Decimal(str(self.OVERDRAFT_LIMIT))
        
        if amount_decimal > available_balance:
            raise InsufficientFundsError(
                f"Insufficient funds: ${float(self._balance):.2f} balance, "
                f"${self.OVERDRAFT_LIMIT:.2f} overdraft available, "
                f"${float(amount_decimal):.2f} requested"
            )
        
        self._balance -= amount_decimal
        transaction = self._add_transaction(float(amount_decimal), 'withdrawal', description)
        return transaction


class Bank:
    """Manages multiple accounts and provides banking operations"""
    
    def __init__(self, name: str):
        self.name = name
        self.accounts: Dict[str, Account] = {}
        self._next_account_number = 1000
    
    def create_account(self, account_type: str, owner_name: str, initial_balance: float = 0.0) -> Account:
        """Create a new account of specified type"""
        account_number = f"{self._next_account_number:08d}"
        self._next_account_number += 1
        
        if account_type.lower() == 'savings':
            account = SavingsAccount(account_number, owner_name, initial_balance)
        elif account_type.lower() == 'checking':
            account = CheckingAccount(account_number, owner_name, initial_balance)
        else:
            raise AccountError(f"Unknown account type: {account_type}")
        
        self.accounts[account_number] = account
        return account
    
    def transfer(self, from_account: str, to_account: str, amount: float) -> Dict[str, Transaction]:
        """Transfer money between accounts"""
        if from_account not in self.accounts:
            raise AccountError(f"Source account not found: {from_account}")
        if to_account not in self.accounts:
            raise AccountError(f"Destination account not found: {to_account}")
        if from_account == to_account:
            raise AccountError("Cannot transfer to the same account")
        
        # Withdraw from source account
        withdrawal = self.accounts[from_account].withdraw(amount, f"Transfer to {to_account}")
        
        # Deposit to destination account
        deposit = self.accounts[to_account].deposit(amount, f"Transfer from {from_account}")
        
        return {
            'withdrawal': withdrawal,
            'deposit': deposit
        }
    
    def get_total_deposits(self) -> float:
        """Calculate total deposits across all accounts"""
        return sum(account.get_balance() for account in self.accounts.values())
    
    def apply_interest_to_all(self) -> Dict[str, float]:
        """Apply interest to all savings accounts"""
        interest_applied = {}
        for account_number, account in self.accounts.items():
            if isinstance(account, SavingsAccount):
                interest = account.calculate_interest()
                if interest > 0:
                    account.deposit(interest, "Monthly interest")
                    interest_applied[account_number] = interest
        return interest_applied


# ============================================================================
# EXTERNAL SERVICES (TO DEMONSTRATE MOCKING)
# ============================================================================

class CurrencyConverter:
    """External service for currency conversion (will be mocked in tests)"""
    
    @staticmethod
    def convert(amount: float, from_currency: str, to_currency: str) -> float:
        """
        Simulates calling an external API for currency conversion.
        In real scenario, this would make an HTTP request.
        """
        # Simulate API delay
        import time
        time.sleep(0.1)
        
        # Simulate exchange rates
        rates = {
            ('USD', 'EUR'): 0.85,
            ('USD', 'GBP'): 0.73,
            ('EUR', 'USD'): 1.18,
            ('GBP', 'USD'): 1.37,
        }
        
        key = (from_currency.upper(), to_currency.upper())
        if key in rates:
            return amount * rates[key]
        
        raise ValueError(f"Unsupported currency conversion: {from_currency} to {to_currency}")


class NotificationService:
    """External notification service (will be mocked in tests)"""
    
    @staticmethod
    def send_email(recipient: str, subject: str, body: str) -> bool:
        """Simulates sending an email notification"""
        # Simulate network call
        import random
        success = random.random() > 0.1  # 90% success rate
        
        if success:
            print(f"Email sent to {recipient}: {subject}")
        else:
            print(f"Failed to send email to {recipient}")
        
        return success
    
    @staticmethod
    def send_sms(phone_number: str, message: str) -> bool:
        """Simulates sending an SMS notification"""
        # Simulate network call
        import random
        success = random.random() > 0.2  # 80% success rate
        
        if success:
            print(f"SMS sent to {phone_number}: {message}")
        else:
            print(f"Failed to send SMS to {phone_number}")
        
        return success


# ============================================================================
# UNIT TESTS USING UNITTEST FRAMEWORK
# ============================================================================

import unittest
from unittest.mock import Mock, MagicMock, patch, call, PropertyMock
from io import StringIO


class TestTransaction(unittest.TestCase):
    """Test cases for Transaction class using unittest framework"""
    
    def setUp(self):
        """
        setUp method runs before each test method.
        This is a unittest fixture that provides common test data.
        """
        self.transaction = Transaction(100.50, 'deposit', 'Test deposit')
    
    def tearDown(self):
        """
        tearDown method runs after each test method.
        Used for cleanup (if needed).
        """
        pass
    
    def test_transaction_creation(self):
        """Test that transaction is created with correct attributes"""
        # Assertions verify expected behavior
        self.assertEqual(self.transaction.amount, 100.50)
        self.assertEqual(self.transaction.type, 'deposit')
        self.assertEqual(self.transaction.description, 'Test deposit')
        self.assertIsInstance(self.transaction.timestamp, datetime.datetime)
    
    def test_transaction_to_dict(self):
        """Test serialization to dictionary"""
        transaction_dict = self.transaction.to_dict()
        
        # Check dictionary structure and values
        self.assertEqual(transaction_dict['amount'], 100.50)
        self.assertEqual(transaction_dict['type'], 'deposit')
        self.assertEqual(transaction_dict['description'], 'Test deposit')
        self.assertIn('timestamp', transaction_dict)
        self.assertIn('id', transaction_dict)
    
    def test_negative_amount_transaction(self):
        """Test that transaction can be created with negative amount (for withdrawals)"""
        transaction = Transaction(-50.25, 'withdrawal', 'ATM withdrawal')
        self.assertEqual(transaction.amount, -50.25)


class TestAccountBaseClass(unittest.TestCase):
    """Test the abstract Account base class"""
    
    def test_abstract_method(self):
        """Test that Account cannot be instantiated directly (abstract class)"""
        with self.assertRaises(TypeError):
            Account("12345", "John Doe", 100.0)


class TestSavingsAccount(unittest.TestCase):
    """Test cases for SavingsAccount class"""
    
    def setUp(self):
        """Set up test data for each test"""
        self.account = SavingsAccount("SAV001", "Alice", 1000.0)
    
    def test_initial_balance(self):
        """Test account is created with correct initial balance"""
        self.assertEqual(self.account.get_balance(), 1000.0)
    
    def test_deposit(self):
        """Test depositing money increases balance"""
        self.account.deposit(500.0, "Paycheck")
        self.assertEqual(self.account.get_balance(), 1500.0)
        
        # Check transaction was recorded
        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 2)  # Initial deposit + our deposit
        self.assertEqual(transactions[-1].type, 'deposit')
        self.assertEqual(transactions[-1].amount, 500.0)
    
    def test_invalid_deposit(self):
        """Test that invalid deposit amounts raise errors"""
        with self.assertRaises(AccountError):
            self.account.deposit(-100.0)
        
        with self.assertRaises(AccountError):
            self.account.deposit(0.0)
    
    def test_withdraw_sufficient_funds(self):
        """Test successful withdrawal"""
        transaction = self.account.withdraw(200.0, "Groceries")
        self.assertEqual(self.account.get_balance(), 800.0)
        self.assertEqual(transaction.amount, 200.0)
        self.assertEqual(transaction.type, 'withdrawal')
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawal with insufficient funds raises error"""
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(1500.0)
    
    def test_calculate_interest(self):
        """Test interest calculation"""
        # With $1000 at 2% annual rate, monthly interest = 1000 * (0.02/12) = $1.67
        interest = self.account.calculate_interest()
        self.assertAlmostEqual(interest, 1.67, places=2)
        
        # Test with different balance
        self.account.deposit(2000.0)
        interest = self.account.calculate_interest()
        self.assertAlmostEqual(interest, 5.00, places=2)  # 3000 * (0.02/12) = 5.00


class TestCheckingAccount(unittest.TestCase):
    """Test cases for CheckingAccount class with overdraft"""
    
    def setUp(self):
        self.account = CheckingAccount("CHK001", "Bob", 500.0)
    
    def test_overdraft_within_limit(self):
        """Test withdrawal within overdraft limit"""
        # Try to withdraw $900 when balance is $500 (overdraft limit is $500)
        self.account.withdraw(900.0)
        self.assertEqual(self.account.get_balance(), -400.0)
    
    def test_overdraft_exceeds_limit(self):
        """Test withdrawal exceeding overdraft limit raises error"""
        # Try to withdraw $1200 when balance is $500 (total available = $1000)
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(1200.0)
    
    def test_no_interest_on_checking(self):
        """Test that checking accounts don't earn interest"""
        self.assertEqual(self.account.calculate_interest(), 0.0)


class TestBank(unittest.TestCase):
    """Test cases for Bank class"""
    
    def setUp(self):
        self.bank = Bank("Test Bank")
        self.savings = self.bank.create_account('savings', 'Alice', 1000.0)
        self.checking = self.bank.create_account('checking', 'Bob', 500.0)
    
    def test_create_account(self):
        """Test account creation"""
        self.assertEqual(len(self.bank.accounts), 2)
        
        # Verify account numbers are sequential
        account_numbers = list(self.bank.accounts.keys())
        self.assertTrue(account_numbers[0] < account_numbers[1])
    
    def test_transfer_success(self):
        """Test successful transfer between accounts"""
        result = self.bank.transfer(
            self.savings.account_number,
            self.checking.account_number,
            300.0
        )
        
        # Check balances updated correctly
        self.assertEqual(self.savings.get_balance(), 700.0)
        self.assertEqual(self.checking.get_balance(), 800.0)
        
        # Check transaction records
        self.assertEqual(result['withdrawal'].amount, 300.0)
        self.assertEqual(result['deposit'].amount, 300.0)
    
    def test_transfer_insufficient_funds(self):
        """Test transfer with insufficient funds raises error"""
        with self.assertRaises(InsufficientFundsError):
            self.bank.transfer(
                self.checking.account_number,
                self.savings.account_number,
                1000.0  # More than checking balance
            )
    
    def test_get_total_deposits(self):
        """Test calculation of total deposits across all accounts"""
        total = self.bank.get_total_deposits()
        self.assertEqual(total, 1500.0)  # 1000 + 500
        
        # Add another account
        self.bank.create_account('savings', 'Charlie', 750.0)
        total = self.bank.get_total_deposits()
        self.assertEqual(total, 2250.0)  # 1000 + 500 + 750
    
    def test_apply_interest_to_all(self):
        """Test interest application to savings accounts only"""
        # Create more accounts
        another_savings = self.bank.create_account('savings', 'Diana', 2000.0)
        
        # Apply interest
        interest_applied = self.bank.apply_interest_to_all()
        
        # Should have applied interest to 2 savings accounts
        self.assertEqual(len(interest_applied), 2)
        
        # Check interest was calculated correctly
        # First savings: 1000 * (0.02/12) = 1.67
        # Second savings: 2000 * (0.02/12) = 3.33
        total_interest = sum(interest_applied.values())
        self.assertAlmostEqual(total_interest, 5.00, places=1)
        
        # Checking account should not have received interest
        self.assertAlmostEqual(self.checking.get_balance(), 500.0)


# ============================================================================
# PARAMETRIZED TESTS
# ============================================================================

class ParametrizedAccountTests(unittest.TestCase):
    """
    Demonstrates parameterized testing using unittest's subTest.
    This allows running the same test logic with different inputs.
    """
    
    # Test data for parameterized tests
    deposit_test_cases = [
        (100.0, 1100.0, "Small deposit"),
        (1000.0, 2000.0, "Large deposit"),
        (0.01, 1000.01, "Very small deposit"),
        (999.99, 1999.99, "Deposit with cents"),
    ]
    
    withdrawal_test_cases = [
        (100.0, 900.0, "Small withdrawal"),
        (500.0, 500.0, "Half balance withdrawal"),
        (999.99, 0.01, "Withdrawal leaving small balance"),
    ]
    
    def test_multiple_deposits(self):
        """Parameterized test for multiple deposit scenarios"""
        for deposit_amount, expected_balance, description in self.deposit_test_cases:
            with self.subTest(deposit_amount=deposit_amount, description=description):
                # Recreate account for each subtest to ensure isolation
                account = SavingsAccount("TEST001", "Test User", 1000.0)
                account.deposit(deposit_amount)
                self.assertAlmostEqual(account.get_balance(), expected_balance, places=2)
    
    def test_multiple_withdrawals(self):
        """Parameterized test for multiple withdrawal scenarios"""
        for withdrawal_amount, expected_balance, description in self.withdrawal_test_cases:
            with self.subTest(withdrawal_amount=withdrawal_amount, description=description):
                account = SavingsAccount("TEST002", "Test User", 1000.0)
                account.withdraw(withdrawal_amount)
                self.assertAlmostEqual(account.get_balance(), expected_balance, places=2)
    
    def test_invalid_withdrawals(self):
        """Test various invalid withdrawal amounts"""
        invalid_amounts = [-100.0, -0.01, 0.0, 1001.0, 1500.0]
        
        for amount in invalid_amounts:
            with self.subTest(invalid_amount=amount):
                account = SavingsAccount("TEST003", "Test User", 1000.0)
                
                if amount <= 0:
                    with self.assertRaises(AccountError):
                        account.withdraw(amount)
                else:  # amount > balance
                    with self.assertRaises(InsufficientFundsError):
                        account.withdraw(amount)


# ============================================================================
# MOCKING DEMONSTRATION WITH UNITTEST.MOCK
# ============================================================================

class TestBankWithMocks(unittest.TestCase):
    """Demonstrates various mocking techniques"""
    
    def setUp(self):
        self.bank = Bank("Mock Bank")
        self.account = self.bank.create_account('savings', 'Mock User', 1000.0)
    
    def test_mock_account_method(self):
        """Test using Mock to replace a method"""
        # Create a mock object
        mock_account = Mock(spec=Account)
        
        # Configure the mock's return value
        mock_account.get_balance.return_value = 500.0
        mock_account.account_number = "MOCK001"
        mock_account.owner_name = "Mock Owner"
        
        # Use the mock
        self.assertEqual(mock_account.get_balance(), 500.0)
        
        # Verify the method was called
        mock_account.get_balance.assert_called_once()
    
    def test_mock_with_side_effect(self):
        """Test mock with side effects"""
        mock_account = Mock()
        
        # Make get_balance return different values each time it's called
        mock_account.get_balance.side_effect = [100.0, 200.0, 300.0]
        
        self.assertEqual(mock_account.get_balance(), 100.0)
        self.assertEqual(mock_account.get_balance(), 200.0)
        self.assertEqual(mock_account.get_balance(), 300.0)
        
        # Next call would raise StopIteration, or we can set what happens next
        mock_account.get_balance.side_effect = ValueError("No more values")
        with self.assertRaises(ValueError):
            mock_account.get_balance()
    
    def test_patch_function(self):
        """Demonstrate patching a function with @patch decorator"""
        
        # Test that datetime.now() can be patched
        with patch('datetime.datetime') as mock_datetime:
            # Configure the mock
            fixed_time = datetime.datetime(2023, 1, 1, 12, 0, 0)
            mock_datetime.now.return_value = fixed_time
            
            # Create transaction - it will use our mocked datetime
            transaction = Transaction(100.0, 'deposit')
            self.assertEqual(transaction.timestamp, fixed_time)
    
    def test_patch_class_method(self):
        """Patch a method of a class"""
        
        # Temporarily replace calculate_interest method
        with patch.object(SavingsAccount, 'calculate_interest') as mock_interest:
            # Configure the mock
            mock_interest.return_value = 50.0  # Always return $50 interest
            
            # Create account and test
            account = SavingsAccount("PATCH001", "Test", 1000.0)
            interest = account.calculate_interest()
            
            # Should get our mocked value
            self.assertEqual(interest, 50.0)
            
            # Verify the mock was called
            mock_interest.assert_called_once()
    
    def test_patch_multiple_methods(self):
        """Patch multiple methods at once"""
        
        with patch.object(Account, 'deposit') as mock_deposit, \
             patch.object(Account, 'withdraw') as mock_withdraw:
            
            # Configure mocks
            mock_deposit.return_value = Transaction(100.0, 'deposit', 'Mocked')
            mock_withdraw.return_value = Transaction(50.0, 'withdrawal', 'Mocked')
            
            # Create a real account but with mocked methods
            account = SavingsAccount("MULTI001", "Test", 1000.0)
            
            # Calls will use our mocks
            deposit_result = account.deposit(100.0)
            withdraw_result = account.withdraw(50.0)
            
            # Verify mocks were called
            mock_deposit.assert_called_once_with(100.0, "")
            mock_withdraw.assert_called_once_with(50.0, "")
            
            # Verify we got mocked transactions
            self.assertEqual(deposit_result.amount, 100.0)
            self.assertEqual(withdraw_result.amount, 50.0)
    
    def test_mock_external_service(self):
        """Mock an external service to avoid actual API calls"""
        
        # Patch the CurrencyConverter.convert method
        with patch('__main__.CurrencyConverter.convert') as mock_convert:
            # Configure the mock
            mock_convert.return_value = 85.0  # 100 USD = 85 EUR
            
            # Call the method (won't actually make API call)
            result = CurrencyConverter.convert(100.0, 'USD', 'EUR')
            
            # Verify result and that mock was called correctly
            self.assertEqual(result, 85.0)
            mock_convert.assert_called_once_with(100.0, 'USD', 'EUR')
    
    def test_verify_notification_sent(self):
        """Verify that notifications are sent when account balance is low"""
        
        # Create a real account
        account = SavingsAccount("NOTIFY001", "Notification Test", 100.0)
        
        # Mock the notification service
        with patch('__main__.NotificationService.send_email') as mock_send_email:
            # Configure the mock
            mock_send_email.return_value = True
            
            # Simulate low balance scenario
            if account.get_balance() < 150.0:
                NotificationService.send_email(
                    "customer@example.com",
                    "Low Balance Alert",
                    f"Your account balance is ${account.get_balance():.2f}"
                )
            
            # Verify email was sent
            mock_send_email.assert_called_once()
            
            # Check call arguments
            args, kwargs = mock_send_email.call_args
            self.assertEqual(args[0], "customer@example.com")
            self.assertEqual(args[1], "Low Balance Alert")
            self.assertIn("Your account balance is $100.00", args[2])
    
    def test_mock_property(self):
        """Demonstrate mocking a property"""
        
        with patch.object(Account, 'account_number', new_callable=PropertyMock) as mock_prop:
            # Configure the property mock
            mock_prop.return_value = "MOCKED-ACCT-NUM"
            
            # Create account - account_number property will return our mocked value
            account = SavingsAccount("REAL001", "Test", 1000.0)
            
            # This will use our mocked property
            self.assertEqual(account.account_number, "MOCKED-ACCT-NUM")
            
            # The real account_number is still "REAL001", but our test sees the mocked value


# ============================================================================
# PYTEST STYLE TESTS (TO SHOW DIFFERENCES FROM UNITTEST)
# ============================================================================

# These tests would typically be in a separate file for pytest
# but we include them here to show the differences

"""
# pytest tests use plain functions and assert statements (no TestCase class)
# Install pytest first: pip install pytest

import pytest

# pytest fixtures (different from unittest fixtures)
@pytest.fixture
def savings_account():
    '''pytest fixture that provides a SavingsAccount instance'''
    return SavingsAccount("PYTEST001", "Pytest User", 1000.0)

@pytest.fixture
def bank_with_accounts():
    '''pytest fixture that provides a Bank with test accounts'''
    bank = Bank("Pytest Bank")
    bank.create_account('savings', 'Alice', 1000.0)
    bank.create_account('checking', 'Bob', 500.0)
    return bank

# pytest test function (notice no class needed)
def test_deposit_pytest(savings_account):
    '''pytest test using fixture'''
    savings_account.deposit(500.0)
    assert savings_account.get_balance() == 1500.0

# pytest parameterized test (different syntax from unittest)
@pytest.mark.parametrize("deposit,expected_balance", [
    (100.0, 1100.0),
    (1000.0, 2000.0),
    (0.01, 1000.01),
])
def test_multiple_deposits_pytest(savings_account, deposit, expected_balance):
    '''Parameterized test in pytest'''
    savings_account.deposit(deposit)
    assert savings_account.get_balance() == pytest.approx(expected_balance, 0.01)

# pytest test with exception checking
def test_insufficient_funds_pytest(savings_account):
    '''Test exception handling in pytest'''
    with pytest.raises(InsufficientFundsError):
        savings_account.withdraw(1500.0)

# pytest fixture with setup/teardown
@pytest.fixture
def temporary_account(tmpdir):
    '''Fixture with setup and teardown using pytest's tmpdir'''
    # Setup
    account = SavingsAccount("TEMP001", "Temp User", 1000.0)
    
    yield account  # This is what tests receive
    
    # Teardown (optional)
    # Could clean up files, database connections, etc.
    # tmpdir is a pytest fixture that provides temporary directory

# pytest.mark decorators for test organization
@pytest.mark.slow
def test_slow_operation():
    '''Marked as slow - can be run separately: pytest -m slow'''
    import time
    time.sleep(2)  # Simulate slow test
    assert True

@pytest.mark.integration
def test_integration():
    '''Marked as integration test'''
    assert True
"""


# ============================================================================
# TEST COVERAGE DEMONSTRATION
# ============================================================================

"""
# coverage.py is used to measure test coverage
# Install: pip install coverage

# Basic usage from command line:
# 1. Run tests with coverage: coverage run -m pytest test_banking.py
# 2. Generate report: coverage report -m
# 3. Generate HTML report: coverage html

# Programmatic usage (can be included in tests):
import coverage

cov = coverage.Coverage()
cov.start()

# Run your tests here
# unittest.main()

cov.stop()
cov.save()
cov.report()

# HTML report for detailed view
cov.html_report(directory='htmlcov')

# What coverage measures:
# - Statement coverage: Which statements were executed
# - Branch coverage: Which code branches were taken (if/else)
# - Function coverage: Which functions were called
# - Line coverage: Which lines were executed

# Aim for high coverage but 100% isn't always practical or necessary
# Focus on critical paths and complex logic
"""


# ============================================================================
# TEST SUITE RUNNER AND EXAMPLES
# ============================================================================

class TestExamples:
    """
    Examples of different test scenarios and patterns.
    Not a unittest class - just for demonstration.
    """
    
    @staticmethod
    def demonstrate_test_doubles():
        """Show different types of test doubles"""
        print("\n" + "="*60)
        print("DEMONSTRATING TEST DOUBLES")
        print("="*60)
        
        # 1. Dummy - object that's passed around but never used
        class DummyLogger:
            def debug(self, msg): pass
            def info(self, msg): pass
            def error(self, msg): pass
        
        dummy = DummyLogger()
        print("1. Dummy object created (implements interface but does nothing)")
        
        # 2. Fake - simplified working implementation
        class FakeDatabase:
            def __init__(self):
                self.data = {}
            
            def store(self, key, value):
                self.data[key] = value
            
            def retrieve(self, key):
                return self.data.get(key)
        
        fake_db = FakeDatabase()
        fake_db.store("test", "value")
        print(f"2. Fake database: stored and retrieved: {fake_db.retrieve('test')}")
        
        # 3. Stub - provides canned answers
        class StubExchangeRate:
            def get_rate(self, from_curr, to_curr):
                # Always returns same rate regardless of input
                return 1.5
        
        stub = StubExchangeRate()
        print(f"3. Stub exchange rate: USD to EUR = {stub.get_rate('USD', 'EUR')}")
        
        # 4. Spy - records interactions for verification
        class SpyEmailService:
            def __init__(self):
                self.sent_emails = []
            
            def send(self, to, subject, body):
                # Record the call
                self.sent_emails.append({
                    'to': to,
                    'subject': subject,
                    'body': body
                })
                # Could also call real service here
                return True
            
            def get_sent_count(self):
                return len(self.sent_emails)
        
        spy = SpyEmailService()
        spy.send("user@example.com", "Test", "Hello")
        print(f"4. Spy email service: sent {spy.get_sent_count()} email(s)")
        
        # 5. Mock - pre-programmed with expectations
        from unittest.mock import Mock
        mock_service = Mock()
        mock_service.process_payment.return_value = True
        mock_service.process_payment("order_123", 100.0)
        print("5. Mock service: process_payment called")
        mock_service.process_payment.assert_called_once_with("order_123", 100.0)
        
        print("\nTest doubles help isolate code under test from dependencies")
    
    @staticmethod
    def demonstrate_test_organization():
        """Show how to organize tests effectively"""
        print("\n" + "="*60)
        print("TEST ORGANIZATION PATTERNS")
        print("="*60)
        
        print("1. Arrange-Act-Assert (AAA) Pattern:")
        print("   Arrange: Set up test data and conditions")
        print("   Act: Execute the code being tested")  
        print("   Assert: Verify the results")
        print()
        
        print("2. Test Naming Conventions:")
        print("   test_[method]_[scenario]_[expected]")
        print("   Example: test_withdraw_insufficient_funds_raises_error")
        print()
        
        print("3. Test File Organization:")
        print("   tests/")
        print("   ├── unit/")
        print("   │   ├── test_accounts.py")
        print("   │   ├── test_bank.py")
        print("   │   └── test_transactions.py")
        print("   ├── integration/")
        print("   │   └── test_bank_integration.py")
        print("   ├── conftest.py (shared pytest fixtures)")
        print("   └── __init__.py")
        print()
        
        print("4. Test Categories:")
        print("   - Unit tests: Test individual components in isolation")
        print("   - Integration tests: Test interactions between components")
        print("   - System tests: Test entire system")
        print("   - Smoke tests: Basic functionality checks")
        print("   - Regression tests: Ensure bugs don't reoccur")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("PYTHON TESTING DEMONSTRATION")
    print("="*70)
    
    # Demonstrate test doubles
    TestExamples.demonstrate_test_doubles()
    
    # Demonstrate test organization
    TestExamples.demonstrate_test_organization()
    
    print("\n" + "="*70)
    print("RUNNING UNIT TESTS")
    print("="*70)
    
    # Run unittest tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    # Run tests with text test runner
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed")
    
    print("\n" + "="*70)
    print("HOW TO RUN TESTS WITH DIFFERENT TOOLS")
    print("="*70)
    print("\n1. Run with unittest (already did):")
    print("   python -m unittest test_banking.py")
    
    print("\n2. Run with pytest (install pytest first):")
    print("   pytest test_banking.py -v")
    
    print("\n3. Run with coverage (install coverage.py first):")
    print("   coverage run -m pytest test_banking.py")
    print("   coverage report -m")
    print("   coverage html  # Generates detailed HTML report")
    
    print("\n4. Run specific test class:")
    print("   pytest test_banking.py::TestSavingsAccount -v")
    
    print("\n5. Run tests matching pattern:")
    print("   pytest -k \"test_withdraw\" -v")
    
    print("\n6. Run with different verbosity:")
    print("   pytest -v  # Verbose")
    print("   pytest -q  # Quiet")
    print("   pytest -x  # Stop on first failure")
    
    print("\n" + "="*70)
    print("KEY TESTING PRINCIPLES")
    print("="*70)
    print("""
    1. Tests should be FAST
    2. Tests should be ISOLATED/INDEPENDENT
    3. Tests should be REPEATABLE
    4. Tests should be SELF-VALIDATING (pass/fail without manual check)
    5. Tests should be TIMELY (written before or with the code)
    
    Remember:
    - Test behaviors, not implementations
    - One assertion per test (when possible)
    - Use meaningful test names
    - Keep tests simple and readable
    - Don't test external libraries (they have their own tests)
    - Mock expensive or unreliable dependencies
    - Aim for high coverage of business logic
    """)