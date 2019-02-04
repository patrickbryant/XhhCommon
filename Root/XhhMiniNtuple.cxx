#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include <xAODJet/JetContainer.h>
#include <xAODTracking/VertexContainer.h>
#include <xAODEventInfo/EventInfo.h>
#include <AthContainers/ConstDataVector.h>
#include <SampleHandler/MetaFields.h>


#include "xAODParticleEvent/ParticleContainer.h"

#include <xAODAnaHelpers/HelpTreeBase.h>
#include <XhhCommon/XhhMiniNtuple.h>
#include <XhhCommon/Helpers.h>

#include <xAODAnaHelpers/HelperFunctions.h>
#include <xAODAnaHelpers/HelperClasses.h>

#include "TEnv.h"
#include "TSystem.h"

//#define DEBUG std::cerr << __FILE__ << "::" << __LINE__ << std::endl
 
// this is needed to distribute the algorithm to the workers
ClassImp(XhhMiniNtuple)

using std::cout;  using std::endl;
using std::string; using std::vector;

XhhMiniNtuple :: XhhMiniNtuple () :
  m_name(""),
  m_writeAll(false),
  m_cutflowHist(0),
  m_cutflowHistW(0),
  m_cutflowFirst(0),
  m_iCutflow(0),
  m_isMC(false),
  m_resolvedJetsName(""),
  m_boostedHcandName(""),
  m_jetCleaningName("EMTopoJetCleaning"),
  m_evtDetailStr(""),
  m_trigDetailStr(""),
  m_resolvedJetDetailStr(""),
  m_boostedJetDetailStr(""),
  m_truthDetailStr(""),
  m_inCaloJetName(""),
  m_inTrackJetName(""),
  m_inTruthParticleName(""),
  m_muonContainerName(""),
  m_muonDetailStr(""),
  m_elecContainerName(""),
  m_elecDetailStr(""),
  m_metContainerName(""),
  m_metDetailStr(""),
  m_doResolutionStudy(false),
  m_debug(false), 
  m_doXhhTagging(false),     //defualt turned off!
  m_doFatJetMassCut(true),
  m_FatJetMassCut(40.),     // in GeV
  m_FatJetPtSkimCut(400.),  // in GeV
  m_TrackJetWP("70"),
  m_storeLeptonVeto(false),
  m_storeMETVeto(false),
  m_storeTruth(true),
  m_doResolved(true),
  m_doLeptop(true),
  m_doBoosted(true),
  m_eventCuts(""),
  m_resolvedSysName(""),
  m_boostedSysName(""),
  m_weight(1.0),
  m_weight_mhh(1.0),
  m_weight_xs(1.0),
  m_cleanEvent(1.0)
{
  this->SetName("XhhMiniNtuple"); // needed if you want to retrieve this algo with wk()->getAlg(ALG_NAME) downstream
}

