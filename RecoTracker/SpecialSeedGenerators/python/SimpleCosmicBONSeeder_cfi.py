import FWCore.ParameterSet.Config as cms

from RecoTracker.SpecialSeedGenerators.CombinatorialSeedGeneratorForCosmics_cfi import layerInfo

def makeSimpleCosmicSeedLayers(*layers):
    layerList = cms.vstring()
    if 'ALL' in layers: 
        layers = [ 'TOB', 'TEC', 'TOBTEC', 'TECSKIP' ]
    if 'TOB' in layers:
        layerList += ['TOB4+TOB5+TOB6',
                      'TOB3+TOB5+TOB6',
                      'TOB3+TOB4+TOB5',
                      'TOB3+TOB4+TOB6',
                      'TOB2+TOB4+TOB5',
                      'TOB2+TOB3+TOB5']
    if 'TEC' in layers:
        TECwheelTriplets = [ (i,i+1,i+2) for i in range(7,0,-1)]
        layerList += [ 'TEC%d_pos+TEC%d_pos+TEC%d_pos' % ls for ls in TECwheelTriplets ]
        layerList += [ 'TEC%d_neg+TEC%d_neg+TEC%d_neg' % ls for ls in TECwheelTriplets ]
    if 'TECSKIP' in layers:
        TECwheelTriplets = [ (i-1,i+1,i+2) for i in range(7,1,-1)] + [ (i-1,i,i+2) for i in range(7,1,-1)  ]
        layerList += [ 'TEC%d_pos+TEC%d_pos+TEC%d_pos' % ls for ls in TECwheelTriplets ]
        layerList += [ 'TEC%d_neg+TEC%d_neg+TEC%d_neg' % ls for ls in TECwheelTriplets ]
    if 'TOBTEC' in layers:
        layerList += [ 'TOB6+TEC1_pos+TEC2_pos',
                       'TOB6+TEC1_neg+TEC2_neg',
                       'TOB6+TOB5+TEC1_pos',
                       'TOB6+TOB5+TEC1_neg' ]
    #print "SEEDING LAYER LIST = ", layerList
    return layerList
    

simpleCosmicBONSeeds = cms.EDProducer("SimpleCosmicBONSeeder",
    TTRHBuilder = cms.string('WithTrackAngle'),
    ClusterCheckPSet = cms.PSet(
            doClusterCheck = cms.bool(True),
            MaxNumberOfCosmicClusters = cms.uint32(300),
            ClusterCollectionLabel = cms.InputTag("siStripClusters"),
            DontCountDetsAboveNClusters = cms.uint32(0),  # if N > 0, ignore in total the dets with more than N clusters
    ),
    maxTriplets = cms.int32(50000),
    maxSeeds    = cms.int32(10000),
    RegionPSet = cms.PSet(
        originZPosition  = cms.double(0.0),
        originRadius     = cms.double(150.0),
        originHalfLength = cms.double(90.0),
        ptMin = cms.double(0.1),
    ),
    TripletsPSet = cms.PSet(
        layerInfo,
        layerList = makeSimpleCosmicSeedLayers('ALL'),
        debugLevel = cms.untracked.uint32(0),  # debug triplet finding (0 to 3)
    ),
    rescaleError    = cms.double(1),  # we don't need it anymore. At least for runs with BON
    seedOnMiddle    = cms.bool(False), # after finding the triplet, add only two hits to the seed

    ClusterChargeCheck = cms.PSet(
        checkCharge                 = cms.bool(False), # Apply cuts on cluster charge
        matchedRecHitsUseAnd        = cms.bool(True), # Both clusters in the pair should pass the charge cut
        Thresholds  = cms.PSet( # Uncorrected thresholds
            TIB = cms.int32(0), #
            TID = cms.int32(0), # FIXME: to be optimized
            TOB = cms.int32(0), # these are simple guesses from DQM of run 66615
            TEC = cms.int32(0), #
        ),
    ),
    HitsPerModuleCheck = cms.PSet(
        checkHitsPerModule = cms.bool(False), # Apply cuts on the number of hits per module 
        Thresholds  = cms.PSet( # 
            TIB = cms.int32(99999), #
            TID = cms.int32(99999), # FIXME: to be optimized
            TOB = cms.int32(99999), # 
            TEC = cms.int32(99999), #
        ),
    ),
    minimumGoodHitsInSeed = cms.int32(0),   # At least two high charge clusters in the seed
                                      
    writeTriplets   = cms.bool(False), # write the triplets to the Event as OwnVector<TrackingRecHit>
    helixDebugLevel = cms.untracked.uint32(0), # debug FastHelix (0 to 2)
    seedDebugLevel  = cms.untracked.uint32(0), # debug seed building (0 to 3)
)
simpleCosmicBONSeeds.TripletsPSet.TEC.useSimpleRphiHitsCleaner = False
