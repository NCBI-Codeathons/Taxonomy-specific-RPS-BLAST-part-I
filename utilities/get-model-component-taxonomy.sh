#!/bin/bash
# get-model-component-taxonomy.sh: Retrieve the model's component taxonomy
#
# Created: Thu Oct 17 13:32:34 2019

export PATH=/opt/sybase/utils/bin:/bin:/usr/bin
set -euo pipefail
shopt -s nullglob

if [ $# -ne 3 ] ; then
    echo "Usage: $0 <domain ID> <username> <password>"
    exit 1
fi

MODEL=${1}
U=${2:-$USER}
P=${3:-""}
SERVER=dddsql50
DB=cdart
 
sqsh-ms -mbcp -S $SERVER -D $DB -U $U -P $P -o $MODEL-components.tsv <<EOF
\set bcp_colsep="\t"
\set bcp_rowsep=""
select a.domgi, (select accession from DomainGi where domgi = a.domgi) accession, 
b.taxid, (select orgname from cdart..Tax where taxid = b.taxid) as taxOrg, 
count(distinct b.pig) as nPig, count(c.gi) as nGi
from cdart..DomainGi a with (NOLOCK) inner join cdart..HitDomgiVu b with (NOLOCK)
on a.domgi = b.domgi
inner join cdart..Gi2Nr c with (NOLOCK) on b.pig = c.pig
where a.accession = '$MODEL'
group by a.domgi, b.taxid
order by accession, nPig desc, nGi desc, b.taxid
go
EOF
