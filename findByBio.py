from account import Account
import time


def find_accounts_with_key():
    for account in example_account.get_followers():
        account_biography = example_account.query_biography(account)
        time.sleep(1)
        if key_to_find in account_biography:
            accounts_with_key.append(account)


example_account = Account(input("Username: "), input("Password: "))
key_to_find = input("String are you searching: ")

accounts_with_key = []

find_accounts_with_key()

if not accounts_with_key:
    print("No account was found")
    example_account.close()
else:
    print('{} accounts have "{}" inside of there bio: {}'.format(len(accounts_with_key), key_to_find,
                                                                 accounts_with_key))
