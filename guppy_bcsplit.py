#!/usr/bin/python3

import sys
import os
import csv
import getopt
from Bio import SeqIO

def touch(path):
    with open(path, 'w'):
        os.utime(path, None)

def main(argv):

	barcodes_file = ''
	fastq_file = ''
	prefix = ''
	summary_file = ''
	nr_mandatory_args = 0

	try:
		opts, args = getopt.getopt(argv,"hb:f:p:s:",["barcode=","fastq=","prefix=","summary="])
	except getopt.GetoptError:
		print('parameter error. usage: guppy_bcsplit.py -b <barcode_file> -f <fastq_file> -p <your_prefix> -s <summary_file (optional)>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('usage: guppy_bcsplit.py -b <barcode_file> -f <fastq_file> -p <your_prefix> -s <summary_file (optional)>')
			sys.exit()
		elif opt in ("-b", "--barcode"):
			barcodes_file = arg
			nr_mandatory_args += 1
		elif opt in ("-f", "--fastq"):
			fastq_file = arg
			nr_mandatory_args += 1
		elif opt in ("-p", "--prefix"):
			prefix = arg
			nr_mandatory_args += 1
		elif opt in ("-s", "--summary"):
			summary_file = arg
		else:
			assert False, "unhandled option"

	if(nr_mandatory_args < 3):
		print('parameter error. usage: guppy_bcsplit.py -b <barcode_file> -f <fastq_file> -p <your_prefix> -s <summary_file (optional)>')
		sys.exit(2)


	read_to_barcode = {}
	my_stats = {}

	with open(barcodes_file) as csvfile:
		readCSV = csv.reader(csvfile, delimiter='\t')
		header = ' '.join(next(readCSV))
		if('barcode' not in header):
			print('Barcode file seems to be not valid.')
			sys.exit(2)
			
		for row in readCSV:
			if row[1] in my_stats:
				my_stats[row[1]] += 1
			else:
				my_stats[row[1]] = 1	
			read_to_barcode[row[0]] = row[1]

	if(summary_file != ''):
		with open(summary_file, "w") as summ_file_handle:
			for x in sorted(my_stats):
				summ_file_handle.write(x+':'+str(my_stats[x])+'\n')

	for x in my_stats:
		current_barcode = x
		touch(prefix + '_' + current_barcode + '.fastq')	

	fastq_parser = SeqIO.parse(fastq_file, "fastq") 
	for fastq_rec in fastq_parser:     
		read_name = fastq_rec.id
		current_barcode = read_to_barcode[read_name]
		with open(prefix + '_' + current_barcode + '.fastq', 'a') as fastq_handle:
			SeqIO.write(fastq_rec, fastq_handle, "fastq")

if __name__ == "__main__":
	main(sys.argv[1:])
