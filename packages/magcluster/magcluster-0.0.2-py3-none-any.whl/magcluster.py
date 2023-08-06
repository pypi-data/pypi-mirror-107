#!/usr/bin/env python3


import argparse
from subprocess import run
from sys import argv
import pandas as pd
# import pandas
def get_magcluster_parser():
    parser = argparse.ArgumentParser(
             prog="Magcluster", 
             description='Magnetosome gene cluster anaylise', 
             usage='%(prog)s [options]', 
             formatter_class=argparse.RawTextHelpFormatter, 
             epilog=
            "General usage\n-------------\n"
            "Magnetosome gene annotation:\n"
            "  $ magcluster maga XXX.fa\n\n"
            "Magnetosome gene screen:\n"
            "  $ magcluster magsc XXX.faa XXX.gbk\n\n"
            "Magnetosome gene cluster mapping:\n"
            "  $ magcluster magm XXX_screened.gbk\n\n"
            # "Direct analyse:\n"
            # "  $ magcluster -ascm XXX.fa\n\n"
            
            "Runjia, 2021"
            )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help='show magcluster version number and exit')
    # parser.add_argument('-ascm', action='store_true', help='directly analyse from genome file to genecluster mapping.')
    #构建子命令
    subparsers = parser.add_subparsers(title='Subcommands', dest="subparser_name")
    #构建maga子命令
    parser_maga = subparsers.add_parser('maga', help='Magnetosome gene annotation with Prokka')
    parser_maga.add_argument('fafile', type=str, help='Genome files need to be annotated')

    General = parser_maga.add_argument_group('General')
    #General.add_argument('--version', help='Print version and exit', action="store_true")
    #General.add_argument('--docs', help='Show full manual/documentation', action="store_true")
    #General.add_argument('--citation', help='Print citation for referencing Prokka', action="store_true")
    General.add_argument('--quiet', help='No screen output (default OFF)', action="store_true")
    General.add_argument('--debug', help='Debug mode: keep all temporary files (default OFF)', action="store_true")

    Setup = parser_maga.add_argument_group('Setup')
    Setup.add_argument('--listdb', help='List all configured databases', action="store_true")
    Setup.add_argument('--setupdb', help='Index all installed databases', action="store_true")
    Setup.add_argument('--cleandb', help='Remove all database indices', action="store_true")
    Setup.add_argument('--depends', help='List all software dependencies', action="store_true")

    Outputs = parser_maga.add_argument_group('Outputs')
    Outputs.add_argument('--outdir', type=str, help="Output folder [auto] (default '')")
    Outputs.add_argument('--prefix', type=str, help='Filename output prefix [auto] (default '')')
    Outputs.add_argument('--force', help='Force overwriting existing output folder (default OFF)', action="store_true")
    Outputs.add_argument('--addgenes', help="Add 'gene' features for each 'CDS' feature (default OFF)", action="store_true")
    Outputs.add_argument('--addmrna', help="Add 'mRNA' features for each 'CDS' feature (default OFF)", action="store_true")
    Outputs.add_argument('--locustag', type=str, help="Locus tag prefix (default 'PROKKA')")
    Outputs.add_argument('--increment', type=int, help="Locus tag counter increment (default '1')")
    Outputs.add_argument('--gffver', type=int, help="GFF version (default '3')")
    Outputs.add_argument('--compliant', help='Force Genbank/ENA/DDJB compliance: --genes --mincontiglen 200 --centre XXX (default OFF)', action="store_true")

    somthing = parser_maga.add_argument_group('XXX (default OFF)')
    somthing.add_argument('--centre', type=str, help="Sequencing centre ID. (default '')")
    somthing.add_argument('--accver', type=int, help="Version to put in Genbank file (default '1')")

    Organism_details = parser_maga.add_argument_group('Organism details')
    Organism_details.add_argument('--genus', type=str, help="Genus name (default 'Genus')")
    Organism_details.add_argument('--species', type=str, help="Species name (default 'species')")
    Organism_details.add_argument('--strain', type=str, help="Strain name (default 'strain')")
    Organism_details.add_argument('--plasmid', type=str, help="Plasmid name or identifier (default '')")

    Annotations = parser_maga.add_argument_group('Annotations')
    Annotations.add_argument('--kingdom', type=str, help="Annotation mode: Archaea|Bacteria|Viruses (default 'Bacteria')")
    Annotations.add_argument('--gcode', type=int, help="Genetic code / Translation table (set if --kingdom is set) (default '0')")
    Annotations.add_argument('--gram', type=str, help="Gram: -/neg +/pos (default '')")
    Annotations.add_argument('--usegenus', help='Use genus-specific BLAST databases (needs --genus) (default OFF)', action="store_true")
    Annotations.add_argument('--proteins', type=str, help='Fasta file of trusted proteins to first annotate from (default '')')
    Annotations.add_argument('--hmms', type=str, help="Trusted HMM to first annotate from (default '')")
    Annotations.add_argument('--metagenome', help='Improve gene predictions for highly fragmented genomes (default OFF)', action="store_true")
    Annotations.add_argument('--rawproduct', help='Do not clean up /product annotation (default OFF)', action="store_true")
    Annotations.add_argument('--cdsrnaolap', help="Allow [tr]RNA to overlap CDS (default OFF)", action="store_true")

    Computation = parser_maga.add_argument_group('Computation')
    Computation.add_argument('--cpus', type=int, help="Number of CPUs to use [0=all] (default '8')")
    Computation.add_argument('--fast', help='Fast mode - skip CDS /product searching (default OFF)', action="store_true")
    Computation.add_argument('--noanno', help='For CDS just set /product="unannotated protein" (default OFF)', action="store_true")
    Computation.add_argument('--mincontiglen', type=int, help="Minimum contig size [NCBI needs 200] (default '1')")
    Computation.add_argument('--evalue', type=float, help="Similarity e-value cut-off (default '1e-06')")
    Computation.add_argument('--rfam', help="Enable searching for ncRNAs with Infernal+Rfam (SLOW!) (default '0')", action="store_true")
    Computation.add_argument('--norrna', help="Don't run rRNA search (default OFF)", action="store_true")
    Computation.add_argument('--notrna', help="Don't run tRNA search (default OFF)", action="store_true")
    Computation.add_argument('--rnammer', help="Prefer RNAmmer over Barrnap for rRNA prediction (default OFF)", action="store_true")
    
    #构建magsc子命令
    parser_magsc = subparsers.add_parser('magsc', help='Magnetosome gene screening with magscreen')
    parser_magsc.add_argument('-faa', '--faafile', required=True, type=str, help='.faa file to analyse')
    parser_magsc.add_argument('-gbk', '--gbkfile', required=True, type=str, help='.gbk/.gbf file to analyse')
    #构建magm子命令
    parser_magm = subparsers.add_parser('magm', help='Magnetosome gene cluster mapping with Clinker')
    inputs = parser_magm.add_argument_group("Input options")
    inputs.add_argument('gbkfiles', help="Gene cluster GenBank files", nargs="*")
    inputs.add_argument("-r", "--ranges", 
           help="Scaffold extraction ranges. If a range is specified, only features within the range will be extracted from the scaffold. Ranges should be formatted like: scaffold:start-end"
           " (e.g. scaffold_1:15000-40000)", nargs="+",
    )

    alignment = parser_magm.add_argument_group("Alignment options")
    alignment.add_argument(
        "-na",
        "--no_align",
        help="Do not align clusters",
        action="store_true",
    )
    alignment.add_argument(
        "-i",
        "--identity",
        help="Minimum alignment sequence identity [default: 0.3]",
        type=float,
        default=0.3
    )
    alignment.add_argument(
        "-j",
        "--jobs",
        help="Number of alignments to run in parallel (0 to use the number of CPUs) [default: 0]",
        type=int,
        default=0,
    )

    output = parser_magm.add_argument_group("Output options")
    output.add_argument("-s", "--session", help="Path to clinker session")
    output.add_argument("-ji", "--json_indent", type=int, help="Number of spaces to indent JSON [default: none]")
    output.add_argument("-f", "--force", help="Overwrite previous output file", action="store_true")
    output.add_argument("-o", "--output", help="Save alignments to file")
    output.add_argument(
        "-p",
        "--plot",
        nargs="?",
        const=True,
        default=False,
        help="Plot cluster alignments using clustermap.js. If a path is given,"
        " clinker will generate a portable HTML file at that path. Otherwise,"
        " the plot will be served dynamically using Python's HTTP server."
    )
    output.add_argument("-dl", "--delimiter", help="Character to delimit output by [default: human readable]")
    output.add_argument("-dc", "--decimals", help="Number of decimal places in output [default: 2]", default=2)
    output.add_argument(
        "-hl",
        "--hide_link_headers",
        help="Hide alignment column headers",
        action="store_true",
    )
    output.add_argument(
        "-ha",
        "--hide_aln_headers",
        help="Hide alignment cluster name headers",
        action="store_true",
    )

    viz = parser_magm.add_argument_group("Visualisation options")
    viz.add_argument(
        "-ufo",
        "--use_file_order",
        action="store_true",
        help="Display clusters in order of input files"
    )

    return parser

