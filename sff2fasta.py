"""
	SFF2FASTA Converter

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

"""

# Standard Library Imports
import os
import sys
import glob
import json
import signal
import shutil
import tempfile
import argparse
import datetime
import subprocess

# Shared Constants
STATUS_SUCCESS = 0
STATUS_FAILURE = 1

SFF_EXTENTION = '*.sff'
FASTQ_EXTENTION = '*.fastq'
FASTA_EXTENTION = '*.fasta'

SFF2FASTQ_EXE_PATH = "./submodules/sff2fastq/sff2fastq"
FASTQ2FASTA_EXE_PATH = "./submodules/fastq2fasta/fastq2fasta"
TEMP_DIR = "./temp/"
LOG_DIR = "./logs/"

# Shared Variables
PROCESS_LOG_FILE = None
FAILED_FILES_LOG = None

# Processes
SFF2FASTQ_PROC = None
FASTQ2FASTA_PROC = None

#------------------------------------------------------------------------------
def exit_routine(v:int=1):
	'''
		SFF to FASTA Conversion Tool: Exit Routine Handler
	'''
	global SFF2FASTQ_PROC
	global FASTQ2FASTA_PROC
	global PROCESS_LOG_FILE
	global FAILED_FILES_LOG
	global TEMP_DIR

	print_logger(f"Exit Routine Initiated...", log_file=PROCESS_LOG_FILE, verbosity=v)

	if not SFF2FASTQ_PROC is None:
		print_logger(f"Killing Subprocess: SFF2FASTQ", log_file=PROCESS_LOG_FILE, verbosity=v)
		SFF2FASTQ_PROC.kill()
		
	if not FASTQ2FASTA_PROC is None:
		print_logger(f"Killing Subprocess: FASTQ2FASTA", log_file=PROCESS_LOG_FILE, verbosity=v) 
		FASTQ2FASTA_PROC.kill()

	print_logger(f"Removing Temporary Directory", log_file=PROCESS_LOG_FILE, verbosity=v)
	shutil.rmtree(TEMP_DIR)

	print_logger(f"Exit Routine Finished.", log_file=PROCESS_LOG_FILE, verbosity=v)

	PROCESS_LOG_FILE.close()
	FAILED_FILES_LOG.close()
		
	sys.exit(0)

#------------------------------------------------------------------------------
def sigterm_handler(sig, frame):
	'''
		SFF to FASTA Conversion Tool: SIGTERM Handler
	'''
	print(f"SIGINT Recieved: Stoping Processes!")
	
	exit_routine()

#------------------------------------------------------------------------------
def print_logger(mesg:str, log_file=LOG_DIR, verbosity:int=0):
	'''
		SFF to FASTA Conversion Tool: Print-Logger
		mode: [0, Log Only; 1, Log and Print to Console; 2, Print Only]
	'''
	global PROCESS_LOG_FILE
	global FAILED_FILES_LOG

	if verbosity == 0 or verbosity == 1:
		# If verbosity level is set to 0 or 1 Log Output Message
		log_file.write(f"{mesg}\n")
	if verbosity == 1 or verbosity == 2:
		# If verbosity level is set to 1 or 2 Print Output Message
		print(f"{mesg}")
	else:
		# If verbosity level is not 0, 1, or 3 Only Log Output Message
		#	also handeled by argument parser
		log_file.write(f"{mesg}\n")