EL::StatusCode XhhMiniNtuple :: setupJob (EL::Job& job)
{
  Info("setupJob()", "Calling setupJob \n");
  job.useXAOD();
  xAOD::Init("XhhMiniNtuple").ignore();

  EL::OutputStream outForTree(m_name.c_str());
  job.outputAdd (outForTree);
  Info("setupJob()", "Ready\n");

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhMiniNtuple :: initialize ()
{
  Info("initialize()", m_name.c_str());
  m_event = wk()->xaodEvent();
  m_store = wk()->xaodStore();

  if(m_debug) Info("initialize()", "after add store");
  //if (m_resolvedSysName.empty() && m_boostedSysName.empty()) this->AddTree("");

  //string recs_file = "$ROOTCOREBIN/data/JetSubStructureUtils/config_13TeV_20150710_Htagging.dat"; //this one is old
  string recs_file = "$ROOTCOREBIN/data/JetSubStructureUtils/config_13TeV_Htagging_MC15_Prerecommendations_20150812.dat";
  if (m_doXhhTagging) {

    //H tagging
    //m_BoostedXbbTagger = new BoostedXbbTagger( "BoostedXbbTagger" );
    //m_BoostedXbbTagger->setProperty( "ConfigFile", "XbbTagger/XbbTagger_AntiKt10LCTopoTrimmed_1BTag_MC15c_20161118.dat");
    //ANA_CHECK( m_BoostedXbbTagger->initialize());
    //
    //// old V-tagging tool
    //m_WbosonTaggerMedium = new JetSubStructureUtils::BosonTag("medium", "smooth", "$ROOTCOREBIN/data/JetSubStructureUtils/config_13TeV_Wtagging_MC15_Prerecommendations_20150809.dat", false, false);
    //m_ZbosonTaggerMedium = new JetSubStructureUtils::BosonTag("medium", "smooth", "$ROOTCOREBIN/data/JetSubStructureUtils/config_13TeV_Ztagging_MC15_Prerecommendations_20150809.dat", false, false);
    //
    //m_WbosonTaggerTight = new JetSubStructureUtils::BosonTag("tight", "smooth", "$ROOTCOREBIN/data/JetSubStructureUtils/config_13TeV_Wtagging_MC15_Prerecommendations_20150809.dat", false, false);
    //m_ZbosonTaggerTight = new JetSubStructureUtils::BosonTag("tight", "smooth", "$ROOTCOREBIN/data/JetSubStructureUtils/config_13TeV_Ztagging_MC15_Prerecommendations_20150809.dat", false, false);
    //
    //// new V-tagging tool
    //m_smoothedWTagger_50 = new SmoothedWZTagger("SmoothedWTagger_50");
    //m_smoothedWTagger_50->setProperty("ConfigFile", "SmoothedWZTaggers/SmoothedContainedWTagger_AntiKt10LCTopoTrimmed_FixedSignalEfficiency50_MC15c_20161215.dat");
    //ANA_CHECK( m_smoothedWTagger_50->initialize());
    //
    //m_smoothedZTagger_50 = new SmoothedWZTagger("SmoothedZTagger_50");
    //m_smoothedZTagger_50->setProperty("ConfigFile", "SmoothedWZTaggers/SmoothedContainedZTagger_AntiKt10LCTopoTrimmed_FixedSignalEfficiency50_MC15c_20161215.dat");
    //ANA_CHECK( m_smoothedZTagger_50->initialize());
    //
    //m_smoothedWTagger_80 = new SmoothedWZTagger("SmoothedWTagger_80");
    //m_smoothedWTagger_80->setProperty("ConfigFile", "SmoothedWZTaggers/SmoothedContainedWTagger_AntiKt10LCTopoTrimmed_FixedSignalEfficiency80_MC15c_20161215.dat");
    //ANA_CHECK( m_smoothedWTagger_80->initialize());
    //
    //m_smoothedZTagger_80 = new SmoothedWZTagger("SmoothedZTagger_80");
    //m_smoothedZTagger_80->setProperty("ConfigFile", "SmoothedWZTaggers/SmoothedContainedZTagger_AntiKt10LCTopoTrimmed_FixedSignalEfficiency80_MC15c_20161215.dat");
    //ANA_CHECK( m_smoothedZTagger_80->initialize());
  }


  m_hhWeightTool = new xAOD::hhWeightTool("hhWeights");
  m_hhWeightTool->initialize();

  if(m_debug) Info("initialize()", "after rec file");

  //
  // Set isMC flag
  //
  const xAOD::EventInfo* eventInfo(nullptr);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store, msg()));
  m_isMC = ( eventInfo->eventType( xAOD::EventInfo::IS_SIMULATION ) ) ? true : false;

  //
  // Interlock on m_doResolutionStudy
  //
  if(!m_isMC) m_doResolutionStudy = false;
 
  //
  // Cut Flow 
  //
  TFile *file = wk()->getOutputFile("cutflow");
  m_cutflowHist  = (TH1D*)file->Get("cutflow");
  m_cutflowHistW = (TH1D*)file->Get("cutflow_weighted");

  m_cutflowFirst = m_cutflowHist->GetXaxis()->FindBin("XhhMiniTreeAll");
  m_cutflowHistW->GetXaxis()->FindBin("XhhMiniTreeAll");

  m_cutflowHist ->GetXaxis()->FindBin("XhhMiniTreePreSel");
  m_cutflowHistW->GetXaxis()->FindBin("XhhMiniTreePreSel");

  if(m_debug) Info("initialize()", "left");
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhMiniNtuple::AddTree(string syst = "")
{
  Info("AddTree()", "%s", m_name.c_str() );
  // needed here and not in initalize since this is called first

  string treeName = "XhhMiniNtuple";
  if (!syst.empty()) treeName += syst;
  TTree * outTree = new TTree(treeName.c_str(), treeName.c_str());
  if( !outTree ) {
    Error("AddTree()","Failed to instantiate output tree!");
    return EL::StatusCode::FAILURE;
  }

  // get the file we created already
  TFile* treeFile = wk()->getOutputFile( m_name.c_str() );
  outTree->SetDirectory( treeFile );


  m_helpTree[syst] = new HelpTreeBase( m_event, outTree, treeFile );

  // if want to add to same file as ouput histograms
  // wk()->addOutput( outTree );

  m_helpTree[syst]->AddEvent(m_evtDetailStr);
  m_helpTree[syst]->AddTrigger(m_trigDetailStr);

  m_helpTree[syst]->AddJets   (m_resolvedJetDetailStr,    "resolvedJets");
  m_helpTree[syst]->AddFatJets(m_boostedJetDetailStr,     "boostedJets");

  if(!m_muonContainerName.empty())
    m_helpTree[syst]->AddMuons(m_muonDetailStr);

  if(!m_elecContainerName.empty())
    m_helpTree[syst]->AddElectrons(m_elecDetailStr);

  if(!m_metContainerName.empty())
    m_helpTree[syst]->AddMET(m_metDetailStr);

  // Truth particles
  if(!m_inTruthParticleName.empty() && m_isMC){
    m_helpTree[syst]->AddTruthParts("truth", m_truthDetailStr);
    outTree->Branch("truth_mtt",             &b_truth_mtt, "truth_mtt/D");
  }


  // Higgs candidates from boosted selection
  outTree->Branch("hcand_boosted_n", &b_hcand_boosted_n, "hcand_boosted_n/I");
  outTree->Branch("hcand_boosted_pt", &b_hcand_boosted_pt);
  outTree->Branch("hcand_boosted_ptcalo", &b_hcand_boosted_ptcalo);
  outTree->Branch("hcand_boosted_ptTA", &b_hcand_boosted_ptTA);
  outTree->Branch("hcand_boosted_eta", &b_hcand_boosted_eta);
  outTree->Branch("hcand_boosted_etacalo", &b_hcand_boosted_etacalo);
  outTree->Branch("hcand_boosted_etaTA", &b_hcand_boosted_etaTA);
  outTree->Branch("hcand_boosted_phi", &b_hcand_boosted_phi);
  outTree->Branch("hcand_boosted_phicalo", &b_hcand_boosted_phicalo);
  outTree->Branch("hcand_boosted_phiTA", &b_hcand_boosted_phiTA);
  outTree->Branch("hcand_boosted_m", &b_hcand_boosted_m);
  outTree->Branch("hcand_boosted_mcalo", &b_hcand_boosted_mcalo);
  outTree->Branch("hcand_boosted_mTA", &b_hcand_boosted_mTA);
  outTree->Branch("hcand_boosted_htag", &b_hcand_boosted_htag);
  outTree->Branch("hcand_boosted_htag_muoncor_pt", &b_hcand_boosted_htag_muoncor_pt);
  outTree->Branch("hcand_boosted_htag_muoncor_eta", &b_hcand_boosted_htag_muoncor_eta);
  outTree->Branch("hcand_boosted_htag_muoncor_phi", &b_hcand_boosted_htag_muoncor_phi);
  outTree->Branch("hcand_boosted_htag_muoncor_m", &b_hcand_boosted_htag_muoncor_m);
  outTree->Branch("hcand_boosted_htag_loose", &b_hcand_boosted_htag_loose);
  outTree->Branch("hcand_boosted_htag_medium", &b_hcand_boosted_htag_medium);
  outTree->Branch("hcand_boosted_htag_tight", &b_hcand_boosted_htag_tight);
  outTree->Branch("hcand_boosted_Wtag_medium", &b_hcand_boosted_Wtag_medium);
  outTree->Branch("hcand_boosted_Ztag_medium", &b_hcand_boosted_Ztag_medium);
  outTree->Branch("hcand_boosted_Wtag_tight", &b_hcand_boosted_Wtag_tight);
  outTree->Branch("hcand_boosted_Ztag_tight", &b_hcand_boosted_Ztag_tight);
  outTree->Branch("hcand_boosted_smoothWtag_50", &b_hcand_boosted_smoothWtag_50);
  outTree->Branch("hcand_boosted_smoothZtag_50", &b_hcand_boosted_smoothZtag_50);
  outTree->Branch("hcand_boosted_smoothWtag_80", &b_hcand_boosted_smoothWtag_80);
  outTree->Branch("hcand_boosted_smoothZtag_80", &b_hcand_boosted_smoothZtag_80);
  outTree->Branch("hcand_boosted_dRjj", &b_hcand_boosted_dRjj);
  outTree->Branch("hcand_boosted_C2", &b_hcand_boosted_C2);
  outTree->Branch("hcand_boosted_D2", &b_hcand_boosted_D2);
  outTree->Branch("hcand_boosted_Tau21", &b_hcand_boosted_Tau21);
  outTree->Branch("hcand_boosted_Tau21WTA", &b_hcand_boosted_Tau21WTA);
  outTree->Branch("hcand_boosted_nTrack", &b_hcand_boosted_nTrack);
  outTree->Branch("hcand_boosted_nHBosons", &b_hcand_boosted_nHBosons);
  outTree->Branch("hcand_boosted_nWBosons", &b_hcand_boosted_nWBosons);
  outTree->Branch("hcand_boosted_nZBosons", &b_hcand_boosted_nZBosons);

  outTree->Branch("jet_ak2track_asso_n", &b_jet_ak2track_asso_n);
  outTree->Branch("jet_ak2track_asso_n_addl", &b_jet_ak2track_asso_n_addl);
  outTree->Branch("jet_ak2track_asso_pt", &b_jet_ak2track_asso_pt);
  outTree->Branch("jet_ak2track_asso_eta", &b_jet_ak2track_asso_eta);
  outTree->Branch("jet_ak2track_asso_phi", &b_jet_ak2track_asso_phi);
  outTree->Branch("jet_ak2track_asso_m", &b_jet_ak2track_asso_m);
  outTree->Branch("jet_ak2track_asso_MV2c00", &b_jet_ak2track_asso_MV2c00);
  outTree->Branch("jet_ak2track_asso_MV2c10", &b_jet_ak2track_asso_MV2c10);
  outTree->Branch("jet_ak2track_asso_MV2c20", &b_jet_ak2track_asso_MV2c20);
  outTree->Branch("jet_ak2track_asso_MV2c100", &b_jet_ak2track_asso_MV2c100);
  outTree->Branch("jet_ak2track_asso_sys", &b_jet_ak2track_asso_sys);
  outTree->Branch("jet_ak2track_asso_sysname", &b_jet_ak2track_asso_sysname);
  outTree->Branch("boosted_bevent_sys", &b_boosted_bevent_sys);

  outTree->Branch("truth_hcand_boosted_n", &b_truth_hcand_boosted_n, "truth_hcand_boosted_n/I");
  outTree->Branch("truth_hcand_boosted_match", &b_truth_hcand_boosted_matched);
  outTree->Branch("truth_hcand_boosted_pt", &b_truth_hcand_boosted_pt);
  outTree->Branch("truth_hcand_boosted_eta", &b_truth_hcand_boosted_eta);
  outTree->Branch("truth_hcand_boosted_phi", &b_truth_hcand_boosted_phi);
  outTree->Branch("truth_hcand_boosted_m", &b_truth_hcand_boosted_m);
  outTree->Branch("truth_hcand_boosted_c2", &b_truth_hcand_boosted_c2);
  outTree->Branch("truth_hcand_boosted_d2", &b_truth_hcand_boosted_d2);

  if(m_storeLeptonVeto){
    outTree->Branch("n_muons_veto", &b_n_muons_veto, "n_muons_veto/I");
    outTree->Branch("n_electrons_veto", &b_n_electrons_veto, "n_electrons_veto/I");
    outTree->Branch("event_cleaning_qqbb", &b_event_cleaning_qqbb, "event_cleaning_qqbb/O");
  }

  if(m_storeMETVeto){
    outTree->Branch("METsum", &b_METsum, "METsum/D");
    outTree->Branch("METphi", &b_METphi, "METphi/D");
  }

  outTree->Branch("passedEmulatedTriggers",       &m_passEmulatedTriggers        );

  // outTree->Branch("passed_cuts", &b_passed_cuts);
  // outTree->Branch("decay_match_ind", &b_decay_match_ind);

  outTree->Branch("weight",      &m_weight,     "weight/F"      );
  outTree->Branch("weight_mhh",  &m_weight_mhh, "weight_mhh/F"  );
  outTree->Branch("weight_xs",   &m_weight_xs,  "weight_xs/F"   );
  outTree->Branch("cleanEvent",  &m_cleanEvent, "cleanEvent/F"  );
    

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhMiniNtuple :: histInitialize () { return EL::StatusCode::SUCCESS; }
EL::StatusCode XhhMiniNtuple :: fileExecute    () { return EL::StatusCode::SUCCESS; }
EL::StatusCode XhhMiniNtuple :: changeInput    (bool /*firstFile*/) { return EL::StatusCode::SUCCESS; }

EL::StatusCode XhhMiniNtuple::execute ()
{

  const xAOD::EventInfo* eventInfo(0);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store));
  //
  // JZXW Pile-up Fluctuation Killer
  //
  if(m_isMC && (killPileupFluctuation() != 1)) return EL::StatusCode::SUCCESS;

  // 
  // For the cut flow
  //
  m_iCutflow = m_cutflowFirst;

  //
  // Set this first, as it's needed by passCut()
  //
  if(m_isMC){
    m_mcEventWeight = eventInfo->mcEventWeight();
  }  else{
    m_mcEventWeight = 1;
  }

  if (m_resolvedSysName.empty() && m_boostedSysName.empty()) {

    executeSingle("", "", true);

    //
    // Do Systematics
    //
  } else{

    //
    // Do Nominal
    //   (do the cut flow calculation here)
    //
    executeSingle("", "", true);

    //
    // Do Resolved Systematics
    //
    if(!m_resolvedSysName.empty()){

      // get vector of string giving the names
      vector<string>* resolvedSystNames(nullptr);
      ANA_CHECK( HelperFunctions::retrieve(resolvedSystNames, m_resolvedSysName, 0, m_store, msg()) );
    
      // Loop over resolved systematics 
      for ( string& resSystName : *resolvedSystNames ) {
      
	if(resSystName.empty()) continue;

	if(m_debug) Info("execute",  "systName %s", resSystName.c_str());

	executeSingle(resSystName, "", false);
	
      }
    }

    //
    // Do Boosted Systematics
    //
    if(!m_boostedSysName.empty()){

      // get vector of string giving the names
      vector<string>* boostedSystNames(nullptr);
      ANA_CHECK( HelperFunctions::retrieve(boostedSystNames, m_boostedSysName, 0, m_store, msg()) );
    
      // Loop over resolved systematics 
      for ( string& boostSystName : *boostedSystNames ) {
      
	if(boostSystName.empty()) continue;

	if(m_debug) Info("execute",  "systName %s", boostSystName.c_str());

	executeSingle("", boostSystName, false);
	
      }

    }

  }
  
  return EL::StatusCode::SUCCESS;

}