def capture_args():
    return argv

def magene_screen(locus_tags, gbkfile_path):
    #读入gbk文件
    with open(gbkfile_path,'r') as f:
        allcontents = f.read()
        allcontigs = allcontents.split('LOCUS') #使用LOCUS分隔不同contig

        mag_contigs = [] #设定包含有mag基因的contig

    #筛选含有mag基因的contig
        for locus_tag in locus_tags:
            for contig in allcontigs:
                if locus_tag in contig:
                    mag_contigs.append(contig)
        mag_contigs_unique = [contig for contig in set(mag_contigs)] #删除mag_contigs中的重复，保证唯一

    #将丢失的‘LOCUS’字样重新加入,length格式更正	
        mag_contigs_unique_normalized = [] 
        for contig in mag_contigs_unique:
            node_tag = contig.split()[0]
            contig_length = node_tag.split('_')[3]
            contig_tem_list = list(contig)
            len_index = contig_tem_list.index('b')
            contig_tem_list.insert(len_index, contig_length + ' ')
            contig_with_len = ''.join(contig_tem_list)
            contig_normalized = 'LOCUS' + contig_with_len
            mag_contigs_unique_normalized.append(contig_normalized)
        # print(len(mag_contigs_unique_normalized))



    #使用join将所有mag_contigs_unique_normalized整合成一个string/text
    magtext = ''.join(mag_contigs_unique_normalized)

    #使用with open函数写出magene.gbk文件，作为后续基因簇绘图的输入文件
    clean_gbk = gbkfile_path.rstrip('.gbk')+'_clean.gbk'
    with open(clean_gbk,'w') as f:
        f.write(magtext)
    return clean_gbk

