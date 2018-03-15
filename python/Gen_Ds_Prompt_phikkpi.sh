#!/bin/bash

 ptArr=(0 1.8 3.8 5.7 9.5 19)
 pthatArr=(0 0 0 2 3.5 9)
 ptnameArr=(pt0 pt1p8 pt3p8 pt5p7ph2 pt9p5ph3p5 pt19ph9)


 #DataSetNam=Ds_Prompt_phikkpi_pt1p8_cfg.py
 Channel=phikkpi
 PNP=Prompt
 PNParton=4


for idx in {0..5}  #start from 0
do

echo pt=${ptArr[${idx}]}
echo pthat=${pthatArr[${idx}]}

echo filename= Ds_${PNP}_${Channel}_${ptnameArr[${idx}]}_cfg.py

cat > Ds_${PNP}_${Channel}_${ptnameArr[${idx}]}_cfg.py <<EOF
import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(5020.0),
    maxEventsToPrint = cms.untracked.int32(0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2010.DEC'),
            operates_on_particles = cms.vint32(),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt.pdl'),
            list_forced_decays = cms.vstring('MyD_s+','MyD_s-'),
      user_decay_embedded= cms.vstring(
"""
Alias        MyD_s+                 D_s+
Alias        MyD_s-                 D_s-
ChargeConj   MyD_s-                 MyD_s+
Alias        Myphi                  phi
Decay MyD_s+
    1.000           Myphi     pi+     SVS;
Enddecay
CDecay MyD_s-
Decay Myphi
    1.000           K+        K-      VSS;
Enddecay
End
"""
       )


        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
            'HardQCD:all = on',
            'PhaseSpace:pTHatMin = ${pthatArr[${idx}]}', #min pthat
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CUEP8M1Settings',
            'processParameters',
        )
    )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

partonfilter = cms.EDFilter("PythiaFilter",
    ParticleID = cms.untracked.int32(${PNParton}) # 4 for prompt D0 and 5 for non-prompt D0
    )

DsDaufilter = cms.EDFilter("PythiaMomDauFilter",
    ParticleID = cms.untracked.int32(431),
    MomMinPt = cms.untracked.double(${ptArr[${idx}]}),
    MomMinEta = cms.untracked.double(-2.4),
    MomMaxEta = cms.untracked.double(2.4),
    DaughterIDs = cms.untracked.vint32(333, 211),
    NumberDaughters = cms.untracked.int32(2),
    DaughterID = cms.untracked.int32(333),
    DescendantsIDs = cms.untracked.vint32(321 , -321),
    NumberDescendants = cms.untracked.int32(2),
)
Dsrapidityfilter = cms.EDFilter("PythiaFilter",
      ParticleID = cms.untracked.int32(431),
                                  MinPt = cms.untracked.double(${ptArr[${idx}]}),
                  MaxPt = cms.untracked.double(500.),
                  MinRapidity = cms.untracked.double(-1.2),
                  MaxRapidity = cms.untracked.double(1.2),
                  )

ProductionFilterSequence = cms.Sequence(generator*partonfilter*DsDaufilter*Dsrapidityfilter)

EOF

done