EL::StatusCode XhhMiniNtuple::executeSingle(string resolvedSys, string boostedSys, bool countEvents) {
  if(m_debug) cout << " In executeSingle"  << resolvedSys << " " << boostedSys << endl;

  //
  //  Count All Events
  //
  if(countEvents) passCut(); 
  
  //
  // Start with stuff which is common to boosted and resolved
  //
  string syst = "";
  if(!resolvedSys.empty()) syst = "Resolved_"+resolvedSys;
  if(!boostedSys.empty())  syst = "Boosted_" +boostedSys;

  if( m_helpTree.find( syst ) == m_helpTree.end() ) { AddTree( syst ); }

  const xAOD::EventInfo* eventInfo(0);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store));
  
  const xAOD::VertexContainer* vertices(0);
  ANA_CHECK( HelperFunctions::retrieve(vertices, "PrimaryVertices", m_event, m_store));

  const xAOD::Vertex *pv = 0;
  pv = vertices->at( HelperFunctions::getPrimaryVertexLocation( vertices ) );


  // Retrieve the container of Higgs candidate from boosted selection
  const xAOD::ParticleContainer* boostedHCands(0);
  if(m_debug) cout << " Getting boosted H candidates: "  << m_boostedHcandName+boostedSys << endl;  
  ANA_CHECK( HelperFunctions::retrieve(boostedHCands, m_boostedHcandName+boostedSys, m_event, m_store));  

  // Retrieve the container of resolved jets
  const xAOD::JetContainer* resolvedJets(0);
  if(m_debug) cout << " Getting resolved Jets: "  << m_resolvedJetsName+resolvedSys << endl;  
  ANA_CHECK( HelperFunctions::retrieve(resolvedJets, m_resolvedJetsName+resolvedSys, m_event, m_store));  

  // Retrieve the container of Prompt Muons
  const xAOD::MuonContainer* promptMuons(nullptr);
  if(m_debug) cout << " Getting prompt muons: "  << m_promptMuonContainerName << endl;  
  ANA_CHECK( HelperFunctions::retrieve(promptMuons, m_promptMuonContainerName, m_event, m_store) );

  // Retrieve the container of Prompt Electrons
  const xAOD::ElectronContainer* electrons(nullptr);
  if(m_debug) cout << " Getting prompt electrons: "  << m_elecContainerName << endl;  
  ANA_CHECK( HelperFunctions::retrieve(electrons, m_elecContainerName, m_event, m_store) );

  // Retrieve the container of truth fat-jet (MC only, hard-coded in)
  if(m_debug) cout << " Getting AntiKt10TruthTrimmedPtFrac5SmallR20Jets" << endl;
  const xAOD::JetContainer* truthFatJet(0);
  if(m_isMC){
    ANA_CHECK( HelperFunctions::retrieve(truthFatJet, "AntiKt10TruthTrimmedPtFrac5SmallR20Jets", m_event, m_store));
  }


  //
  // Count the number of resolved bjets 
  //
  unsigned int nResolvedBTags = 0;
  for(const xAOD::Jet* jet : *resolvedJets) {
    if((bool)(jet->auxdecor< char >("isBJet"))) ++nResolvedBTags;
  }

  //
  // Count the boosted jet kinematics
  //
  unsigned int nBoostedJetPassMCut  = 0;
  unsigned int nBoostedJetPassPtCut = 0;
  for(auto hcand : *boostedHCands) {
    const xAOD::Jet* fatJet = hcand->auxdecor< const xAOD::Jet* >("caloJet");
    if(fatJet) {
      if((!m_doFatJetMassCut) || (fatJet->m()  >  m_FatJetMassCut*1000)) nBoostedJetPassMCut++;
      if(fatJet->pt() > m_FatJetPtSkimCut*1000) nBoostedJetPassPtCut++;
    }
  }

  //
  //  only fill ntup if:
  //    - 2 resolved predijets and 2 bjets
  //    - 2 fatjets, 1 jet with pt > 300 GeV
  //    - 1 leptop, 1 prompt muon and 2 bjets
  //
  bool PassResolvedNJets      = (resolvedJets->size()      > 3);
  bool PassResolvedNBJets     = (nResolvedBTags            > 1);

  bool PassNPromptLeptons     = ((promptMuons->size()       > 0) || (electrons->size() > 0));

  bool PassBoostedNHCands     = (boostedHCands->size()     > 1);
  bool PassBoostedHCandM      = (nBoostedJetPassMCut       > 1);
  bool PassBoostedHCandPt     = (nBoostedJetPassPtCut      > 0);

  bool PassResolvedPreSel    = PassResolvedNJets      && PassResolvedNBJets && m_doResolved;
  bool PassBoostedPreSel     = PassBoostedNHCands     && PassBoostedHCandPt && PassBoostedHCandM && m_doBoosted;

  //turn off the leptop seleciton for now
  bool PassLepTopPreSel      = PassNPromptLeptons &&   (resolvedJets->size() > 1) && m_doLeptop;
  bool PassLepTopBoosted     = PassNPromptLeptons &&   (boostedHCands->size() > 0) && m_doLeptop;

  if(m_debug){ 
    cout << "Run/Event " << eventInfo->runNumber() << " / " << eventInfo->eventNumber() << endl;
  }

  if(m_debug){ 
    cout << " PassResolvedPreSel: "  << PassResolvedPreSel << endl;  
    cout << "\t nResolvedBTags: " << nResolvedBTags << endl;
    cout << "\t resolvedJets->size(): " << resolvedJets->size() << endl;
    cout << " PassBoostedPreSel: "  << PassBoostedPreSel << endl;  
  }

  if (!m_writeAll){
    if(!PassResolvedPreSel && !PassBoostedPreSel && !PassLepTopPreSel && !PassLepTopBoosted) return EL::StatusCode::SUCCESS;
  }
  if(m_debug) cout << " Pass XhhPresection: "  << endl;  
  
  //
  //  Count All Events
  //
  if(countEvents) passCut(); 

  //
  // Fill Event info
  //
  if(m_debug) cout << " Filling event " << endl;  
  m_helpTree[syst]->FillEvent( eventInfo );

  double xs            = wk()->metaData()->castDouble(SH::MetaFields::crossSection    ,1); 
  double filtEff       = wk()->metaData()->castDouble(SH::MetaFields::filterEfficiency,1); 

  m_weight_xs = xs * filtEff;
  m_weight    = m_mcEventWeight * xs * filtEff;

  //
  // Fill Trigger Info
  //
  if(m_debug) cout << " Filling trigger " << endl;  
  m_helpTree[syst]->FillTrigger( eventInfo );

  m_passEmulatedTriggers.clear();
  static SG::AuxElement::ConstAccessor< std::vector< std::string > > passTrigsEMUL("passTriggersEmulation");
  if( passTrigsEMUL.isAvailable( *eventInfo ) ) { 
    m_passEmulatedTriggers = passTrigsEMUL( *eventInfo ); 
  }else{
    if(m_debug) cout << "ERROR:: passTriggersEmulation not avalible." << endl;
  }

  static SG::AuxElement::ConstAccessor< char > passCleaning("cleanEvent_"+m_jetCleaningName);
  m_cleanEvent = bool(passCleaning( *eventInfo ));

  //
  // Fill MeT Info
  //
  if(!m_metContainerName.empty()){
    if(m_debug) cout << "Getting Met" << m_metContainerName << endl;
    const xAOD::MissingETContainer* metcontainer(nullptr);
    ANA_CHECK( HelperFunctions::retrieve(metcontainer, m_metContainerName, m_event, m_store, msg()) );
    m_helpTree[syst]->FillMET( metcontainer );
  }

  //
  // Fill Muon
  //
  if(!m_muonContainerName.empty()){
    if(m_debug) cout << " Filling muons " << endl;  
    const xAOD::MuonContainer* muons(nullptr);
    ANA_CHECK( HelperFunctions::retrieve(muons, m_muonContainerName, m_event, m_store) );
    m_helpTree[syst]->FillMuons(  muons, HelperFunctions::getPrimaryVertex( vertices ) );
  }

  //
  // Fill Electrons
  //
  if(!m_elecContainerName.empty()){
    if(m_debug) cout << " Filling Elecs " << endl;  
    const xAOD::ElectronContainer* elecs(nullptr);
    ANA_CHECK( HelperFunctions::retrieve(elecs, m_elecContainerName, m_event, m_store));
    m_helpTree[syst]->FillElectrons(  elecs, HelperFunctions::getPrimaryVertex( vertices ) );
  }

  //
  // Fill Leptons for veto
  //
  if(m_storeLeptonVeto){
    b_n_muons_veto = 0;
    b_n_electrons_veto = 0;

    const xAOD::MuonContainer* MuonsVeto(0);
    if(m_debug) cout << "Getting muons for veto" << endl;
    ANA_CHECK( HelperFunctions::retrieve(MuonsVeto, "Muons_Veto_OR", m_event, m_store));

    const xAOD::ElectronContainer* ElectronsVeto(0);
    if(m_debug) cout << "Getting electrons for veto" << endl;
    ANA_CHECK( HelperFunctions::retrieve(ElectronsVeto, "Electrons_Veto_OR", m_event, m_store));

    b_n_muons_veto = MuonsVeto->size();
    b_n_electrons_veto = ElectronsVeto->size();

    // now we also store event cleaning decision
    b_event_cleaning_qqbb = true;

    const xAOD::JetContainer* JetsEventClean(0);
    if(m_debug) cout << "Getting jets for event cleaning" << endl;
    ANA_CHECK( HelperFunctions::retrieve(JetsEventClean, "AntiKt4EMTopoJets_Calib_OR", m_event, m_store));

    for(auto jet : *JetsEventClean){
      bool isBadJet = !(jet->auxdata<char>("cleanJet"));
      bool isPU = (jet->auxdata<float>("Jvt") < 0.59);

      if( (jet->pt() > 20000.) && (jet->pt() < 60000.) ){
        if(fabs(jet->eta()) < 2.4){
          b_event_cleaning_qqbb = !(isBadJet && (!isPU));
        }
        else{
          b_event_cleaning_qqbb = (!isBadJet);
        }
      }
      else if(jet->pt() >= 60000.){
        b_event_cleaning_qqbb = (!isBadJet);
      }

      if(!b_event_cleaning_qqbb) break;
    }
  }

  //
  // Fill MET for veto
  //
  if(m_storeMETVeto){
    b_METsum = 0.;
    b_METphi = 0.;

    const xAOD::MissingETContainer* METVeto(0);
    if(m_debug) cout << "Getting MET for veto" << endl;
    ANA_CHECK( HelperFunctions::retrieve(METVeto, "MET_Veto", m_event, m_store));

    b_METsum = (*METVeto)["FinalTrk"]->met();
    b_METphi = (*METVeto)["FinalTrk"]->phi();
  }

  //
  // Fill Truth
  //
  const xAOD::TruthParticleContainer* truth_particles_unsort(0);
  xAOD::TruthParticleContainer* truth_particles(0);
  if (!m_inTruthParticleName.empty() && m_isMC && m_storeTruth){
    if(m_debug) cout << " Getting Truth Particles"  << endl;  
    ANA_CHECK( HelperFunctions::retrieve(truth_particles_unsort, m_inTruthParticleName, m_event, m_store));

    truth_particles = new xAOD::TruthParticleContainer(*truth_particles_unsort);//memory leak
    truth_particles->sort(sort_pt<xAOD::TruthParticle>());

    // truth particles
    b_truth_mtt = -100.;
    
    if(m_debug) cout << " Filling truth particles " << endl;  
    m_helpTree[syst]->ClearTruth("truth");
    const xAOD::TruthParticle* h1 = 0;
    const xAOD::TruthParticle* h2 = 0;

    for(unsigned int i=0; i<truth_particles->size(); i++){
      const xAOD::TruthParticle* curr_truth = truth_particles->at(i);
      if(!curr_truth) continue;
      //In current signal sample RSG has 0 pT, and ROOT generates a warning if you call eta on a TVector3 in that case; this suppresses that warning - Tomo
      if (curr_truth->pt() < 1e-9) continue;//note that the RSGs are not saved in this case
      
      int pdg_id = curr_truth->pdgId();
      int status = curr_truth->status();
      int nChildren = curr_truth->nChildren();

      bool passGraviton = (pdg_id == 39          && (status == 22  || status == 11));
      bool passHiggs = (curr_truth->isHiggs() && (status == 22  || (status == 11 && nChildren > 1 )));
      if(passHiggs){
	if     (!h1){ h1 = curr_truth; }
	else if(!h2){ h2 = curr_truth; }
	else{ cout << "ERROR::Too many truth higgs ! " << endl; }
      }
      
      bool parentHiggs = false;
      int nParents = curr_truth->nParents();
      bool parentW = false;      
      for(int iparent = 0; iparent < nParents; ++iparent){
      	const xAOD::TruthParticle* parent = curr_truth->parent(iparent);
      	if(parent && parent->isHiggs()){
      	  parentHiggs = true;
      	}

	if(parent && parent->isW()){
	  parentW = true;
	} 
      }

      bool passParentW = (parentW && (status == 3));

      bool passBquarkFromHiggs = (abs(pdg_id) == 5      && parentHiggs);
      
      //Stop BHadron matching
      //bool passBHadron = (curr_truth->isBottomHadron() && came_from_b_quark(curr_truth) && !has_b_hadron_child(curr_truth));//memory leak
      
      //Keep quarks that are at least 50 GeV; For TeV dijet
      //bool passHardQuark = (abs(pdg_id) < 7 && curr_truth->pt() > 50);

      //Save Graviton, Higgs, b-quarks
      if(passGraviton || passHiggs || passBquarkFromHiggs || passParentW ){
	m_helpTree[syst]->FillTruth(  curr_truth, "truth" );
      }
    }

    if(h1 && h2){
      float mhh = (h1->p4()+h2->p4()).M();
      m_weight_mhh = m_hhWeightTool->getWeight(mhh);
      //cout << "mhh " << mhh << " hh weight " << m_hhWeightTool->getWeight(mhh) << endl;;
    }else{
      m_weight_mhh = 1.0;
      //cout << "ERROR::Too few truth higgs ! " << endl; 
    }

    if(!getEventMtt(truth_particles, b_truth_mtt)){
      Warning("execute()", "Unable to calculate truth_mtt!");
    }
    
  } // if isMC
  if (truth_particles){delete truth_particles;}

  //
  // Fill Boosted Higgs Candidates
  //
  b_hcand_boosted_n = 0;
  b_hcand_boosted_pt.clear();
  b_hcand_boosted_ptTA.clear();
  b_hcand_boosted_ptcalo.clear();
  b_hcand_boosted_eta.clear();
  b_hcand_boosted_etaTA.clear();
  b_hcand_boosted_etacalo.clear();
  b_hcand_boosted_phi.clear();
  b_hcand_boosted_phiTA.clear();
  b_hcand_boosted_phicalo.clear();
  b_hcand_boosted_m.clear();
  b_hcand_boosted_mTA.clear();
  b_hcand_boosted_mcalo.clear();
  b_hcand_boosted_htag.clear();
  b_hcand_boosted_htag_muoncor_pt.clear();
  b_hcand_boosted_htag_muoncor_eta.clear();
  b_hcand_boosted_htag_muoncor_phi.clear();
  b_hcand_boosted_htag_muoncor_m.clear();
  b_hcand_boosted_htag_loose.clear();
  b_hcand_boosted_htag_medium.clear();
  b_hcand_boosted_htag_tight.clear();
  b_hcand_boosted_Wtag_medium.clear();
  b_hcand_boosted_Ztag_medium.clear();
  b_hcand_boosted_Wtag_tight.clear();
  b_hcand_boosted_Ztag_tight.clear();
  b_hcand_boosted_smoothWtag_50.clear();
  b_hcand_boosted_smoothZtag_50.clear();
  b_hcand_boosted_smoothWtag_80.clear();
  b_hcand_boosted_smoothZtag_80.clear();
  b_hcand_boosted_dRjj.clear();
  b_hcand_boosted_C2.clear();
  b_hcand_boosted_D2.clear();
  b_hcand_boosted_Tau21.clear();
  b_hcand_boosted_Tau21WTA.clear();
  b_hcand_boosted_nTrack.clear();
  b_hcand_boosted_nHBosons.clear();
  b_hcand_boosted_nWBosons.clear();
  b_hcand_boosted_nZBosons.clear();

  b_jet_ak2track_asso_n.clear();
  b_jet_ak2track_asso_n_addl.clear();
  b_jet_ak2track_asso_pt.clear();
  b_jet_ak2track_asso_eta.clear();
  b_jet_ak2track_asso_phi.clear();
  b_jet_ak2track_asso_m.clear();
  b_jet_ak2track_asso_MV2c00.clear();
  b_jet_ak2track_asso_MV2c10.clear();
  b_jet_ak2track_asso_MV2c20.clear();
  b_jet_ak2track_asso_MV2c100.clear();
  b_jet_ak2track_asso_sys.clear();
  b_jet_ak2track_asso_sysname.clear();
  b_boosted_bevent_sys.clear();

  b_truth_hcand_boosted_n = 0;
  b_truth_hcand_boosted_matched.clear();
  b_truth_hcand_boosted_pt.clear();
  b_truth_hcand_boosted_eta.clear();
  b_truth_hcand_boosted_phi.clear();
  b_truth_hcand_boosted_m.clear();
  b_truth_hcand_boosted_c2.clear();
  b_truth_hcand_boosted_d2.clear();


  m_helpTree[syst]->ClearFatJets("boostedJets");
  // loop over boosted Higgs candidates
  for(auto hcand : *boostedHCands) {  

    const xAOD::Jet* fatJet = hcand->auxdecor< const xAOD::Jet* >("caloJet");
    //const xAOD::Jet* leadingTrackJet = hcand->auxdecor< const xAOD::Jet* >("leadJet");
    //const xAOD::Jet* subleadingTrackJet = hcand->auxdecor< const xAOD::Jet* >("sublJet");
    //const xAOD::Jet* subsubleadingTrackJet = hcand->auxdecor< const xAOD::Jet* >("subsublJet");
    std::vector<const xAOD::Jet*> assotrkjets_fatJet = hcand->auxdecor< std::vector<const xAOD::Jet*> >("allTrkJet");
    float dRjj = hcand->auxdecor< float > ("dRjj");
    b_hcand_boosted_dRjj.push_back( dRjj );


    if(fatJet) {
      //fill the jet information first    
      m_helpTree[syst]->FillFatJet(fatJet, "boostedJets");
      //fill the boosted information
      b_hcand_boosted_n++;
      b_hcand_boosted_pt.push_back( fatJet->pt() );
      b_hcand_boosted_eta.push_back( fatJet->eta() );
      b_hcand_boosted_phi.push_back(fatJet->phi() );
      b_hcand_boosted_m.push_back( fatJet->m() );
      //other variables
      b_hcand_boosted_C2.push_back( getC2(fatJet) );
      b_hcand_boosted_D2.push_back( getD2(fatJet) );
      b_hcand_boosted_Tau21.push_back( getTau21(fatJet, false) );
      b_hcand_boosted_Tau21WTA.push_back( getTau21(fatJet, true) );
      b_hcand_boosted_nTrack.push_back( fatJet->auxdata<int>("GhostTrackCount") );

      //if commented out, this will be the same as Calo mass
      const xAOD::JetFourMom_t caloP4 = fatJet->jetP4("JetJMSScaleMomentumCalo");
      const xAOD::JetFourMom_t trackAsP4 = fatJet->jetP4("JetJMSScaleMomentumTA");

    
      b_hcand_boosted_mTA.push_back(   trackAsP4.M() );
      b_hcand_boosted_ptTA.push_back(  trackAsP4.Pt()  );
      b_hcand_boosted_etaTA.push_back( trackAsP4.Eta() );
      b_hcand_boosted_phiTA.push_back( trackAsP4.Phi() );


      b_hcand_boosted_mcalo.push_back(   caloP4.M() );
      b_hcand_boosted_ptcalo.push_back(  caloP4.Pt() );
      b_hcand_boosted_etacalo.push_back( caloP4.Eta() );
      b_hcand_boosted_phicalo.push_back( caloP4.Phi() );


      const xAOD::Jet* fatJetParentJet = 0;
      try{
        auto el = fatJet->auxdata<ElementLink<xAOD::JetContainer> >("Parent");
        if(!el.isValid()){
          Warning("executeSingle()", "Invalid link to \"Parent\" from fat-jet.");
        }
        else{
          fatJetParentJet = (*el);
        }
      }catch(...){
        Warning("executeSingle()", "Unable to get parent jet of fat-jet for truth labeling. Trimmed jet area would be used!");
        fatJetParentJet = fatJet;
      }

      if(m_isMC){
        b_hcand_boosted_nHBosons.push_back( fatJetParentJet->auxdata<int>("GhostHBosonsCount") );
        b_hcand_boosted_nWBosons.push_back( fatJetParentJet->auxdata<int>("GhostWBosonsCount") );
        b_hcand_boosted_nZBosons.push_back( fatJetParentJet->auxdata<int>("GhostZBosonsCount") );
      }
      else{
        b_hcand_boosted_nHBosons.push_back(-1);
        b_hcand_boosted_nWBosons.push_back(-1);
        b_hcand_boosted_nZBosons.push_back(-1);
      }


//      if (m_doXhhTagging) {
//
//        //H tag      
//        //b_hcand_boosted_htag.push_back( m_BoostedXbbTagger->result( *fatJet, true ) );
//        //TLorentzVector b_hcand_boosted_htag_muoncor= m_BoostedXbbTagger->getCorrectedJetTLV(*fatJet);   
//
//        b_hcand_boosted_htag_muoncor_pt.push_back(b_hcand_boosted_htag_muoncor.Pt());  
//        b_hcand_boosted_htag_muoncor_eta.push_back(b_hcand_boosted_htag_muoncor.Eta());  
//        b_hcand_boosted_htag_muoncor_phi.push_back(b_hcand_boosted_htag_muoncor.Phi());  
//        b_hcand_boosted_htag_muoncor_m.push_back(b_hcand_boosted_htag_muoncor.M());  
//
//
//        int Wtag_pass_medium = m_WbosonTaggerMedium->result(*fatJet);
//        int Ztag_pass_medium = m_ZbosonTaggerMedium->result(*fatJet);
//        b_hcand_boosted_Wtag_medium.push_back(Wtag_pass_medium);
//        b_hcand_boosted_Ztag_medium.push_back(Ztag_pass_medium);
//
//        int Wtag_pass_tight = m_WbosonTaggerTight->result(*fatJet);
//        int Ztag_pass_tight = m_ZbosonTaggerTight->result(*fatJet);
//        b_hcand_boosted_Wtag_tight.push_back(Wtag_pass_tight);
//        b_hcand_boosted_Ztag_tight.push_back(Ztag_pass_tight);
//
//        b_hcand_boosted_smoothWtag_50.push_back( m_smoothedWTagger_50->result(*fatJet, true) );
//        b_hcand_boosted_smoothZtag_50.push_back( m_smoothedZTagger_50->result(*fatJet, true) );
//        b_hcand_boosted_smoothWtag_80.push_back( m_smoothedWTagger_80->result(*fatJet, true) );
//        b_hcand_boosted_smoothZtag_80.push_back( m_smoothedZTagger_80->result(*fatJet, true) );
//      }

      // get matched truth jet
      if(m_doResolutionStudy){
        double dRcut = 0.8;

        const xAOD::Jet* MatchedTruthFatJet = 0;
        double dRmatch = 9e9;
        for(auto truthjet: *truthFatJet){
          double dR = truthjet->p4().DeltaR(fatJet->p4());
          if(dR > dRcut) continue;

          if(dR < dRmatch){
            dRmatch = dR;
            MatchedTruthFatJet = truthjet;
          }
        }

        if(MatchedTruthFatJet){
          b_truth_hcand_boosted_n++;

          b_truth_hcand_boosted_matched.push_back( 1 );
          b_truth_hcand_boosted_pt.push_back( MatchedTruthFatJet->pt() );
          b_truth_hcand_boosted_eta.push_back( MatchedTruthFatJet->eta() );
          b_truth_hcand_boosted_phi.push_back( MatchedTruthFatJet->phi() );
          b_truth_hcand_boosted_m.push_back( MatchedTruthFatJet->m() );
          b_truth_hcand_boosted_c2.push_back( getC2(MatchedTruthFatJet) );
          b_truth_hcand_boosted_d2.push_back( getD2(MatchedTruthFatJet) );
        }
        else{
          b_truth_hcand_boosted_matched.push_back( 0 );
          b_truth_hcand_boosted_pt.push_back( 0. );
          b_truth_hcand_boosted_eta.push_back( 0. );
          b_truth_hcand_boosted_phi.push_back( 0. );
          b_truth_hcand_boosted_m.push_back( 0. );
          b_truth_hcand_boosted_c2.push_back( 0. );
          b_truth_hcand_boosted_d2.push_back( 0. );
        }
      }

      int ak2track_asso_n=0;
      std::vector<float> ak2track_asso_pt;
      std::vector<float> ak2track_asso_eta;
      std::vector<float> ak2track_asso_phi;
      std::vector<float> ak2track_asso_m;
      std::vector<float> ak2track_asso_MV2c00;
      std::vector<float> ak2track_asso_MV2c10;
      std::vector<float> ak2track_asso_MV2c20;
      std::vector<float> ak2track_asso_MV2c100;
      std::vector<vector<float> > ak2track_asso_sys;

      std::string BTag_SF_FixedCutBEff_XX_GLOBAL( TString::Format("BTag_SF_FixedCutBEff_%s_GLOBAL", m_TrackJetWP.data()).Data() );   // retrieve global SF
      std::string BTag_SF_FixedCutBEff_XX       ( TString::Format("BTag_SF_FixedCutBEff_%s", m_TrackJetWP.data()).Data() );          // retrieve jet-by-jet SF
      std::string FTSys_FixedCutBEff_XX         ( TString::Format("FTSys_FixedCutBEff_%s", m_TrackJetWP.data()).Data() );            // retrieve list of FT systematics names

      b_boosted_bevent_sys = eventInfo->auxdecor<std::vector<float>>(BTag_SF_FixedCutBEff_XX_GLOBAL);

      //retrive the boosted b-tag systematic names
      vector<std::string>* boostedbtagSystNames(nullptr);
      ANA_CHECK( HelperFunctions::retrieve(boostedbtagSystNames, FTSys_FixedCutBEff_XX, 0, m_store, msg()) );
      b_jet_ak2track_asso_sysname = *boostedbtagSystNames;


      for(auto fatJetTrackJet : assotrkjets_fatJet){
        ak2track_asso_n++; 
        ak2track_asso_pt.push_back( fatJetTrackJet->pt() );
        ak2track_asso_eta.push_back( fatJetTrackJet->eta() );
        ak2track_asso_phi.push_back( fatJetTrackJet->phi() );
        ak2track_asso_m.push_back( fatJetTrackJet->m() );
        ak2track_asso_MV2c00.push_back( MV2(fatJetTrackJet, "MV2c00") );
        ak2track_asso_MV2c10.push_back( MV2(fatJetTrackJet, "MV2c10") );
        ak2track_asso_MV2c20.push_back( MV2(fatJetTrackJet, "MV2c20") );
        ak2track_asso_MV2c100.push_back( MV2(fatJetTrackJet, "MV2c100") );
        ak2track_asso_sys.push_back(fatJetTrackJet->auxdecor<std::vector<float> >(BTag_SF_FixedCutBEff_XX));
      }
      //save all the vectors 
      b_jet_ak2track_asso_n.push_back( ak2track_asso_n );
      b_jet_ak2track_asso_n_addl.push_back( hcand->auxdecor< int > ("ak2track_asso_n") - ak2track_asso_n );
      b_jet_ak2track_asso_pt.push_back( ak2track_asso_pt );
      b_jet_ak2track_asso_eta.push_back( ak2track_asso_eta );
      b_jet_ak2track_asso_phi.push_back( ak2track_asso_phi );
      b_jet_ak2track_asso_m.push_back( ak2track_asso_m );
      b_jet_ak2track_asso_MV2c00.push_back( ak2track_asso_MV2c00 );
      b_jet_ak2track_asso_MV2c10.push_back( ak2track_asso_MV2c10 );
      b_jet_ak2track_asso_MV2c20.push_back( ak2track_asso_MV2c20 );
      b_jet_ak2track_asso_MV2c100.push_back( ak2track_asso_MV2c100 );
      b_jet_ak2track_asso_sys.push_back( ak2track_asso_sys );
    }
    else{
      cout<<"WARNING : NO FAT-JET ASSOCIATED TO A BOOSTED HIGGS CANDIDATE!"<<endl;
    }
  }


  //
  // Fill Resolved Higgs Candidates
  //
  m_helpTree[syst]->ClearJets("resolvedJets");

  // Fill resolved jets
  if(!m_resolvedJetsName.empty()){
    if(m_debug) cout << " Filling resolved jets " << endl;  
    for(auto jet_itr: *resolvedJets){
      m_helpTree[syst]->FillJet(  jet_itr, pv, HelperFunctions::getPrimaryVertexLocation( vertices ), "resolvedJets"  );
    }
  }

    
  // fill the tree
  if(m_debug) cout << " Filling Tree"  << endl;
  m_helpTree[syst]->Fill();
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhMiniNtuple :: postExecute () { return EL::StatusCode::SUCCESS; }

