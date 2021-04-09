"""
	SFF2FASTA Converter
"""

# Standard Library Imports
import os
import glob
import json
import tempfile
import argparse

# Third Party Imports

# Other Imports


# Constants
SFF_EXTENTION = '*.sff'

def sff2fastq(sff_path, fastq_path):
	pass

def fastq2fasta(fastq_path, fasta_path):
	pass

def process_files(sff_filepaths:list, args):
	
	batch_size = ( len(sff_filepaths) % args.batch_size if not args.batch_size is None else len(sff_filepaths) % 10 )

	temp_dir = tempfile.mkdtemp()

	# TODO: Batching

	for sff_path in sff_filepaths:

		sff_dir, sff_filename = os.path.split(sff_path)

		if not args.output_fasta is None:
			if os.path.isdir(args.output_fasta) and os.path.exists(args.output_fasta):
				fasta_path = os.path.join(args.output_fasta, sff_filename, '.fasta')
			else:
				print(f"ERROR: Output Directory Does not exist or is not a directory")
				exit(1)

		fastq_path = os.path.join(temp_dir, sff_filename, '.fasta')

		if os.path.exists(sff_path):

			sff2fastq(sff_path, fastq_path)

		if os.path.exists(fastq_path):

			fastq2fasta(fastq_path, fasta_path)

		
	# Check Batch Processed Corectly

	# Increment Batch

def get_input_files(input_path:str)->list:
	
	if os.path.isdir(input_path):
		use_input_path = os.path.join(input_path, SFF_EXTENTION)
	elif os.path.isfile(input_path):
		use_input_path = input_path

	try:
		# Specified input is a directory of files.
		sff_filepaths = [f for f in glob.glob(use_input_path)]
	except:
		print(f"ERROR: Bad Input Directory or File")

	return sff_filepaths
	

def parse_args():
	"""
		-i, --input_sff : Full path to input .sff file or directory containing .sff files.
		-o, --output_fasta : Directory to output .fasta file or files. Default: Same directory as input.
		-b, --batch_size : 
	"""

	parser = argparse.ArgumentParser(description='SFF to FASTA Conversion Tool')
	parser.add_argument('-i', '--input_sff', type=str),
						help='Full path to input .sff file or directory containing .sff files. Required.')
	parser.add_argument('-o', '--output_fasta', type=str, default=None,
						help='Directory to output .fasta file or files. Default: Same directory as input. Optional.')				
	parser.add_argument('-b', '--batch_size', type=int, default=None,
						help='Batch size. Default: No batching.')

	args = parser.parse_args()

	return args

def main():
	'''
		SFF to FASTA Conversion Tool Entry Point
	'''

	args = parse_args()

	sff_filepaths = get_input_files(args.input_path)

	process_files(sff_filepaths)

# Run main function if this file is called directly
if __name__ == "__main__":
	main()