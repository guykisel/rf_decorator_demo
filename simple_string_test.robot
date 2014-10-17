*** Settings ***
Library           SimpleStringPrinterLibrary

*** Test Cases ***
Can Print Part Of String Integers
    Print String    Hello World    ${1}    ${3}

Can Print Part Of String Integers As Strings
    Print String    Hello World    1    3
