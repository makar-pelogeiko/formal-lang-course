#!/bin/bash

actdrect="$1/../project/parser"

cd $actdrect
pwd
apt-get install default-jdk
wget https://www.antlr.org/download/antlr-4.9.2-complete.jar

export CLASSPATH=".:$actdrect/antlr-4.9.2-complete.jar:$CLASSPATH"
alias antlr4="java -jar $actdrect/antlr-4.9.2-complete.jar"

antlr4 -Dlanguage=Python3 grammarGQL.g4 -visitor -o dist
