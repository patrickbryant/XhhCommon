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
#include <XhhCommon/XhhTestBoostedNtuple.h>
#include <XhhCommon/Helpers.h>

#include <xAODAnaHelpers/HelperFunctions.h>
#include <xAODAnaHelpers/HelperClasses.h>

#include "TEnv.h"
#include "TSystem.h"

//#define DEBUG std::cerr << __FILE__ << "::" << __LINE__ << std::endl
 
// this is needed to distribute the algorithm to the workers
ClassImp(XhhTestBoostedNtuple)

using std::cout;  using std::endl;
using std::string; using std::vector;

XhhTestBoostedNtuple :: XhhTestBoostedNtuple () :
  m_name(""),
  m_cutflowHist(0),
  m_cutflowHistW(0),
  m_cutflowFirst(0),
  m_iCutflow(0),
  m_isMC(false),
  m_evtDetailStr(""),
  m_trigDetailStr(""),
  m_fatJetDetailStr(""),
  m_truthDetailStr(""),
  m_inFatJetName(""),
  m_inJetName(""),
  m_inTruthFatJetName("AntiKt10TruthTrimmedPtFrac5SmallR20Jets"),
  m_inTruthParticleName(""),
  m_metContainerName(""),
  m_metDetailStr(""),
  m_debug(false), 
  m_doFatJetMassCut(true),
  m_FatJetPtSkimCut(400.),  // in GeV
  m_eventCuts(""),
  m_boostedSysName(""),
  m_weight(1.0),
  m_weight_xs(1.0)
{
  this->SetName("XhhTestBoostedNtuple"); // needed if you want to retrieve this algo with wk()->getAlg(ALG_NAME) downstream
}

EL::StatusCode XhhTestBoostedNtuple :: setupJob (EL::Job& job)
{
  Info("setupJob()", "Calling setupJob \n");
  job.useXAOD();
  xAOD::Init("XhhTestBoostedNtuple").ignore();

  EL::OutputStream outForTree(m_name.c_str());
  job.outputAdd (outForTree);
  Info("setupJob()", "Ready\n");

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhTestBoostedNtuple :: initialize ()
{
  Info("initialize()", m_name.c_str());
  m_event = wk()->xaodEvent();
  m_store = wk()->xaodStore();

  if(m_debug) Info("initialize()", "after add store");


  if(m_debug) Info("initialize()", "after rec file");

  //
  // Set isMC flag
  //
  const xAOD::EventInfo* eventInfo(nullptr);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store, msg()));
  m_isMC = ( eventInfo->eventType( xAOD::EventInfo::IS_SIMULATION ) ) ? true : false;

 
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

EL::StatusCode XhhTestBoostedNtuple::AddTree(string syst = "")
{
  Info("AddTree()", "%s", m_name.c_str() );
  // needed here and not in initalize since this is called first

  string treeName = "XhhTestBoostedNtuple";
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

  m_helpTree[syst]->AddEvent(m_evtDetailStr);
  m_helpTree[syst]->AddTrigger(m_trigDetailStr);

  m_helpTree[syst]->AddJets(m_jetDetailStr,     "resolvedJets");
  m_helpTree[syst]->AddFatJets(m_fatJetDetailStr,     "boostedJets");

  if(m_isMC  && !m_inTruthFatJetName.empty())
    m_helpTree[syst]->AddTruthFatJets("kinematic",     "truth_boostedJets");

  if(!m_metContainerName.empty())
    m_helpTree[syst]->AddMET(m_metDetailStr);

  // Truth particles
  if(!m_inTruthParticleName.empty() && m_isMC){
    m_helpTree[syst]->AddTruthParts("truth", m_truthDetailStr);
  }


  // outTree->Branch("passed_cuts", &b_passed_cuts);
  // outTree->Branch("decay_match_ind", &b_decay_match_ind);

  outTree->Branch("weight",    &m_weight,    "weight/F");
  outTree->Branch("weight_xs", &m_weight_xs, "weight_xs/F");
    

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhTestBoostedNtuple :: histInitialize () { return EL::StatusCode::SUCCESS; }
EL::StatusCode XhhTestBoostedNtuple :: fileExecute    () { return EL::StatusCode::SUCCESS; }
EL::StatusCode XhhTestBoostedNtuple :: changeInput    (bool /*firstFile*/) { return EL::StatusCode::SUCCESS; }

EL::StatusCode XhhTestBoostedNtuple::execute ()
{

  const xAOD::EventInfo* eventInfo(0);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store));

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

  if (m_boostedSysName.empty()) {

    executeSingle("", true);

    //
    // Do Systematics
    //
  } else{

    //
    // Do Nominal
    //   (do the cut flow calculation here)
    //
    executeSingle("", true);


    //
    // Do Boosted Systematics
    //
    if(!m_boostedSysName.empty()){

      // get vector of string giving the names
      vector<string>* boostedSystNames(nullptr);
      ANA_CHECK( HelperFunctions::retrieve(boostedSystNames, m_boostedSysName, 0, m_store, msg()) );
    
      // Loop over boosted systematics 
      for ( string& boostSystName : *boostedSystNames ) {
      
	if(boostSystName.empty()) continue;

	if(m_debug) Info("execute",  "systName %s", boostSystName.c_str());

	executeSingle(boostSystName, false);
	
      }

    }

  }
  
  return EL::StatusCode::SUCCESS;

}

