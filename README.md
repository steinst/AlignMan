AlignMan
==============

This is a tool for manual word alignment of parallel sentences.

Requirements
--------
- SpaCy
- tokenizer

Usage
--------
In order to do the word alignments a database, containing the sentences to align, has to be created. Then a graphical tool can be used to do the alignments, and finally the alignments can be exported from the database in various formats.

#### Create new database
```
python3 primeDB.py --input-file examples/sentences.txt
```


The input file should be a list of aligned sentences, separated by a tab. The sentences should ideally be tokenized.:
```
What can I order for you ?    Hvað get ég pantað handa ykkur ?

I 'll have one of those .    Ég þigg einn svoleiðis .

What are you worrying about ?    Hvaða áhyggjur eru þetta ?
```

An example file is included, `examples/sentences.txt`. 
	
It is also possible to use untokenized sentences by adding the flag `--tokenize`. Currently it only supports English and Icelandic. It assumes the first sentence is in English and uses SpaCy to tokenize it, and that the latter sentence is in Icelandic and uses tokenizer from Miðeind to tokenize that.

`--db-name dbname.db` changes the name of the output database from the default `alignments.db`.
	

#### Manual Word Alignment
```
python3 align.py
```

The tool can be run for one user by running the file without any parameters. By using the `--user` parameter a second user can be selected. The users then align the sentences separately and when both have finished a sentence the alignments are rated as `sure` or `possible`. All alignments that both evaluators set as 1-to-1 are tagged `sure`. Other alignments, the ones that only one evaluator creates or if one or both create 1-to-many, many-to-1 or many-to-many, they are tagged as `possible`.

How to use the tool:

... instructions...


#### Export manual alignments
```
python3 export_alignments.py --alignments
```

It is possible to export the alignments in two different formats by adding the parameter `--alignment-format`:

| 'classic' (default) | Alignments are exported as ... |
| 'pharaoh' | Alignments are exported as ... |

Examples of both export formats are available in the `examples` folder.

This script can also export the sentences that were aligned by using the `--sentences` flag. For other options, run `python3 export_alignments.py -h`.

License
-------

Copyright (C) 2021, Steinþór Steingrímsson

Licensed under the terms of the Apache License, version 2.0. A full copy of the license can be found in LICENSE.