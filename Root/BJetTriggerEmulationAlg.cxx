#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include <xAODEventInfo/EventInfo.h>
#include <AthContainers/ConstDataVector.h>
#include <SampleHandler/MetaFields.h>

#include <xAODAnaHelpers/HelpTreeBase.h>
#include <XhhCommon/BJetTriggerEmulationAlg.h>
#include <XhhCommon/Helpers.h>

#include <xAODAnaHelpers/HelperFunctions.h>
#include <xAODAnaHelpers/HelperClasses.h>


#include "TEnv.h"
#include "TSystem.h"

//#define DEBUG std::cerr << __FILE__ << "::" << __LINE__ << std::endl
 
// this is needed to distribute the algorithm to the workers
ClassImp(BJetTriggerEmulationAlg)

using std::cout;  using std::endl;
using std::string; using std::vector;

BJetTriggerEmulationAlg :: BJetTriggerEmulationAlg () :
  m_name(""),
  m_triggerConfiguration(""),
  m_debug(false),
  m_testMCMenu(false),
  m_load2015Chains(false),
  m_load2016Chains(false),
  m_onlyLoadhh4bChains(true),
  m_verbosity(0)
{
  this->SetName("BJetTriggerEmulationAlg"); // needed if you want to retrieve this algo with wk()->getAlg(ALG_NAME) downstream
}

