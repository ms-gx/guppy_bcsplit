import sys
import os
import csv
import pathlib
from Bio import SeqIO


def touch(path):
    with open(path, 'w'):
        os.utime(path, None)

if(len(sys.argv) < 4):
	sys.stderr.write('not enough parameters\n')	
	exit()

barcodes_file = '' 
fastq_file = ''
prefix = '' 

try:
	opts, args = getopt.getopt(argv,"hb:f:p",["barcodefile=","fastqfile=","-prefix"])
except getopt.GetoptError:
      print 'guppy_bcsplit.py -b <barcode_file> -f <fastq_file> -p <your_prefix>'
      sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print 'guppy_bcsplit.py -b <barcode_file> -f <fastq_file> -p <your_prefix>'
		sys.exit()
	elif opt in ("-i", "--ifile"):
		inputfile = arg
	elif opt in ("-o", "--ofile"):
		outputfile = arg
print 'Input file is "', inputfile
ürint 'Output file is "', outputfile

#barcodes_file = sys.argv[1]
#fastq_file = sys.argv[2]
#prefix = sys.argv[3]

read_to_barcode = {}
my_stats = {}

with open(barcodes_file) as csvfile:
	readCSV = csv.reader(csvfile, delimiter='\t')
	next(readCSV)
	for row in readCSV:
		if row[1] in my_stats:
			my_stats[row[1]] += 1
		else:
			my_stats[row[1]] = 1	
		read_to_barcode[row[0]] = row[1]

for x in sorted(my_stats):
	print (x+':'+str(my_stats[x]))

for x in my_stats:
	current_barcode = x
	touch(prefix + '_' + current_barcode + '.fastq')	

fastq_parser = SeqIO.parse(fastq_file, "fastq") 
for fastq_rec in fastq_parser:     
	read_name = fastq_rec.id
	current_barcode = read_to_barcode[read_name]
	with open(prefix + '_' + current_barcode + '.fastq', 'a') as fastq_handle:
		SeqIO.write(fastq_rec, fastq_handle, "fastq")
