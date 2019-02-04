#ifndef CutTool_CutTool_H
#define CutTool_CutTool_H

namespace xAOD{
  class EventInfo_v1;
}

//
// put your configuration variables here as public variables.
// that way they can be set directly from CINT and python.
// float cutValue;
//
class CutTool 
{


 public:
  // this is a standard constructor
  CutTool ();

  void Init(TString EventCuts);
  Bool_t PassEventCuts(const xAOD::EventInfo_v1* eventInfo);
  std::vector<TString>  fEventCuts;  
};

#endif
