#!/bin/bash
set -e
if [ -n "${DEV_PBP}" ]; then

    PTK=./pbp/ptk
    KERNEL=./pbp/kernel
    DAS=./pbp/das
    TAS=./pbp/tas
    T2T=./pbp/t2t

    rm -rf pbp
    mkdir -p ${PTK} ${KERNEL} ${DAS} ${TAS} ${T2T}

    cp ~/projects/zd/kernel0d.py ${KERNEL}/kernel0d.py
    cp ~/projects/rt/stubbed-out-repl.py ${KERNEL}/repl.py
    cp ~/projects/0D/das2json/das2json.mjs ${DAS}/das2json.mjs
    cp ~/projects/t2t/nanodsl .${T2T}
    chmod a+x ${T2T}/nanodsl
    cp -R ~/projects/t2t/lib ${T2T}

    RT=~/projects/rt
    cp ${RT}/cldecode.{ohm,rewrite} ${TAS}
    cp ${RT}/cleanup.py ${TAS}
    cp ${RT}/clindenter.mjs ${TAS}
    cp ${RT}/clmvline.py ${TAS}
    cp ${RT}/clrelocate.py ${TAS}
    cp ${RT}/emit.ohm ${TAS}
    cp ${RT}/emitPython.rewrite ${TAS}
    cp ${RT}/emitcl.rewrite ${TAS}
    cp ${RT}/emitjs.rewrite ${TAS}
    cp ${RT}/empty.rt ${TAS}
    cp ${RT}/errgrep.py ${TAS}
    cp ${RT}/indenter.mjs ${TAS}
    cp ${RT}/internalize.{ohm,rewrite} ${TAS}
    cp ${RT}/jsdecode.{ohm,rewrite} ${TAS}
    cp ${RT}/jsindenter.mjs ${TAS}
    cp ${RT}/jsrelocate.py ${TAS}
    cp ${RT}/main.py ${TAS}
    cp ${RT}/pydecode.{ohm,rewrite} ${TAS}
    cp ${RT}/pyrelocate.py ${TAS}
    cp ${RT}/rt2all.drawio.json ${TAS}
    cp ${RT}/semantics.{ohm,rewrite} ${TAS}
    cp ${RT}/support.js ${TAS}
    cp ${RT}/syntax.{ohm,rewrite} ${TAS}
    cp ${RT}/unencode.mjs ${TAS}

    cp ${RT}/ndsl ${TAS}
    chmod a+x ${TAS}/ndsl
fi