def magpro_screen(faafile_path):
    with open(faafile_path,'r') as f:
        allLine = f.readlines()

        #筛选出与Magnetosome有关的部分
        allLineClean = []
        readable = False
        for line in allLine:
            if '>' in line:
                if 'Magnetosome' in line:
                    allLineClean.append(line)
                    readable = True
                elif readable:
                    readable = False
            elif readable:
                allLineClean.append(line)

        #获取Magnetosome的行名、序号、蛋白名
        seqname = [] #行名
        seqname_tag = []#行名拆开后带有样本名的基因tag

        seqnumber = []#用于连续性比较的序号
        proname = []#蛋白名
        for line in allLineClean:
            if '>' in line:
                seqname.append(line)

                a = line.split()
                b = a[0]
                seqname_tag.append(b)
                
                c = b.split('_')
                seqnumber.append(int(c[1]))


                proindex = a.index('protein') + 1
                proname.append(a[proindex])

        #获取Mag序列
        allSeq = [] #所有Mag序列
        tmpSeq = ''
        for line in allLineClean:
            if '>' in line:
                if len(tmpSeq) > 0:
                    allSeq.append(tmpSeq)
                    tmpSeq = ''
            else:
                tmpSeq += line
        if tmpSeq != '':
            allSeq.append(tmpSeq)


        #获取连续基因
        MIN_LENGTH = 2 #序列被认为连续的最小长度
        MIN_DISTANCE = 2 #序列被认为断开的最小间隔

        maglist_tag = []
        templist = []

        seqname_tag_final = []#确定为磁小体蛋白的蛋白tag
        temp_seqname_tag_final = []#暂存的磁小体蛋白tag列表

        magpro_namelist = []#确定为磁小体蛋白的蛋白名列表
        temp_magpro_namelist = []#暂存的磁小体蛋白名列表

        magpro_seq = [] #确定为磁小体蛋白的序列
        temp_magpro_seq = [] #暂存的磁小体蛋白序列
        for index, i in enumerate(seqnumber):
            _len = len(templist)
            if _len == 0:
                templist.append(i)
                temp_seqname_tag_final.append(seqname_tag[index])
                temp_magpro_namelist.append(proname[index])
                temp_magpro_seq.append(allSeq[index])
            elif i - templist[-1] <= MIN_DISTANCE:
                templist.append(i)
                temp_seqname_tag_final.append(seqname_tag[index])
                temp_magpro_namelist.append(proname[index])
                temp_magpro_seq.append(allSeq[index])
            elif _len == 1:
                templist = [i]
                temp_seqname_tag_final =[seqname_tag[index]]
                temp_magpro_namelist = [proname[index]]
                temp_magpro_seq = [allSeq[index]]
            elif _len >= MIN_LENGTH: #每当出现断点，
                maglist_tag.append(templist) #更新maglist_tag
                seqname_tag_final.append(temp_seqname_tag_final)#更新磁小体基因tag
                magpro_namelist.append(temp_magpro_namelist)
                magpro_seq.append(temp_magpro_seq)
                templist = [i] #将templist清空
                temp_seqname_tag_final = [seqname_tag[index]]
                temp_magpro_namelist = [proname[index]]
                temp_magpro_seq = [allSeq[index]]
        if len(templist) >= MIN_LENGTH: #若循环结束后,templist中包含连续序列
            maglist_tag.append(templist)
            seqname_tag_final.append(temp_seqname_tag_final)
            magpro_namelist.append(temp_magpro_namelist)
            magpro_seq.append(temp_magpro_seq)

        # print(maglist_tag)
        # print(seqname_tag_final)
        # print(magpro_namelist)
        #输出磁小体基因簇的长度/磁小体基因的个数
        magpro_number = 0
        for i in magpro_seq:
            magpro_number += len(i)
        # print(magpro_number)
        # print(sum([len(i) for i in magpro_seq]))

        #把嵌套列表释放成一个列表
        tag = [i for j in seqname_tag_final for i in j]#磁小体基因的prokka注释标号
        name = [i for j in magpro_namelist for i in j]#磁小体基因的名称
        length = [len(i) for j in magpro_seq for i in j ]#磁小体基因的长度
        sequence = [i for j in magpro_seq for i in j]#磁小体基因序列
        
        magpro_dictionary = {
            'tag': tag,
            'name': name,
            'length': length,
            'sequence': sequence,
        }
        mag_df = pd.DataFrame(
            magpro_dictionary
        )
        mag_df.to_excel('magpro.xlsx', sheet_name = 'magpro', index = False)
       
        # print(tag)
        # print(name)
        # print(length)

        locus_tags = []
        for i in tag:
            locus_tag = i.split('>')[1]
            locus_tags.append(locus_tag)
        # print(locus_tags)
        return locus_tags

