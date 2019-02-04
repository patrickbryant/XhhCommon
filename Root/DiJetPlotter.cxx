#include "xAODParticleEvent/ParticleContainer.h"
#include <XhhCommon/DiJetPlotter.h>
#include <xAODAnaHelpers/JetHists.h>
#include <EventLoop/Worker.h>
#include <iostream>


DiJetPlotter :: DiJetPlotter (std::string name, std::string detailStr) : 
  HistogramManager(name,detailStr)
{
}

DiJetPlotter :: ~DiJetPlotter(){}

StatusCode DiJetPlotter::initialize()
{
  h_Pt   = book(m_name, "dijetPt",   "DiJet Pt",   250, 0, 2500); 
  h_Eta  = book(m_name, "dijetEta",  "DiJet Eta",  100, -5,  5); 
  h_Mass = book(m_name, "dijetMass", "DiJet Mass", 100, 0, 300); 
  h_dR   = book(m_name, "dijetdR", "DiJet #Delta R", 100, -0.1, 7); 
  
  h_leadJet = new JetHists(m_name+"LeadJet_",m_detailStr);
  ANA_CHECK(h_leadJet -> initialize());

  h_sublJet = new JetHists(m_name+"SublJet_",m_detailStr);
  ANA_CHECK(h_sublJet -> initialize());

  return StatusCode::SUCCESS;
}

void DiJetPlotter::record(EL::Worker* wk)
{
  HistogramManager::record( wk );
  h_leadJet -> record( wk );
  h_sublJet -> record( wk );
  return;
}


StatusCode DiJetPlotter::execute( const xAOD::ParticleContainer* dijets, float eventWeight ) 
{
  xAOD::ParticleContainer::const_iterator dijet_itr = dijets->begin();
  xAOD::ParticleContainer::const_iterator dijet_end = dijets->end();
  for( ; dijet_itr != dijet_end; ++dijet_itr ) {
    ANA_CHECK(execute( (*dijet_itr), eventWeight ));
  }
  return StatusCode::SUCCESS;
}
 

StatusCode DiJetPlotter :: execute (const xAOD::Particle* dijet, float eventWeight)
{
  const xAOD::Jet* leadJet = dijet->auxdata< const xAOD::Jet* >("leadJet");
  if(leadJet) 
    ANA_CHECK(h_leadJet->execute( leadJet, eventWeight ));

  const xAOD::Jet* sublJet = dijet->auxdata< const xAOD::Jet* >("sublJet");
  if(sublJet) 
    ANA_CHECK(h_sublJet->execute( sublJet, eventWeight ));

  h_Pt ->Fill( dijet->pt()/1000, eventWeight); // GeV
  h_Eta->Fill( dijet->eta(), eventWeight); 
  h_Mass->Fill( dijet->m()/1000, eventWeight); 
  
  if(leadJet && sublJet)
    h_dR->Fill(leadJet->p4().DeltaR(sublJet->p4()), eventWeight);


  return StatusCode::SUCCESS;
}