EL::StatusCode XhhMiniNtuple :: finalize () {

  Info("finalize()", m_name.c_str());


  if (!m_helpTree.empty()){
    for( auto tree : m_helpTree) {
      if (tree.second) delete tree.second;
    }
  }

//  if (m_doXhhTagging){
//    delete m_higgsTaggerLoose;
//    delete m_higgsTaggerMedium;
//    delete m_higgsTaggerTight;
//
//    delete m_BoostedXbbTagger; 
//
//    delete m_WbosonTaggerMedium;
//    delete m_ZbosonTaggerMedium;
//
//    delete m_smoothedWTagger_50;
//    delete m_smoothedZTagger_50;
//    delete m_smoothedWTagger_80;
//    delete m_smoothedZTagger_80;
//  }

  return EL::StatusCode::SUCCESS;
}

 

EL::StatusCode XhhMiniNtuple :: histFinalize ()
{
  TFile * treeFile = wk()->getOutputFile( m_name.c_str() );
  
  //check if histogram exists
  if ((!m_cutflowHist) || (!m_cutflowHistW)){
    return EL::StatusCode::SUCCESS;
  }
  //
  // Write out the cut flow histograms
  //

  TH1F* thisCutflowHist = (TH1F*) m_cutflowHist->Clone();
  std::string thisName = thisCutflowHist->GetName();
  thisCutflowHist->SetName( (thisName+"_XhhMiniNtuple").c_str() );
  thisCutflowHist->SetDirectory( treeFile );
  
  TH1F* thisCutflowHistW = (TH1F*) m_cutflowHistW->Clone();
  thisName = thisCutflowHistW->GetName();
  thisCutflowHistW->SetName( (thisName+"_XhhMiniNtuple").c_str() );
  thisCutflowHistW->SetDirectory( treeFile );
  
  //
  // Write out the Metadata
  //
  TFile *fileMD = wk()->getOutputFile("metadata");
  if (fileMD){
    TH1D* m_histEventCount   = (TH1D*)fileMD->Get("MetaData_EventCount");
    TH1F* thisHistEventCount = (TH1F*) m_histEventCount->Clone();
    thisName = thisHistEventCount->GetName();
    thisHistEventCount->SetName( (thisName+"_XhhMiniNtuple").c_str() );
    thisHistEventCount->SetDirectory( treeFile );
  }
  //
  // Write out the jet multiplicities
  //
  TH1* m_nJet  = wk()->getOutputHist("XhhCutFlow/nJet");
  if (m_nJet){
    TH1F* nJetClone = (TH1F*) m_nJet->Clone();
    thisName = nJetClone->GetName();
    nJetClone->SetName( (thisName).c_str() );
    nJetClone->SetDirectory( treeFile );
  }

  TH1* m_nBJet  = wk()->getOutputHist("XhhCutFlow/nBJet");
  if (m_nBJet){
    TH1F* nBJetClone = (TH1F*) m_nBJet->Clone();
    thisName = nBJetClone->GetName();
    nBJetClone->SetName( (thisName ).c_str() );
    nBJetClone->SetDirectory( treeFile );
  }
  
  return EL::StatusCode::SUCCESS;
}

