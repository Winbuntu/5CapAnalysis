import pysam
import os
import getopt
import sys

def main():

	try:
		opts,args = getopt.getopt(sys.argv[1:], "i:o:", ["input_bam=", "output_bam="])
	except getopt.GetoptError:
		print "Not correct parameter!"
		print "gene_list,input_bam,output_bam"
		sys.exit(1)

	print opts
	print args

	for opt,arg in opts:
		#print arg
		if opt in ("-i", "--input_bam"):
			sam_file_name = arg
			#print arg
		if opt in ("-o", "--output_bam"):
			dereplicated_bam_name = arg
			#print arg


	samfile = pysam.AlignmentFile(sam_file_name,"rb")
	
	dereplicated_bam = pysam.AlignmentFile((dereplicated_bam_name),"wb",template = samfile)

	seen_read = set()

	for read in samfile:
		read_id = read.query_name  + "_" + str(read.template_length)
		#print read_id
		if read_id not in seen_read:
			dereplicated_bam.write(read)
			seen_read.add(read_id)


	samfile.close()
	dereplicated_bam.close()


if __name__ == '__main__':
	main()
