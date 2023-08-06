version = "0.4"
from bs4 import BeautifulSoup


def main():
    print("hello world this actually works???")
    soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
    print(soup.prettify())
