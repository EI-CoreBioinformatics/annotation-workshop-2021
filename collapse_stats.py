#!/usr/bin/env python3

import argparse
import sys
import re

__doc__ = "Script to collapse various stat files into one."

def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("-o", "--out", default=sys.stdout,
                        type=argparse.FileType("w"))
    parser.add_argument("stat", type=argparse.FileType("rt"),
                        nargs="+")
    args = parser.parse_args()

    data = []
    # 5 --------------------------------- |   Sn |   Pr |   F1 |
    # 17
    # 24
    # 31
    
    for stat in args.stat:
        new = dict()
        new["stat"] = []
        new["matches"] = []
        new["features"] = []
        new["high_level"] = []
        for num, line in enumerate([_ for _ in stat if _.strip()], start=1):
            line = line.rstrip()
            # 1 Command line:
            # 2 /tgac/software/testing/mikado/0.19.0/x86_64/bin/mikado.py compare [..]
            # 3 27643 reference RNAs in 14475 genes
            # 4 16142 predicted RNAs in  11379 genes
            if num < 3:
                continue
            elif num == 3:
                
                ref_transcr, ref_genes = [int(_) for _ in re.sub(" reference RNAs in", "", re.sub(" genes", "", line)).split()]
                new["ref_transcr"] = ["{0},,".format(ref_transcr)]
                new["ref_genes"] = ["{0},,".format(ref_genes)]
            elif num == 4:
                pred_transcr, pred_genes = [int(_) for _ in re.sub(" predicted RNAs in", "",
                                                                 re.sub(" genes", "", line)).split()]
                new["pred_transcr"] = ["{0},,".format(pred_transcr)]
                new["pred_genes"] = ["{0},,".format(pred_genes)]
            elif num in range(6, 17):
                # 6                         Base level: 51.90  87.35  65.11
                # 7             Exon level (stringent): 33.26  49.68  39.85
                # 8               Exon level (lenient): 60.83  86.77  71.52
                # 9                       Intron level: 62.69  93.31  74.99
                # 10                 Intron chain level: 36.76  58.92  45.27
                # 11       Transcript level (stringent): 0.00  0.00  0.00
                # 12   Transcript level (>=95% base F1): 8.41  13.84  10.46
                # 13   Transcript level (>=80% base F1): 29.08  46.36  35.74
                # 14          Gene level (100% base F1): 0.00  0.00  0.00
                # 15         Gene level (>=95% base F1): 13.46  16.93  15.00
                # 16         Gene level (>=80% base F1): 44.54  56.05  49.64
                new["stat"].append(",".join(line.split(":")[1].lstrip().split()))
            elif num in range(18, 24):
                # 18             Matching intron chains: 8581
                # 19              Matched intron chains: 9467
                # 20    Matching monoexonic transcripts: 521
                # 21     Matched monoexonic transcripts: 560
                # 22         Total matching transcripts: 9102
                # 23          Total matched transcripts: 10027
                try:
                    new["matches"].append("{0},,".format(line.split(":")[1].lstrip()))
                except IndexError:
                    continue
            elif num in range(25, 31):
                # 25           Missed exons (stringent): 50191/75208  (66.74%)
                # 26            Novel exons (stringent): 25337/50354  (50.32%)
                # 27             Missed exons (lenient): 27299/69689  (39.17%)
                # 28              Novel exons (lenient): 6466/48856  (13.23%)
                # 29                     Missed introns: 21355/57235  (37.31%)
                # 30                      Novel introns: 2573/38453  (6.69%)
                try:
                    new["features"].append("{0},,".format(line.split(":")[1].lstrip()))
                except IndexError:
                    continue
            elif num in range(32,36):
                # 32                 Missed transcripts: 6595/27643  (23.86%)
                # 33                  Novel transcripts: 132/16142  (0.82%)
                # 34                       Missed genes: 3877/14475  (26.78%)
                # 35                        Novel genes: 102/11379  (0.90%)
                try:
                    new["high_level"].append("{0},,".format(line.split(":")[1].lstrip()))
                except IndexError:
                    continue
            else:
                continue
        data.append(new)
        continue

    for key in ["stat", "matches", "features", "high_level",
                "ref_transcr", "ref_genes", "pred_transcr", "pred_genes"]:
        print(key)
        for row in zip(*[_[key] for _ in data]):
            print(",".join(row), file=args.out)
            continue
        if not ("pred" in key or "ref" in key):
            print("", file=args.out)
        else:
            pass
        continue
    
    # assert len(data) == len(args.stat), len(data)
    # print(data)
            
main()