def main():
    parser = get_magcluster_parser()
    args = parser.parse_args()
    magcluster(args, subparser_name=args.subparser_name)

def magcluster(args, subparser_name=None):
    """user args to run magcluster""" 
    if subparser_name:
        if subparser_name == 'maga':
            maga()
        elif subparser_name == 'magsc':
            magsc(args)
        elif subparser_name == 'magm':
            magm()

def maga():
    usr_args = capture_args()
    del usr_args[0:2]
    usr_args.insert(0, 'prokka')
    if '--outdir' not in usr_args:
        usr_args.append('--outdir')
        usr_args.append('maga_annotation')
    if '--prefix' not in usr_args:
        usr_args.append('--prefix')
        usr_args.append('maga_')
    run(usr_args)

def magsc(args):
    print('[The protein file is screening...]')
    locus_tags = magpro_screen(faafile_path = args.faafile)
    print("[A xlsx file named as 'magpro' is generated.]")
    print('[The genbank file is screening...]')
    clean_gbk = magene_screen(locus_tags, gbkfile_path = args.gbkfile)
    print("[A .gbk file named as 'clean_gbk' is produced.]")
    print('[Thank you for using magash.]')

def magm():
    usr_args = capture_args()
    del usr_args[0:2]
    usr_args.insert(0, 'clinker')
    run(usr_args)

# def ascm(ascm_args):
#     print('111111111')

#############################################
if __name__ == '__main__':
    main()