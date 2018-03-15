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
            list_forced_decays = cms.vstring('MyD+','MyD-'),
			user_decay_embedded= cms.vstring(
"""
Alias        MyD+                   D+
Alias        MyD-                   D-
ChargeConj   MyD-                   MyD+
Alias        Myphi                  phi
Decay MyD+
		1.000						Myphi			pi+			SVS;
Enddecay
CDecay MyD-
Decay Myphi
		1.000						K+				K-			VSS;			
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
            'PhaseSpace:pTHatMin = 0.', #min pthat
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CUEP8M1Settings',
            'processParameters',
        )
    )
)

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

DsDaufilter = cms.EDFilter("PythiaMomDauFilter",
    ParticleID = cms.untracked.int32(411),
    MomMinPt = cms.untracked.double(4.),
    MomMinEta = cms.untracked.double(-2.4),
    MomMaxEta = cms.untracked.double(2.4),
    DaughterIDs = cms.untracked.vint32(333, 211),
    NumberDaughters = cms.untracked.int32(2),
    DaughterID = cms.untracked.int32(333),
    DescendantsIDs = cms.untracked.vint32(321 , -321),
    NumberDescendants = cms.untracked.int32(2),
)
Dsrapidityfilter = cms.EDFilter("PythiaFilter",
      ParticleID = cms.untracked.int32(411),
                                  MinPt = cms.untracked.double(4.),
								  MaxPt = cms.untracked.double(500.),
								  MinRapidity = cms.untracked.double(-1.2),
								  MaxRapidity = cms.untracked.double(1.2),
								  )

ProductionFilterSequence = cms.Sequence(generator*DsDaufilter*Dsrapidityfilter)



