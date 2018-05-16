RTLib Project
=============

Intro
-----

The RTLib code goal is to make the process as simple as possible. Run update.sh, point it at the inputs, and expect an additional PEP_new column at the end. There are still some parameters that you will need to tweak manually as the default settings have not been fully generalized yet.

# Installation

```
# clone the git repo
git clone https://github.com/blahoink/RTLib
# install with pip
cd RTLib
pip install ./
```

If there is an update in the codebase, then you can pull updates from the server with:

```
cd RTLib
git pull origin master
```

Then uninstall and reinstall the package

```
pip uninstall rtlib
pip install ./
```

# Known bugs:

- I/O issues when outputting to a Google File Stream folder. Output to a local folder instead, and then drag it into Google File Stream later

Files
-----

converter.py  - converts MQ files to intermediate format with only essential columns

align.py      - generates initial values and runs STAN alignment

update.py     - uses alignment data to update original PEP

update.py has calls to both align.py and converter.py, so if you want to run the full pipeline and not just a section of it, stick with using update.py.

Parameters
----------

View parameters anytime yourself by typing "update.py -h". Also look at "testing.sh" to see some examples of past runs.

```
usage: update.py input [input ...]
                 [-h] [-o OUTPUT] [-t {MQ,PD}] [-v] [--include-contaminants]
                 [--include-decoys]
                 [--filter-retention-length FILTER_RETENTION_LENGTH]
                 [--filter-pep FILTER_PEP] [--filter-num-exps FILTER_NUM_EXPS]
                 [-e EXCLUSION_LIST] [--remove-exps REMOVE_EXPS] [-m]
                 [--stan-file STAN_FILE] [--mu-min MU_MIN]
                 [--rt-distortion RT_DISTORTION] [--prior-iters PRIOR_ITERS]
                 [--stan-iters STAN_ITERS] [--stan-attempts STAN_ATTEMPTS]
                 [-f] [--save-params] [-p PARAMS_FOLDER] [-c]
                 [--combined-name COMBINED_NAME]
                 [--output-suffix OUTPUT_SUFFIX] [--add-diagnostic-cols]
```

[input]:           List of input files. In our case, evidence.txt files from MQ.

-o:              Output folder. Avoid putting this folder in Google File Stream directly.

-t:              Input file type. For our use, type in "-t MQ" for MaxQuant

-v:              Verbose option.

# Filters:

Filters exclude PSMs from the alignment process and _do not_ remove them from the file entirely. Filtered-out PSMs will still appear in the output files, but they are not guaranteed to have an updated PEP (PEP_new)

--include-contaminants:  |

--include-decoys:        |-- Don't set these to true please

--filter-retention-length: Filter out PSMs with a retention length greater than this value. Default: max(RT) / 60. For a 180-minute run, this filter is at 3 minutes.

--filter-pep:              Filter out PSMs with a PEP greater than this value. Default: 0.5.

--filter-num-exps:         Filter out PSMs that appear in less than this number of experiments (raw files) over the entire set. Default: 3

-e:                        Path to an exclusion list of UniProt IDs. PSMs belonging to any of these protein IDs will be excluded.

--remove-exps:             Regular expression to exclude any raw files. For example, to exclude SQC_61A and SQC61B from alignment, set this to "--remove-exps 61A\|61B".

# Alignment Parameters:

--stan-file:          Manually specify the STAN file to use for alignment. Leave this out to use the provided STAN file.

--mu-min:             Floor the canonical RTs at this value. Default: 1 minute.

--rt-distortion:      Distort the initial canonical RTs and observed RTs to guarantee that the initial values are a certain distance away from the optima. Default: 0 minutes. Increase this value if STAN is consistently failing out and is unable to reach an optima.

--prior-iters:        Number of iterations to run for the initial value generation. Default: 10

--stan-iters:         Maximum number of iterations for STAN. Default: 100,000. This should be plenty, only increase if STAN is consistently hitting its upper limit without converging normally.

--stan-attempts:      Number of times to run STAN if the first attempts fail out. This is sometimes useful when the STAN alignment is particularly susceptible to RNG. Default: 3 attempts.

-f:                   Generate diagnostic figures, which will be put in [output]/alignment_figures

--save-params:        Save alignment parameters to text files so that this alignment can be referenced later without re-running the entire thing.

# Update Parameters:

-p:               Folder containing the alignment parameters saved from a previous run using "--save-params". If the parameters exist, this skips the entire alignment step and only runs the update.

-c:               Combine separate input files into one output file. For example, if 4 separate evidence files were fed into the alignment, then they will be combined into one file for the output. Default behavior is to keep separate input files as separate output files.

--combined-name:  If using combined output file, this is the name of that file. Default: "ev_combined.txt"

--output-suffix:  If not using combined output files, this is the suffix that is appended to the input file name. For example, if input file was "evidence.txt", and suffix was "_c", then output file would be named "evidence_c.txt"

--add-diagnostic-cols: Append extra columns to output file. Default behavior is to only append the PEP_new column, and this option just adds a few more.


Example runs
============

```
./update.sh /gd/SingleCell_Data/FP17/evidence.txt --type MQ -e ~/git/RTLib/pd_exclude.txt -f -v --save-params -o ~/git/RTLib/Alignments/FP17_20180511_2
```

```
./update.sh /gd/Slavov_Lab/SingleCell_Data/SCOPE-QE-QC/SQC55_hiFDR/evidence.txt /gd/Slavov_Lab/SingleCell_Data/SCOPE-QE-QC/SQC57_hiFDR/evidence.txt /gd/Slavov_Lab/SingleCell_Data/SCOPE-QE-QC/SQC61_hiFDR/evidence.txt /gd/Slavov_Lab/SingleCell_Data/SCOPE-QE-QC/SQC65_hiFDR/evidence.txt -t MQ -e ~/git/RTLib/pd_exclude.txt -f -v --prior-iters 15 --filter-pep 0.5 --remove-exps 61A\|61B -o ~/git/RTLib/Alignments/NCE_20180514_1
```