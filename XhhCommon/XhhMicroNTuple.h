#ifndef XhhMicroNTuple_XhhMicroNTuple_H
#define XhhMicroNTuple_XhhMicroNTuple_H

#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>

//#include "JetSubStructureUtils/BoostedXbbTag.h"

#include "xAODRootAccess/Init.h"
#include "xAODRootAccess/TEvent.h"
#include "xAODRootAccess/TStore.h"
#include "TTree.h"

class HelpTreeBase;
class CutTool;

class XhhMicroNTuple : public EL::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:

  std::string m_name;                  
  bool m_debug;

  xAOD::TEvent *m_event;               //!
  xAOD::TStore *m_store;               //!

  std::string m_evtDetailStr;
  std::string m_trigDetailStr;
  /* std::string m_inCaloJetName;   //! */
  /* std::string m_inTrackJetName;   //! */
  /* std::string m_inTruthParticleName; //! */
  std::string m_jetDetailStr;	      	      
  std::string m_inJetName;   
  std::string m_inBJetName;  
  std::string m_inDiJetName; 

  std::string m_eventCuts;          

private:

  std::map< std::string, HelpTreeBase* > m_helpTree; //!
  CutTool*      m_cutTool;  //!
  /* JetSubStructureUtils::BoostedXbbTag* m_higgsTaggerLoose = nullptr; */
  /* JetSubStructureUtils::BoostedXbbTag* m_higgsTaggerMedium = nullptr; */
  /* JetSubStructureUtils::BoostedXbbTag* m_higgsTaggerTight = nullptr; */

protected:

  std::string m_evtContainerName;   //!

  // For the systematics
  std::string m_jetSystematics;       //!
  std::string m_bJetSystematics;       //!

private: 

  // branches
  int   b_nbjets;
  int   b_PassXhhL1;

  float b_dijet1_pt, b_dijet1_eta, b_dijet1_phi, b_dijet1_m;
  float b_dijet2_pt, b_dijet2_eta, b_dijet2_phi, b_dijet2_m;

  float b_dijet1_jet1_pt, b_dijet1_jet1_eta, b_dijet1_jet1_phi, b_dijet1_jet1_m;
  float b_dijet1_jet2_pt, b_dijet1_jet2_eta, b_dijet1_jet2_phi, b_dijet1_jet2_m;

  float b_dijet1_jet1_MV2c00, b_dijet1_jet1_MV2c10, b_dijet1_jet1_MV2c20;
  float b_dijet1_jet2_MV2c00, b_dijet1_jet2_MV2c10, b_dijet1_jet2_MV2c20;

  float b_dijet2_jet1_pt, b_dijet2_jet1_eta, b_dijet2_jet1_phi, b_dijet2_jet1_m;
  float b_dijet2_jet2_pt, b_dijet2_jet2_eta, b_dijet2_jet2_phi, b_dijet2_jet2_m;

  float b_dijet2_jet1_MV2c00, b_dijet2_jet1_MV2c10, b_dijet2_jet1_MV2c20;
  float b_dijet2_jet2_MV2c00, b_dijet2_jet2_MV2c10, b_dijet2_jet2_MV2c20;

  float b_dijet1_dRjet1jet2, b_dijet2_dRjet1jet2;

public:

  // this is a standard constructor
  XhhMicroNTuple ();                                           //!

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode setupJob (EL::Job& job);           //!
  virtual EL::StatusCode fileExecute ();                    //!
  virtual EL::StatusCode treeInitialize (std::string);      //!
  virtual EL::StatusCode changeInput (bool firstFile);      //!
  virtual EL::StatusCode initialize ();                     //!
  virtual EL::StatusCode execute ();                        //!
  virtual EL::StatusCode postExecute ();                    //!
  virtual EL::StatusCode finalize ();                       //!
  virtual EL::StatusCode treeFinalize ();                   //!

  // these are the functions not inherited from Algorithm
  virtual EL::StatusCode configure ();                      //!
  EL::StatusCode executeSingle(std::string jetSyst="", std::string bJetSyst="", std::string dijetSyst=""); //!

  // this is needed to distribute the algorithm to the workers
  ClassDef(XhhMicroNTuple, 1);                                 //!
};

#endif
