# SFF2FASTA
Python script to convert SFF to FASTA.

# LICENSE

MIT License

Copyright (c) 2021 shuko-tech

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[See LICENSE](LICENSE)

# DOWNLOADING THE TOOL
```
git clone --recursive https://github.com/shuko-tech/SFF2FASTA.git
cd ./SFF2FASTA
```

# BUILDING THE SUBMODULES
```
cd ./submodules/sff2fastq/ && make && cd ../../

cd ./submodules/fastq2fasta/ && g++ src/fastq2fasta.cpp -o fastq2fasta && cd ../../
```

# RUNNING THE TOOL
```
usage: python3 ssf2fasta.py [-h] -i INPUT_SFF [-o OUTPUT_FASTA] [-b BATCH_SIZE]

		SFF to FASTA Conversion Tool

		optional arguments:
		-h, --help            show this help message and exit
		-i INPUT_SFF, --input_sff INPUT_SFF
								Full path to input .sff file or directory containing .sff files. Required.
		-o OUTPUT_FASTA, --output_fasta OUTPUT_FASTA
								Directory to output .fasta file or files. Default: Same directory as input. Optional.
		-b BATCH_SIZE, --batch_size BATCH_SIZE
								Batch size. Default: No batching.
		-V VERBOSITY, --verbosity VERBOSITY
								Verbosity mode for output. [0, Log Only; 1, Log and Print to Console; 2, Print Only].
```

# KNOWN ISSUES

To stop the process, the user current must spam ```ctrl-c``` to stop every scheduled sub processing step. User must press ```ctrl-c``` twice as many times as there are files to process. 

It's recomended that you test the tool with one file first to confirm it works, before globing a significant number of files.

Processing takes a long time... so be patient.

----
----

# SFF2FASTQ SUBMODULE

Indraniel Das (indraniel@gmail.com or idas@wustl.edu) The Genome Institute at Washington University

This software was developed at The Genome Institute at Washington University, St. Louis, MO.

## DISCLAIMER

The ssf2fastq software is not owned by shuko-tech. 

See auhors project repository here: [https://github.com/indraniel/sff2fastq](https://github.com/indraniel/sff2fastq)

This software is provided "as is" without warranty of any kind.

----

# SFF2FASTQ SUBMODULE

## DISCLAIMER

The fastq2fasta software is not owned by shuko-tech. 

See auhors project repository here: [https://github.com/dantaki/fastq2fasta](https://github.com/dantaki/fastq2fasta)

This software is provided "as is" without warranty of any kind.

----
----

##### April 09, 2021
