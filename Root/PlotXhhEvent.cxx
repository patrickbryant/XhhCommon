#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>

// EDM includes:
#include "AthContainers/ConstDataVector.h"
#include "xAODEventInfo/EventInfo.h"

// Jet xAOD EDM container
#include "xAODParticleEvent/ParticleContainer.h"

// Jet xAOD EDM container
#include "xAODJet/JetContainer.h"
#include "xAODRootAccess/TStore.h"

#include <XhhCommon/PlotXhhEvent.h>
#include <XhhCommon/DiJetPlotter.h>
#include <XhhCommon/CutTool.h>
#include <xAODAnaHelpers/JetHists.h>
#include "xAODAnaHelpers/HelperFunctions.h"

#include <TSystem.h> 
#include "TEnv.h"

// this is needed to distribute the algorithm to the workers
ClassImp(PlotXhhEvent)

using std::cout; using std::endl;

PlotXhhEvent :: PlotXhhEvent ():
  m_name(""),
  m_eventCuts(""),
  m_signalRegionCut(""),
  m_debug(0),
  m_inJetName(""),
  m_inBJetName(""),
  m_inDiJetName(""),
  m_inTrackJetName(""),
  m_doBlinding(false),
  hJetHists(0),
  hBJetHists(0),
  hDiJetHists(0),
  hLeadDiJet(0),
  hSublDiJet(0),
  m_cutTool(0)
{

  //
  // Hists
  //
  h_nJet           = 0;
  h_nBJet          = 0;
  h_nDiJet         = 0;
  h_DiDiJet_Mass   = 0;
  h_DiDiJet_Mass_l = 0;
  h_DiDiJet_dR     = 0;
  h_DiDiJet_dPhi   = 0;

}

EL::StatusCode PlotXhhEvent :: setupJob (EL::Job& job)
{
  job.useXAOD();
  xAOD::Init("PlotXhhEvent").ignore(); // call before opening first file
  return EL::StatusCode::SUCCESS;
}

TH1F* PlotXhhEvent :: make1DHist (TString name, TString title, unsigned nbins, float low, float high){
  TH1F* h_tmp = new TH1F(m_name+name, title, nbins, low, high); // jet pt [GeV]
  wk()->addOutput (h_tmp);
  return h_tmp;
}