EL::StatusCode XhhTestBoostedNtuple::executeSingle(string boostedSys, bool countEvents) {
  if(m_debug) cout << " In executeSingle"  << boostedSys << endl;

  //
  //  Count All Events
  //
  if(countEvents) passCut(); 
  
  //
  // Start with stuff which is common to boosted 
  //
  string syst = "";
  if(!boostedSys.empty())  syst = "Boosted_" +boostedSys;

  if( m_helpTree.find( syst ) == m_helpTree.end() ) { AddTree( syst ); }

  const xAOD::EventInfo* eventInfo(0);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store));
  
  const xAOD::VertexContainer* vertices(0);
  ANA_CHECK( HelperFunctions::retrieve(vertices, "PrimaryVertices", m_event, m_store));

  const xAOD::Vertex *pv = 0;
  pv = vertices->at( HelperFunctions::getPrimaryVertexLocation( vertices ) );

  const xAOD::JetContainer* jets = 0;
  ANA_CHECK( HelperFunctions::retrieve(jets, m_inJetName+syst, m_event, m_store, msg()));

  const xAOD::JetContainer* fatJets = 0;
  ANA_CHECK( HelperFunctions::retrieve(fatJets, m_inFatJetName+syst, m_event, m_store, msg()));

  // Retrieve the container of truth fat-jet (MC only, hard-coded in)
  if(m_debug) cout << " Getting AntiKt10TruthTrimmedPtFrac5SmallR20Jets" << endl;
  
  const xAOD::JetContainer* truthFatJets(0);
  if(m_isMC){
    ANA_CHECK( HelperFunctions::retrieve(truthFatJets, m_inTruthFatJetName, m_event, m_store));
  }


  //
  // Count the fat jet kinematics
  //
  unsigned int nBoostedJetPassMCut  = 0;
  unsigned int nBoostedJetPassPtCut = 0;
  for(const xAOD::Jet* fatJet : *fatJets) {
    if((!m_doFatJetMassCut) || (fatJet->m()  >  50*1000)) nBoostedJetPassMCut++;
    if(fatJet->pt() > m_FatJetPtSkimCut*1000)             nBoostedJetPassPtCut++;
  }

  //
  //  only fill ntup if:
  //   one boosted jet passes
  //
  bool PassBoostedNHCands     = (fatJets->size()           > 0);
  bool PassBoostedHCandM      = (nBoostedJetPassMCut       > 0);
  bool PassBoostedHCandPt     = (nBoostedJetPassPtCut      > 0);

  bool PassBoostedPreSel     = PassBoostedNHCands   && PassBoostedHCandPt && PassBoostedHCandM;

  if(m_debug){ 
    cout << "Run/Event " << eventInfo->runNumber() << " / " << eventInfo->eventNumber() << endl;
  }

  if(m_debug){ 
    cout << " PassBoostedPreSel: "  << PassBoostedPreSel << endl;  
  }

  if (!PassBoostedPreSel) return EL::StatusCode::SUCCESS;
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

  //
  // Fill MeT Info
  //
  if(!m_metContainerName.empty()){
    if(m_debug) cout << "Getting Met" << m_metContainerName << endl;
    const xAOD::MissingETContainer* metcontainer(nullptr);
    ANA_CHECK(HelperFunctions::retrieve(metcontainer, m_metContainerName, m_event, m_store, msg()) );
    m_helpTree[syst]->FillMET( metcontainer );
  }

  //
  // Fill Truth
  //
  const xAOD::TruthParticleContainer* truth_particles_unsort(0);
  xAOD::TruthParticleContainer* truth_particles(0);
  if (!m_inTruthParticleName.empty() && m_isMC){
    if(m_debug) cout << " Getting Truth Particles"  << endl;  
    ANA_CHECK( HelperFunctions::retrieve(truth_particles_unsort, m_inTruthParticleName, m_event, m_store));
    truth_particles = new xAOD::TruthParticleContainer(*truth_particles_unsort);//memory leak
    truth_particles->sort(sort_pt<xAOD::TruthParticle>());
    
    if(m_debug) cout << " Filling truth particles " << endl;  
    m_helpTree[syst]->ClearTruth("truth");
    for(unsigned int i=0; i<truth_particles->size(); i++){
      const xAOD::TruthParticle* curr_truth = truth_particles->at(i);
      if(!curr_truth) continue;
        
      int pdg_id = curr_truth->pdgId();
      int status = curr_truth->status();
      int nChildren = curr_truth->nChildren();


      bool passGraviton = (pdg_id == 39          && (status == 22  || status == 11));
      bool passHiggs = (curr_truth->isHiggs() && (status == 22  || (status == 11 && nChildren > 1 )));
      
      bool parentHiggs = false;
      int nParents = curr_truth->nParents();
      for(int iparent = 0; iparent < nParents; ++iparent){
	const xAOD::TruthParticle* parent = curr_truth->parent(iparent);
	if(parent && parent->isHiggs()){
	  parentHiggs = true;
	}
      }
      bool passBquarkFromHiggs = (abs(pdg_id) == 5      && parentHiggs);
      

      bool passBHadron = (curr_truth->isBottomHadron() && came_from_b_quark(curr_truth) && !has_b_hadron_child(curr_truth));//memory leak
      
      //Save Graviton, Higgs, b-quarks
      if(passGraviton || passHiggs || passBquarkFromHiggs || passBHadron)
	{
	  m_helpTree[syst]->FillTruth(  curr_truth, "truth" );
	}
      
    }

    
  } // if isMC
  delete truth_particles;    


  //
  // Fill Jets
  //
  m_helpTree[syst]->ClearJets("resolvedJets");
  for(const xAOD::Jet* jet : *jets) {
    m_helpTree[syst]->FillJet(jet, pv, HelperFunctions::getPrimaryVertexLocation( vertices ), "resolvedJets");
  }


  //
  // Fill Boosted Higgs Candidates
  //
  m_helpTree[syst]->ClearFatJets("boostedJets");
  for(const xAOD::Jet* fatJet : *fatJets) {
    m_helpTree[syst]->FillFatJet(fatJet, "boostedJets");
  }

  //
  // Fill Truth Boosted Higgs Candidates
  //
  if(m_isMC && !m_inTruthFatJetName.empty()){
    m_helpTree[syst]->ClearTruthFatJets("truth_boostedJets");
    // loop over boosted Higgs candidates
    for(const xAOD::Jet* truthFatJet : *truthFatJets) {  
      m_helpTree[syst]->FillTruthFatJet(truthFatJet, "truth_boostedJets");
    }
  }
  
    
  // fill the tree
  if(m_debug) cout << " Filling Tree"  << endl;
  m_helpTree[syst]->Fill();
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhTestBoostedNtuple :: postExecute () { return EL::StatusCode::SUCCESS; }

