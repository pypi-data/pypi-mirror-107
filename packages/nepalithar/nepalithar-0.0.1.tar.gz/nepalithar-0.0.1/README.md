# Nepali Thar

This is a simple Nepali Thar package. This package can be used to generate list of Nepali surnames and detect them.

## Features:
 - Split name based on surname.
 - Detects the position of Nepali Surname in a text.
 - Checks if the words is Nepali Surname or not.
 - Gives a list of Nepali Surname's.

## How to Import

    >>> import nepalithar
    
    >>> thar = nepalithar.Caste()

## Check Nepali Surname

    >> thar.is_true("Rajesh")

    False

    >>> thar.is_true("Hamal")

    True

## Get Random n number of Surname

    >> thar.get(3)

    ['Kutal', 'Shrestha', 'Rapacha']


## Get Position of Surname in a text

    >> thar.get_position("Rajesh Hamal Madhu Bhattarai")

    [1, 3]

## Detect Position along with surname

    >> thar.detect('Rajesh Hamal Madhu Bhattarai')

    [(1, 'Hamal'), (3, 'Bhattarai')]

## Split a group of name based on surname

    >> thar.split_name("Rajesh Hamal Madhu Bhattarai")
    ['Rajesh Hamal', 'Madhu Bhattarai']

## References:
 - Nepali Thar Dataset : https://github.com/amitness/thar

## Others:
 - Note: Package created during COVID-19 quarantine out-of-boredom.