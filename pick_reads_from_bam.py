import pysam
import os
import getopt
import sys


def main():

	try:
		opts,args = getopt.getopt(sys.argv[1:], "g:i:o:", ["gene_list=","input_bam=", "output_bam="])
	except getopt.GetoptError:
		print "Not correct parameter!"
		print "gene_list,input_bam,output_bam"
		sys.exit(1)

	print opts
	print args

	for opt,arg in opts:
		if opt in ("-g", "--gene_list"):
			gene_list_name = arg
			print arg
		if opt in ("-i", "--input_bam"):
			sam_file_name = arg
			print arg
		if opt in ("-o", "--output_bam"):
			filtered_bam_name = arg
			print arg



	samfile = pysam.AlignmentFile(sam_file_name,"rb")
	
	filtered_bam = pysam.AlignmentFile((filtered_bam_name+"_temp.bam"),"wb",template = samfile)

	fp = open(gene_list_name,"r")

	count = 0

	for gene in fp:
		[chrom,start_pos,end_pos,gene_strand] = gene.strip().split("\t")
		print chrom,start_pos,end_pos,gene_strand

		# count = count +1
		# if count >5:
		# 	break

		#gene_strand = "+"
	# reverse strand gene, pick the read-pair on reverse strand, and with adapter at right

		if gene_strand == "-":
			for read in samfile.fetch(chrom,int(start_pos),int(end_pos) ):
				#print read

				if read.is_reverse == True: # reverse read only for gene on reverse strand
					opt_type,opt_length = read.cigartuples[-1] # check if a long softclip at right
					

					if (opt_type == 4) and (opt_length >=20): # add adapter check here
						if read.is_paired and (read.mate_is_unmapped==False):
							filtered_bam.write(read)
							#filtered_bam.write(samfile.mate(read))
			continue

		if gene_strand == "+":
			for read in samfile.fetch(chrom,int(start_pos),int(end_pos)):
				#print read
				if read.is_reverse == False: # forward read only for gene on forward strand
					opt_type,opt_length = read.cigartuples[0] # check if a long softclip at left
					

					if (opt_type == 4) and (opt_length >=20): # add adapter check here
						if read.is_paired and (read.mate_is_unmapped==False):
							filtered_bam.write(read)
							#filtered_bam.write(samfile.mate(read))




	samfile.close()
	filtered_bam.close()
	fp.close()

	os.system("samtools sort " +  filtered_bam_name+"_temp.bam  " + filtered_bam_name )
	os.system("samtools index "+filtered_bam_name+".bam")




if __name__ == '__main__':
	main()
	




