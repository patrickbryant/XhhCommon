#ifndef XhhTestBoostedNtuple_XhhTestBoostedNtuple_H
#define XhhTestBoostedNtuple_XhhTestBoostedNtuple_H

#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>
//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

#include "xAODRootAccess/Init.h"
#include "xAODRootAccess/TEvent.h"
#include "xAODRootAccess/TStore.h"
#include "TTree.h"
#include "TH1D.h"

#include <xAODTruth/TruthParticleContainer.h>

class HelpTreeBase;

class XhhTestBoostedNtuple : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:

  std::string m_name;                  
  TH1D* m_cutflowHist;    //!
  TH1D* m_cutflowHistW;   //!
  int m_cutflowFirst;     //!
  int m_iCutflow;         //!
  bool m_isMC;            //!

  xAOD::TEvent *m_event;               //!
  xAOD::TStore *m_store;               //!

  std::string m_evtDetailStr;
  std::string m_trigDetailStr;
  std::string m_fatJetDetailStr;
  std::string m_jetDetailStr;
  std::string m_truthDetailStr;
  std::string m_inFatJetName;
  std::string m_inJetName;
  std::string m_inTruthFatJetName;
  std::string m_inTruthParticleName;
  std::string m_metContainerName;
  std::string m_metDetailStr;

  bool   m_debug;
  bool   m_doFatJetMassCut;
  double m_FatJetPtSkimCut;
  std::string m_eventCuts;
  std::string m_boostedSysName;     

private:

  std::map< std::string, HelpTreeBase* > m_helpTree; //!

private: 

  float m_mcEventWeight; 
  float m_weight;
  float m_weight_xs;

  //
  // For cutflow counting
  //
  void passCut();

public:

  // this is a standard constructor
  XhhTestBoostedNtuple ();                                           //!

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode setupJob (EL::Job& job);           //!
  virtual EL::StatusCode fileExecute ();                    //!
  virtual EL::StatusCode histInitialize ();                 //!
  virtual EL::StatusCode changeInput (bool firstFile);      //!
  virtual EL::StatusCode initialize ();                     //!
  virtual EL::StatusCode execute ();                        //!
  virtual EL::StatusCode postExecute ();                    //!
  virtual EL::StatusCode finalize ();                       //!
  virtual EL::StatusCode histFinalize ();                   //!

  virtual EL::StatusCode AddTree (std::string);      //!


  // these are the functions not inherited from Algorithm
  EL::StatusCode executeSingle(std::string boostedSys ="", 
			       bool countEvents = false);


  // this is needed to distribute the algorithm to the workers
  ClassDef(XhhTestBoostedNtuple, 1);                                 //!
};

#endif
