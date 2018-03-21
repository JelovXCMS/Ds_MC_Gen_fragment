

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
##            user_decay_file = cms.vstring('Run2Ana/lambdapkpi/data/lambdaC_kstar892_kpi.dec'),
            list_forced_decays = cms.vstring('MyD_s+','MyD_s-'),
			user_decay_embedded= cms.vstring(
"""
Alias        MyD_s+                 D_s+
Alias        MyD_s-                 D_s-
ChargeConj   MyD_s-                 MyD_s+
Alias        Myanti-K*0             anti-K*0
Alias        MyK*0                  K*0 
ChargeConj   MyK*0                  Myanti-K*0
Decay MyD_s+
		1.000           Myanti-K*0  K+      SVS;
Enddecay
CDecay MyD_s-
Decay Myanti-K*0
		1.000						K-				pi+			VSS;			
Enddecay
CDecay MyK*0
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
            'PhaseSpace:pTHatMin = 9', #min pthat
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
    ParticleID = cms.untracked.int32(5) # 4 for prompt D0 and 5 for non-prompt D0
    )

DsDaufilter = cms.EDFilter("PythiaMomDauFilter",
    ParticleID = cms.untracked.int32(431),
    MomMinPt = cms.untracked.double(19),
    MomMinEta = cms.untracked.double(-2.4),
    MomMaxEta = cms.untracked.double(2.4),
    DaughterIDs = cms.untracked.vint32(-313, 321),
    NumberDaughters = cms.untracked.int32(2),
    DaughterID = cms.untracked.int32(-313),
    DescendantsIDs = cms.untracked.vint32(-321 , 211),
    NumberDescendants = cms.untracked.int32(2),
)
Dsrapidityfilter = cms.EDFilter("PythiaFilter",
      ParticleID = cms.untracked.int32(431),
                                  MinPt = cms.untracked.double(19),
								  MaxPt = cms.untracked.double(500.),
								  MinRapidity = cms.untracked.double(-1.2),
								  MaxRapidity = cms.untracked.double(1.2),
								  )

ProductionFilterSequence = cms.Sequence(generator*partonfilter*DsDaufilter*Dsrapidityfilter)


