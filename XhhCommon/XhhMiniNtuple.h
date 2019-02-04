#ifndef XhhMiniNtuple_XhhMiniNtuple_H
#define XhhMiniNtuple_XhhMiniNtuple_H

#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>
//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

#include "JetSubStructureUtils/BoostedXbbTag.h"
#include "JetSubStructureUtils/BosonTag.h"

#include "xAODRootAccess/Init.h"
#include "xAODRootAccess/TEvent.h"
#include "xAODRootAccess/TStore.h"
#include "TTree.h"
#include "TH1D.h"

#include <xAODTruth/TruthParticleContainer.h>

//#include "BoostedJetTaggers/IJSSTagger.h"
//#include "BoostedJetTaggers/SmoothedWZTagger.h"
//#include "BoostedJetTaggers/BoostedXbbTagger.h"

#include "hhTruthWeightTools/hhWeightTool.h"

class HelpTreeBase;

class XhhMiniNtuple : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:

  std::string m_name;                  
  bool m_writeAll;
  TH1D* m_cutflowHist;    //!
  TH1D* m_cutflowHistW;   //!
  int m_cutflowFirst;     //!
  int m_iCutflow;         //!
  bool m_isMC;            //!

  xAOD::TEvent *m_event;               //!
  xAOD::TStore *m_store;               //!

  std::string m_resolvedJetsName;
  std::string m_resolvedHcandName;
  std::string m_boostedHcandName;

  std::string m_jetCleaningName;
  
  std::string m_evtDetailStr;
  std::string m_trigDetailStr;
  std::string m_resolvedJetDetailStr;
  std::string m_boostedJetDetailStr;
  std::string m_boostedFatJetDetailStr;
  std::string m_truthDetailStr;
  std::string m_inCaloJetName;
  std::string m_inTrackJetName;
  std::string m_inTruthParticleName;
  std::string m_muonContainerName;
  std::string m_promptMuonContainerName;
  std::string m_muonDetailStr;
  std::string m_elecContainerName;
  std::string m_elecDetailStr;
  std::string m_metContainerName;
  std::string m_metDetailStr;
  bool        m_doResolutionStudy;
  bool        m_debug;
  bool        m_doXhhTagging;
  bool        m_doFatJetMassCut;
  double      m_FatJetMassCut;
  double      m_FatJetPtSkimCut;
  std::string m_TrackJetWP;
  bool        m_storeLeptonVeto;
  bool        m_storeMETVeto;
  bool        m_storeTruth;
  bool        m_doResolved;
  bool        m_doLeptop;
  bool        m_doBoosted;
  std::string m_eventCuts;
  std::string m_resolvedSysName;      
  std::string m_boostedSysName;     

private:

  std::map< std::string, HelpTreeBase* > m_helpTree; //!
  //JetSubStructureUtils::BoostedXbbTag* m_higgsTaggerLoose = nullptr;  //! 
  //JetSubStructureUtils::BoostedXbbTag* m_higgsTaggerMedium = nullptr; //!
  //JetSubStructureUtils::BoostedXbbTag* m_higgsTaggerTight = nullptr;  //!
  //JetSubStructureUtils::BosonTag*      m_WbosonTaggerMedium = nullptr; //!
  //JetSubStructureUtils::BosonTag*      m_ZbosonTaggerMedium = nullptr; //!
  //JetSubStructureUtils::BosonTag*      m_WbosonTaggerTight = nullptr; //!
  //JetSubStructureUtils::BosonTag*      m_ZbosonTaggerTight = nullptr; //!
  //SmoothedWZTagger*                    m_smoothedWTagger_50 = nullptr; //!
  //SmoothedWZTagger*                    m_smoothedZTagger_50 = nullptr; //!
  //SmoothedWZTagger*                    m_smoothedWTagger_80 = nullptr; //!
  //SmoothedWZTagger*                    m_smoothedZTagger_80 = nullptr; //!
  //BoostedXbbTagger*                    m_BoostedXbbTagger = nullptr;  //!

  xAOD::hhWeightTool*                        m_hhWeightTool = nullptr; //!

