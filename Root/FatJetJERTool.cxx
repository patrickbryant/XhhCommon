/******************************************
 *
 * Interface to FatJet JERTool
 *
 * Qi Zeng (qi.zeng@cern.ch)
 *
 *
 ******************************************/

// head file
#include "XhhCommon/FatJetJERTool.h"

// c++ include(s):
#include <iostream>

// EL include(s):
#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>

// EDM include(s):
#include "xAODEventInfo/EventInfo.h"
#include "xAODBase/IParticleHelpers.h"
#include "xAODBase/IParticleContainer.h"
#include "xAODBase/IParticle.h"
#include "AthContainers/ConstDataVector.h"
#include "AthContainers/DataVector.h"
#include "xAODCore/ShallowCopy.h"
#include "xAODCore/AuxContainerBase.h"

// package include(s):
#include "xAODAnaHelpers/HelperFunctions.h"

// ROOT include(s):
#include "TEnv.h"
#include "TSystem.h"

// this is needed to distribute the algorithm to the workers
ClassImp(FatJetJERTool)


// Only CINT or python configuration is supported
// TEnv configuration is not supported this moment
FatJetJERTool :: FatJetJERTool (std::string className) :
    Algorithm(className)
{
  // Here you put any code for the base initialization of variables,
  // e.g. initialize all pointers to 0.  Note that you should only put
  // the most basic initialization here, since this method will be
  // called on both the submission and the worker node.  Most of your
  // initialization code will go into histInitialize() and
  // initialize().

  Info("FatJetJERTool()", "Calling constructor");


  // Inheritted from base class
  m_debug                   = false;
  m_systName                = "Nominal";
  m_systVal                 = 0;

  // input/output jet container name
  m_inContainerName         = "";
  m_outContainerName        = "";

  // Truth Jet Container Name (in case of MC)
  m_TruthJetContainerName   = ""; // "AntiKt10TruthTrimmedPtFrac5SmallR20Jets";

  // jet algorithm
  m_jetAlgo                 = ""; // "AntiKt10LCTopoTrimmedPtFrac5SmallR20";

  // systematics name vector
  m_inputAlgo               = "";
  m_outputAlgo              = "";

  // configuration root file
  m_JERConfig               = "";

  // whether smearing is applied
  m_runJERSmearing          = false;

  // sort output jet contaienr
  m_sort                    = true;

  // user-defined seed for random number
  m_userSeed                = 0;

  // data/MC
  m_isMC                    = true;

  // name of deep copy container
  m_outDCContainerName      = "";
  m_outDCAuxContainerName   = "";

  // list of smearing types to be considered
  m_JERTypes                = {""};

  // actual configuration root file
  m_JERConfigFile           = 0;
  std::map<std::string, TH1*> dummy;
  m_JERConfigHists          = dummy;

  // random number generator
  m_random = TRandom3();
}