EL::StatusCode XhhTestBoostedNtuple :: finalize () {

  Info("finalize()", m_name.c_str());

  if (!m_helpTree.empty()){
    for( auto tree : m_helpTree) {
      if (tree.second) delete tree.second;
    }
  }

  return EL::StatusCode::SUCCESS;
}

 

EL::StatusCode XhhTestBoostedNtuple :: histFinalize ()
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
  thisCutflowHist->SetName( (thisName+"_XhhTestBoostedNtuple").c_str() );
  thisCutflowHist->SetDirectory( treeFile );
  
  TH1F* thisCutflowHistW = (TH1F*) m_cutflowHistW->Clone();
  thisName = thisCutflowHistW->GetName();
  thisCutflowHistW->SetName( (thisName+"_XhhTestBoostedNtuple").c_str() );
  thisCutflowHistW->SetDirectory( treeFile );
  
  //
  // Write out the Metadata
  //
  TFile *fileMD = wk()->getOutputFile("metadata");
  if (fileMD){
    TH1D* m_histEventCount   = (TH1D*)fileMD->Get("MetaData_EventCount");
    TH1F* thisHistEventCount = (TH1F*) m_histEventCount->Clone();
    thisName = thisHistEventCount->GetName();
    thisHistEventCount->SetName( (thisName+"_XhhTestBoostedNtuple").c_str() );
    thisHistEventCount->SetDirectory( treeFile );
  }
  
  return EL::StatusCode::SUCCESS;
}

//
// Easy method for automatically filling cutflow and incrementing counter
//
void XhhTestBoostedNtuple::passCut(){
  m_cutflowHist ->Fill(m_iCutflow, 1);
  m_cutflowHistW->Fill(m_iCutflow, m_mcEventWeight);
  m_iCutflow++;
}