private: 

  // Truth variables
  double b_truth_mtt;

  // Higgs candidates from boosted selection
  int                b_hcand_boosted_n;
  std::vector<float> b_hcand_boosted_pt;
  std::vector<float> b_hcand_boosted_ptcalo;
  std::vector<float> b_hcand_boosted_ptTA;
  std::vector<float> b_hcand_boosted_eta;
  std::vector<float> b_hcand_boosted_etacalo;
  std::vector<float> b_hcand_boosted_etaTA;
  std::vector<float> b_hcand_boosted_phi;
  std::vector<float> b_hcand_boosted_phicalo;
  std::vector<float> b_hcand_boosted_phiTA;
  std::vector<float> b_hcand_boosted_m;
  std::vector<float> b_hcand_boosted_mcalo;
  std::vector<float> b_hcand_boosted_mTA;
  std::vector<float> b_hcand_boosted_htag_muoncor_pt ;
  std::vector<float> b_hcand_boosted_htag_muoncor_eta;
  std::vector<float> b_hcand_boosted_htag_muoncor_phi;
  std::vector<float> b_hcand_boosted_htag_muoncor_m;
  std::vector<int>   b_hcand_boosted_htag;
  std::vector<int>   b_hcand_boosted_htag_loose;
  std::vector<int>   b_hcand_boosted_htag_medium;
  std::vector<int>   b_hcand_boosted_htag_tight;
  std::vector<int>   b_hcand_boosted_Wtag_medium;
  std::vector<int>   b_hcand_boosted_Ztag_medium;
  std::vector<int>   b_hcand_boosted_Wtag_tight;
  std::vector<int>   b_hcand_boosted_Ztag_tight;
  std::vector<int>   b_hcand_boosted_smoothWtag_50;
  std::vector<int>   b_hcand_boosted_smoothZtag_50;
  std::vector<int>   b_hcand_boosted_smoothWtag_80;
  std::vector<int>   b_hcand_boosted_smoothZtag_80;
  std::vector<float> b_hcand_boosted_dRjj;
  std::vector<float> b_hcand_boosted_D2;
  std::vector<float> b_hcand_boosted_C2;
  std::vector<float> b_hcand_boosted_Tau21;
  std::vector<float> b_hcand_boosted_Tau21WTA;
  std::vector<int>   b_hcand_boosted_nTrack;
  std::vector<int>   b_hcand_boosted_nHBosons;
  std::vector<int>   b_hcand_boosted_nWBosons;
  std::vector<int>   b_hcand_boosted_nZBosons;

  std::vector<int>                  b_jet_ak2track_asso_n;
  std::vector<int>                  b_jet_ak2track_asso_n_addl;
  std::vector< std::vector<float> > b_jet_ak2track_asso_pt;
  std::vector< std::vector<float> > b_jet_ak2track_asso_eta;
  std::vector< std::vector<float> > b_jet_ak2track_asso_phi;
  std::vector< std::vector<float> > b_jet_ak2track_asso_m;
  std::vector< std::vector<float> > b_jet_ak2track_asso_MV2c00;
  std::vector< std::vector<float> > b_jet_ak2track_asso_MV2c10;
  std::vector< std::vector<float> > b_jet_ak2track_asso_MV2c20;
  std::vector< std::vector<float> > b_jet_ak2track_asso_MV2c100;
  std::vector< std::vector< std::vector<float> > >  b_jet_ak2track_asso_sys;
  std::vector<std::string> b_jet_ak2track_asso_sysname;
  std::vector<float>  b_boosted_bevent_sys;

  // TruthJet of Higgs candidates, for MC only
  int                 b_truth_hcand_boosted_n;
  std::vector<int>    b_truth_hcand_boosted_matched;
  std::vector<float>  b_truth_hcand_boosted_pt;
  std::vector<float>  b_truth_hcand_boosted_eta;
  std::vector<float>  b_truth_hcand_boosted_phi;
  std::vector<float>  b_truth_hcand_boosted_m;
  std::vector<float>  b_truth_hcand_boosted_d2;
  std::vector<float>  b_truth_hcand_boosted_c2;

  // Loose lepton for veto purpose
  int                 b_n_muons_veto;
  int                 b_n_electrons_veto;
  bool                b_event_cleaning_qqbb;

  // MET for veto purpose
  double              b_METsum;
  double              b_METphi;

  float m_mcEventWeight; 
  float m_weight;
  float m_weight_mhh;
  float m_weight_xs;
  float m_cleanEvent;

  std::vector<std::string> m_passEmulatedTriggers;


  /* //Boosted Branches */
  /* std::vector<int> b_n_asso_with_sv; */
  /* int b_n_pass_htagger_loose; */
  /* int b_n_pass_htagger_medium; */
  /* int b_n_pass_htagger_tight; */

  //
  // For cutflow counting
  //
  void passCut();

  //
  // For mtt slices
  //
  bool getEventMtt(const xAOD::TruthParticleContainer* Truths, double& mtt);

  //
  // KillPileupFluctuation (remove high weight event in JZXW). Inherited from ProofAna
  //
  int killPileupFluctuation();    // return 1 means event is good; 0 means event is not good

  //
  // Substructure Computation 
  //

  double getD2(const xAOD::Jet* inputJet);
  double getC2(const xAOD::Jet* inputJet);
  double getTau21(const xAOD::Jet* inputJet, bool doWTA);

public:

  // this is a standard constructor
  XhhMiniNtuple ();                                           //!

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
  EL::StatusCode executeSingle(std::string resolvedSys="", 
                               std::string boostedSys ="", 
			       bool countEvents = false);


  // this is needed to distribute the algorithm to the workers
  ClassDef(XhhMiniNtuple, 1);                                 //!
};

#endif
