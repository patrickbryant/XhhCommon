#ifndef BJetTriggerEmulationAlg_BJetTriggerEmulationAlg_H
#define BJetTriggerEmulationAlg_BJetTriggerEmulationAlg_H

#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>

//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

#include "xAODRootAccess/Init.h"
#include "xAODRootAccess/TEvent.h"
#include "xAODRootAccess/TStore.h"

#include <TrigBtagEmulationTool/TrigBtagEmulationTool.h>
#include <boost/algorithm/string/replace.hpp>


class HelpTreeBase;

class BJetTriggerEmulationAlg : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:

  std::string m_name;                  
  std::string m_triggerConfiguration;

  bool        m_debug;
  bool        m_testMCMenu;
  bool        m_load2015Chains;
  bool        m_load2016Chains;
  bool        m_onlyLoadhh4bChains;
  int         m_verbosity;

  xAOD::TEvent *m_event;               //!
  xAOD::TStore *m_store;               //!

private:


  Trig::TrigBtagEmulationTool*         m_emulationTool      = nullptr;  //!
  Trig::TrigBtagEmulationTool*         m_emulationTool2015  = nullptr;  //!
  void addEmulatedChain    (const std::string& trigName, const std::string& trigConfig, Trig::TrigBtagEmulationTool* trigTool, bool compWithTDT = false);

  struct trigCounter{
    std::string m_trigName;
    std::string m_trigNameNoComb;
    unsigned int m_nPassEmu;
    unsigned int m_nPassTDT;
    unsigned int m_compWithTDT;
    Trig::TrigBtagEmulationTool* m_trigTool;
    SG::AuxElement::Decorator< char > decorator;


  trigCounter(std::string trigName, bool compWithTDT, Trig::TrigBtagEmulationTool* trigTool) : 
    m_trigName(trigName), m_nPassEmu(0), m_nPassTDT(0), m_compWithTDT(compWithTDT), m_trigTool(trigTool), decorator(SG::AuxElement::Decorator< char >("EMUL_"+m_trigName))
    {
      m_trigNameNoComb = m_trigName;
      boost::replace_all(m_trigNameNoComb, "bcomb", "b");
      //std::cout << "Was " << m_trigName << " Now " << m_trigNameNoComb << std::endl;;
    }

    void count(const std::vector<std::string>& passTriggersTDT){
      bool passEmu = m_trigTool->isPassed(m_trigName);

      if(passEmu) ++m_nPassEmu;

      if(m_compWithTDT){
      
	bool passTDT = (find(passTriggersTDT.begin(), passTriggersTDT.end(),  m_trigNameNoComb  ) != passTriggersTDT.end());
	//std::cout << m_trigName << " In count " << passEmu << " " << passTDT << " " << m_nPassEmu << " " << m_nPassTDT <<std::endl;

	if( (passEmu && !passTDT) || (!passEmu && passTDT) ){
	  std::cout << m_trigNameNoComb << " mismatch: " << m_trigName  << " ... PassEmulation:  " << passEmu << "   PassTDT" << passTDT << std::endl;
	  //for(auto t : passTriggersTDT) std::cout << t << std::endl;
	  
	  m_trigTool->setProperty("Verbosity",2);
	  m_trigTool->execute();
	  m_trigTool->setProperty("Verbosity",0);
	  
	}

	if(passTDT) ++m_nPassTDT;
      }


      
    }

    void finalize(){
      std::cout << m_trigName << ": ";
      std::cout  << "Emu: " << m_nPassEmu;
      if(m_compWithTDT)
	std::cout << "  TDT: " << m_nPassTDT;
      std::cout << std::endl;
	
    }

  };

  std::vector<trigCounter> m_trigCounters; //!

public:

  // this is a standard constructor
  BJetTriggerEmulationAlg ();                                           //!

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode setupJob (EL::Job& job);           //!
  virtual EL::StatusCode fileExecute ();                    //!
  virtual EL::StatusCode changeInput (bool firstFile);      //!
  virtual EL::StatusCode initialize ();                     //!
  virtual EL::StatusCode execute ();                        //!
  virtual EL::StatusCode postExecute ();                    //!
  virtual EL::StatusCode finalize ();                       //!


  // this is needed to distribute the algorithm to the workers
  ClassDef(BJetTriggerEmulationAlg, 1);                                 //!
};

#endif