#------------------------------------------------------------------------------
def sff2fastq(sff_path:str, fastq_path:str, args):
	'''
		SFF to FASTA Conversion Tool: Execute sff2fastq program
	'''
	global SFF2FASTQ_PROC
	global PROCESS_LOG_FILE
	global FAILED_FILES_LOG

	# Build sff2fastq shell command 
	cmd = f"{SFF2FASTQ_EXE_PATH} -o {fastq_path} {sff_path}"
	print(f"{cmd}")
	
	try:
		# Try executing command, return status
		#_res = os.system(cmd)
		SFF2FASTQ_PROC = subprocess.Popen([f"{SFF2FASTQ_EXE_PATH}", "-o", f"{fastq_path}", f"{sff_path}"])
		
		print_logger(f"SFF2FASTQ: Processing ...", log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
		_res = SFF2FASTQ_PROC.wait()

	except:
		# Something went wrong, return None
		_res = None

	print_logger(f"SFF2FASTQ Finished with exit code/mesg: {_res if not _res is None else 'ERROR'}", 
		log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
	return _res

#------------------------------------------------------------------------------
def fastq2fasta(fastq_path:str, fasta_path:str, args):
	'''
		SFF to FASTA Conversion Tool: Execute fastq2fasta program
	'''
	global FASTQ2FASTA_PROC
	global PROCESS_LOG_FILE
	global FAILED_FILES_LOG

	# Build sff2fastq shell command
	cmd = f"{FASTQ2FASTA_EXE_PATH} -i {fastq_path} -o {fasta_path}"
	print(f"{cmd}")

	try:
		# Try executing command
		#_res = os.system(cmd)
		FASTQ2FASTA_PROC = subprocess.Popen([f"{FASTQ2FASTA_EXE_PATH}", "-i", f"{fastq_path}", "-o", f"{fasta_path}"])

		print_logger(f"FASTQ2FASTA: Processing ...", log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
		_res = FASTQ2FASTA_PROC.wait()

	except:
		# Something went wrong, return None
		print(f"ERROR: Failed to Run fastq2fasta.")
		_res = None

	print_logger(f"FASTQ2FASTA Finished with exit code/mesg: {_res if not _res is None else 'ERROR'}", 
		log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
	return _res

#------------------------------------------------------------------------------
def process_files(sff_filepaths:list, args)->int:
	'''
		SFF to FASTA Conversion Tool: Convert SFF to FASTA
	'''
	global PROCESS_LOG_FILE
	global FAILED_FILES_LOG

	_status = STATUS_SUCCESS

	# Determing batch size for incremental processing
	batch_size = ( args.batch_size if not args.batch_size is None else len(sff_filepaths) )
	print_logger(f"Using batch size [{batch_size}]", log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)

	# Itterate through batches
	for k in range(0, len(sff_filepaths), batch_size):

		# Get Batch of File Paths
		batch = sff_filepaths[k:k+batch_size]
		print_logger(f"Now Processing Batch with Range [{k}:{k+batch_size}] ...", 
			log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)

		# Itterate through file paths in batch
		for sff_path in batch:
			print_logger(f"Now Processing SFF File [{sff_path}] ...", 
				log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)

			# Split File Path into Directory, Filename, File Extention
			sff_dir, sff_filename = os.path.split(sff_path)
			sff_filename, sff_file_ext = os.path.splitext(sff_filename)

			# If no output directory is specified, use input directory for output
			if not args.output_fasta is None:

				# Create output directory if it does not already exist
				if not os.path.exists(args.output_fasta):
					print_logger(f"Specified output directory [{args.output_fasta}] does not exits, creating it now...",
						log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
					os.mkdir(args.output_fasta)
				
				# Check if specified output directory is a valid directory path
				if os.path.isdir(args.output_fasta):

					# Join specified output directory path with new FASTA filename and extention
					fasta_path = os.path.join(args.output_fasta, f"{sff_filename}.fasta")
				else:
					print_logger(f"ERROR: Specified output directory [{args.output_fasta}] is not a directory.", 
						log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
					sys.exit(STATUS_FAILURE)
			else:
				# Join implied input directory path with new FASTA filename and extention
				fasta_path = os.path.join(sff_dir, f"{sff_filename}.fasta")

			# Create temporary file staging directory if it does not already exist
			if not os.path.exists(TEMP_DIR):
				os.mkdir(TEMP_DIR)

			# Join temporary file staging directory path with temp FASTQ filename and extention
			fastq_path = os.path.join(TEMP_DIR, f"{sff_filename}.fastq")

			print_logger(f"Converting SSF File [{sff_path}] to FASTA File [{fasta_path}] ...", 
				log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)

			# If SSF file exits process it using sff2fastq program
			if os.path.exists(sff_path):
				print_logger(f"Running sff2fastq ...", 
					log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
				_res = sff2fastq(sff_path, fastq_path, args)
			
			# Check if sff2fastq program finished sucessfully
			if _res is None:
				print_logger(f"ERROR: Failed to Run sff2fasta.\n Continuing to process remainging files ...", 
					log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
				print_logger(f"{sff_path}", log_file=FAILED_FILES_LOG)
				_status = STATUS_FAILURE
				continue # continue operator just proceeds in the next itteration of the current loop

			# If FASTQ file exits process it using fastq2fasta program, 
			# 	this also checks sff2fastq operation was sucessful
			if os.path.exists(fastq_path):
				print_logger(f"Running fastq2fasta ...", 
					log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
				_res = fastq2fasta(fastq_path, fasta_path, args)

			# Check if sff2fastq program finished sucessfully
			if _res is None:
				print_logger(f"ERROR: Failed to Run sff2fasta.\n Continuing to process remainging files ...", 
					log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
				print_logger(f"{sff_path}", log_file=FAILED_FILES_LOG)
				_status = STATUS_FAILURE
				continue

			# Delete temporary FASTQ file 
			os.remove(fastq_path)
			
		# Check Batch Processed Corectly
		if not os.path.exists(fasta_path):
			print_logger(f"ERROR: Failed to Run sff2fasta. Output FASTA File not Created.\n Continuing to process remainging files ...", 
					log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
			print_logger(f"{sff_path}", log_file=FAILED_FILES_LOG)
			_status = STATUS_FAILURE

	return STATUS_SUCCESS

#------------------------------------------------------------------------------
def get_input_files(args)->list:
	'''
		SFF to FASTA Conversion: Get Input SFF File(s)
	'''
	global PROCESS_LOG_FILE
	global FAILED_FILES_LOG

	if os.path.isdir(args.input_sff):
		use_input_path = os.path.join(args.input_sff, SFF_EXTENTION)
	elif os.path.isfile(args.input_sff):
		use_input_path = args.input_sff
	
	try:
		# Specified input is a directory of files.
		sff_filepaths = [f for f in glob.glob(use_input_path)]
	except:
		print_logger(f"ERROR: No Files in input directory or file does not exist.", 
			log_file=PROCESS_LOG_FILE, verbosity=args.verbosity)
		sys.exit(STATUS_FAILURE)

	return sff_filepaths	

#------------------------------------------------------------------------------
def run(args):
	'''
		SFF to FASTA Conversion Tool Runner
	'''
	_status = STATUS_SUCCESS

	# Get all .sff input files specified. 1+ Files
	sff_filepaths = get_input_files(args)

	# Process input selection and return status
	return process_files(sff_filepaths, args)

#------------------------------------------------------------------------------
def parse_args():
	'''
	
		SFF to FASTA Conversion Tool Argument Parser
	
		usage: ssf2fasta.py [-h] [-i INPUT_SFF] [-o OUTPUT_FASTA] [-b BATCH_SIZE]

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
	'''

	# Create parser object and add arguments
	parser = argparse.ArgumentParser(description='SFF to FASTA Conversion Tool')
	parser.add_argument('-i', '--input_sff', type=str, required=True,
						help='Full path to input .sff file or directory containing .sff files. Required.')
	parser.add_argument('-o', '--output_fasta', type=str, default=None,
						help='Directory to output .fasta file or files. Default: Same directory as input. Optional.')				
	parser.add_argument('-b', '--batch_size', type=int, default=None,
						help='Batch size. Default: No batching.')
	parser.add_argument('-v', '--verbosity', type=int, choices=[0,1,2], default=0,
						help='Verbosity mode for output. [0, Log Only; 1, Log and Print to Console; 2, Print Only]')

	# Parse <stdin> arguments with above options
	args = parser.parse_args()

	# Return parsed arguments object
	return args

#------------------------------------------------------------------------------
def main():
	'''
		SFF to FASTA Conversion Tool Entry Point
	'''
	global LOG_DIR
	global PROCESS_LOG_FILE
	global FAILED_FILES_LOG

	_status = STATUS_SUCCESS

	signal.signal(signal.SIGINT, sigterm_handler)

	# Create Log Directory if it Does Not Already Exist
	if not os.path.exists(LOG_DIR):
		os.mkdir(LOG_DIR)
	# Open Log Files
	timestamp = datetime.date.today()
	PROCESS_LOG_FILE = open(os.path.join(LOG_DIR, f"ssf2fasta_log_{timestamp.strftime('%m.%d.%Y_%H:%M')}"), "w")
	FAILED_FILES_LOG = open(os.path.join(LOG_DIR, f"failed_sff_log_{timestamp.strftime('%m.%d.%Y_%H:%M')}"), "w")

	# Parse Arguments
	args = parse_args()

	# Run Conversion Tool
	_status = run(args)

	# Clean Up
	exit_routine()

	sys.exit(_status)

#------------------------------------------------------------------------------
# Run main function if this file is called directly
if __name__ == "__main__":
	main()