EL::StatusCode FatJetJERTool :: setupJob (EL::Job& job)
{
  // Here you put code that sets up the job on the submission object
  // so that it is ready to work with your algorithm, e.g. you can
  // request the D3PDReader service or add output files.  Any code you
  // put here could instead also go into the submission script.  The
  // sole advantage of putting it here is that it gets automatically
  // activated/deactivated when you add/remove the algorithm from your
  // job, which may or may not be of value to you.

  Info("setupJob()", "Calling setupJob");

  job.useXAOD ();
  xAOD::Init( "FatJetJERTool" ).ignore(); // call before opening first file

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode FatJetJERTool :: histInitialize ()
{
  // Here you do everything that needs to be done at the very
  // beginning on each worker node, e.g. create histograms and output
  // trees.  This method gets called before any input files are
  // connected.
  ANA_CHECK(xAH::Algorithm::algInitialize());
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode FatJetJERTool :: fileExecute ()
{
  // Here you do everything that needs to be done exactly once for every
  // single file, e.g. collect a list of all lumi-blocks processed

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode FatJetJERTool :: changeInput (bool /*firstFile*/)
{
  // Here you do everything you need to do when we change input files,
  // e.g. resetting branch addresses on trees.  If you are using
  // D3PDReader or a similar service this method is not needed.
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode FatJetJERTool :: initialize ()
{
  // Here you do everything that you need to do after the first input
  // file has been connected and before the first event is processed,
  // e.g. create additional histograms based on which variables are
  // available in the input files.  You can also create all of your
  // histograms and trees in here, but be aware that this method
  // doesn't get called if no events are processed.  So any objects
  // you create here won't be available in the output if you have no
  // input events.

  Info("initialize()", "Initializing FatJetJERTool Interface... ");

  m_event = wk()->xaodEvent();
  m_store = wk()->xaodStore();

  const xAOD::EventInfo* eventInfo(nullptr);
  ANA_CHECK(HelperFunctions::retrieve(eventInfo, m_eventInfoContainerName, m_event, m_store, msg()) );
  m_isMC = ( eventInfo->eventType( xAOD::EventInfo::IS_SIMULATION ) );

  // Interlock on m_isMC and m_runJERSmearing
  if(!m_isMC){
    Info("initialize()", "This is MC. No Jet Smearing will be run");
    m_runJERSmearing = false;
  }

  if(m_runJERSmearing){
    if(m_systName.compare("Nominal") == 0){
      m_JERTypes = {
        "JET_JMR",      // smearing on mass
        "JET_JER",      // smearing on pT
        "JET_JD2R",     // smearing on D2
      };

      m_systVal = 0;   // Lock on 0
    }
    else{
      Error("initialize()", "Undefined systematic name for FatJetJERTool %s. Only \"Nominal\" is supported now!", m_systName.c_str());
      return EL::StatusCode::FAILURE;
    }
  }
  else{
    m_JERTypes = {""};
  }

  m_outDCContainerName = m_outContainerName + "DeepCopy";
  m_outDCAuxContainerName = m_outDCContainerName + "Aux.";

  // Get Configuration file
  // Histograms are dynamically loaded in the flight
  std::string m_JERConfig_Expand = gSystem->ExpandPathName(m_JERConfig.c_str());
  m_JERConfigFile = TFile::Open(m_JERConfig_Expand.c_str());

  if(!m_JERConfigFile){
    Error("initialize()", "Unable to get JER configuration root file %s, expanded as %s.", m_JERConfig.c_str(), m_JERConfig_Expand.c_str());
    return EL::StatusCode::FAILURE;
  }

  std::map<std::string, TH1*> dummy;
  m_JERConfigHists = dummy;

  Info("initialize()", "Number of events in file: %lld ", m_event->getEntries() );

  return EL::StatusCode::SUCCESS;
}

// Workflow:
// inJets (should already have JES applied) --> deep copy for each kind of smearing --> apply smearing --> store the smeared jet collection --> append the smearing as systematic name to inputAlgo
EL::StatusCode FatJetJERTool :: execute ()
{
  // Here you do everything that needs to be done on every single
  // events, e.g. read input variables, apply cuts, and fill
  // histograms and trees.  This is where most of your actual analysis
  // code will go.

  if ( m_debug ) { Info("execute()", "Applying FatJet JER Smearing ... "); }

  // truth jet container
  const xAOD::JetContainer* truthJetContainer(nullptr);
  if(m_isMC){
    ANA_CHECK(HelperFunctions::retrieve(truthJetContainer, m_TruthJetContainerName, m_event, m_store, msg()));
  }

  // Initialize with existing systematics
  std::vector<std::string>* existingSystName(nullptr);
  ANA_CHECK(HelperFunctions::retrieve(existingSystName, m_inputAlgo, 0, m_store, msg()));

  // prepare all available systematics (existing ones + JER)
  std::vector<std::pair<std::string, bool> > systList;
  for(auto systName : *existingSystName){
    systList.push_back( std::make_pair(systName, true) );
  }
  for(auto systName : m_JERTypes){
    systList.push_back( std::make_pair(systName, false) );
  }

  std::vector<std::string>* vecOutContainerNames = new std::vector< std::string >;
  for(auto systNamePair : systList){
    std::string systName = systNamePair.first;
    bool    existingSyst = systNamePair.second;

    // No JER smearing at all
    if((!existingSyst) && (systName.empty())) continue;

    std::string outDCContainerName(m_outDCContainerName);
    std::string outDCAuxContainerName(m_outDCAuxContainerName);
    std::string outContainerName(m_outContainerName);

    outDCContainerName += systName;
    outDCAuxContainerName += systName;
    outContainerName += systName;
    vecOutContainerNames->push_back( systName );

    // get the input collection from TEvent or TStore
    std::string inContainerName(m_inContainerName);
    if(existingSyst) inContainerName += systName;
    const xAOD::JetContainer* inJets(nullptr);
    ANA_CHECK(HelperFunctions::retrieve(inJets, inContainerName, m_event, m_store, msg()) );

    // create deep copy
    xAOD::JetContainer* calibJetsDC = new xAOD::JetContainer();
    xAOD::AuxContainerBase* calibJetsDCAux = new xAOD::AuxContainerBase();
    calibJetsDC->setStore(calibJetsDCAux);

    // CDV
    ConstDataVector<xAOD::JetContainer>* calibJetsCDV = new ConstDataVector<xAOD::JetContainer>(SG::VIEW_ELEMENTS);
    calibJetsCDV->reserve( inJets->size() );

    for(auto jet : *inJets){
      // apply deep copy
      xAOD::Jet* newjet = new xAOD::Jet();
      calibJetsDC->push_back(newjet);
      *newjet = *jet;

      // apply the smearing now
      if(!existingSyst){
        const xAOD::Jet* MatchedTruthJet = getMatchedTruthJet(newjet, truthJetContainer);
        if(!applySmearing(newjet, MatchedTruthJet, systName)){
          Error("execute()", "Failure during \"applySmearing\" function");
          return EL::StatusCode::FAILURE;
        }
      }

      // store
      calibJetsCDV->push_back(newjet);
    }

    if(m_sort){
      std::sort(calibJetsCDV->begin(), calibJetsCDV->end(), HelperFunctions::sort_pt);
    }

    // add deep copy to TStore
    ANA_CHECK( m_store->record(calibJetsDC, outDCContainerName) );
    ANA_CHECK( m_store->record(calibJetsDCAux, outDCAuxContainerName)  );

    // add CDV to TStore
    ANA_CHECK( m_store->record(calibJetsCDV, outContainerName)  );
  }

  // store all systematics
  ANA_CHECK( m_store->record(vecOutContainerNames, m_outputAlgo) );

  if (m_debug){ m_store->print(); }

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode FatJetJERTool :: postExecute ()
{
  // Here you do everything that needs to be done after the main event
  // processing.  This is typically very rare, particularly in user
  // code.  It is mainly used in implementing the NTupleSvc.

  if ( m_debug ) { Info("postExecute()", "Calling postExecute"); }

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode FatJetJERTool :: finalize ()
{
  // This method is the mirror image of initialize(), meaning it gets
  // called after the last event has been processed on the worker node
  // and allows you to finish up any objects you created in
  // initialize() before they are written to disk.  This is actually
  // fairly rare, since this happens separately for each worker node.
  // Most of the time you want to do your post-processing on the
  // submission node after all your histogram outputs have been
  // merged.  This is different from histFinalize() in that it only
  // gets called on worker nodes that processed input events.

  Info("finalize()", "Finalizing FatJetJERTool ...");

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode FatJetJERTool :: histFinalize ()
{
  // This method is the mirror image of histInitialize(), meaning it
  // gets called after the last event has been processed on the worker
  // node and allows you to finish up any objects you created in
  // histInitialize() before they are written to disk.  This is
  // actually fairly rare, since this happens separately for each
  // worker node.  Most of the time you want to do your
  // post-processing on the submission node after all your histogram
  // outputs have been merged.  This is different from finalize() in
  // that it gets called on all worker nodes regardless of whether
  // they processed input events.

  Info("histFinalize()", "Calling histFinalize");
  ANA_CHECK(xAH::Algorithm::algFinalize());
  return EL::StatusCode::SUCCESS;
}

const xAOD::Jet* FatJetJERTool :: getMatchedTruthJet(const xAOD::Jet* jet, const xAOD::JetContainer* truthJetContainer)
{
  double dRCut = 0.8;   // hard-coded

  const xAOD::Jet* MatchedTruthJet = 0;
  double dRMatch = 9e9;
  for(auto truthjet : *truthJetContainer){
    double dR = truthjet->p4().DeltaR(jet->p4());
    if(dR > dRCut) continue;

    if(dR < dRMatch){
      dRMatch = dR;
      MatchedTruthJet = truthjet;
    }
  }

  return MatchedTruthJet;
}

bool FatJetJERTool :: applySmearing (xAOD::Jet* jet, const xAOD::Jet* truthjet, std::string JERType)
{
  if(truthjet == 0){
    if(jet->pt() > 250.e3){
      Info("applySmearing", "Unable to find matched truth jet for smearing, even the jet is above 250 GeV. This jet will be skipped.");
    }
    return true;
  }

  std::string HistKey("");
  if(JERType.compare("JET_JER") == 0){
    std::string MassBin = getMassBin(truthjet->m()/1000.);
    std::string HistKey = TString::Format("PtResponseResolution_vs_TruthPt_%s__BeforeCaloJetKinematicCut", MassBin.c_str()).Data();

    // get MC Resolution
    if(m_JERConfigHists.find(HistKey) == m_JERConfigHists.end()){
      m_JERConfigHists[HistKey] = (TH1*)(m_JERConfigFile->Get(HistKey.c_str()));
    }

    TH1* refHist = m_JERConfigHists[HistKey];
    if(!refHist){
      Warning("applySmearing()", "Unable to find histogram %s in JERConfig root file.", HistKey.c_str());
      return false;
    }

    double resolution = refHist->GetBinContent( getTruthPtBin(truthjet->pt()/1000.) );

    // assume an absolute 2% uncertainty on resolution
    double resolution_var = TMath::Sqrt(0.02 * (2*resolution + 0.02));
    double smearFactor = getSmearingFactor(jet, resolution_var);

    // apply smearing
    xAOD::JetFourMom_t p4 = jet->jetP4();
    jet->setJetP4( xAOD::JetFourMom_t(smearFactor * p4.Pt(), p4.Eta(), p4.Phi(), p4.M()) );
  }
  else if(JERType.compare("JET_JMR") == 0){
    std::string MassBin = getMassBin(truthjet->m()/1000.);
    std::string HistKey = TString::Format("MResponseResolution_vs_TruthPt_%s__BeforeCaloJetKinematicCut", MassBin.c_str()).Data(); 

    // get MC Resolution
    if(m_JERConfigHists.find(HistKey) == m_JERConfigHists.end()){
      m_JERConfigHists[HistKey] = (TH1*)(m_JERConfigFile->Get(HistKey.c_str()));
    }

    TH1* refHist = m_JERConfigHists[HistKey];
    if(!refHist){
      Warning("applySmearing()", "Unable to find histogram %s in JERConfig root file.", HistKey.c_str());
      return false;
    }

    double resolution = refHist->GetBinContent( getTruthPtBin(truthjet->pt()/1000.) );

    // assume a 20% relative uncertainty on resolution
    double resolution_var = TMath::Sqrt(1.2*1.2 - 1.*1.) * resolution;
    double smearFactor = getSmearingFactor(jet, resolution_var);

    // apply smearing
    xAOD::JetFourMom_t p4 = jet->jetP4();
    jet->setJetP4( xAOD::JetFourMom_t(p4.Pt(), p4.Eta(), p4.Phi(), smearFactor * p4.M()) );
  }
  else if(JERType.compare("JET_JD2R") == 0){
    std::string MassBin = getMassBin(truthjet->m()/1000.);
    std::string HistKey = TString::Format("D2ResponseResolution_vs_TruthPt_%s__BeforeCaloJetKinematicCut", MassBin.c_str()).Data(); 

    // get MC Resolution
    if(m_JERConfigHists.find(HistKey) == m_JERConfigHists.end()){
      m_JERConfigHists[HistKey] = (TH1*)(m_JERConfigFile->Get(HistKey.c_str()));
    }

    TH1* refHist = m_JERConfigHists[HistKey];
    if(!refHist){
      Warning("applySmearing()", "Unable to find histogram %s in JERConfig root file.", HistKey.c_str());
      return false;
    }

    double resolution = refHist->GetBinContent( getTruthPtBin(truthjet->pt()/1000.) );

    // assume a 15% relative uncertainty on resolution
    double resolution_var = TMath::Sqrt(1.15*1.15 - 1.*1.) * resolution;
    double smearFactor = getSmearingFactor(jet, resolution_var);

    // apply smearing
    // By definition of D2, we can simply apply the smearing on ECF3
    jet->auxdata<float>("ECF3") = smearFactor * jet->auxdata<float>("ECF3");
  }
  else{
    Warning("applySmearing()", "Undefined JERType %s. Unable to apply smearing on it.", JERType.c_str());
    return false;
  }

  return true;
}

// copied from JERSmearingTool
double FatJetJERTool :: getSmearingFactor(const xAOD::Jet* jet, double sigma)
{
  // Set the seed
  long int seed = m_userSeed;
  if(seed == 0) seed = 1.e+5*std::abs(jet->phi());
  m_random.SetSeed(seed);

  // Calculate the smearing factor
  double smear = m_random.Gaus(1.0, sigma);
  if(smear > 0) return smear;

  // If smear factor is negative, then retry the calculation
  int tries = 1;
  const int maxTries = 20;
  while(smear <= 0 && tries <= maxTries){
    smear = m_random.Gaus(1.0, sigma);
    tries++;
  }

  // If smear factor is still negative, something is wrong.
  if(smear <= 0){
    Warning("getSmearingFactor()", "Negative smear factor after %d tries. No smearing will be applied.", maxTries);
    smear = 1.;
  }

  return smear;
}

