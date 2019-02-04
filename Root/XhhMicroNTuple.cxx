#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include <xAODJet/JetContainer.h>
#include <xAODTracking/VertexContainer.h>
#include <xAODEventInfo/EventInfo.h>
#include <AthContainers/ConstDataVector.h>

#include "xAODParticleEvent/ParticleContainer.h"
//#include <xAODTruth/TruthParticleContainer.h>
//#include <xAODTruth/TruthVertex.h>

#include <xAODAnaHelpers/HelpTreeBase.h>
#include <XhhCommon/XhhMicroNTuple.h>
#include <XhhCommon/CutTool.h>
#include <XhhCommon/Helpers.h>

#include <xAODAnaHelpers/HelperFunctions.h>
#include <xAODAnaHelpers/HelperClasses.h>


#include "TEnv.h"
#include "TSystem.h"

using std::cout;  using std::endl;

//#define DEBUG std::cerr << __FILE__ << "::" << __LINE__ << std::endl
 
// this is needed to distribute the algorithm to the workers
ClassImp(XhhMicroNTuple)

XhhMicroNTuple :: XhhMicroNTuple () :
  m_name(""),
  m_debug(false),
  m_cutTool(nullptr)
{
  this->SetName("XhhMicroNTuple"); // needed if you want to retrieve this algo with wk()->getAlg(ALG_NAME) downstream
}