EL::StatusCode BJetTriggerEmulationAlg :: setupJob (EL::Job& job)
{
  Info("setupJob()", "Calling setupJob \n");
  job.useXAOD();
  xAOD::Init("BJetTriggerEmulationAlg").ignore();

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode BJetTriggerEmulationAlg :: initialize ()
{
  Info("initialize()", m_name.c_str());
  m_event = wk()->xaodEvent();
  m_store = wk()->xaodStore();

  if(m_debug) Info("initialize()", "after add store");
  //if (m_resolvedSysName.empty() && m_boostedSysName.empty()) this->AddTree("");

  //
  //  BJet Trigger Tool (2016)
  //
  m_emulationTool = new Trig::TrigBtagEmulationTool("Trig::TrigBtagEmulationTool/TrigBtagEmulationTool");
  if (m_emulationTool->setProperty("UseTriggerNavigation",false).isFailure() ){
    std::cout<<"Error in TrigBtagEmulationTool setting Property"<<std::endl;
    return EL::StatusCode::FAILURE;
  }

  if (m_emulationTool->setProperty("TrigDecisionToolName","ToolSvc.TrigDecTool").isFailure()){
    std::cout<<"Error in TrigBtagEmulationTool ::: Not possible to define Trigger Decision Tool"<<std::endl;
    return EL::StatusCode::FAILURE;
  }
  
  if (m_emulationTool->setProperty("xAODConfigToolName","xAODConfigTool").isFailure()){
    std::cout<<"Error in TrigBtagEmulationTool ::: Not possible to define Trigger Decision Tool"<<std::endl;
    return EL::StatusCode::FAILURE;
  }

  if (m_emulationTool->setProperty("Verbosity",m_verbosity).isFailure()){
    std::cout<<"Error in TrigBtagEmulationTool ::: Not possible to define Verbosity"<<std::endl;
    return EL::StatusCode::FAILURE;
  }

  
  if (m_emulationTool->initialize().isFailure())  {
    std::cout<<"Error in TrigBtagEmulationTool initialisation"<<std::endl;
    return EL::StatusCode::FAILURE;
  }


  //
  //  BJet Trigger Tool (2015)
  //
  m_emulationTool2015 = new Trig::TrigBtagEmulationTool("Trig::TrigBtagEmulationTool/TrigBtagEmulationTool2015");
  if (m_emulationTool2015->setProperty("UseTriggerNavigation",false).isFailure() ){
    std::cout<<"Error in TrigBtagEmulationTool setting Property"<<std::endl;
    return EL::StatusCode::FAILURE;
  }

  if (m_emulationTool2015->setProperty("InputChain","HLT_j35_bperf").isFailure()){
    std::cout<<"Error in TrigBtagEmulationTool ::: Not possible to define Trigger Decision Tool"<<std::endl;
    return EL::StatusCode::FAILURE;
  }

  if (m_emulationTool2015->setProperty("InputChainSplit","HLT_j35_bperf_split").isFailure()){
    std::cout<<"Error in TrigBtagEmulationTool ::: Not possible to define Trigger Decision Tool"<<std::endl;
    return EL::StatusCode::FAILURE;
  }

  if (m_emulationTool2015->setProperty("TrigDecisionToolName","ToolSvc.TrigDecTool").isFailure()){
    std::cout<<"Error in TrigBtagEmulationTool ::: Not possible to define Trigger Decision Tool"<<std::endl;
    return EL::StatusCode::FAILURE;
  }
  
  if (m_emulationTool2015->setProperty("xAODConfigToolName","xAODConfigTool").isFailure()){
    std::cout<<"Error in TrigBtagEmulationTool ::: Not possible to define Trigger Decision Tool"<<std::endl;
    return EL::StatusCode::FAILURE;
  }

  if (m_emulationTool2015->setProperty("Verbosity",m_verbosity).isFailure()){
    std::cout<<"Error in TrigBtagEmulationTool ::: Not possible to define Verbosity"<<std::endl;
    return EL::StatusCode::FAILURE;
  }

  
  if (m_emulationTool2015->initialize().isFailure())  {
    std::cout<<"Error in TrigBtagEmulationTool initialisation"<<std::endl;
    return EL::StatusCode::FAILURE;
  }


  if(m_onlyLoadhh4bChains){

    //
    // 2015
    //
    addEmulatedChain("HLT_j70_bcombmedium_3j70_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_4j70,EMUL_HLT_j70_bcombmedium",m_emulationTool2015, true);
    addEmulatedChain("HLT_2j35_bcombtight_2j35_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_4j35,EMUL_HLT_2j35_bcombtight", m_emulationTool2015, true);
    addEmulatedChain("HLT_j100_2j55_bcombmedium",               "L1_J75_3J20,EMUL_HLT_3j55,EMUL_HLT_2j55_bcombmedium,EMUL_HLT_j100", m_emulationTool2015);
    addEmulatedChain("HLT_j225_bcombloose",                     "L1_J100,EMUL_HLT_j225_bcombloose", m_emulationTool2015, true);

    addEmulatedChain("HLT_j70_bperf_3j70_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_4j70",m_emulationTool2015, true);
    addEmulatedChain("HLT_2j35_bperf_2j35_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_4j35" ,m_emulationTool2015, true);
    addEmulatedChain("HLT_j100_2j55_bperf",               "L1_J75_3J20,EMUL_HLT_3j55,EMUL_HLT_j100",m_emulationTool2015, true);
    addEmulatedChain("HLT_j225_bperf",                     "L1_J100,EMUL_HLT_j225",m_emulationTool2015, true);

    //
    // 2016
    //
    addEmulatedChain("HLT_j225_bmv2c2060_split",  "L1_J100,EMUL_HLT_j225_bmv2c2060_split", m_emulationTool);
    addEmulatedChain("HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_4j75,EMUL_HLT_j75_bmv2c2070_split", m_emulationTool);
    addEmulatedChain("HLT_j100_2j55_bmv2c2060_split",         "L1_J75_3J20,EMUL_HLT_3j55,EMUL_HLT_2j55_bmv2c2060_split,EMUL_HLT_j100", m_emulationTool);
    addEmulatedChain("HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25", "L1_4J15.0ETA25,EMUL_HLT_4j35,EMUL_HLT_2j35_bmv2c2060_split", m_emulationTool);

  } else {

    if(m_testMCMenu){
      
      // 
      //  1-tag
      // 
      addEmulatedChain("HLT_j175_bmv2c2077_split","L1_J100,EMUL_HLT_j175_bmv2c2077_split", m_emulationTool, true);
      addEmulatedChain("HLT_j175_bmv2c2085_split","L1_J100,EMUL_HLT_j175_bmv2c2085_split", m_emulationTool, true);
      addEmulatedChain("HLT_j225_bmv2c2085_split","L1_J100,EMUL_HLT_j225_bmv2c2085_split", m_emulationTool, true);
      addEmulatedChain("HLT_j300_bmv2c2085_split","L1_J100,EMUL_HLT_j300_bmv2c2085_split", m_emulationTool, true);
      addEmulatedChain("HLT_j300_bmv2c2077_split","L1_J100,EMUL_HLT_j300_bmv2c2077_split", m_emulationTool);
    
      // 
      //  1-tag + 3-jets
      // 
      addEmulatedChain("HLT_j70_bmv2c2070_split_3j70","L1_4J20,EMUL_HLT_4j70,EMUL_HLT_j70_bmv2c2070_split", m_emulationTool, true);
      addEmulatedChain("HLT_j75_bmv2c2077_split_3j75","L1_4J20,EMUL_HLT_4j75,EMUL_HLT_j75_bmv2c2077_split", m_emulationTool, true);
    
      addEmulatedChain("HLT_j65_bmv2c2070_split_3j65_L13J25.0ETA23","L1_3J25.0ETA23,EMUL_HLT_4j65,EMUL_HLT_j65_bmv2c2070_split", m_emulationTool, true);
      addEmulatedChain("HLT_j70_bmv2c2070_split_3j70_L13J25.0ETA23","L1_3J25.0ETA23,EMUL_HLT_4j70,EMUL_HLT_j70_bmv2c2070_split", m_emulationTool, true);
      addEmulatedChain("HLT_j70_bmv2c2077_split_3j70_L13J25.0ETA23","L1_3J25.0ETA23,EMUL_HLT_4j70,EMUL_HLT_j70_bmv2c2077_split", m_emulationTool, true);
      addEmulatedChain("HLT_j75_bmv2c2077_split_3j75_L13J25.0ETA23","L1_3J25.0ETA23,EMUL_HLT_4j75,EMUL_HLT_j75_bmv2c2077_split", m_emulationTool, true);
    
      addEmulatedChain("HLT_j65_bmv2c2070_split_3j65_L14J15.0ETA25","L1_4J15.0ETA25,EMUL_HLT_4j65,EMUL_HLT_j65_bmv2c2070_split", m_emulationTool, true);
      addEmulatedChain("HLT_j70_bmv2c2077_split_3j70_L14J15.0ETA25","L1_4J15.0ETA25,EMUL_HLT_4j70,EMUL_HLT_j70_bmv2c2077_split", m_emulationTool, true);
    
      //
      //  2-tag
      //
      addEmulatedChain("HLT_j150_bmv2c2077_split_j50_bmv2c2077_split","L1_J100,EMUL_HLT_2j50_bmv2c2077_split,EMUL_HLT_j150_bmv2c2077_split", m_emulationTool, true);
      addEmulatedChain("HLT_j175_bmv2c2077_split_j60_bmv2c2077_split","L1_J100,EMUL_HLT_2j60_bmv2c2077_split,EMUL_HLT_j175_bmv2c2077_split", m_emulationTool, true);
      
      //
      //  2-tag + jet
      //
      addEmulatedChain("HLT_2j65_bmv2c2070_split_j65","L1_3J25.0ETA23,EMUL_HLT_3j65,EMUL_HLT_2j65_bmv2c2070_split", m_emulationTool, true);
      addEmulatedChain("HLT_2j70_bmv2c2070_split_j70","L1_3J25.0ETA23,EMUL_HLT_3j70,EMUL_HLT_2j70_bmv2c2070_split", m_emulationTool, true);
      addEmulatedChain("HLT_2j70_bmv2c2077_split_j70","L1_3J25.0ETA23,EMUL_HLT_3j70,EMUL_HLT_2j70_bmv2c2077_split", m_emulationTool, true);
      addEmulatedChain("HLT_2j75_bmv2c2077_split_j75","L1_3J25.0ETA23,EMUL_HLT_3j75,EMUL_HLT_2j75_bmv2c2077_split", m_emulationTool, true);
    
      addEmulatedChain("HLT_j100_2j55_bmv2c2077_split","L1_J75_3J20,EMUL_HLT_3j55,EMUL_HLT_2j55_bmv2c2077_split,EMUL_HLT_j100", m_emulationTool, true);
    
      //
      //  2-tag + 2 jets
      //
      addEmulatedChain("HLT_2j55_bmv2c2077_split_2j55","L1_4J20,EMUL_HLT_4j55,EMUL_HLT_2j55_bmv2c2077_split", m_emulationTool, true);
    
      addEmulatedChain("HLT_2j35_bmv2c2070_split_2j35_L14J15.0ETA25","L1_4J15.0ETA25,EMUL_HLT_4j35,EMUL_HLT_2j35_bmv2c2070_split", m_emulationTool, true);
      addEmulatedChain("HLT_2j45_bmv2c2077_split_2j45_L14J15.0ETA25","L1_4J15.0ETA25,EMUL_HLT_4j45,EMUL_HLT_2j45_bmv2c2077_split", m_emulationTool, true);
    																 
      addEmulatedChain("HLT_2j35_bmv2c2070_split_2j35_L13J25.0ETA23","L1_3J25.0ETA23,EMUL_HLT_4j35,EMUL_HLT_2j35_bmv2c2070_split", m_emulationTool, true);
      addEmulatedChain("HLT_2j45_bmv2c2070_split_2j45_L13J25.0ETA23","L1_3J25.0ETA23,EMUL_HLT_4j45,EMUL_HLT_2j45_bmv2c2070_split", m_emulationTool, true);
      addEmulatedChain("HLT_2j45_bmv2c2077_split_2j45_L13J25.0ETA23","L1_3J25.0ETA23,EMUL_HLT_4j45,EMUL_HLT_2j45_bmv2c2077_split", m_emulationTool, true);
      addEmulatedChain("HLT_2j55_bmv2c2077_split_2j55_L13J25.0ETA23","L1_3J25.0ETA23,EMUL_HLT_4j55,EMUL_HLT_2j55_bmv2c2077_split", m_emulationTool, true);
  
      //
      //  tag + ht 
      //
      addEmulatedChain("HLT_j55_bmv2c2077_split_ht500_L14J20","L1_4J20,EMUL_HLT_ht500_split,EMUL_HLT_j55_bmv2c2077_split", m_emulationTool, false);
      addEmulatedChain("HLT_j55_bmv2c2070_split_ht500_L14J20","L1_4J20,EMUL_HLT_ht500,EMUL_HLT_j55_bmv2c2070_split"      , m_emulationTool, false);
  
      addEmulatedChain("HLT_2j55_bmv2c2070_split_ht300_L14J20","L1_4J20,EMUL_HLT_ht300,EMUL_HLT_2j55_bmv2c2070_split", m_emulationTool, false);
      addEmulatedChain("HLT_2j55_bmv2c2077_split_ht300_L14J20","L1_4J20,EMUL_HLT_ht300,EMUL_HLT_2j55_bmv2c2077_split", m_emulationTool, false);
  
    }//Test Chains
  
    //
    // 2015 Chains
    //
    if(m_load2015Chains){
  
      //
      // 1-tag
      //
      addEmulatedChain("HLT_j300_bcombloose","L1_J100,EMUL_HLT_j300_bcombloose", m_emulationTool2015);
      addEmulatedChain("HLT_j225_bcombloose","L1_J100,EMUL_HLT_j225_bcombloose", m_emulationTool2015);

      addEmulatedChain("HLT_j300_bcombloose_split","L1_J100,EMUL_HLT_j300_bcombloose_split", m_emulationTool2015, true);
      addEmulatedChain("HLT_j225_bcombloose_split","L1_J100,EMUL_HLT_j225_bcombloose_split", m_emulationTool2015, true);
  
  
      //
      // 1b + 3j      
      //
      addEmulatedChain("HLT_j75_bcombmedium_3j75",              "L1_4J20,EMUL_HLT_4j75,EMUL_HLT_j75_bcombmedium"       , m_emulationTool2015);
      addEmulatedChain("HLT_j70_bcombtight_3j70",               "L1_4J20,EMUL_HLT_4j70,EMUL_HLT_j70_bcombtight"        , m_emulationTool2015);
      addEmulatedChain("HLT_j70_bcombmedium_3j70_L13J25.0ETA23","L1_3J25.0ETA23,EMUL_HLT_4j70,EMUL_HLT_j70_bcombmedium", m_emulationTool2015);
      addEmulatedChain("HLT_j65_bcombtight_3j65_L13J25.0ETA23", "L1_3J25.0ETA23,EMUL_HLT_4j65,EMUL_HLT_j65_bcombtight" , m_emulationTool2015);
      addEmulatedChain("HLT_j70_bcombmedium_3j70_L14J15.0ETA25","L1_4J15.0ETA25,EMUL_HLT_4j70,EMUL_HLT_j70_bcombmedium", m_emulationTool2015);
      addEmulatedChain("HLT_j65_bcombtight_3j65_L14J15.0ETA25", "L1_4J15.0ETA25,EMUL_HLT_4j65,EMUL_HLT_j65_bcombtight" , m_emulationTool2015);
  
      //
      // 2b
      //
      addEmulatedChain("HLT_j175_bcombmedium_j60_bcombmedium","L1_J100,EMUL_HLT_2j60_bcombmedium,EMUL_HLT_j175_bcombmedium", m_emulationTool2015);
      addEmulatedChain("HLT_j150_bcombmedium_j50_bcombmedium","L1_J100,EMUL_HLT_2j50_bcombmedium,EMUL_HLT_j150_bcombmedium", m_emulationTool2015);
      addEmulatedChain("HLT_j175_bcombmedium_split_j60_bcombmedium_split", "L1_J100,EMUL_HLT_2j60_bcombmedium_split,EMUL_HLT_j175_bcombmedium_split", m_emulationTool2015, true);
      
  
      //
      // 2b + 1j
      //
      addEmulatedChain("HLT_j100_2j55_bcombmedium","L1_J75_3J20,EMUL_HLT_3j55,EMUL_HLT_2j55_bcombmedium,EMUL_HLT_j100", m_emulationTool2015);
      addEmulatedChain("HLT_2j75_bcombmedium_j75", "L1_3J25.0ETA23,EMUL_3j75,EMUL_HLT_2j75_bcombmedium", m_emulationTool2015);
      addEmulatedChain("HLT_2j70_bcombtight_j70",  "L1_3J25.0ETA23,EMUL_3j70,EMUL_HLT_2j70_bcombtight" , m_emulationTool2015);
      addEmulatedChain("HLT_2j70_bcombmedium_j70", "L1_3J25.0ETA23,EMUL_3j70,EMUL_HLT_2j70_bcombmedium", m_emulationTool2015);
      addEmulatedChain("HLT_2j65_bcombtight_j65",  "L1_3J25.0ETA23,EMUL_3j65,EMUL_HLT_2j65_bcombtight" , m_emulationTool2015);
  
      //
      // 2b + 2j
      //  
      addEmulatedChain("HLT_2j55_bcombmedium_2j55",                "L1_4J20,EMUL_HLT_4j55,EMUL_HLT_2j55_bcombmedium", m_emulationTool2015);
      addEmulatedChain("HLT_2j45_bcombtight_2j45",                 "L1_4J20,EMUL_HLT_4j45,EMUL_HLT_2j45_bcombtight" , m_emulationTool2015);
      addEmulatedChain("HLT_2j45_bcombmedium_2j45_L13J25.0ETA23",  "L1_3J25.0ETA23,EMUL_HLT_4j45,EMUL_HLT_2j45_bcombmedium", m_emulationTool2015);
      addEmulatedChain("HLT_2j35_bcombtight_2j35_L13J25.0ETA23",   "L1_3J25.0ETA23,EMUL_HLT_4j35,EMUL_HLT_2j35_bcombtight" , m_emulationTool2015);
      addEmulatedChain("HLT_2j45_bcombmedium_2j45_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_4j45,EMUL_HLT_2j45_bcombmedium", m_emulationTool2015);
      addEmulatedChain("HLT_2j35_bcombtight_2j35_L14J15.0ETA25",   "L1_4J15.0ETA25,EMUL_HLT_4j35,EMUL_HLT_2j35_bcombtight" , m_emulationTool2015);
      
      addEmulatedChain("HLT_2j45_bcombmedium_split_2j45_L14J15.0ETA25", "L1_4J15.0ETA25,EMUL_HLT_4j45,EMUL_HLT_2j45_bcombmedium_split", m_emulationTool2015, true);
      addEmulatedChain("HLT_2j55_bcombmedium_split_2j55_L13J25.0ETA23", "L1_3J25.0ETA23,EMUL_HLT_4j55,EMUL_HLT_2j55_bcombmedium_split", m_emulationTool2015, true);

      addEmulatedChain("HLT_2j35_bcombtight_split_2j35_L14J15.0ETA25","L1_4J15.0ETA25,EMUL_HLT_4j35,EMUL_HLT_2j35_bcombtight_split",    m_emulationTool2015, true);
      addEmulatedChain("HLT_2j45_bcombtight_split_2j45_L13J25.0ETA23","L1_3J25.0ETA23,EMUL_HLT_4j45,EMUL_HLT_2j45_bcombtight_split",   m_emulationTool2015, true);

    }

  
    //
    // 2016 Chains
    //
    if(m_load2016Chains){
  
      //
      // 1-tag
      //
      addEmulatedChain("HLT_j175_bmv2c2040_split",  "L1_J100,EMUL_HLT_j175_bmv2c2040_split", m_emulationTool);
      addEmulatedChain("HLT_j225_bmv2c2060_split",  "L1_J100,EMUL_HLT_j225_bmv2c2060_split", m_emulationTool);
      addEmulatedChain("HLT_j225_bmv2c2050_split",  "L1_J100,EMUL_HLT_j225_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_j275_bmv2c2070_split",  "L1_J100,EMUL_HLT_j275_bmv2c2070_split", m_emulationTool);
      addEmulatedChain("HLT_j275_bmv2c2060_split",  "L1_J100,EMUL_HLT_j275_bmv2c2060_split", m_emulationTool);
      addEmulatedChain("HLT_j300_bmv2c2077_split",  "L1_J100,EMUL_HLT_j300_bmv2c2077_split", m_emulationTool);
      addEmulatedChain("HLT_j300_bmv2c2070_split",  "L1_J100,EMUL_HLT_j300_bmv2c2070_split", m_emulationTool);
      addEmulatedChain("HLT_j360_bmv2c2085_split",  "L1_J100,EMUL_HLT_j360_bmv2c2085_split", m_emulationTool);
  
  
  
      //
      // 1b + 3j
      //
      addEmulatedChain("HLT_j75_bmv2c2060_split_3j75_L14J20",         "L1_4J20,EMUL_HLT_4j75,EMUL_HLT_j75_bmv2c2060_split", m_emulationTool);
      addEmulatedChain("HLT_j75_bmv2c2060_split_3j75_L14J15",         "L1_4J15,EMUL_HLT_4j75,EMUL_HLT_j75_bmv2c2060_split", m_emulationTool);
      addEmulatedChain("HLT_j75_bmv2c2060_split_3j75_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_4j75,EMUL_HLT_j75_bmv2c2060_split", m_emulationTool);
      addEmulatedChain("HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_4j75,EMUL_HLT_j75_bmv2c2070_split", m_emulationTool);
  
      //
      // 2b
      //
      addEmulatedChain("HLT_j150_bmv2c2050_split_j50_bmv2c2050_split",   "L1_J100,EMUL_HLT_2j50_bmv2c2050_split,EMUL_HLT_j150_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_j175_bmv2c2050_split_j50_bmv2c2050_split",   "L1_J100,EMUL_HLT_2j50_bmv2c2050_split,EMUL_HLT_j175_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_j150_bmv2c2060_split_j50_bmv2c2060_split",   "L1_J100,EMUL_HLT_2j50_bmv2c2060_split,EMUL_HLT_j150_bmv2c2060_split", m_emulationTool);
      addEmulatedChain("HLT_j175_bmv2c2060_split_j50_bmv2c2050_split",   "L1_J100,EMUL_HLT_2j50_bmv2c2060_split,EMUL_HLT_j175_bmv2c2060_split", m_emulationTool);
  
      //
      // 2b + 1j
      //
      addEmulatedChain("HLT_2j70_bmv2c2050_split_j70_L13J40",   "L1_3J40,EMUL_HLT_3j70,EMUL_HLT_2j70_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_2j75_bmv2c2060_split_j75_L13J40",   "L1_3J40,EMUL_HLT_3j75,EMUL_HLT_2j75_bmv2c2060_split", m_emulationTool);
      addEmulatedChain("HLT_j100_2j55_bmv2c2050_split",         "L1_J75_3J20,EMUL_HLT_3j55,EMUL_HLT_2j55_bmv2c2050_split,EMUL_HLT_j100", m_emulationTool);
      addEmulatedChain("HLT_j100_2j55_bmv2c2060_split",         "L1_J75_3J20,EMUL_HLT_3j55,EMUL_HLT_2j55_bmv2c2060_split,EMUL_HLT_j100", m_emulationTool);

      //
      // 2b + 2j
      //  
      addEmulatedChain("HLT_2j35_bmv2c2050_split_2j35_L14J20",        "L1_4J20,EMUL_HLT_4j35,EMUL_HLT_2j35_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_2j35_bmv2c2050_split_2j35_L14J15",        "L1_4J15,EMUL_HLT_4j35,EMUL_HLT_2j35_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_2j35_bmv2c2050_split_2j35_L14J15.0ETA25", "L1_4J15.0ETA25,EMUL_HLT_4j35,EMUL_HLT_2j35_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_2j35_bmv2c2060_split_2j35_L14J15",        "L1_4J15,EMUL_HLT_4j35,EMUL_HLT_2j35_bmv2c2060_split", m_emulationTool);
      addEmulatedChain("HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25", "L1_4J15.0ETA25,EMUL_HLT_4j35,EMUL_HLT_2j35_bmv2c2060_split", m_emulationTool);
  
      //
      // 2b + 3j
      //
      addEmulatedChain("HLT_2j45_bmv2c2050_split_3j45_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_5j45,EMUL_HLT_2j45_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_2j45_bmv2c2060_split_3j45_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_5j45,EMUL_HLT_2j45_bmv2c2060_split", m_emulationTool);
      addEmulatedChain("HLT_2j45_bmv2c2050_split_3j45",                "L1_5J15.0ETA25,EMUL_HLT_5j45,EMUL_HLT_2j45_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_2j45_bmv2c2060_split_3j45",                "L1_5J15.0ETA25,EMUL_HLT_5j45,EMUL_HLT_2j45_bmv2c2060_split", m_emulationTool);
      addEmulatedChain("HLT_2j45_bmv2c2070_split_3j45_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_5j45,EMUL_HLT_2j45_bmv2c2070_split", m_emulationTool);
      addEmulatedChain("HLT_2j45_bmv2c2070_split_3j45",                "L1_5J15.0ETA25,EMUL_HLT_5j45,EMUL_HLT_2j45_bmv2c2070_split", m_emulationTool);
      addEmulatedChain("HLT_2j45_bmv2c2077_split_3j45",                "L1_5J15.0ETA25,EMUL_HLT_5j45,EMUL_HLT_2j45_bmv2c2077_split", m_emulationTool);
      addEmulatedChain("HLT_2j45_bmv2c2077_split_3j45_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_HLT_5j45,EMUL_HLT_2j45_bmv2c2077_split", m_emulationTool);
  
      //
      // b + ht
      //
      addEmulatedChain("HLT_j55_bmv2c2050_split_ht500_L14J20",                 "L1_4J20,EMUL_HLT_ht500_split,EMUL_HLT_j55_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_j55_bmv2c2050_split_ht500_L1HT190-J15.ETA21",      "L1_HT190-J15.ETA21,EMUL_HLT_ht500_split,EMUL_HLT_j55_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_j55_bmv2c2050_split_ht500_L1HT190-J15s5.ETA21",    "L1_HT190-J15s5.ETA21,EMUL_HLT_ht500_split,EMUL_HLT_j55_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_j55_bmv2c2050_split_ht500_L14J15",                 "L1_4J15,EMUL_HLT_ht500_split,EMUL_HLT_j55_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_j55_bmv2c2060_split_ht500_L14J15",                 "L1_4J15,EMUL_HLT_ht500_split,EMUL_HLT_j55_bmv2c2060_split", m_emulationTool);
      
      addEmulatedChain("HLT_2j55_bmv2c2050_split_ht300_L14J20",                "L1_4J20,EMUL_HLT_ht300_split,EMUL_HLT_2j55_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_2j55_bmv2c2050_split_ht300_L1HT190-J15.ETA21",     "L1_HT190-J15.ETA21,EMUL_HLT_ht300_split,EMUL_HLT_2j55_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_2j55_bmv2c2050_split_ht300_L1HT190-J15s5.ETA21",   "L1_HT190-J15s5.ETA21,EMUL_HLT_ht300_split,EMUL_HLT_2j55_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_2j55_bmv2c2050_split_ht300_L14J15",                "L1_4J15,EMUL_HLT_ht300_split,EMUL_HLT_2j55_bmv2c2050_split", m_emulationTool);
      addEmulatedChain("HLT_2j55_bmv2c2060_split_ht300_L14J15",                "L1_4J15,EMUL_HLT_ht300_split,EMUL_HLT_2j55_bmv2c2060_split", m_emulationTool);
  
      //
      // 3b
      //
      addEmulatedChain("HLT_3j55_bmv2c2070_split_L13J35.0ETA23", "L1_3J25.0ETA23,EMUL_HLT_3j55_bmv2c2070_split", m_emulationTool);
      addEmulatedChain("HLT_3j45_bmv2c2060_split_L13J35.0ETA23", "L1_3J25.0ETA23,EMUL_HLT_3j45_bmv2c2060_split", m_emulationTool);
  
      //
      // 3b + 1j
      //
      addEmulatedChain("HLT_3j35_bmv2c2060_split",                    "L1_4J20,EMUL_HLT_3j35_bmv2c2060_split", m_emulationTool);
      addEmulatedChain("HLT_3j55_bmv2c2070_split",                    "L1_3J40,EMUL_HLT_3j55_bmv2c2070_split", m_emulationTool);
      addEmulatedChain("HLT_3j35_bmv2c2060_split_L14J15.0ETA25",      "L1_4J15.0ETA25,EMUL_HLT_3j35_bmv2c2060_split", m_emulationTool);
  
      addEmulatedChain("HLT_3j35_bmv2c2077_split_j35",                "L1_4J20,EMUL_4j35,EMUL_HLT_3j35_bmv2c2077_split", m_emulationTool);
      addEmulatedChain("HLT_3j35_bmv2c2077_split_j35_L14J15.0ETA25",  "L1_4J15.0ETA25,EMUL_4j35,EMUL_HLT_3j35_bmv2c2077_split", m_emulationTool);
  
  
    }// 2016 Chains

  } // Not only hh-chains
  
  if(m_debug) Info("initialize()", "left");
  return EL::StatusCode::SUCCESS;
}


EL::StatusCode BJetTriggerEmulationAlg :: fileExecute    () { return EL::StatusCode::SUCCESS; }
EL::StatusCode BJetTriggerEmulationAlg :: changeInput    (bool /*firstFile*/) { return EL::StatusCode::SUCCESS; }

EL::StatusCode BJetTriggerEmulationAlg::execute ()
{

  const xAOD::EventInfo* eventInfo(0);
  ANA_CHECK(HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store) );

  // push back
  m_emulationTool    ->execute();
  m_emulationTool2015->execute();

  std::vector<std::string> passTriggersTDT;
  static SG::AuxElement::ConstAccessor< std::vector< std::string > > passTrigs("passTriggers");
  passTriggersTDT = passTrigs( *eventInfo ); 

  std::vector<std::string> passTriggersEMUL;

  for(trigCounter& tc: m_trigCounters){
    tc.count(passTriggersTDT);

    if(tc.m_trigTool->isPassed(tc.m_trigName))
      passTriggersEMUL.push_back( tc.m_trigNameNoComb );
  }

  static SG::AuxElement::Decorator< std::vector< std::string > >  passTrigsEMUL("passTriggersEmulation");
  passTrigsEMUL( *eventInfo ) = passTriggersEMUL;

  return EL::StatusCode::SUCCESS;

}


EL::StatusCode BJetTriggerEmulationAlg :: postExecute () { return EL::StatusCode::SUCCESS; }

EL::StatusCode BJetTriggerEmulationAlg :: finalize () {

  Info("finalize()", m_name.c_str());

  for(trigCounter& tc: m_trigCounters)
    tc.finalize();

  return EL::StatusCode::SUCCESS;
}

 
void BJetTriggerEmulationAlg::addEmulatedChain(const std::string& trigName, const std::string& trigConfig, Trig::TrigBtagEmulationTool* trigTool, bool compWithTDT)
{
  std::vector<std::string> emulatedChainDescription;
  emulatedChainDescription.push_back(trigName);

  std::string token;
  std::istringstream ss(trigConfig);
  while ( std::getline(ss, token, ',') ) {
    emulatedChainDescription.push_back(token);
  }  

  trigTool->addEmulatedChain(emulatedChainDescription);
  m_trigCounters.push_back(trigCounter(trigName, compWithTDT, trigTool));
 
  return;
}
