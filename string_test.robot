*** Settings ***
Library           StringPrinterLibrary

*** Test Cases ***
Can Print Part Of String Integers
    Print String    Hello World    ${1}    ${3}

Can Print Part Of String Integers As Strings
    Print String    Hello World    1    3

Can Print Part Of String Integers Class
    Print String Cls    Hello World    ${1}    ${3}

Can Print Part Of String Integers As Strings Class
    Print String Cls    Hello World    1    3
