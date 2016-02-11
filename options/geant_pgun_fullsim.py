from Gaudi.Configuration import *
from Configurables import ApplicationMgr, HepMCDumper, FCCDataSvc

podioevent = FCCDataSvc("EventDataSvc")

# reader = HepMCReader("Reader", Filename="example_MyPythia.dat")
# reader.DataOutputs.hepmc.Path = "hepmc"
from Configurables import ParticleGunAlg, MomentumRangeParticleGun, FlatSmearVertex#, Gaudi__ParticlePropertySvc
gen = ParticleGunAlg("ParticleGun", ParticleGunTool="MomentumRangeParticleGun", VertexSmearingToolPGun="FlatSmearVertex")
gen.DataOutputs.hepmc.Path = "hepmc"

from Configurables import Gaudi__ParticlePropertySvc
ppservice = Gaudi__ParticlePropertySvc("ParticlePropertySvc", ParticlePropertiesFile="/afs/cern.ch/lhcb/software/releases/GAUDI/GAUDI_v26r4/GaudiExamples/tests/data/ParticleTable.txt")

from Configurables import HepMCConverter
hepmc_converter = HepMCConverter("Converter")
hepmc_converter.DataInputs.hepmc.Path="hepmc"
hepmc_converter.DataOutputs.genparticles.Path="allGenParticles"
hepmc_converter.DataOutputs.genvertices.Path="allGenVertices"

from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc", detectors=['file:DetectorDescription/Detectors/compact/TestTracker.xml'],
                    OutputLevel = DEBUG)

from Configurables import G4SimSvc
geantservice = G4SimSvc("G4SimSvc", detector='G4DD4hepDetector', physicslist="G4FtfpBert",
                        actions="G4FullSimActions")

from Configurables import G4SimAlg, G4SaveTrackerHits, G4SaveCalHits
savetrackertool = G4SaveTrackerHits("G4SaveTrackerHits")
savetrackertool.DataOutputs.trackClusters.Path = "clusters"
savetrackertool.DataOutputs.trackHits.Path = "hits"
savetrackertool.DataOutputs.trackHitsClusters.Path = "hitClusterAssociation"
savehcaltool = G4SaveCalHits("G4SaveHCalHits", caloType = "HCal")
savehcaltool.DataOutputs.caloClusters.Path = "caloClusters"
savehcaltool.DataOutputs.caloHits.Path = "caloHits"
geantsim = G4SimAlg("G4SimAlg",
                        outputs= ["G4SaveTrackerHits/G4SaveTrackerHits", "G4SaveCalHits/G4SaveHCalHits"])
geantsim.DataInputs.genParticles.Path="allGenParticles"

from Configurables import PodioWrite, PodioOutput
out = PodioOutput("out",
                   OutputLevel=DEBUG)
out.outputCommands = ["keep *"]

ApplicationMgr( TopAlg = [gen, hepmc_converter, geantsim, out],
                EvtSel = 'NONE',
                EvtMax   = 1,
                ExtSvc = [podioevent, geoservice, geantservice, ppservice], # order! geo needed by geant
                OutputLevel=DEBUG
 )