EL::StatusCode PlotXhhEvent :: histInitialize ()
{
  Info("histInitialize()", "%s", m_name.c_str() );
  // needed here and not in initalize since this is called first

  m_cutTool      = new CutTool();
  m_cutTool ->Init(m_eventCuts);
    
  //
  //  Event level Hists
  //
  h_nJet   = make1DHist("nJet"      , "nJet;   nJet;    Entries", 10,-0.5,9.5);
  if(!m_inBJetName.empty()){h_nBJet  = make1DHist("nBJet"     , "nBJet;  nBJet;   Entries", 10,-0.5,9.5);}
  if(!m_inTrackJetName.empty()){h_nTrackJet   = make1DHist("nJet"      , "nJet;   nJet;    Entries", 10,-0.5,9.5);}
  h_nDiJet = make1DHist("nDiJet"    , "nDiJet; nDiJet;  Entries", 10,-0.5,9.5);

  //
  // Pair of DiJet hists
  //
  h_DiDiJet_Mass   = make1DHist("DiDiJet_Mass",   "DiDiJetMass; M_{dj,di}; Entries",          100, 200, 2000);
  h_DiDiJet_Mass_l = make1DHist("DiDiJet_Mass_l", "DiDiJetMass; M_{dj,di}; Entries",          100, 200, 4000);
  h_DiDiJet_dR     = make1DHist("DiDiJet_dR",     "DiDiJetDR;   #DeltaR_{dj,di}; Entries",    100, -0.1, 5);
  h_DiDiJet_dPhi   = make1DHist("DiDiJet_dPhi",   "DiDiJetDPhi  #Delta#Phi_{dj,di}; Entries", 100, -3.2, 3.2);

  h_Jet_diJetMass   = make1DHist("Jet_diJetMass",   "JetDiJetMass; M_{jj}; Entries",          100, 200, 2000);
  h_Jet_diJetMass_l = make1DHist("Jet_diJetMass_l", "JetDiJetMass; M_{jj}; Entries",          100, 200, 4000);
  h_Jet_diJetdR     = make1DHist("Jet_diJetdR",     "JetDiJetDR;   #DeltaR_{jj}; Entries",    100, -0.1, 5);
  h_Jet_diJetdPhi   = make1DHist("Jet_diJetdPhi",   "JetDiJetDPhi  #Delta#Phi_{jj}; Entries", 100, -3.2, 3.2);

  h_trigInfo = make1DHist("triggers", "triggers", 3, 0, 3);
  const char* triggers[13] = {"L1_J12","L1_J15","L1_J20","L1_J25","L1_J30","L1_J40","L1_J50","L1_J75",
			      "L1_J85","L1_J100","L1_J120","L1_J400","L1_4J20"};
  h_trigInfo->SetCanExtend(TH1::kAllAxes);

  for(int i=0; i<12; i++){
    h_trigInfo->Fill(triggers[i], 0.0);
  }


  //Removing flavorTag for now due to segfault
  //hJetHists   = new JetHists(m_name+"Jet_", "kinematic energy flavorTag" );
  hJetHists   = new JetHists(m_name+"Jet_", "kinematic energy truth" );
  hJetHists   -> initialize();
  hJetHists -> record( wk() );

  if(!m_inBJetName.empty()){
    hBJetHists  = new JetHists(m_name+"BJet_", "kinematic energy flavorTag" );
    hBJetHists  -> initialize();
    hBJetHists -> record( wk() );
  }

  if(!m_inTrackJetName.empty()){
    hTrackJetHists = new JetHists(m_name+"TrackJet_", "kinematic constituent flavorTag");
    hTrackJetHists->initialize();
    hTrackJetHists->record( wk() );
  }

  if(!m_inDiJetName.empty()){
    hDiJetHists = new DiJetPlotter(m_name+"DiJet_", "kinematic energy truth");
    hDiJetHists -> initialize();
    hDiJetHists -> record( wk() );

    hLeadDiJet  = new DiJetPlotter(m_name+"LeadDiJet_","kinematic energy truth constituent flavorTag");
    hLeadDiJet  -> initialize();
    hLeadDiJet -> record( wk() );

    hSublDiJet  = new DiJetPlotter(m_name+"SublDiJet_", "kinematic energy truth constituent flavorTag");
    hSublDiJet -> initialize();
    hSublDiJet -> record( wk() );
  }
  
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode PlotXhhEvent :: configure ()
{

  return EL::StatusCode::SUCCESS;
}


EL::StatusCode PlotXhhEvent :: fileExecute ()
{
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode PlotXhhEvent :: changeInput (bool )
{
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode PlotXhhEvent :: initialize ()
{
  
  m_event = wk()->xaodEvent();
  m_store = wk()->xaodStore();
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode PlotXhhEvent :: execute ()
{
  if(m_debug) cout << "In PlotXhhEvent" <<endl;

  const xAOD::EventInfo* eventInfo(nullptr);
  ANA_CHECK(HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store, msg()) );

  //
  // Event Cuts
  //
  if(!m_cutTool->PassEventCuts(eventInfo))
    return true;
  
  //Don't plot anything in the signal region
  if (m_doBlinding && eventInfo->auxdecor< bool > (m_signalRegionCut)){
    return EL::StatusCode::SUCCESS;
  }

  
  float eventWeight(1);
  if( eventInfo->isAvailable< float >( "mcEventWeight" ) ) {
    eventWeight = eventInfo->auxdecor< float >( "mcEventWeight" );
    //std::cout << eventInfo->auxdecor< float >( "mcEventWeight" ) << std::endl;
  }

  if( eventInfo->isAvailable<std::vector<std::string> > ("passTriggers") ){
    std::vector<std::string> trigs = eventInfo->auxdata<std::vector<std::string> > ("passTriggers");
    for(unsigned int i=0; i<trigs.size(); i++){
      h_trigInfo->Fill(trigs[i].c_str(), eventWeight);
    }
  }


  //
  // Fill Jets
  //
  const xAOD::JetContainer* jets(nullptr);
  ANA_CHECK(HelperFunctions::retrieve(jets, m_inJetName, m_event, m_store, msg()) );

  unsigned int nJet = jets->size();
  hJetHists->execute( jets, eventWeight );
  h_nJet->Fill(nJet, eventWeight);

  if(nJet > 1){
    const xAOD::Jet* leadJet = jets->at(0);
    const xAOD::Jet* sublJet = jets->at(1);

    TLorentzVector DiJetMom = (leadJet->p4() + sublJet->p4());

    h_Jet_diJetMass  ->Fill(DiJetMom.M()/1000. , eventWeight);
    h_Jet_diJetMass_l->Fill(DiJetMom.M()/1000. , eventWeight);

    h_Jet_diJetdR  ->Fill(leadJet->p4().DeltaR(sublJet->p4()),     eventWeight);
    h_Jet_diJetdPhi  ->Fill(leadJet->p4().DeltaPhi(sublJet->p4()), eventWeight);
  }


  if(!m_inTrackJetName.empty()){
    const xAOD::JetContainer* trackjets(nullptr);
    ANA_CHECK(HelperFunctions::retrieve(trackjets, m_inTrackJetName, m_event, m_store, msg()) );
    hTrackJetHists->execute(trackjets, eventWeight);
    h_nTrackJet->Fill(trackjets->size(), eventWeight);
  }

  //
  // Fill B Jets
  //
  if(!m_inBJetName.empty()){
    const xAOD::JetContainer* bjets(nullptr);
    ANA_CHECK(HelperFunctions::retrieve(bjets, m_inBJetName, m_event, m_store, msg()) );

    unsigned int nBJet = bjets->size();
    hBJetHists->execute( bjets, eventWeight );
    h_nBJet->Fill(nBJet, eventWeight);
  }

  //
  // Fill Di-jets 
  //
  if(!m_inDiJetName.empty()){
    const xAOD::ParticleContainer* dijets(nullptr);
    //const xAOD::JetContainer* dijets(nullptr);
    ANA_CHECK(HelperFunctions::retrieve(dijets, m_inDiJetName, m_event, m_store, msg()) );

    unsigned int nDiJet = dijets->size();
    hDiJetHists->execute(dijets, eventWeight);
    h_nDiJet->Fill(nDiJet, eventWeight);

    //
    //  Fill DiDiJet Hists
    //
    if(nDiJet > 1){
      const xAOD::Particle* leadDiJet = dijets->at(0);
      const xAOD::Particle* sublDiJet = dijets->at(1);

      hLeadDiJet->execute(leadDiJet, eventWeight);
      hSublDiJet->execute(sublDiJet, eventWeight);

      TLorentzVector DiDiJetMom = (leadDiJet->p4() + sublDiJet->p4());

      h_DiDiJet_Mass  ->Fill(DiDiJetMom.M()/1000 , eventWeight);
      h_DiDiJet_Mass_l->Fill(DiDiJetMom.M()/1000 , eventWeight);

      h_DiDiJet_dR  ->Fill(leadDiJet->p4().DeltaR(sublDiJet->p4()),     eventWeight);
      h_DiDiJet_dPhi  ->Fill(leadDiJet->p4().DeltaPhi(sublDiJet->p4()), eventWeight);
    }
  }

  if(m_debug) cout << "Leave PlotXhhEvent " << endl;

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode PlotXhhEvent :: postExecute ()
{
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode PlotXhhEvent :: finalize ()
{
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode PlotXhhEvent :: histFinalize ()
{
  h_trigInfo->LabelsDeflate();
  return EL::StatusCode::SUCCESS;
}