//
// Easy method for automatically filling cutflow and incrementing counter
//
void XhhMiniNtuple::passCut(){
  m_cutflowHist ->Fill(m_iCutflow, 1);
  m_cutflowHistW->Fill(m_iCutflow, m_mcEventWeight);
  m_iCutflow++;
}

//
// Function to calcualte mtt for future stiching. Adopted from Ruth's code
//

bool XhhMiniNtuple::getEventMtt(const xAOD::TruthParticleContainer* Truths, double& mtt){
  // Initialization
  mtt = -100.;

  // Basic Check
  if(!Truths){
    Warning("getEventMtt()", "Null ptr to TruthParticleContainer!");
    return false;
  }


  // Loop over Truth Particles
  std::vector<unsigned> tops, antitops;
  for(unsigned iTruth = 0; iTruth < Truths->size(); iTruth++){
    const xAOD::TruthParticle* Truth = Truths->at(iTruth);
    if( (Truth->pt() > 0.) && (Truth->absPdgId() == 6) && (Truth->status() == 3) ){
      if(Truth->pdgId() == -6)
        antitops.push_back(iTruth);
      else 
        tops.push_back(iTruth);
    }
    else 
      continue;
  }

  // take whatever maximum combination
  for(unsigned it = 0; it < tops.size(); it++){
    const xAOD::TruthParticle* Top = Truths->at(tops.at(it));

    for(unsigned iat = 0; iat < antitops.size(); iat++){  
      const xAOD::TruthParticle* ATop = Truths->at(antitops.at(iat));

      // It is important to reconstruct TLorentzVector using pt/eta/phi/e, since the mass of truth particle is wrong here! (it could be off-shell)

      TLorentzVector top_4p;
      top_4p.SetPtEtaPhiE(Top->pt(), Top->eta(), Top->phi(), Top->e());

      TLorentzVector atop_4p;
      atop_4p.SetPtEtaPhiE(ATop->pt(), ATop->eta(), ATop->phi(), ATop->e());

      TLorentzVector sum = top_4p + atop_4p;
      double currentMtt = sum.M();

      if(currentMtt > mtt) mtt = currentMtt;
    }
  }

  return true;
}

