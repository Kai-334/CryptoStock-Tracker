from project import(
    validate_ticker,
    add_stock,
    validate_crypto,
    add_crypto,
    sell_stock,
    sell_crypto,
    Portfolio
)

def test_validate_ticker():
    valid, name = validate_ticker("AAPL")
    assert valid == True
    assert name == "Apple Inc."

    invalid, _ = validate_ticker("AAAPL")
    assert invalid == False

def test_add_stock():
    portfolio = Portfolio("Test Portfolio")
    result = add_stock(portfolio, "AAPL", 5, 150, confirmation='y')

    assert "Added" in result
    assert portfolio.stocks["AAPL"]["shares"] == 5

def test_validate_crypto():
    valid, name = validate_crypto("BTC")
    assert valid == True
    assert  name == "Bitcoin"

    invalid, _ = validate_crypto("BBTCC")
    assert invalid == False

def test_add_crypto():
    portfolio = Portfolio("Test Portfolio")
    result = add_crypto(portfolio, "BTC", 1, 30000, confirmation='y')

    assert "Added" in result
    assert portfolio.crypto["BTC"]["amount"] == 1

def test_sell_stock():
    portfolio = Portfolio("Test Portfolio")
    add_stock(portfolio, "AAPL", 5, 150, confirmation='y')
    result =  sell_stock(portfolio, "AAPL", 3)

    assert "Sold" in result
    assert portfolio.stocks["AAPL"]["shares"] == 2

def test_sell_crypto():
    portfolio = Portfolio("Test Portfolio")
    add_crypto(portfolio, "BTC", 1, 30000, confirmation='y')
    result = sell_crypto(portfolio, "BTC", 0.5)

    assert "Sold" in result
    assert portfolio.crypto["BTC"]["amount"] == 0.5