EL::StatusCode XhhMicroNTuple :: setupJob (EL::Job& job)
{
  Info("setupJob()", "Calling setupJob \n");
  job.useXAOD();
  xAOD::Init("XhhMicroNTuple").ignore();

  EL::OutputStream outForTree(m_name.c_str());
  job.outputAdd (outForTree);
  Info("setupJob()", "Ready\n");

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhMicroNTuple :: initialize ()
{
  Info("initialize()", m_name.c_str());
  m_event = wk()->xaodEvent();
  m_store = wk()->xaodStore();

  this->configure(); 

  m_cutTool = new CutTool();
  m_cutTool->Init(m_eventCuts);

  if (m_jetSystematics.empty() && m_bJetSystematics.empty()) this->treeInitialize("");

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhMicroNTuple::treeInitialize(std::string syst = "")
{
  Info("treeInitialize()", "%s", m_name.c_str() );
  // needed here and not in initalize since this is called first

  std::string treeName = "XhhMicroNTuple";
  if (!syst.empty()) treeName += "_" + syst;
  TTree * outTree = new TTree(treeName.c_str(), treeName.c_str());
  if( !outTree ) {
    Error("treeInitialize()","Failed to instantiate output tree!");
    return EL::StatusCode::FAILURE;
  }

  // get the file we created already
  TFile* treeFile = wk()->getOutputFile(m_name.c_str());
  m_helpTree[syst] = new HelpTreeBase( m_event, outTree, treeFile );

  // tell the tree to go into the file
  outTree->SetDirectory( treeFile );

  // if want to add to same file as ouput histograms
  // wk()->addOutput( outTree );

  m_helpTree[syst]->AddEvent(m_evtDetailStr);
  m_helpTree[syst]->AddTrigger(m_trigDetailStr);

  //
  // Resolved branches
  //
  if(!m_inJetName.empty()) m_helpTree[syst]->AddJets     (m_jetDetailStr); 

  outTree->Branch("nbjets", &b_nbjets, "nbjets/I");

  // lead dijet
  outTree->Branch("dijet1_pt"         , &b_dijet1_pt         ,  "dijet1_pt/F"); 
  outTree->Branch("dijet1_eta"        , &b_dijet1_eta        ,  "dijet1_eta/F");
  outTree->Branch("dijet1_phi"        , &b_dijet1_phi        ,  "dijet1_phi/F");
  outTree->Branch("dijet1_m"          , &b_dijet1_m          ,  "dijet1_m/F");   
  outTree->Branch("dijet1_dRjet1jet2" , &b_dijet1_dRjet1jet2 ,  "dijet1_dRjet1jet2/F");

  // lead dijet, lead jet
  outTree->Branch("dijet1_jet1_pt"     , &b_dijet1_jet1_pt     ,  "dijet1_jet1_pt/F"); 
  outTree->Branch("dijet1_jet1_eta"    , &b_dijet1_jet1_eta    ,  "dijet1_jet1_eta/F");
  outTree->Branch("dijet1_jet1_phi"    , &b_dijet1_jet1_phi    ,  "dijet1_jet1_phi/F");
  outTree->Branch("dijet1_jet1_m"      , &b_dijet1_jet1_m      ,  "dijet1_jet1_m/F");   
  outTree->Branch("dijet1_jet1_MV2c00" , &b_dijet1_jet1_MV2c00 ,  "dijet1_jet1_MV2c00/F");
  outTree->Branch("dijet1_jet1_MV2c10" , &b_dijet1_jet1_MV2c10 ,  "dijet1_jet1_MV2c10/F");
  outTree->Branch("dijet1_jet1_MV2c20" , &b_dijet1_jet1_MV2c20 ,  "dijet1_jet1_MV2c20/F");

  // lead dijet, sublead jet
  outTree->Branch("dijet1_jet2_pt"     , &b_dijet1_jet2_pt     ,  "dijet1_jet2_pt/F"); 
  outTree->Branch("dijet1_jet2_eta"    , &b_dijet1_jet2_eta    ,  "dijet1_jet2_eta/F");
  outTree->Branch("dijet1_jet2_phi"    , &b_dijet1_jet2_phi    ,  "dijet1_jet2_phi/F");
  outTree->Branch("dijet1_jet2_m"      , &b_dijet1_jet2_m      ,  "dijet1_jet2_m/F");   
  outTree->Branch("dijet1_jet2_MV2c00" , &b_dijet1_jet2_MV2c00 ,  "dijet1_jet2_MV2c00/F");
  outTree->Branch("dijet1_jet2_MV2c10" , &b_dijet1_jet2_MV2c10 ,  "dijet1_jet2_MV2c10/F");
  outTree->Branch("dijet1_jet2_MV2c20" , &b_dijet1_jet2_MV2c20 ,  "dijet1_jet2_MV2c20/F");

  // sublead dijet
  outTree->Branch("dijet2_pt"         , &b_dijet2_pt         ,  "dijet2_pt/F"); 
  outTree->Branch("dijet2_eta"        , &b_dijet2_eta        ,  "dijet2_eta/F");
  outTree->Branch("dijet2_phi"        , &b_dijet2_phi        ,  "dijet2_phi/F");
  outTree->Branch("dijet2_m"          , &b_dijet2_m          ,  "dijet2_m/F");   
  outTree->Branch("dijet2_dRjet1jet2" , &b_dijet2_dRjet1jet2 ,  "dijet2_dRjet1jet2/F");

  // sublead dijet, lead jet
  outTree->Branch("dijet2_jet1_pt"     , &b_dijet2_jet1_pt     ,  "dijet2_jet1_pt/F"); 
  outTree->Branch("dijet2_jet1_eta"    , &b_dijet2_jet1_eta    ,  "dijet2_jet1_eta/F");
  outTree->Branch("dijet2_jet1_phi"    , &b_dijet2_jet1_phi    ,  "dijet2_jet1_phi/F");
  outTree->Branch("dijet2_jet1_m"      , &b_dijet2_jet1_m      ,  "dijet2_jet1_m/F");
  outTree->Branch("dijet2_jet1_MV2c00" , &b_dijet2_jet1_MV2c00 ,  "dijet2_jet1_MV2c00/F");
  outTree->Branch("dijet2_jet1_MV2c10" , &b_dijet2_jet1_MV2c10 ,  "dijet2_jet1_MV2c10/F");
  outTree->Branch("dijet2_jet1_MV2c20" , &b_dijet2_jet1_MV2c20 ,  "dijet2_jet1_MV2c20/F");

  // sublead dijet, sublead jet
  outTree->Branch("dijet2_jet2_pt"     , &b_dijet2_jet2_pt     ,  "dijet2_jet2_pt/F");
  outTree->Branch("dijet2_jet2_eta"    , &b_dijet2_jet2_eta    ,  "dijet2_jet2_eta/F");
  outTree->Branch("dijet2_jet2_phi"    , &b_dijet2_jet2_phi    ,  "dijet2_jet2_phi/F");
  outTree->Branch("dijet2_jet2_m"      , &b_dijet2_jet2_m      ,  "dijet2_jet2_m/F");
  outTree->Branch("dijet2_jet2_MV2c00" , &b_dijet2_jet2_MV2c00 ,  "dijet2_jet2_MV2c00/F");
  outTree->Branch("dijet2_jet2_MV2c10" , &b_dijet2_jet2_MV2c10 ,  "dijet2_jet2_MV2c10/F");
  outTree->Branch("dijet2_jet2_MV2c20" , &b_dijet2_jet2_MV2c20 ,  "dijet2_jet2_MV2c20/F");

  // Trigger Study
  outTree->Branch("PassXhhL1"  , &b_PassXhhL1 , "PassXhhL1/I");

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhMicroNTuple :: configure ()
{
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhMicroNTuple :: fileExecute () { return EL::StatusCode::SUCCESS; }
EL::StatusCode XhhMicroNTuple :: changeInput (bool /*firstFile*/) { return EL::StatusCode::SUCCESS; }


EL::StatusCode XhhMicroNTuple::execute ()
{
  // Get EventInfo the PrimaryVertices
  const xAOD::EventInfo* eventInfo(0);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store));

  // Event Cuts
  if(!m_cutTool->PassEventCuts(eventInfo)) return EL::StatusCode::SUCCESS;

  bool m_doSystematics = false;
  if (!m_doSystematics) {

    executeSingle();

  } 
  
  //
  //  Machinerary for dealing with the systematics
  //
  //else { // get the list of systematics to run over
  //  
  //  // get vector of jet systamtics giving the names
  //  std::vector<std::string>* systNames(nullptr);
  //  ANA_CHECK( HelperFunctions::retrieve(systNames, m_jetSystematics, 0, m_store) ,"");
  //
  //  // loop over systematics
  //  for (auto systName : *systNames) {
  //    if (m_helpTree.find(systName) == m_helpTree.end()) this->treeInitialize(systName); 
  //    executeSingle(systName);
  //  }
  //
  //}

  return EL::StatusCode::SUCCESS;

}

EL::StatusCode XhhMicroNTuple::executeSingle(std::string jetSyst, std::string bJetSyst, std::string dijetSyst) {

  if(m_debug) cout << "XhhMicroNTuple::In executeSingle"  << endl;
  if(m_debug) m_store->print();

  std::string syst = jetSyst + bJetSyst + dijetSyst;
  
  const xAOD::EventInfo* eventInfo(0);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store));

  const xAOD::VertexContainer* vertices(0);
  ANA_CHECK( HelperFunctions::retrieve(vertices, "PrimaryVertices", m_event, m_store));

  const xAOD::JetContainer* jets(0);
  ANA_CHECK( HelperFunctions::retrieve(jets, m_inJetName+jetSyst, m_event, m_store));

  const xAOD::JetContainer* bjets(0);
  if (!m_inBJetName.empty()){//add condition for boosted analysis
    ANA_CHECK( HelperFunctions::retrieve(bjets, m_inBJetName+bJetSyst, m_event, m_store));
  }

  const xAOD::ParticleContainer* diJets(0);
  ANA_CHECK( HelperFunctions::retrieve(diJets, m_inDiJetName+dijetSyst, m_event, m_store));

  //
  //  Only fill the ntuple if we have 2 dijets
  //
  if (diJets->size() < 2) return EL::StatusCode::SUCCESS;

  m_helpTree[syst]->FillEvent( eventInfo );
  m_helpTree[syst]->FillTrigger( eventInfo );
  
  if (!m_inBJetName.empty()){//add condition for boosted analysis
    b_nbjets        = bjets->size();
    if( eventInfo->isAvailable< bool >( "L1_4J20" ) ){
      if ( eventInfo->auxdata< bool > ("L1_4J20") ||
	   eventInfo->auxdata< bool > ("L1_J100") ) {
	b_PassXhhL1 =  1;
      } else {
	b_PassXhhL1 =  0;
      }
    } else {
      b_PassXhhL1   = -1;
    }
  } else {
    b_nbjets        =  0;
    b_PassXhhL1     = -1;
  }

  //
  // dijet 1 branches
  //
  const xAOD::Particle*   dijet1 = diJets->at(0);
  b_dijet1_pt           = dijet1->pt(); 
  b_dijet1_eta          = dijet1->eta();
  b_dijet1_phi          = dijet1->phi();
  b_dijet1_m            = dijet1->m();	 
  b_dijet1_dRjet1jet2   = dijet1->auxdata<float>("dRjj");

  const xAOD::Jet*        dijet1_jet1 = dijet1->auxdata< const xAOD::Jet* >("leadJet");
  b_dijet1_jet1_pt      = dijet1_jet1->pt();
  b_dijet1_jet1_eta     = dijet1_jet1->eta();
  b_dijet1_jet1_phi     = dijet1_jet1->phi();
  b_dijet1_jet1_m       = dijet1_jet1->m();
  b_dijet1_jet1_MV2c00  = MV2(dijet1_jet1, "MV2c00");
  b_dijet1_jet1_MV2c10  = MV2(dijet1_jet1, "MV2c10");
  b_dijet1_jet1_MV2c20  = MV2(dijet1_jet1, "MV2c20");

  const xAOD::Jet*        dijet1_jet2 = dijet1->auxdata< const xAOD::Jet* >("sublJet");
  b_dijet1_jet2_pt      = dijet1_jet2->pt();
  b_dijet1_jet2_eta     = dijet1_jet2->eta();
  b_dijet1_jet2_phi     = dijet1_jet2->phi();
  b_dijet1_jet2_m       = dijet1_jet2->m();
  b_dijet1_jet2_MV2c00  = MV2(dijet1_jet2, "MV2c00");
  b_dijet1_jet2_MV2c10  = MV2(dijet1_jet2, "MV2c10");
  b_dijet1_jet2_MV2c20  = MV2(dijet1_jet2, "MV2c20");

  //
  // dijet 2 branches
  //
  const xAOD::Particle*   dijet2 = diJets->at(1);
  b_dijet2_pt           = dijet2->pt(); 
  b_dijet2_eta          = dijet2->eta();
  b_dijet2_phi          = dijet2->phi();
  b_dijet2_m            = dijet2->m();	 
  b_dijet2_dRjet1jet2   = dijet2->auxdata<float>("dRjj");

  const xAOD::Jet*       dijet2_jet1 = dijet2->auxdata< const xAOD::Jet* >("leadJet");
  b_dijet2_jet1_pt     = dijet2_jet1->pt();
  b_dijet2_jet1_eta    = dijet2_jet1->eta();
  b_dijet2_jet1_phi    = dijet2_jet1->phi();
  b_dijet2_jet1_m      = dijet2_jet1->m();
  b_dijet2_jet1_MV2c00 = MV2(dijet2_jet1, "MV2c00");
  b_dijet2_jet1_MV2c10 = MV2(dijet2_jet1, "MV2c10");
  b_dijet2_jet1_MV2c20 = MV2(dijet2_jet1, "MV2c20");

  const xAOD::Jet*       dijet2_jet2 = dijet2->auxdata< const xAOD::Jet* >("sublJet");
  b_dijet2_jet2_pt     = dijet2_jet2->pt();
  b_dijet2_jet2_eta    = dijet2_jet2->eta();
  b_dijet2_jet2_phi    = dijet2_jet2->phi();
  b_dijet2_jet2_m      = dijet2_jet2->m();
  b_dijet2_jet2_MV2c00 = MV2(dijet2_jet2, "MV2c00");
  b_dijet2_jet2_MV2c10 = MV2(dijet2_jet2, "MV2c10");
  b_dijet2_jet2_MV2c20 = MV2(dijet2_jet2, "MV2c20");

  // njets is defined as all the jets > 40 Gev / eta < 2.5 and jvf cut
  //  so this means all the bjets + other jets > 40 GeV
  //b_nVtx                  = vertices("NPV3Trks");
  //b_njets                 =  jets->size();

//  unsigned int nOJet = jets(fOtherJetType);
//  for(unsigned int iOJet = 0; iOJet < nOJet; iOJet++){
//    Particle& thisJet = jet(iOJet, fOtherJetType);
//    
//    if(thisJet.p.Pt() > 40)       
//      ++b_njets;
//
//    b_extraJetpt .push_back(thisJet.p.Pt ()      );
//    b_extraJeteta.push_back(thisJet.p.Eta()      );
//    b_extraJetphi.push_back(thisJet.p.Phi()      );
//    b_extraJetm.  push_back(thisJet.p.M  ()      );
//    b_extraJetmv1.push_back(thisJet.Float("flavor_weight_MV1") );
//
//  }

  //
  //  Fill Other Jets
  //
  //m_helpTree[syst]->FillJets( *jets, HelperFunctions::getPrimaryVertexLocation(vertices) );

  // fill the tree
  m_helpTree[syst]->Fill();
  
  return EL::StatusCode::SUCCESS;

}

EL::StatusCode XhhMicroNTuple :: postExecute () { return EL::StatusCode::SUCCESS; }

EL::StatusCode XhhMicroNTuple :: finalize () {

  Info("finalize()", m_name.c_str());

  if (!m_helpTree.empty()){
    for( auto tree : m_helpTree) {
      if (tree.second) delete tree.second;
    }
  }

  if (m_cutTool) {
    delete m_cutTool; m_cutTool = 0;
  }

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode XhhMicroNTuple :: treeFinalize () { return EL::StatusCode::SUCCESS; }
