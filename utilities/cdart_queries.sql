select a.domgi, (select accession from DomainGi where domgi = a.domgi) accession, 
b.taxid, (select orgname from cdart..Tax where taxid = b.taxid) as taxOrg, 
count(distinct b.pig) as nPig, count(c.gi) as nGi
from cdart..DomainGi a with (NOLOCK) inner join cdart..HitDomgiVu b with (NOLOCK)
on a.domgi = b.domgi
inner join cdart..Gi2Nr c with (NOLOCK) on b.pig = c.pig
--where a.accession = 'pfam00385'
--where a.accession in ('pfam00352', 'pfam00385', 'pfam10536', 'TIGR00607', 'TIGR03687')
group by a.domgi, b.taxid
order by accession, nPig desc, nGi desc, b.taxid
go

select x.domgi, (select accession from DomainGi where domgi = x.domgi) accession, count(x.taxid) as nTaxid, sum(x.nPig) as nPigTotal, sum(x.nGi) as nGiTotal from (
select a.domgi, b.taxid, count(distinct b.pig) as nPig, count(c.gi) as nGi
from cdart..DomainGi a with (NOLOCK) inner join cdart..HitDomgiVu b with (NOLOCK)
on a.domgi = b.domgi
inner join cdart..Gi2Nr c with (NOLOCK) on b.pig = c.pig
--where a.accession = 'pfam00385'
--where a.accession in ('pfam00352', 'pfam00385', 'pfam10536', 'TIGR00607', 'TIGR03687')
group by a.domgi, b.taxid
) x
group by x.domgi
order by accession
go




'pfam04432', 'TIGR2345', 'pfam02481', 'pfam12784' ,'pfam04432','pfam13175','pfam10339','pfam10341','pfam10342','TIGR02710'