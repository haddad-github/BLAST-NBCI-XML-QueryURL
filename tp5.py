from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast import NCBIXML

from urllib.request import urlopen
import json

#recherche blastp local dans base de donnee e tcreer fichier xml
blastp_cline = NcbiblastpCommandline(
    query="mystery_protein.fasta",
    db="human_proteome",
    out="blastp_results.xml",
    outfmt=5,
    num_threads=1,
)

stdout, stderr = blastp_cline()

#variable de comparaison et stoquer alignement avec plus haut bits
i = 0
meilleur = []

with open("blastp_results.xml", "r") as i_file:
     blast_record = NCBIXML.read(i_file)
     
     for alignement in blast_record.alignments:
         for hsp in alignement.hsps:
             if hsp.bits > i:
                i = hsp.bits
                meilleur = alignement
                
#title du meilleur alignement
numero_id = meilleur.title.split("|")[1]

#formation de l'url avec filtre gene et homo sapiens; trouver id a l'aide de symbol
url = "https://rest.ensembl.org/xrefs/symbol/{species}/{symbol}"
opt = ["content-type=application/json", "object_type=gene", "species=homo_sapiens"]

query_url = "{}?{}".format(url, ";".join(opt)).format(species="homo_sapiens", symbol=numero_id)

#lire le resultat
stream = urlopen(query_url)
resultat = json.loads(stream.read().decode())
stream.close()

#print le id du gene
print(resultat[0]["id"])
