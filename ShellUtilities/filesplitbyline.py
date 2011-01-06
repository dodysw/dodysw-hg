"""
filesplitbyline - split a file into n files of max_size(kb) while preserving line (split happen at the end of line), with optional bz2-compressed
Copyright 2011 - Dody Suria Wijaya <dodysw@gmail.com>
GPL v3 License
"""
import sys, os, bz2

def split(file_name, max_size, compress=False):
    curr_size = 0
    split_num = 1   
    file_wo_ext, file_ext = os.path.splitext(file_name)
    if compress:
        file_ext += ".bz2"
        presser = bz2.BZ2Compressor(9)
    new_file = file("%s_%d%s" % (file_wo_ext, split_num, file_ext), "w")
    for line in file(file_name):
        if compress:
            solid = presser.compress(line)
        stream_len = len(solid if compress else line)
        curr_size += stream_len
        if curr_size > max_size:
            new_file.close()
            curr_size = stream_len
            split_num += 1
            new_file = file("%s_%d%s" % (file_wo_ext, split_num, file_ext), "w")            
        new_file.write(solid if compress else line)
    new_file.close()
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: filesplitbyline.py <filetosplit> <maxsize_kb> [compress]"
        print "Will be splitted to <filetosplit_1.fileext> where 1 is n number of splits, line is preserved (line won't splited in the middle)"
        print "E.g. filesplitbyline.py data.csv <maxsize_kb> [compress]
        sys.exit()
    filename, maxsize = sys.argv[1:3]
    if len(sys.argv) > 3:
        compress = sys.argv[3]
    split(filename, int(maxsize)*1024, compress)