int XhhMiniNtuple::killPileupFluctuation(){
  const xAOD::EventInfo* eventInfo(0);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store));

  int mcChannelNumber = eventInfo->mcChannelNumber();
  if ((mcChannelNumber < 361020) || (mcChannelNumber > 361032)){//only do it for dijet MC samples?
    return 1;//check MC number first to save time;
  }

  const xAOD::JetContainer* AntiKt4TruthJets(0);
  ANA_CHECK( HelperFunctions::retrieve(AntiKt4TruthJets, "AntiKt4TruthJets", m_event, m_store));

  const xAOD::JetContainer* AntiKt4EMTopoJets(0);
  ANA_CHECK( HelperFunctions::retrieve(AntiKt4EMTopoJets, "AntiKt4EMTopoJets_Calib", m_event, m_store));

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  // all jet collections are pre-assumed to be sorted by pT; 
  float ratio = 1;
  if((AntiKt4TruthJets->size() >= 1) && (AntiKt4EMTopoJets->size() >= 2)){
    float ptave = (AntiKt4EMTopoJets->at(0)->pt() + AntiKt4EMTopoJets->at(1)->pt())/2.;
    float pttruth = AntiKt4TruthJets->at(0)->pt();
    ratio = ptave/pttruth;
  }
  //remove events if ratio is too high
  if(ratio > 1.4){return 0;}
  else{return 1;}
}

