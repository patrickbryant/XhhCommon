/********************************************************
 * FatJetJERTool
 *
 * This class handles jet energy resolution systematics, 
 * while official FatJet JETSmearTool is not available
 *
 * Qi Zeng (qi.zeng@cern.ch)
 *
 ********************************************************/

#ifndef XhhCommon_FatJetJERTool_H
#define XhhCommon_FatJetJERTool_H

// algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

// EDM Include
#include "xAODJet/JetContainer.h"

// ROOT Include
#include "TFile.h"
#include "TH1.h"
#include "TRandom3.h"

class FatJetJERTool : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  // configuration variables
  
  std::string m_inContainerName;
  std::string m_outContainerName;

  std::string m_TruthJetContainerName;

  std::string m_jetAlgo;

  std::string m_inputAlgo;
  std::string m_outputAlgo;

  std::string m_JERConfig;
  
  bool    m_runJERSmearing;
  bool    m_sort;

  long int m_userSeed;

private:

  bool m_isMC;            //!

  std::string m_outDCContainerName;     //!
  std::string m_outDCAuxContainerName;  //!

  std::vector<std::string> m_JERTypes;  //!

  TFile*  m_JERConfigFile;                       //!
  std::map<std::string, TH1*> m_JERConfigHists;  //!

  TRandom3 m_random; //!

  const xAOD::Jet* getMatchedTruthJet(const xAOD::Jet* jet, const xAOD::JetContainer* truthJetContainer);
  bool applySmearing(xAOD::Jet* jet, const xAOD::Jet* truthjet, std::string JERType);
  double getSmearingFactor(const xAOD::Jet* jet, double sigma);

  std::string getMassBin(double mass){
    if(mass < 50)        return "M0";
    else if(mass < 100)  return "M1";
    else if(mass < 150)  return "M2";
    else                 return "M3";
  }

  int getTruthPtBin(double pt){
    if(pt < 250)       return 1;  // under flow
    else if(pt < 500)  return 1;
    else if(pt < 1000) return 2;
    else if(pt < 1500) return 3;
    else if(pt < 2000) return 4;
    else               return 4;  // overflow bin
  }

  // variables that don't get filled at submission time should be
  // protected from being send from the submission node to the worker
  // node (done by the //!)
public:
  // Tree *myTree; //!
  // TH1 *myHist; //!


  // this is a standard constructor
  FatJetJERTool (std::string className = "FatJetJERTool");

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


  /// @cond
  // this is needed to distribute the algorithm to the workers
  ClassDef(FatJetJERTool, 1);
  /// @endcond

};

#endif
