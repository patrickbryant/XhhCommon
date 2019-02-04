#ifndef PlotXhhEvent_PlotXhhEvent_H
#define PlotXhhEvent_PlotXhhEvent_H

#include "xAODAnaHelpers/Algorithm.h"
#include "xAODRootAccess/Init.h"
#include "xAODRootAccess/TEvent.h"
#include "xAODRootAccess/TStore.h"

// used to make histograms
#include <TH1.h>

class DiJetPlotter;
class CutTool;
class JetHists;

class PlotXhhEvent : public xAH::Algorithm
{


public:

  std::string m_name;
  std::string m_eventCuts;
  std::string m_signalRegionCut;
  bool        m_debug;

  xAOD::TEvent *m_event; //!
  xAOD::TStore *m_store; //!

  std::string m_inJetName;
  std::string m_inBJetName;
  std::string m_inDiJetName;
  std::string m_inTrackJetName;
  bool m_doBlinding;

 private:

  //
  //  No //! for these guys as they are configuration
  //
 


  // store the histogram
  JetHists*     hJetHists; //!
  JetHists*     hBJetHists; //!
  JetHists*     hTrackJetHists; //!
  DiJetPlotter* hDiJetHists; //!
  DiJetPlotter* hLeadDiJet; //!
  DiJetPlotter* hSublDiJet; //!

  TH1*          h_nJet; //!
  TH1*          h_nBJet; //!
  TH1*          h_nDiJet; //!
  TH1*          h_DiDiJet_Mass; //!  
  TH1*          h_DiDiJet_Mass_l; //!
  TH1*          h_DiDiJet_dR; //!
  TH1*          h_DiDiJet_dPhi; //!
  TH1*          h_Jet_diJetMass; //!  
  TH1*          h_Jet_diJetMass_l; //!
  TH1*          h_Jet_diJetdR; //!
  TH1*          h_Jet_diJetdPhi; //!
  TH1*          h_nTrackJet; //!
  TH1*          h_trigInfo; //!

  CutTool*      m_cutTool; //!

  TH1F* make1DHist (TString name, TString title, unsigned nbins, float low, float high);

 public:

  // this is a standard constructor
  PlotXhhEvent ();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode setupJob (EL::Job& job);
  virtual EL::StatusCode fileExecute ();
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode changeInput (bool firstFile);
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode postExecute ();
  virtual EL::StatusCode finalize ();
  virtual EL::StatusCode histFinalize ();

  // these are the functions not inherited from Algorithm
  virtual EL::StatusCode configure ();

  // this is needed to distribute the algorithm to the workers
  ClassDef(PlotXhhEvent, 1);
};

#endif
