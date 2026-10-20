from Bio import SeqIO
import glob
import os
import logging
import subprocess
from dmtcp_util import request_dmtcp_checkpoint

def count_nucleotides(fasta_file):
    """
    Count the total number of A, T, G, and C nucleotides
    in all sequences in a FASTA file.
    """

    counts = {
        "A": 0,
        "T": 0,
        "G": 0,
        "C": 0,
    }

    for record in SeqIO.parse(fasta_file, "fasta"):

        sequence = str(record.seq).upper()

        counts["A"] += sequence.count("A")
        counts["T"] += sequence.count("T")
        counts["G"] += sequence.count("G")
        counts["C"] += sequence.count("C")

    return counts

def calculate_gc_content(fasta_file):
    """
    Calculate the overall GC content of all sequences
    in the FASTA file.
    """
    total_gc = 0
    total_bases = 0

    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence = str(record.seq).upper()

        total_gc += sequence.count("G") + sequence.count("C")
        total_bases += (
            sequence.count("A")
            + sequence.count("T")
            + sequence.count("G")
            + sequence.count("C")
        )

    if total_bases == 0:
        return 0

    gc_content = (total_gc / total_bases) * 100

    return gc_content

def count_sequences(fasta_file):
    """
    Count the number of sequences in the FASTA file.
    """
    count = 0

    for record in SeqIO.parse(fasta_file, "fasta"):
        count += 1

    return count


def main():

    fasta_files = glob.glob("*.fasta")

    output_file = "fasta_analysis.txt"

    with open(output_file, "w") as outfile:

        for fasta_file in fasta_files:

            nucleotide_counts = count_nucleotides(fasta_file)

            gc_content = calculate_gc_content(fasta_file)

            number_of_sequences = count_sequences(fasta_file)


            outfile.write("================================\n")
            outfile.write(f"File: {os.path.basename(fasta_file)}\n")
            outfile.write("================================\n")
            outfile.write(f"A: {nucleotide_counts['A']}\n")
            outfile.write(f"T: {nucleotide_counts['T']}\n")
            outfile.write(f"G: {nucleotide_counts['G']}\n")
            outfile.write(f"C: {nucleotide_counts['C']}\n")
            outfile.write(f"GC Content: {gc_content:.2f}%\n")
            outfile.write(
                f"Number of Sequences: {number_of_sequences}\n"
            )
            outfile.write("\n")

    print(f"Analysis completed. Results saved to {output_file}")

if __name__ == "__main__":
    main()
