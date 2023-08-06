# Species Recognition Model

Species detection package for Vetstoria

## Installation

Install the VetstoriaNER using the python package manager (pip)
    ```
    pip install VetstoriaNER
    ```

## How to work on with VetstoriaNER

1. Import to a script file

    ```
    from VetstoriaNER import EntityRecognizer
    ```

2. passing of parameters

    ```
    ner = EntityRecognizer('<model name or path>')
    recognizer = ner.recognizeSpecies('<phrase or the sentence>')
    ```   

#### Actual code will look like :
```
from VetstoriaNER import EntityRecognizer

ner = EntityRecognizer('recognize-model')
recognizer = ner.recognizeSpecies('i have a cat') 

print(recognizer)
```

## LICENSE

```
MIT License

Copyright (c) 2020 VetstoriaNER

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

