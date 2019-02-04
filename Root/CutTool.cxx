#include <EventLoop/Worker.h>
#include <XhhCommon/CutTool.h>
#include <TString.h>
#include <TObjString.h>
#include <TObjArray.h>
#include "xAODEventInfo/EventInfo.h"

CutTool :: CutTool ()
{
}

void CutTool::Init(TString EventCuts)
{
  fEventCuts.clear();

  TObjArray* addTrkToJets = EventCuts.Tokenize(",");
  for(int i = 0; i<addTrkToJets->GetEntries(); ++i) {
    TObjString* triggerObj = (TObjString*)addTrkToJets->At(i);
    fEventCuts.push_back(triggerObj->GetString());
  }
  
  return;
}

Bool_t CutTool::PassEventCuts(const xAOD::EventInfo_v1* eventInfo)
{
  std::vector<TString>::const_iterator IEvt  =  fEventCuts.begin();
  std::vector<TString>::const_iterator IEvtE =  fEventCuts.end();
  for(;IEvt != IEvtE; ++IEvt){
    
    const std::string thisCutName = (*IEvt).Data();

    if(!eventInfo->auxdata< bool > ( thisCutName )){
      return false;
    }
  
  }
  
  return true;
}

