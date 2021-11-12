#!/bin/bash
# Runs scripts locally to produce static documentation files

./get_todos.sh ../pymotifcounter > source/todo_list.txt
rst_include include ../README_prime.rst ../README.rst
pandoc -s --from rst --to markdown -o ../README.md ../README.rst