double XhhMiniNtuple::getD2(const xAOD::Jet* jet){
  if(jet->getAttribute<double>("ECF2") == 0.){
    Warning("getD2()", "ECF2 returns 0. -1 will be returned");
    return -1.;
  }

  return (jet->getAttribute<double>("ECF3") * TMath::Power(jet->getAttribute<double>("ECF1"), 3) )/(TMath::Power(jet->getAttribute<double>("ECF2"), 3));
}

double XhhMiniNtuple::getTau21(const xAOD::Jet* jet, bool doWTA){
  std::string WTAappendix = (doWTA ? "_wta" : "");

  if(jet->getAttribute<double>("Tau1"+WTAappendix) == 0.){
    Warning("getTau21", "Tau1%s returns 0. -1 will be returned", WTAappendix.data());
  }

  return jet->getAttribute<double>("Tau2"+WTAappendix)/jet->getAttribute<double>("Tau1"+WTAappendix);
}

double XhhMiniNtuple::getC2(const xAOD::Jet* jet){
  if(jet->getAttribute<double>("ECF2") == 0.){
    Warning("getC2()", "ECF2 returns 0. -1 will be returned");
    return -1.;
  }

  return (jet->getAttribute<double>("ECF3") * TMath::Power(jet->getAttribute<double>("ECF1"), 1) )/(TMath::Power(jet->getAttribute<double>("ECF2"), 2));
}

