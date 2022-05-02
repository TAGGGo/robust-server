Our server uses "try" "except" in Python to handle dangerous activities.

1. If parser cannot parse XML, the server will catch the exception and safely return, waiting for the next request.

2. If request XML has an unsupported root tag, the server will catch the exception and safely return, waiting for the next request.

3. If request tries to create an existed account, or the account has a negative balance, the server will catch the exception and continue running.

4. If request tries to assign shares to an account which doesn't exist, or the number of shares is negative, the server will catch the exception and continue running.

5. If request has an unsupported child tag, the server will catch the exception and continue running.

6. If user requests an order, which the symbol amount is zero, or buyer does not have enough balance, or seller does not have enough shares, the server will catch the exception and continue running.

7. If account id and transaction id don't match, the server will handle this and add "error" tag to return XML.

8. If order status is other than "open" "executed" "canceled", the server will catch the exception and continue running.

9. Buy order and sell order will not match if they belong to the same user.