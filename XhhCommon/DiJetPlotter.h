#ifndef DiJetPlotter_DiJetPlotter_H
#define DiJetPlotter_DiJetPlotter_H

#include <xAODAnaHelpers/HistogramManager.h>
#include <EventLoop/Worker.h>
#include "xAODParticleEvent/ParticleContainer.h"


class JetHists; // forward declaration                                                                                                                        
//
// put your configuration variables here as public variables.
// that way they can be set directly from CINT and python.
// float cutValue;
//
class DiJetPlotter : public HistogramManager
{

 private:
  // store the histogram
  TH1 *h_Pt; //!
  TH1 *h_Eta; //!
  TH1 *h_Mass; //!
  TH1 *h_dR; //!

  // for holding the set of histogram codes
#ifndef __CINT__
  JetHists* h_leadJet; //!
  JetHists* h_sublJet; //!


  
#endif // not __CINT__                                                                                                                                      

 public:
  // this is a standard constructor
  DiJetPlotter (std::string name, std::string detailStr);
  ~DiJetPlotter();

  StatusCode initialize();
  StatusCode execute( const xAOD::ParticleContainer* dijets,  float eventWeight );
  StatusCode execute( const xAOD::Particle* dijet,  float eventWeight );
  void record(EL::Worker* wk);
  using HistogramManager::book; // make other overloaded functions of book() show up                 
  using HistogramManager::execute; // overload

};

#endif
