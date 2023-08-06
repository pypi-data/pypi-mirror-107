version = "0.5"
from bs4 import BeautifulSoup


def main():
    print("hello world this actually works???")
    print("beautiful script on progress..")
    soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
    print(soup.prettify())
